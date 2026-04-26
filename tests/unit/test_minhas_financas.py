import csv
from datetime import date
from decimal import Decimal

from import_expenses.inter_credit_card import Transaction
from import_expenses.minhas_financas import (
    format_credit_card_row,
    truncate_description,
    write_credit_card_import_csv,
)


def test_format_credit_card_row() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="GNT*TEMU",
        amount=Decimal("54.15"),
        source_category="VESTUARIO",
        source_transaction_type="Parcela 1/4",
    )

    row = format_credit_card_row(transaction)

    assert row == {
        "description": "GNT*TEMU",
        "amount": "54.15",
        "due_date": "25/04/2026",
        "category": "Outros",
        "subcategory": "",
        "account": "",
        "credit_card": "Inter",
        "notes": (
            "Inter category: VESTUARIO; "
            "Inter type: Parcela 1/4; "
            "Transaction date: 25/04/2026"
        ),
    }


def test_truncate_description_limits_text_to_35_characters() -> None:
    description = "COMPRA INTERNACIONAL COM DESCRICAO MUITO LONGA"

    assert truncate_description(description) == "COMPRA INTERNACIONAL COM DESCRICAO "
    assert len(truncate_description(description)) == 35


def test_format_credit_card_row_defaults_category_to_outros() -> None:
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="GNT*TEMU",
        amount=Decimal("54.15"),
        source_category="VESTUARIO",
        source_transaction_type="Parcela 1/4",
    )

    row = format_credit_card_row(transaction)

    assert row["category"] == "Outros"


def test_write_credit_card_import_csv(tmp_path) -> None:
    output_path = tmp_path / "minhas-financas.csv"
    transaction = Transaction(
        transaction_date=date(2026, 4, 25),
        description="GNT*TEMU",
        amount=Decimal("54.15"),
        source_category="VESTUARIO",
        source_transaction_type="Parcela 1/4",
    )

    write_credit_card_import_csv([transaction], output_path)

    header = output_path.read_text(encoding="utf-8").splitlines()[0]
    assert (
        header
        == "description,amount,due_date,category,subcategory,account,credit_card,notes"
    )

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows == [
        {
            "description": "GNT*TEMU",
            "amount": "54.15",
            "due_date": "25/04/2026",
            "category": "Outros",
            "subcategory": "",
            "account": "",
            "credit_card": "Inter",
            "notes": (
                "Inter category: VESTUARIO; "
                "Inter type: Parcela 1/4; "
                "Transaction date: 25/04/2026"
            ),
        }
    ]
