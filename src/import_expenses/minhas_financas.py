import csv
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
]

DEFAULT_CATEGORY = "Outros"
MAX_DESCRIPTION_LENGTH = 35


def write_credit_card_import_csv(
    transactions: Iterable[Transaction],
    path: str | Path,
) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(format_credit_card_row(transaction) for transaction in transactions)


def format_credit_card_row(transaction: Transaction) -> dict[str, str]:
    return {
        "description": truncate_description(transaction.description),
        "amount": format_amount(transaction.amount),
        "due_date": transaction.transaction_date.strftime("%d/%m/%Y"),
        "category": DEFAULT_CATEGORY,
        "subcategory": "",
        "account": "",
        "credit_card": "Inter",
        "notes": format_notes(transaction),
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
