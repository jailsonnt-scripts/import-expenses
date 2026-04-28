from datetime import date
from decimal import Decimal

import pytest

from import_expenses.inter_checking_account import (
    parse_inter_checking_account_statement,
)


def test_parse_inter_checking_account_statement(tmp_path) -> None:
    ofx_path = tmp_path / "statement.ofx"
    ofx_path.write_text(
        "<OFX><BANKACCTFROM><BANKID>077</BANKID><ACCTTYPE>CHECKING</ACCTTYPE>"
        "</BANKACCTFROM><BANKTRANLIST><STMTTRN>"
        "<TRNTYPE>CREDIT</TRNTYPE><DTPOSTED>20260425</DTPOSTED>"
        "<TRNAMT>54.15</TRNAMT><FITID>202604250771</FITID>"
        '<MEMO>Pix recebido: "Cp :00000000-CLIENTE EXEMPLO"</MEMO>'
        "<NAME>Cliente Exemplo</NAME></STMTTRN><STMTTRN>"
        "<TRNTYPE>PAYMENT</TRNTYPE><DTPOSTED>20260421</DTPOSTED>"
        "<TRNAMT>-1.00</TRNAMT><FITID>202604210771</FITID>"
        '<MEMO>Pix enviado: "Cp :11111111-LOJA TESTE"</MEMO>'
        "<NAME>Loja Teste</NAME></STMTTRN></BANKTRANLIST></OFX>",
        encoding="utf-8",
    )

    transactions = parse_inter_checking_account_statement(ofx_path)

    assert len(transactions) == 2
    assert transactions[0].transaction_date == date(2026, 4, 25)
    assert transactions[0].description == "Cliente Exemplo"
    assert transactions[0].amount == Decimal("54.15")
    assert transactions[0].source_transaction_type == "CREDIT"
    assert transactions[0].fit_id == "202604250771"
    assert transactions[1].amount == Decimal("-1.00")


def test_parse_inter_checking_account_statement_uses_memo_when_name_is_absent(
    tmp_path,
) -> None:
    ofx_path = tmp_path / "statement.ofx"
    ofx_path.write_text(
        "<OFX><BANKACCTFROM><BANKID>077</BANKID><ACCTTYPE>CHECKING</ACCTTYPE>"
        "</BANKACCTFROM><BANKTRANLIST><STMTTRN>"
        "<TRNTYPE>PAYMENT</TRNTYPE><DTPOSTED>20260421</DTPOSTED>"
        "<TRNAMT>-1.00</TRNAMT><FITID>202604210771</FITID>"
        "<MEMO>Tarifa teste</MEMO></STMTTRN></BANKTRANLIST></OFX>",
        encoding="utf-8",
    )

    transactions = parse_inter_checking_account_statement(ofx_path)

    assert transactions[0].description == "Tarifa teste"


def test_parse_inter_checking_account_statement_rejects_wrong_bank(tmp_path) -> None:
    ofx_path = tmp_path / "statement.ofx"
    ofx_path.write_text(
        "<OFX><BANKACCTFROM><BANKID>999</BANKID><ACCTTYPE>CHECKING</ACCTTYPE>"
        "</BANKACCTFROM><BANKTRANLIST><STMTTRN>"
        "<TRNTYPE>CREDIT</TRNTYPE><DTPOSTED>20260425</DTPOSTED>"
        "<TRNAMT>54.15</TRNAMT><FITID>202604250771</FITID>"
        "<NAME>Cliente Exemplo</NAME></STMTTRN></BANKTRANLIST></OFX>",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="expected BANKID 077"):
        parse_inter_checking_account_statement(ofx_path)


def test_parse_inter_checking_account_statement_rejects_missing_required_tag(
    tmp_path,
) -> None:
    ofx_path = tmp_path / "statement.ofx"
    ofx_path.write_text(
        "<OFX><BANKACCTFROM><BANKID>077</BANKID><ACCTTYPE>CHECKING</ACCTTYPE>"
        "</BANKACCTFROM><BANKTRANLIST><STMTTRN>"
        "<TRNTYPE>CREDIT</TRNTYPE><DTPOSTED>20260425</DTPOSTED>"
        "<FITID>202604250771</FITID><NAME>Cliente Exemplo</NAME>"
        "</STMTTRN></BANKTRANLIST></OFX>",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing TRNAMT"):
        parse_inter_checking_account_statement(ofx_path)


def test_parse_inter_checking_account_statement_rejects_invalid_amount(
    tmp_path,
) -> None:
    ofx_path = tmp_path / "statement.ofx"
    ofx_path.write_text(
        "<OFX><BANKACCTFROM><BANKID>077</BANKID><ACCTTYPE>CHECKING</ACCTTYPE>"
        "</BANKACCTFROM><BANKTRANLIST><STMTTRN>"
        "<TRNTYPE>CREDIT</TRNTYPE><DTPOSTED>20260425</DTPOSTED>"
        "<TRNAMT>invalid</TRNAMT><FITID>202604250771</FITID>"
        "<NAME>Cliente Exemplo</NAME></STMTTRN></BANKTRANLIST></OFX>",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid OFX amount"):
        parse_inter_checking_account_statement(ofx_path)
