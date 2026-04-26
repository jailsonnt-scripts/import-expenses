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

```bash
python -m import_expenses --input inter-credit-card.csv --output minhas-financas.csv
```

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
