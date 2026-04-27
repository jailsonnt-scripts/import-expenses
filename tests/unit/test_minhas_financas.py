import csv
from datetime import date
from decimal import Decimal

from import_expenses.inter_credit_card import Transaction
from import_expenses.minhas_financas import (
    format_credit_card_row,
    format_transaction_datetime,
    truncate_description,
    write_credit_card_import_csv,
)


def test_format_credit_card_row() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="COMPRA TESTE",
        amount=Decimal("54.15"),
        source_category="COMPRAS",
        source_transaction_type="Parcela 1/4",
    )

    row = format_credit_card_row(transaction)

    assert row == {
        "description": "COMPRA TESTE",
        "amount": "54.15",
        "due_date": "25/04/2026",
        "category": "Outros",
        "subcategory": "Outros",
        "account": "Inter",
        "credit_card": "Inter",
        "notes": (
            "Inter category: COMPRAS; "
            "Inter type: Parcela 1/4; "
            "Transaction date: 25/04/2026"
        ),
        "transaction_datetime": "25/04/2026 08:00",
    }


def test_truncate_description_limits_text_to_35_characters() -> None:
    description = "COMPRA INTERNACIONAL COM DESCRICAO MUITO LONGA"

    assert truncate_description(description) == "COMPRA INTERNACIONAL COM DESCRICAO "
    assert len(truncate_description(description)) == 35


def test_format_credit_card_row_defaults_category_to_outros() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="COMPRA TESTE",
        amount=Decimal("54.15"),
        source_category="COMPRAS",
        source_transaction_type="Parcela 1/4",
    )

    row = format_credit_card_row(transaction)

    assert row["category"] == "Outros"
    assert row["subcategory"] == "Outros"


def test_format_credit_card_row_uses_invoice_due_date() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="COMPRA TESTE",
        amount=Decimal("54.15"),
        source_category="COMPRAS",
        source_transaction_type="Compra à vista",
    )

    row = format_credit_card_row(transaction, due_date=date(2026, 5, 10))

    assert row["due_date"] == "10/05/2026"


def test_format_credit_card_row_preserves_negative_amount() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="ESTORNO",
        amount=Decimal("-13.00"),
        source_category="OUTROS",
        source_transaction_type="Compra à vista",
    )

    row = format_credit_card_row(transaction)

    assert row["amount"] == "-13.00"


def test_format_transaction_datetime_uses_default_time() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="COMPRA TESTE",
        amount=Decimal("54.15"),
        source_category="COMPRAS",
        source_transaction_type="Compra à vista",
    )

    assert format_transaction_datetime(transaction) == "25/04/2026 08:00"


def test_write_credit_card_import_csv(tmp_path) -> None:
    output_path = tmp_path / "minhas-financas.csv"
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="COMPRA TESTE",
        amount=Decimal("54.15"),
        source_category="COMPRAS",
        source_transaction_type="Parcela 1/4",
    )

    write_credit_card_import_csv([transaction], output_path, due_date=date(2026, 5, 10))

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows == [
        [
            "COMPRA TESTE",
            "54.15",
            "10/05/2026",
            "Outros",
            "Outros",
            "Inter",
            "Inter",
            (
                "Inter category: COMPRAS; "
                "Inter type: Parcela 1/4; "
                "Transaction date: 25/04/2026"
            ),
            "25/04/2026 08:00",
        ]
    ]
