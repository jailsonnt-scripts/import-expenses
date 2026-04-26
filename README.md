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

## Usage

```bash
python -m import_expenses.cli --input input.csv --output output.csv --profile nubank-card
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

This project is built incrementally using AI-assisted development (Codex) with strict control over complexity and quality.

---

# 🤖 AGENTS.md (para Codex — curto e direto)

```md
# Project: import-expenses

## Goal
Convert bank and credit card CSV files into a normalized CSV for Minhas Finanças.

## Scope
- Handle checking account and credit card transactions
- Support multiple CSV formats via configuration

## Rules
- Use Python standard library when possible
- Do not ignore invalid data silently
- Keep functions small and testable
- Prefer simple solutions over complex abstractions

## Workflow
- Implement one feature at a time
- Always run tests before finishing a task
- Do not refactor unrelated code

## Commands
- Run tests: pytest
