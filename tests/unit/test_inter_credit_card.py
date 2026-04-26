from datetime import date
from decimal import Decimal

import pytest

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice


def test_parse_inter_credit_card_invoice_with_utf8_headers(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "\ufeffData,Lançamento,Categoria,Tipo,Valor\n"
        '"25/04/2026","GNT*TEMU","VESTUARIO","Parcela 1/4","R$ 54,15"\n'
        '"26/04/2026","MERCADO","ALIMENTACAO","Compra à vista","R$\xa01.234,56"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

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


def test_parse_inter_credit_card_invoice_accepts_legacy_mojibake_header(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "\ufeffData,LanÃ§amento,Categoria,Tipo,Valor\n"
        '"25/04/2026","GNT*TEMU","VESTUARIO","Parcela 1/4","R$ 54,15"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

    assert transactions[0].description == "GNT*TEMU"


def test_parse_inter_credit_card_invoice_rejects_unexpected_columns(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text("Data,Lançamento,Valor\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid columns"):
        parse_inter_credit_card_invoice(csv_path)


def test_parse_inter_credit_card_invoice_rejects_invalid_date(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "Data,Lançamento,Categoria,Tipo,Valor\n"
        '"2026-04-25","GNT*TEMU","VESTUARIO","Parcela 1/4","R$ 54,15"\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        parse_inter_credit_card_invoice(csv_path)
