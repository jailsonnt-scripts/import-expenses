from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
import re


@dataclass(frozen=True)
class CheckingTransaction:
    transaction_date: date
    description: str
    amount: Decimal
    source_transaction_type: str
    fit_id: str
    memo: str


TRANSACTION_PATTERN = re.compile(r"<STMTTRN>(.*?)</STMTTRN>", re.DOTALL | re.IGNORECASE)
REQUIRED_TRANSACTION_TAGS = ["TRNTYPE", "DTPOSTED", "TRNAMT", "FITID"]


def parse_inter_checking_account_statement(path: str | Path) -> list[CheckingTransaction]:
    content = _read_ofx(path)
    _validate_inter_checking_statement(content)
    transaction_blocks = TRANSACTION_PATTERN.findall(content)
    if not transaction_blocks:
        raise ValueError("Invalid OFX: no STMTTRN transactions found")
    return [_parse_transaction(block) for block in transaction_blocks]


def _read_ofx(path: str | Path) -> str:
    data = Path(path).read_bytes()
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("cp1252")


def _validate_inter_checking_statement(content: str) -> None:
    bank_id = _extract_required_tag(content, "BANKID")
    account_type = _extract_required_tag(content, "ACCTTYPE")
    if bank_id != "077":
        raise ValueError(f"Invalid OFX: expected BANKID 077, got {bank_id}")
    if account_type.upper() != "CHECKING":
        raise ValueError(f"Invalid OFX: expected ACCTTYPE CHECKING, got {account_type}")


def _parse_transaction(block: str) -> CheckingTransaction:
    values = {tag: _extract_required_tag(block, tag) for tag in REQUIRED_TRANSACTION_TAGS}
    memo = _extract_optional_tag(block, "MEMO")
    name = _extract_optional_tag(block, "NAME")
    description = name or memo
    if not description:
        raise ValueError("Invalid OFX transaction: expected NAME or MEMO")
    return CheckingTransaction(
        transaction_date=_parse_ofx_date(values["DTPOSTED"]),
        description=description,
        amount=_parse_amount(values["TRNAMT"]),
        source_transaction_type=values["TRNTYPE"],
        fit_id=values["FITID"],
        memo=memo,
    )


def _extract_required_tag(content: str, tag: str) -> str:
    value = _extract_optional_tag(content, tag)
    if value == "":
        raise ValueError(f"Invalid OFX: missing {tag}")
    return value


def _extract_optional_tag(content: str, tag: str) -> str:
    closed_match = re.search(
        rf"<{tag}>(.*?)</{tag}>",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if closed_match is not None:
        return closed_match.group(1).strip()

    open_match = re.search(rf"<{tag}>([^<\r\n]+)", content, re.IGNORECASE)
    if open_match is not None:
        return open_match.group(1).strip()
    return ""


def _parse_ofx_date(value: str) -> date:
    normalized = value[:8]
    try:
        return datetime.strptime(normalized, "%Y%m%d").date()
    except ValueError:
        raise ValueError(f"Invalid OFX date for DTPOSTED: {value}")


def _parse_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value)
    except Exception as error:
        raise ValueError(f"Invalid OFX amount for TRNAMT: {value}") from error
    if not amount.is_finite():
        raise ValueError(f"Invalid OFX amount for TRNAMT: {value}")
    return amount
