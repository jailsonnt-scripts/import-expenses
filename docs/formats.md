# CSV Formats

## Output - Minhas Finanças: Credit Card

Separator: comma `,`

Expected order:

```csv
description,amount,due_date,category,subcategory,account,credit_card,notes
```

Example:

```csv
Café da tarde,4.50,16/02/2019,Alimentação,Lanche,Itaú,Nubank,,16/02/2019 08:34
```

Example with notes:

```csv
Café da tarde,4.50,16/02/2019,Alimentação,Lanche,Itaú,Nubank,Lanchonete da esquina
```

## Default Values
- category must default to Outros
- subcategory must be Outros by default
- future versions may classify categories using AI
- AI-based classification must not be implemented in the initial version

## Rules

- Due date must be in DD/MM/YYYY format
- For credit card transactions, the due date must be the invoice date
- Decimal separator must be a dot (4.50)
- Do not use comma for decimal values
- Category, subcategory, account and credit card are matched by name
- The credit_card field must come after account
- If not a credit card transaction, leave the credit_card field empty
- The notes field is optional and must be the last field
- If a transaction date exists, it may appear after notes
- The app may ignore incomplete rows, but this system must not silently ignore invalid data
- description must be truncated to 35 characters



## Input sources

### Inter (checking account)
### Inter (credit card)

Input - Inter Credit Card Invoice

File characteristics:

Encoding: UTF-8 with BOM may be present
Separator: comma
Fields are quoted with double quotes
Decimal format: Brazilian currency format
Currency prefix: R$
Decimal separator in input: comma
Thousands separator may be dot
Amount may contain non-breaking spaces after R$

Expected columns:

Data
Lançamento
Categoria
Tipo
Valor

Example row:

"25/04/2026","GNT*TEMU","VESTUARIO","Parcela 1/4","R$ 54,15"

Field mapping:

Data → transaction_date
Lançamento → description
Categoria → source_category
Tipo → source_transaction_type
Valor → amount

Parsing rules:

Data must be parsed as DD/MM/YYYY
Valor must remove R$, spaces and non-breaking spaces
Valor must convert Brazilian decimal format to normalized decimal
For credit card purchases, amount should be treated as expense
Categoria from Inter is source metadata only
The initial output category must always be Outros
Tipo should be preserved in notes or metadata
Lançamento may be truncated in output description if it exceeds 35 characters

Example normalized interpretation:

transaction_date: 25/04/2026
description: GNT*TEMU
source_category: VESTUARIO
source_transaction_type: Parcela 1/4
amount: 54.15
output_category: Outros

### Nubank (credit card)
