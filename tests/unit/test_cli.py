import csv
import os
import subprocess
import sys
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
            "--due-date",
            "10/05/2026",
        ],
    )

    assert result.exit_code == 0
    assert "INFO Reading input CSV:" in result.output
    assert "INFO Parsed 1 transactions" in result.output
    assert f"Wrote 1 transactions to {output_path}" in result.output

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert len(rows) == 1
    assert rows[0][0] == "COMPRA TESTE MERCADO"
    assert rows[0][1] == "1234.56"
    assert rows[0][2] == "10/05/2026"
    assert rows[0][3:7] == ["Outros", "Outros", "Inter", "Inter"]
    assert rows[0][8] == "26/04/2026 08:00"


def test_cli_writes_output_csv_to_output_dir(tmp_path) -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "--input",
            str(FIXTURES_DIR / "inter_credit_card_invoice.csv"),
            "--output-dir",
            str(tmp_path),
            "--due-date",
            "10/05/2026",
        ],
    )

    output_path = tmp_path / "inter_credit_card_invoice-minhas-financas.csv"

    assert result.exit_code == 0
    assert output_path.is_file()

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows[0][2] == "10/05/2026"
    assert rows[0][8] == "26/04/2026 08:00"


def test_running_cli_script_path_executes_main(tmp_path) -> None:
    output_path = tmp_path / "minhas-financas.csv"
    project_root = Path(__file__).parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "src" / "import_expenses" / "cli.py"),
            "--input",
            str(FIXTURES_DIR / "inter_credit_card_invoice.csv"),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=project_root,
        env=env,
    )

    assert result.returncode == 0
    assert "INFO Parsed 1 transactions" in result.stdout
    assert output_path.is_file()
