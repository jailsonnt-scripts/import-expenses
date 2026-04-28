# CSV Formats

## Output - Minhas Financas: Credit Card

Separator: comma `,`

Header: none. The first CSV line must be a transaction.

Expected order:

```csv
Descricao,Valor,Data Venc,Categoria,Subcategoria,Conta,Cartao,Observacoes,Data Transacao
```

Example for Inter credit card:

```csv
MERCADO,1234.56,10/05/2026,Outros,Outros,Inter,Inter,Inter category: ALIMENTACAO; Inter type: Compra a vista; Transaction date: 26/04/2026,26/04/2026 08:00
```

Column mapping used by this project:

- Descricao: truncated transaction description
- Valor: normalized transaction amount with dot decimal separator
- Data Venc: invoice due date, provided by CLI `--due-date`
- Categoria: `Outros`
- Subcategoria: `Outros`
- Conta: `Inter` for Inter credit card imports
- Cartao: `Inter`
- Observacoes: source metadata
- Data Transacao: original transaction date and time

## Output - Minhas Financas: Checking Account

Separator: comma `,`

Header: none. The first CSV line must be a transaction.

Expected order:

```csv
Descricao,Valor,Data Venc,Categoria,Subcategoria,Conta,Cartao,Observacoes,Data Transacao
```

Example for Inter checking account:

```csv
Cliente Exemplo,54.15,25/04/2026,Outros,Outros,Inter,,Inter checking type: CREDIT; Fit ID: 202604250771; Transaction date: 25/04/2026,28/04/2026 08:00
```

Column mapping used by this project:

- Descricao: truncated transaction description
- Valor: normalized transaction amount with dot decimal separator
- Data Venc: real-world execution or due date from OFX `DTPOSTED`
- Categoria: `Outros`
- Subcategoria: `Outros`
- Conta: `Inter`
- Cartao: empty
- Observacoes: source metadata
- Data Transacao: effective date when the transaction is created in Minhas Financas, from CLI `--transaction-date` or today's date

## Default Values

- category must default to `Outros`
- subcategory must default to `Outros`
- account must be `Inter` for Inter credit card imports
- credit card must be `Inter` for Inter credit card imports
- future versions may classify categories using AI
- AI-based classification must not be implemented in the initial version

## Rules

- Due date must be in `DD/MM/YYYY` format.
- For credit card transactions, the due date must be the invoice date.
- For Inter credit card imports, the invoice due date should be provided with `--due-date`.
- If `--due-date` is omitted, the transaction date is used as a fallback.
- Output must not include a header row.
- Decimal separator must be a dot, for example `4.50`.
- Do not use comma for decimal values.
- Category, subcategory, account, and credit card are matched by name in Minhas Financas.
- The credit card field must come after account.
- If not a credit card transaction, leave the credit card field empty.
- The notes field is optional and must be the last field.
- Inter output must include a final transaction date/time field after notes so Minhas Financas keeps due date and transaction date separate.
- If the Inter source has no transaction time, use `08:00`.
- The app may ignore incomplete rows, but this system must not silently ignore invalid data.
- Description must be truncated to 35 characters.

## Input Sources

### Inter (checking account)

Input - Inter Checking Account Statement

File characteristics:

- Format: OFX/SGML
- Bank ID: `077`
- Account type: `CHECKING`
- Decimal separator in input: dot
- Amount sign is provided by OFX `TRNAMT`

Required statement tags:

- `BANKID`
- `ACCTTYPE`
- at least one `STMTTRN`

Required transaction tags:

- `TRNTYPE`
- `DTPOSTED`
- `TRNAMT`
- `FITID`
- `NAME` or `MEMO`

Field mapping:

- `DTPOSTED` -> transaction_date and output `Data Venc`
- `NAME` -> description when present
- `MEMO` -> description fallback and notes metadata
- `TRNAMT` -> amount
- `TRNTYPE` -> source_transaction_type
- `FITID` -> source identifier in notes

Parsing rules:

- `BANKID` must be `077`.
- `ACCTTYPE` must be `CHECKING`.
- `DTPOSTED` must be parsed as `YYYYMMDD`; OFX datetime suffixes are ignored.
- `TRNAMT` must parse as a decimal amount and preserve the source sign.
- Missing required statement or transaction data must fail the import.
- Output `Cartao` must be empty.
- Output `Data Transacao` must use `--transaction-date` or today's date when omitted.

### Inter (credit card)

Input - Inter Credit Card Invoice

File characteristics:

- Encoding: UTF-8 with BOM may be present
- Separator: comma
- Fields are quoted with double quotes
- Decimal format: Brazilian currency format
- Currency prefix: `R$`
- Decimal separator in input: comma
- Thousands separator may be dot
- Amount may contain non-breaking spaces after `R$`

Expected columns:

```csv
Data,Lancamento,Categoria,Tipo,Valor
```

The real Inter header may use `Lancamento` with Portuguese accents. Legacy mojibake for the header is also accepted.

Example row:

```csv
"25/04/2026","GNT*TEMU","VESTUARIO","Parcela 1/4","R$ 54,15"
```

Field mapping:

- Data -> transaction_date
- Lancamento -> description
- Categoria -> source_category
- Tipo -> source_transaction_type
- Valor -> amount

Parsing rules:

- Data must be parsed as `DD/MM/YYYY`.
- Valor must remove `R$`, spaces, and non-breaking spaces.
- Valor must convert Brazilian decimal format to normalized decimal.
- For credit card purchases, amount should preserve the parsed source sign.
- Categoria from Inter is source metadata only.
- The initial output category must always be `Outros`.
- Tipo should be preserved in notes or metadata.
- Rows whose Tipo matches `Parcela <number>/<number>` must be omitted from output.
- Rows whose Lancamento is `PAGTO DEBITO AUTOMATICO` must be omitted from output because they represent payment of a previous invoice.
- Lancamento may be truncated in output description if it exceeds 35 characters.

Example normalized interpretation:

```text
transaction_date: 25/04/2026
description: GNT*TEMU
source_category: VESTUARIO
source_transaction_type: Parcela 1/4
amount: 54.15
output_category: Outros
output_amount: 54.15
output_transaction_datetime: 25/04/2026 08:00
```

### Nubank (credit card)

Not implemented yet.
