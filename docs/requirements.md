# Requirements

## Functional

- Read CSV files from different banks
- Support multiple input formats
- Parse transactions into a common structure
- Normalize dates, amounts, and transaction types
- Generate a standardized CSV output for Minhas Financas
- Report invalid rows with line number and reason

## Data Handling

- No invalid row should be silently ignored
- Invalid data must be reported
- Valid data must be preserved unless an explicit business rule excludes it
- Rows excluded by explicit business rules must be covered by tests

## Supported Sources (initial)

- Inter (checking account)
- Inter (credit card)
- Nubank (credit card)

Inter Credit Card Requirements:

- Read CSV exported from Inter credit card invoice
- Support columns: Data, Lancamento, Categoria, Tipo, Valor
- Parse Brazilian currency values such as `R$ 54,15`
- Preserve source category and transaction type for notes or future classification
- Generate output category as `Outros` in the initial version
- Omit installments whose Tipo matches `Parcela X/Y` because Minhas Financas cannot import them correctly
- Omit invoice payments whose Lancamento is `PAGTO DEBITO AUTOMATICO`
- Preserve the parsed source sign when generating credit card amounts
- Generate output without a header row
- Use the invoice due date as `Data Venc` when it is provided by CLI
- Generate `Outros` for both category and subcategory
- Generate `Inter` for both account and credit card fields
- Append transaction date/time after notes, using `08:00` when the source has no time

Inter Checking Account Requirements:

- Read OFX exported from Inter checking account statements
- Validate the OFX as Inter bank `077` and account type `CHECKING`
- Parse transactions from `STMTTRN` entries
- Parse `DTPOSTED` as the real-world transaction or due date
- Parse `TRNAMT` as a decimal amount and preserve the source sign
- Use `NAME` as description, falling back to `MEMO`
- Preserve `TRNTYPE`, `FITID`, transaction date, and memo in notes
- Generate output category and subcategory as `Outros`
- Generate `Inter` for account and an empty credit card field
- Generate `Data Venc` from `DTPOSTED`
- Generate `Data Transacao` from CLI `--transaction-date`, defaulting to today's date
- Prompt for missing CLI input values when they are necessary and cannot be inferred

## Non-functional

- Simple and maintainable code
- Testable components
- No external dependencies unless necessary

## Future Enhancements

- AI-based category classification
- AI-based description enrichment
- Smarter account and credit card mapping

## Implementation Order

1. Inter credit card invoice CSV
2. Inter checking account
3. Nubank credit card
4. Other sources

## Priority

Inter credit card is the first supported format.
All parsing, validation, and normalization logic must be validated using this source before expanding to others.
