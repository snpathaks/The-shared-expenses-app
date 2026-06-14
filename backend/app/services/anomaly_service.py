import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from app.models.enums import AnomalySeverity


KNOWN_USERS = {"Aisha", "Rohan", "Priya", "Meera", "Dev", "Sam"}


@dataclass(frozen=True)
class AnomalyFinding:
    rule_code: str
    severity: AnomalySeverity
    issue_type: str
    message: str
    details: dict
    requires_approval: bool = True


class AnomalyService:
    def inspect_row(self, row_number: int, row: dict[str, str]) -> list[AnomalyFinding]:
        findings: list[AnomalyFinding] = []
        amount_text = row.get("amount", "")
        currency = row.get("currency", "")
        paid_by = row.get("paid_by", "")
        split_type = row.get("split_type", "")
        description = row.get("description", "")
        notes = row.get("notes", "")

        if not paid_by.strip():
            findings.append(self._finding("RULE_004_MISSING_REQUIRED_VALUE", "critical", "Missing payer", row_number))
        elif paid_by.strip() not in KNOWN_USERS:
            findings.append(self._finding("RULE_009_INCONSISTENT_NAME", "warning", "Inconsistent payer name", row_number))

        if not currency.strip():
            findings.append(self._finding("RULE_004_MISSING_REQUIRED_VALUE", "critical", "Missing currency", row_number))
        elif currency.strip() != "INR":
            findings.append(self._finding("RULE_006_CURRENCY_MISMATCH", "critical", "Currency conversion required", row_number))

        try:
            amount = Decimal(amount_text.replace(",", "").strip())
        except (InvalidOperation, AttributeError):
            findings.append(self._finding("RULE_004_MISSING_REQUIRED_VALUE", "critical", "Invalid amount", row_number))
            amount = None

        if amount is not None:
            if amount < 0:
                findings.append(self._finding("RULE_002_NEGATIVE_AMOUNT", "critical", "Negative amount", row_number))
            if amount == 0:
                findings.append(self._finding("RULE_015_ZERO_AMOUNT", "warning", "Zero amount", row_number))
            if currency.strip() == "INR" and abs(amount.as_tuple().exponent) > 2:
                findings.append(self._finding("RULE_016_CURRENCY_PRECISION", "critical", "Too many decimal places", row_number))

        if self._looks_like_settlement(description, notes):
            findings.append(self._finding("RULE_005_SETTLEMENT_AS_EXPENSE", "critical", "Settlement recorded as expense", row_number))

        if split_type in {"unequal", "share"}:
            findings.append(self._finding("RULE_017_SPLIT_TYPE_ALIAS", "warning", "Non-canonical split type", row_number))

        if split_type == "percentage":
            percentages = [Decimal(value) for value in re.findall(r"(\d+(?:\.\d+)?)%", row.get("split_details", ""))]
            if percentages and sum(percentages, Decimal("0")) != Decimal("100"):
                findings.append(self._finding("RULE_008_SPLIT_MISMATCH", "critical", "Percentages do not total 100", row_number))

        for participant in [part.strip() for part in row.get("split_with", "").split(";") if part.strip()]:
            if participant not in KNOWN_USERS:
                findings.append(
                    AnomalyFinding(
                        "RULE_007_UNKNOWN_MEMBER_NAME",
                        AnomalySeverity.CRITICAL,
                        "Unknown participant",
                        f"Unknown participant {participant}",
                        {"row_number": row_number, "participant": participant},
                    )
                )

        return findings

    def _finding(self, rule_code: str, severity: str, issue_type: str, row_number: int) -> AnomalyFinding:
        return AnomalyFinding(
            rule_code=rule_code,
            severity=AnomalySeverity(severity),
            issue_type=issue_type,
            message=issue_type,
            details={"row_number": row_number},
        )

    def _looks_like_settlement(self, description: str, notes: str) -> bool:
        text = f"{description} {notes}".lower()
        return any(keyword in text for keyword in ("paid back", "settlement", "deposit share", "paid aisha"))

