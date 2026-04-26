from pathlib import Path
from typing import Annotated

import typer

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice
from import_expenses.minhas_financas import write_credit_card_import_csv


app = typer.Typer()


@app.command()
def main(
    input_path: Annotated[Path, typer.Option("--input", help="Input file path.")],
    output_path: Annotated[Path, typer.Option("--output", help="Output file path.")],
) -> None:
    transactions = parse_inter_credit_card_invoice(input_path)
    write_credit_card_import_csv(transactions, output_path)
    typer.echo(f"Wrote {len(transactions)} transactions to {output_path}")
