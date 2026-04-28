import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from import_expenses.inter_checking_account import (
    parse_inter_checking_account_statement,
)
from import_expenses.minhas_financas import write_checking_account_import_csv


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_inter_checking_account_happy_path(tmp_path) -> None:
    transactions = parse_inter_checking_account_statement(
        FIXTURES_DIR / "inter_checking_account.ofx"
    )
    output_path = tmp_path / "minhas-financas.csv"

    write_checking_account_import_csv(
        transactions,
        output_path,
        transaction_date=date(2026, 4, 28),
    )

    assert len(transactions) == 2
    assert transactions[0].transaction_date == date(2026, 4, 25)
    assert transactions[0].description == "Cliente Exemplo"
    assert transactions[0].amount == Decimal("54.15")

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows == [
        [
            "Cliente Exemplo",
            "54.15",
            "25/04/2026",
            "Outros",
            "Outros",
            "Inter",
            "",
            (
                "Inter checking type: CREDIT; Fit ID: 202604250771; "
                "Transaction date: 25/04/2026; "
                'Memo: Pix recebido: "Cp :00000000-CLIENTE EXEMPLO"'
            ),
            "28/04/2026 08:00",
        ],
        [
            "Loja Teste",
            "-1.00",
            "21/04/2026",
            "Outros",
            "Outros",
            "Inter",
            "",
            (
                "Inter checking type: PAYMENT; Fit ID: 202604210771; "
                "Transaction date: 21/04/2026; "
                'Memo: Pix enviado: "Cp :11111111-LOJA TESTE"'
            ),
            "28/04/2026 08:00",
        ],
    ]
