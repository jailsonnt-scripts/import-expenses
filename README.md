# Import Expenses

CLI tool to normalize bank and credit card exports into a format compatible with "Minhas Finanças".

## Goal

Provide a simple, reliable way to import financial data from different sources into a single standardized format.

## Features

- Parse CSV and OFX files from supported banks
- Support both checking account and credit card transactions
- Normalize date and amount formats
- Generate import-ready CSV output
- Validate input data and report errors

## Scope

This project focuses on:
- Local file processing (no APIs)
- Data normalization and validation
- CLI usage

## Non-goals

- No direct bank integrations
- No web interface
- No real-time sync

## Installation

```bash
pip install -r requirements.txt
```

## Usage

For Inter credit card invoices, pass the invoice due date. This date is used as
the `Data Venc` value required by Minhas Financas. CSV inputs are inferred as
`inter-credit-card` when `--source` is omitted.

```bash
python -m import_expenses --input inter-credit-card.csv --output minhas-financas.csv --due-date 10/05/2026
```

For Inter checking account statements, use the OFX export. The card field is
empty, `Data Venc` comes from the OFX transaction date, and `Data Transacao`
uses the date when the transaction is created in Minhas Financas. If
`--transaction-date` is omitted, today's date is used. OFX inputs are inferred
as `inter-checking` when `--source` is omitted.

```bash
python -m import_expenses --input inter-checking.ofx --output minhas-financas.csv --transaction-date 28/04/2026
```

You can also choose only the destination directory. The output file will be named
from the input file, with `-minhas-financas.csv` appended.

```bash
python -m import_expenses --input inter-checking.ofx --output-dir ./out --transaction-date 28/04/2026
```

If the input path or source cannot be inferred from the file extension, the CLI
prompts for the missing value.

```bash
python -m import_expenses
```

The output CSV uses the Minhas Financas import order and does not include a
header row:

```csv
Descricao,Valor,Data Venc,Categoria,Subcategoria,Conta,Cartao,Observacoes,Data Transacao
```

Rows are exported with dot decimal separator, `Outros` as category and
subcategory, `Inter` as account, and a final transaction date/time column. If
the source has no time, `08:00` is used.

## Project Structure

```bash
src/import_expenses/
tests/unit/
tests/integration/
tests/fixtures/
docs/
```

## Tests

```bash
pytest
pytest tests/unit
pytest tests/integration
```

## Notes

This project is built incrementally using AI-assisted development with strict control over complexity and quality.
