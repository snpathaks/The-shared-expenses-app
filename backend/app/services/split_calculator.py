from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from app.models.enums import SplitType
from app.services.errors import ValidationError

MONEY_QUANT = Decimal("0.01")


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)


def allocate_remainder(amount: Decimal, user_ids: list[UUID], raw_amounts: list[Decimal]) -> dict[UUID, Decimal]:
    rounded = [quantize_money(value) for value in raw_amounts]
    diff = quantize_money(amount) - sum(rounded, Decimal("0.00"))
    if diff == 0:
        return dict(zip(user_ids, rounded, strict=True))

    remainders = [raw - rounded_value for raw, rounded_value in zip(raw_amounts, rounded, strict=True)]
    index = max(range(len(user_ids)), key=lambda i: (remainders[i], str(user_ids[i])))
    rounded[index] = quantize_money(rounded[index] + diff)
    return dict(zip(user_ids, rounded, strict=True))


class SplitCalculator:
    def calculate(
        self,
        *,
        split_type: SplitType,
        amount: Decimal,
        participants: list[UUID],
        exact_amounts: dict[UUID, Decimal] | None = None,
        percentages: dict[UUID, Decimal] | None = None,
        shares: dict[UUID, Decimal] | None = None,
    ) -> dict[UUID, Decimal]:
        if amount < 0:
            raise ValidationError("Expense amount cannot be negative")
        if not participants:
            raise ValidationError("At least one participant is required")

        if split_type == SplitType.EQUAL:
            raw = [amount / Decimal(len(participants)) for _ in participants]
            return allocate_remainder(amount, participants, raw)

        if split_type == SplitType.EXACT:
            if exact_amounts is None:
                raise ValidationError("Exact split requires exact_amounts")
            total = sum(exact_amounts.values(), Decimal("0.00"))
            if quantize_money(total) != quantize_money(amount):
                raise ValidationError("Exact split amounts must sum to expense amount")
            return {user_id: quantize_money(exact_amounts[user_id]) for user_id in participants}

        if split_type == SplitType.PERCENTAGE:
            if percentages is None:
                raise ValidationError("Percentage split requires percentages")
            total_percentage = sum(percentages.values(), Decimal("0.00"))
            if total_percentage != Decimal("100"):
                raise ValidationError("Percentages must sum to 100")
            raw = [amount * percentages[user_id] / Decimal("100") for user_id in participants]
            return allocate_remainder(amount, participants, raw)

        if split_type == SplitType.SHARES:
            if shares is None:
                raise ValidationError("Share split requires shares")
            total_shares = sum(shares.values(), Decimal("0.00"))
            if total_shares <= 0:
                raise ValidationError("Total shares must be greater than zero")
            raw = [amount * shares[user_id] / total_shares for user_id in participants]
            return allocate_remainder(amount, participants, raw)

        raise ValidationError(f"Unsupported split type: {split_type}")

