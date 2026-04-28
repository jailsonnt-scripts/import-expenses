# Technical Decisions

## Why Python Standard Library

To minimize dependencies and keep the project simple and portable.

## Why src/ layout

Avoid import conflicts and follow modern Python packaging practices.

## Why no pandas

- Overkill for this use case
- Higher complexity
- Less control over parsing behavior

## Incremental Development

The project is built step-by-step using AI assistance to ensure:
- correctness
- simplicity
- test coverage

## Minhas Financas Credit Card Output

Credit card output follows the Minhas Financas CSV import instructions directly:

- no header row
- source amount sign preserved for credit card expenses
- `Outros` for category and subcategory
- `Inter` for account and card fields
- invoice due date supplied by `--due-date`
- final transaction date/time field after notes, defaulting to `08:00` when source time is unavailable

The CLI supports both `--output` for an exact file path and `--output-dir` for choosing only the destination directory.

## Inter Checking Account OFX Output

Inter checking account imports use the OFX export because the bank statement is
available as structured transaction data.

- `DTPOSTED` becomes `Data Venc`
- `TRNAMT` keeps the source sign
- `NAME` is preferred for description, with `MEMO` as fallback
- `Cartao` is empty because this is not a credit card transaction
- `Data Transacao` comes from `--transaction-date` or today's date
- `.ofx` input paths are inferred as `inter-checking`
