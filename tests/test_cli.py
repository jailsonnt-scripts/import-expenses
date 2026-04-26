from typer.testing import CliRunner

from import_expenses.cli import app


def test_cli_accepts_input_and_output() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["--input", "expenses.csv", "--output", "expenses.json"],
    )

    assert result.exit_code == 0
    assert "Input: expenses.csv" in result.output
    assert "Output: expenses.json" in result.output
