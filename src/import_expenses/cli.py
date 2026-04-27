import logging
from datetime import date, datetime
from pathlib import Path
import sys
from typing import Annotated

import typer

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice
from import_expenses.minhas_financas import write_credit_card_import_csv


app = typer.Typer()
LOGGER = logging.getLogger("import_expenses")


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(levelname)s %(message)s",
        stream=sys.stdout,
        force=True,
    )


@app.command()
def main(
    input_path: Annotated[Path, typer.Option("--input", help="Input file path.")],
    output_path: Annotated[
        Path | None,
        typer.Option("--output", help="Output file path."),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Option(
            "--output-dir",
            help="Directory where the output CSV will be written when --output is omitted.",
        ),
    ] = None,
    due_date: Annotated[
        str | None,
        typer.Option(
            "--due-date",
            help="Credit card invoice due date in DD/MM/YYYY format.",
        ),
    ] = None,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL.",
        ),
    ] = "INFO",
) -> None:
    _configure_logging(log_level)

    resolved_input = input_path.expanduser().resolve()
    resolved_output = _resolve_output_path(resolved_input, output_path, output_dir)
    parsed_due_date = _parse_due_date(due_date)

    LOGGER.info("Reading input CSV: %s", resolved_input)
    LOGGER.info("Output CSV will be written to: %s", resolved_output)

    if not resolved_input.is_file():
        LOGGER.error("Input file was not found: %s", resolved_input)
        raise typer.Exit(code=1)

    try:
        transactions = parse_inter_credit_card_invoice(resolved_input)
        LOGGER.info("Parsed %s transactions from %s", len(transactions), resolved_input)
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        write_credit_card_import_csv(transactions, resolved_output, parsed_due_date)
        LOGGER.info("Finished writing CSV: %s", resolved_output)
    except Exception:
        LOGGER.exception("Import failed")
        raise typer.Exit(code=1)

    typer.echo(f"Wrote {len(transactions)} transactions to {resolved_output}")


def _resolve_output_path(
    input_path: Path,
    output_path: Path | None,
    output_dir: Path | None,
) -> Path:
    if output_path is not None and output_dir is not None:
        raise typer.BadParameter("Use either --output or --output-dir, not both.")
    if output_path is not None:
        return output_path.expanduser().resolve()

    target_dir = output_dir.expanduser() if output_dir is not None else Path.cwd()
    output_name = f"{input_path.stem}-minhas-financas.csv"
    return (target_dir / output_name).resolve()


def _parse_due_date(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        raise typer.BadParameter("Use DD/MM/YYYY format for --due-date.")


if __name__ == "__main__":
    app()
