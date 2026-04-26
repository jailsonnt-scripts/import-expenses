from datetime import date
from decimal import Decimal
from pathlib import Path

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_inter_credit_card_invoice_happy_path() -> None:
    transactions = parse_inter_credit_card_invoice(
        FIXTURES_DIR / "inter_credit_card_invoice.csv"
    )

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
