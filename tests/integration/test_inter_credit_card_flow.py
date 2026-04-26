import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice
from import_expenses.minhas_financas import write_credit_card_import_csv


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_inter_credit_card_invoice_happy_path(tmp_path) -> None:
    transactions = parse_inter_credit_card_invoice(
        FIXTURES_DIR / "inter_credit_card_invoice.csv"
    )
    output_path = tmp_path / "minhas-financas.csv"

    write_credit_card_import_csv(transactions, output_path)

    assert len(transactions) == 2

    assert transactions[0].transaction_date == date(2026, 4, 25)
    assert transactions[0].description == "GNT*TEMU"
    assert transactions[0].amount == Decimal("54.15")
    assert transactions[0].source_category == "VESTUARIO"
    assert transactions[0].source_transaction_type == "Parcela 1/4"

    assert transactions[1].transaction_date == date(2026, 4, 26)
    assert transactions[1].description == "MERCADO"
    assert transactions[1].amount == Decimal("1234.56")
    assert transactions[1].source_category == "ALIMENTACAO"
    assert transactions[1].source_transaction_type == "Compra à vista"

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
        },
        {
            "description": "MERCADO",
            "amount": "1234.56",
            "due_date": "26/04/2026",
            "category": "Outros",
            "subcategory": "",
            "account": "",
            "credit_card": "Inter",
            "notes": (
                "Inter category: ALIMENTACAO; "
                "Inter type: Compra à vista; "
                "Transaction date: 26/04/2026"
            ),
        },
    ]
