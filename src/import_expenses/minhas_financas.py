import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from import_expenses.inter_credit_card import Transaction


OUTPUT_FIELDS = [
    "description",
    "amount",
    "due_date",
    "category",
    "subcategory",
    "account",
    "credit_card",
    "notes",
    "transaction_datetime",
]

DEFAULT_CATEGORY = "Outros"
DEFAULT_SUBCATEGORY = "Outros"
DEFAULT_ACCOUNT = "Inter"
DEFAULT_CREDIT_CARD = "Inter"
DEFAULT_TRANSACTION_TIME = "08:00"
MAX_DESCRIPTION_LENGTH = 35


def write_credit_card_import_csv(
    transactions: Iterable[Transaction],
    path: str | Path,
    due_date: date | None = None,
) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDS)
        writer.writerows(
            format_credit_card_row(transaction, due_date) for transaction in transactions
        )


def format_credit_card_row(
    transaction: Transaction,
    due_date: date | None = None,
) -> dict[str, str]:
    row_due_date = due_date or transaction.transaction_date
    return {
        "description": truncate_description(transaction.description),
        "amount": format_amount(transaction.amount),
        "due_date": row_due_date.strftime("%d/%m/%Y"),
        "category": DEFAULT_CATEGORY,
        "subcategory": DEFAULT_SUBCATEGORY,
        "account": DEFAULT_ACCOUNT,
        "credit_card": DEFAULT_CREDIT_CARD,
        "notes": format_notes(transaction),
        "transaction_datetime": format_transaction_datetime(transaction),
    }


def truncate_description(description: str) -> str:
    return description[:MAX_DESCRIPTION_LENGTH]


def format_amount(amount: Decimal) -> str:
    return f"{amount:.2f}"


def format_notes(transaction: Transaction) -> str:
    transaction_date = transaction.transaction_date.strftime("%d/%m/%Y")
    return (
        f"Inter category: {transaction.source_category}; "
        f"Inter type: {transaction.source_transaction_type}; "
        f"Transaction date: {transaction_date}"
    )


def format_transaction_datetime(transaction: Transaction) -> str:
    return f"{transaction.transaction_date.strftime('%d/%m/%Y')} {DEFAULT_TRANSACTION_TIME}"
