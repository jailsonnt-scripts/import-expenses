from datetime import date
from decimal import Decimal

import pytest

from import_expenses.inter_credit_card import parse_inter_credit_card_invoice


def test_parse_inter_credit_card_invoice_with_utf8_headers(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "\ufeffData,Lan\u00e7amento,Categoria,Tipo,Valor\n"
        '"25/04/2026","LOJA PARCELADA TESTE","COMPRAS","Parcela 1/4","R$ 54,15"\n'
        '"26/04/2026","COMPRA TESTE MERCADO","SUPERMERCADO","Compra \u00e0 vista","R$\xa01.234,56"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

    assert len(transactions) == 1
    assert transactions[0].transaction_date == date(2026, 4, 26)
    assert transactions[0].description == "COMPRA TESTE MERCADO"
    assert transactions[0].amount == Decimal("1234.56")
    assert transactions[0].source_category == "SUPERMERCADO"
    assert transactions[0].source_transaction_type == "Compra \u00e0 vista"


def test_parse_inter_credit_card_invoice_accepts_legacy_mojibake_header(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "\ufeffData,Lan\u00c3\u00a7amento,Categoria,Tipo,Valor\n"
        '"25/04/2026","COMPRA TESTE","COMPRAS","Compra \u00e0 vista","R$ 54,15"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

    assert transactions[0].description == "COMPRA TESTE"


def test_parse_inter_credit_card_invoice_filters_installments(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "Data,Lan\u00e7amento,Categoria,Tipo,Valor\n"
        '"25/04/2026","LOJA PARCELADA TESTE","COMPRAS","Parcela 1/4","R$ 54,15"\n'
        '"24/04/2026","LOJA","COMPRAS","Parcela 11/12","R$ 44,84"\n'
        '"26/04/2026","COMPRA TESTE MERCADO","SUPERMERCADO","Compra \u00e0 vista","R$ 12,00"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

    assert [transaction.description for transaction in transactions] == [
        "COMPRA TESTE MERCADO"
    ]


def test_parse_inter_credit_card_invoice_filters_invoice_payment(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "Data,Lan\u00e7amento,Categoria,Tipo,Valor\n"
        '"07/04/2026","PAGTO DEBITO AUTOMATICO","OUTROS","Compra \u00e0 vista","-R$ 13.479,16"\n'
        '"26/04/2026","COMPRA TESTE MERCADO","SUPERMERCADO","Compra \u00e0 vista","R$ 12,00"\n',
        encoding="utf-8",
    )

    transactions = parse_inter_credit_card_invoice(csv_path)

    assert [transaction.description for transaction in transactions] == [
        "COMPRA TESTE MERCADO"
    ]


def test_parse_inter_credit_card_invoice_rejects_unexpected_columns(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text("Data,Lan\u00e7amento,Valor\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid columns"):
        parse_inter_credit_card_invoice(csv_path)


def test_parse_inter_credit_card_invoice_rejects_invalid_date(tmp_path) -> None:
    csv_path = tmp_path / "invoice.csv"
    csv_path.write_text(
        "Data,Lan\u00e7amento,Categoria,Tipo,Valor\n"
        '"2026-04-25","COMPRA TESTE","COMPRAS","Compra \u00e0 vista","R$ 54,15"\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        parse_inter_credit_card_invoice(csv_path)
