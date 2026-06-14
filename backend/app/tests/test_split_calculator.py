from decimal import Decimal
from uuid import uuid4

import pytest

from app.models.enums import SplitType
from app.services.errors import ValidationError
from app.services.split_calculator import SplitCalculator


def test_equal_split_allocates_full_amount_with_rounding() -> None:
    users = [uuid4(), uuid4(), uuid4()]

    result = SplitCalculator().calculate(split_type=SplitType.EQUAL, amount=Decimal("100.00"), participants=users)

    assert sum(result.values(), Decimal("0.00")) == Decimal("100.00")
    assert sorted(result.values()) == [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]


def test_exact_split_rejects_mismatch() -> None:
    users = [uuid4(), uuid4()]

    with pytest.raises(ValidationError, match="sum to expense amount"):
        SplitCalculator().calculate(
            split_type=SplitType.EXACT,
            amount=Decimal("100.00"),
            participants=users,
            exact_amounts={users[0]: Decimal("60.00"), users[1]: Decimal("30.00")},
        )


def test_percentage_split_rejects_non_100_percent() -> None:
    users = [uuid4(), uuid4()]

    with pytest.raises(ValidationError, match="Percentages must sum to 100"):
        SplitCalculator().calculate(
            split_type=SplitType.PERCENTAGE,
            amount=Decimal("100.00"),
            participants=users,
            percentages={users[0]: Decimal("70"), users[1]: Decimal("40")},
        )


def test_share_split_uses_weights() -> None:
    users = [uuid4(), uuid4(), uuid4()]

    result = SplitCalculator().calculate(
        split_type=SplitType.SHARES,
        amount=Decimal("400.00"),
        participants=users,
        shares={users[0]: Decimal("2"), users[1]: Decimal("1"), users[2]: Decimal("1")},
    )

    assert result[users[0]] == Decimal("200.00")
    assert result[users[1]] == Decimal("100.00")
    assert result[users[2]] == Decimal("100.00")

