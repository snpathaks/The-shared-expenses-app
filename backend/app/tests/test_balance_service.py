from decimal import Decimal
from uuid import uuid4

from app.services.balance_service import BalanceService


def test_simplified_settlements_match_debtors_to_creditors() -> None:
    service = BalanceService.__new__(BalanceService)
    aisha = uuid4()
    rohan = uuid4()
    priya = uuid4()

    suggestions = service.simplified_settlements(
        {
            aisha: Decimal("150.00"),
            rohan: Decimal("-100.00"),
            priya: Decimal("-50.00"),
        }
    )

    assert len(suggestions) == 2
    assert suggestions[0].from_user_id == rohan
    assert suggestions[0].to_user_id == aisha
    assert suggestions[0].amount == Decimal("100.00")
    assert suggestions[1].from_user_id == priya
    assert suggestions[1].amount == Decimal("50.00")

