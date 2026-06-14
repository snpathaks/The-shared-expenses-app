from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import SettlementStatus
from app.models.settlement import Settlement
from app.services.errors import ValidationError


class SettlementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def record(
        self,
        *,
        group_id: UUID,
        paid_by: UUID,
        paid_to: UUID,
        settlement_date,
        amount: Decimal,
        currency: str,
        created_by: UUID,
    ) -> Settlement:
        if paid_by == paid_to:
            raise ValidationError("Settlement payer and receiver must be different")
        if amount <= 0:
            raise ValidationError("Settlement amount must be positive")
        settlement = Settlement(
            group_id=group_id,
            paid_by=paid_by,
            paid_to=paid_to,
            settlement_date=settlement_date,
            original_amount=amount,
            original_currency=currency,
            base_amount=amount,
            base_currency=currency,
            exchange_rate=Decimal("1"),
            status=SettlementStatus.ACTIVE,
            created_by=created_by,
        )
        self.db.add(settlement)
        return settlement

