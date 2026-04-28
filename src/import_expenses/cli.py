import logging
from datetime import date, datetime
from pathlib import Path
import sys
from typing import Annotated

import typer

from import_expenses.inter_checking_account import parse_inter_checking_account_statement
from import_expenses.inter_credit_card import parse_inter_credit_card_invoice
from import_expenses.minhas_financas import (
    write_checking_account_import_csv,
    write_credit_card_import_csv,
)


app = typer.Typer()
LOGGER = logging.getLogger("import_expenses")
INTER_CREDIT_CARD_SOURCE = "inter-credit-card"
INTER_CHECKING_SOURCE = "inter-checking"
SUPPORTED_SOURCES = {INTER_CREDIT_CARD_SOURCE, INTER_CHECKING_SOURCE}


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(levelname)s %(message)s",
        stream=sys.stdout,
        force=True,
    )


@app.command()
def main(
    input_path: Annotated[
        Path | None,
        typer.Option("--input", help="Input file path."),
    ] = None,
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
    source: Annotated[
        str | None,
        typer.Option(
            "--source",
            help="Input source: inter-credit-card or inter-checking.",
        ),
    ] = None,
    transaction_date: Annotated[
        str | None,
        typer.Option(
            "--transaction-date",
            help="Effective import transaction date in DD/MM/YYYY format for checking account output.",
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

    provided_input = _prompt_for_input_path(input_path)
    resolved_input = provided_input.expanduser().resolve()
    selected_source = _resolve_source(source, provided_input)
    resolved_output = _resolve_output_path(resolved_input, output_path, output_dir)
    parsed_due_date = _parse_due_date(due_date)
    parsed_transaction_date = _parse_transaction_date(transaction_date)

    LOGGER.info("Reading input file: %s", resolved_input)
    LOGGER.info("Selected source: %s", selected_source)
    LOGGER.info("Output CSV will be written to: %s", resolved_output)

    if not resolved_input.is_file():
        LOGGER.error("Input file was not found: %s", resolved_input)
        raise typer.Exit(code=1)

    try:
        transactions = _parse_transactions(selected_source, resolved_input)
        LOGGER.info("Parsed %s transactions from %s", len(transactions), resolved_input)
        resolved_output.parent.mkdir(parents=True, exist_ok=True)
        _write_output(
            selected_source,
            transactions,
            resolved_output,
            parsed_due_date,
            parsed_transaction_date,
        )
        LOGGER.info("Finished writing CSV: %s", resolved_output)
    except Exception:
        LOGGER.exception("Import failed")
        raise typer.Exit(code=1)

    typer.echo(f"Wrote {len(transactions)} transactions to {resolved_output}")


def _prompt_for_input_path(input_path: Path | None) -> Path:
    if input_path is not None:
        return input_path
    return Path(typer.prompt("Input file path"))


def _resolve_source(source: str | None, input_path: Path) -> str:
    if source is None:
        inferred_source = _infer_source(input_path)
        if inferred_source is not None:
            return inferred_source
        source = typer.prompt("Source (inter-credit-card or inter-checking)")
    if source not in SUPPORTED_SOURCES:
        raise typer.BadParameter(
            "Use inter-credit-card or inter-checking for --source."
        )
    return source


def _infer_source(input_path: Path) -> str | None:
    extension = input_path.suffix.lower()
    if extension == ".csv":
        return INTER_CREDIT_CARD_SOURCE
    if extension == ".ofx":
        return INTER_CHECKING_SOURCE
    return None


def _parse_transactions(source: str, input_path: Path):
    if source == INTER_CREDIT_CARD_SOURCE:
        return parse_inter_credit_card_invoice(input_path)
    if source == INTER_CHECKING_SOURCE:
        return parse_inter_checking_account_statement(input_path)
    raise ValueError(f"Unsupported source: {source}")


def _write_output(
    source: str,
    transactions,
    output_path: Path,
    due_date: date | None,
    transaction_date: date,
) -> None:
    if source == INTER_CREDIT_CARD_SOURCE:
        write_credit_card_import_csv(transactions, output_path, due_date)
        return
    if source == INTER_CHECKING_SOURCE:
        write_checking_account_import_csv(transactions, output_path, transaction_date)
        return
    raise ValueError(f"Unsupported source: {source}")


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


def _parse_transaction_date(value: str | None) -> date:
    if value is None:
        return date.today()
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        raise typer.BadParameter("Use DD/MM/YYYY format for --transaction-date.")


if __name__ == "__main__":
    app()
