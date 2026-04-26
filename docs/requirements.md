# Requirements

## Functional

- Read CSV files from different banks
- Support multiple input formats
- Parse transactions into a common structure
- Normalize:
  - dates
  - amounts
  - transaction types
- Generate a standardized CSV output
- Report invalid rows with line number and reason

## Data Handling

- No row should be silently ignored
- Invalid data must be reported
- Valid data must always be preserved

## Supported Sources (initial)

- Inter (checking account)
- Inter (credit card)
Inter Credit Card Requirements:

Read CSV exported from Inter credit card invoice
Support columns: Data, Lançamento, Categoria, Tipo, Valor
Parse Brazilian currency values such as R$ 54,15
Preserve source category and transaction type for notes or future classification
Generate output category as Outros in the initial version
- Nubank (credit card)

## Non-functional

- Simple and maintainable code
- Testable components
- No external dependencies unless necessary

## Future Enhancements
AI-based category classification
AI-based description enrichment
Smarter account and credit card mapping

## Implementation Order

Inter credit card (invoice CSV)
Inter checking account
Nubank credit card
Other sources

## Priority

Inter credit card is the first supported format
All parsing, validation and normalization logic must be validated using this source before expanding to others