# Import Expenses

CLI tool to normalize bank and credit card CSV files into a format compatible with "Minhas Finanças".

## Goal

Provide a simple, reliable way to import financial data from different sources into a single standardized format.

## Features

- Parse CSV files from multiple banks
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
the `Data Venc` value required by Minhas Financas.

```bash
python -m import_expenses --input inter-credit-card.csv --output minhas-financas.csv --due-date 10/05/2026
```

You can also choose only the destination directory. The output file will be named
from the input file, with `-minhas-financas.csv` appended.

```bash
python -m import_expenses --input inter-credit-card.csv --output-dir ./out --due-date 10/05/2026
```

The output CSV uses the Minhas Financas import order and does not include a
header row:

```csv
Descricao,Valor,Data Venc,Categoria,Subcategoria,Conta,Cartao,Observacoes,Data Transacao
```

Credit card expenses are exported with dot decimal separator, `Outros` as
category and subcategory, `Inter` as account and card, and a final transaction
date/time column. If the source has no time, `08:00` is used.

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
