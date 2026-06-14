from app.models.enums import AnomalySeverity
from app.services.anomaly_service import AnomalyService


def test_detects_settlement_recorded_as_expense() -> None:
    row = {
        "date": "2026-02-25",
        "description": "Rohan paid Aisha back",
        "paid_by": "Rohan",
        "amount": "5000",
        "currency": "INR",
        "split_type": "",
        "split_with": "Aisha",
        "split_details": "",
        "notes": "this is a settlement not an expense??",
    }

    findings = AnomalyService().inspect_row(13, row)

    assert any(finding.rule_code == "RULE_005_SETTLEMENT_AS_EXPENSE" for finding in findings)


def test_detects_percentage_split_mismatch() -> None:
    row = {
        "date": "2026-02-28",
        "description": "Pizza Friday",
        "paid_by": "Aisha",
        "amount": "1440",
        "currency": "INR",
        "split_type": "percentage",
        "split_with": "Aisha;Rohan;Priya;Meera",
        "split_details": "Aisha 30%; Rohan 30%; Priya 30%; Meera 20%",
        "notes": "",
    }

    findings = AnomalyService().inspect_row(14, row)

    assert any(
        finding.rule_code == "RULE_008_SPLIT_MISMATCH" and finding.severity == AnomalySeverity.CRITICAL
        for finding in findings
    )


def test_detects_unknown_participant() -> None:
    row = {
        "date": "11/03/2026",
        "description": "Parasailing",
        "paid_by": "Dev",
        "amount": "150",
        "currency": "USD",
        "split_type": "equal",
        "split_with": "Aisha;Dev's friend Kabir",
        "split_details": "",
        "notes": "",
    }

    findings = AnomalyService().inspect_row(22, row)

    assert any(finding.rule_code == "RULE_007_UNKNOWN_MEMBER_NAME" for finding in findings)

