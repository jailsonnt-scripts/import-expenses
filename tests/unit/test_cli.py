import csv
from pathlib import Path

from typer.testing import CliRunner

from import_expenses.cli import app


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_cli_writes_output_csv(tmp_path) -> None:
    runner = CliRunner()
    output_path = tmp_path / "minhas-financas.csv"

    result = runner.invoke(
        app,
        [
            "--input",
            str(FIXTURES_DIR / "inter_credit_card_invoice.csv"),
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert f"Wrote 2 transactions to {output_path}" in result.output

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 2
