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

## Step 3 - Integration Test Support

Prompt:

Add integration test support.

- Create `tests/unit`, `tests/integration`, and `tests/fixtures`
- Move detailed parser and CLI tests to unit tests
- Add a small fixture CSV for Inter credit card invoices
- Add one happy-path integration test using the parser flow
- Keep detailed success and failure scenarios in unit tests
- Update documentation if test commands changed
- Run pytest before finishing

Outcome:

- Unit tests became the place for detailed parser and CLI behavior
- Integration tests now validate end-to-end success for supported input files
- Shared CSV samples live in `tests/fixtures`

## Step 4 - Testing Policy

Prompt:

Define when to use unit tests vs integration tests.

- Unit tests are the default for detailed behavior
- Unit tests should cover success and failure scenarios
- Integration tests should focus on end-to-end success behavior
- Add integration failure tests only for critical risks
- Keep sample fixtures small and explicit

Outcome:

- Test organization is explicit: `tests/unit`, `tests/integration`, `tests/fixtures`
- New code changes should include or update meaningful tests
- Integration coverage stays focused instead of duplicating unit tests

## Step 5 - Commit And Push Workflow

Prompt:

Define the workflow for `push`, `commit`, and `commit and push` requests.

- Check `git status` and `git diff`
- Run pytest before committing
- Fix failing tests before continuing
- Create focused commits with a short title and bullet-point body
- Push using the configured SSH remote
- Do not force push unless explicitly requested

Outcome:

- Push requests now imply validation, tests, commit, and SSH push
- Commits should stay focused and include concise bullet summaries
- Failing tests block commits

## Step 6 - Prompt Documentation Policy

Prompt:

Document only meaningful and reusable prompts or decisions.

- Update `docs/prompts.md` for new workflows, architecture decisions, testing strategies, or reusable patterns
- Do not log trivial or repetitive changes
- Keep entries concise and structured as prompt plus outcome

Outcome:

- Prompt history records reusable project guidance instead of every small task
- Future prompt updates have a clear trigger and format

## Step 7 - Minhas Finanças Credit Card Output

Prompt:

Add output CSV generation for Minhas Finanças credit card import.

- Use `docs/formats.md` as the source of truth
- Implement output generation only for Inter credit card for now
- Use the standard library `csv` module
- Generate fields in the required Minhas Finanças order
- Format amounts with dot decimal separator and dates as `DD/MM/YYYY`
- Default category to `Outros` and keep subcategory empty
- Limit descriptions to 35 characters
- Preserve useful Inter metadata in notes
- Do not implement AI category classification
- Cover output formatting with unit tests and the fixture-to-output happy path with integration tests

Outcome:

- Inter credit card transactions can now be written as Minhas Finanças credit card CSV rows
- The CLI turns an Inter invoice CSV into an output CSV file
- Unit tests cover row formatting, defaults, and truncation
- Integration tests cover parser-to-output success behavior

## Notes

Prompts are intentionally small to reduce token usage and improve code quality.
