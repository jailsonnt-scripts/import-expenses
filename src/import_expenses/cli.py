import logging
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
    output_path: Annotated[Path, typer.Option("--output", help="Output file path.")],
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
    resolved_output = output_path.expanduser().resolve()

    LOGGER.info("Reading input CSV: %s", resolved_input)
    LOGGER.info("Output CSV will be written to: %s", resolved_output)

    if not resolved_input.is_file():
        LOGGER.error("Input file was not found: %s", resolved_input)
        raise typer.Exit(code=1)

    try:
        transactions = parse_inter_credit_card_invoice(resolved_input)
        LOGGER.info("Parsed %s transactions from %s", len(transactions), resolved_input)
        write_credit_card_import_csv(transactions, resolved_output)
        LOGGER.info("Finished writing CSV: %s", resolved_output)
    except Exception:
        LOGGER.exception("Import failed")
        raise typer.Exit(code=1)

    typer.echo(f"Wrote {len(transactions)} transactions to {output_path}")


if __name__ == "__main__":
    app()
