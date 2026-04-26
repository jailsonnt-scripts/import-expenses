import csv
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Transaction:
    transaction_date: date
    description: str
    amount: Decimal
    source_category: str
    source_transaction_type: str


EXPECTED_COLUMNS = ["Data", "Lançamento", "Categoria", "Tipo", "Valor"]
HEADER_ALIASES = {
    "LanÃ§amento": "Lançamento",
}


def parse_inter_credit_card_invoice(path: str | Path) -> list[Transaction]:
    with Path(path).open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        normalized_fieldnames = _normalize_fieldnames(reader.fieldnames)
        _validate_columns(normalized_fieldnames)
        return [_parse_row(_normalize_row(row)) for row in reader]


def _validate_columns(fieldnames: list[str] | None) -> None:
    if fieldnames != EXPECTED_COLUMNS:
        raise ValueError(f"Invalid columns: expected {EXPECTED_COLUMNS}, got {fieldnames}")


def _normalize_fieldnames(fieldnames: list[str] | None) -> list[str] | None:
    if fieldnames is None:
        return None
    return [HEADER_ALIASES.get(fieldname, fieldname) for fieldname in fieldnames]


def _normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {HEADER_ALIASES.get(key, key): value for key, value in row.items()}


def _parse_row(row: dict[str, str]) -> Transaction:
    return Transaction(
        transaction_date=_parse_date(row["Data"]),
        description=row["Lançamento"],
        amount=_parse_amount(row["Valor"]),
        source_category=row["Categoria"],
        source_transaction_type=row["Tipo"],
    )


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%d/%m/%Y").date()


def _parse_amount(value: str) -> Decimal:
    normalized = (
        value.replace("R$", "")
        .replace("\xa0", "")
        .replace(" ", "")
        .replace(".", "")
        .replace(",", ".")
    )
    return Decimal(normalized)
