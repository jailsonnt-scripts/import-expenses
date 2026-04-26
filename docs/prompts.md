# Prompts History

## Step 1 - CLI Scaffold

Create a minimal Python 3.12 CLI project using Typer.

- No business logic yet
- Use `src/import_expenses` layout
- Add a simple CLI with `--input` and `--output`
- Add pytest setup
- Add `pyproject.toml` with dependencies
- Keep it simple and minimal

## Step 2 - Inter Credit Card CSV Parser

Add a CSV parser for Inter credit card invoice.

- Use Python standard library `csv`
- Follow the input file format defined in `docs/formats.md`
- Support columns: `Data`, `Lançamento`, `Categoria`, `Tipo`, `Valor`
- Parse `Data` as `DD/MM/YYYY`
- Parse `Valor` from Brazilian currency format into `Decimal`
- Return a list of transactions
- Preserve `Categoria` and `Tipo` as metadata
- Keep implementation simple
- Include basic tests with sample data
- Do not implement normalization or output formatting yet

## Step 3 - Validation

Add validation with error reporting.

## Notes

Prompts are intentionally small to reduce token usage and improve code quality.
