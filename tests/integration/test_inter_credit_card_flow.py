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

    write_credit_card_import_csv(transactions, output_path, due_date=date(2026, 5, 10))

    assert len(transactions) == 1
    assert transactions[0].transaction_date == date(2026, 4, 26)
    assert transactions[0].description == "COMPRA TESTE MERCADO"
    assert transactions[0].amount == Decimal("1234.56")
    assert transactions[0].source_category == "SUPERMERCADO"
    assert transactions[0].source_transaction_type == "Compra \u00e0 vista"

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows == [
        [
            "COMPRA TESTE MERCADO",
            "1234.56",
            "10/05/2026",
            "Outros",
            "Outros",
            "Inter",
            "Inter",
            (
                "Inter category: SUPERMERCADO; "
                "Inter type: Compra \u00e0 vista; "
                "Transaction date: 26/04/2026"
            ),
            "26/04/2026 08:00",
        ],
    ]
