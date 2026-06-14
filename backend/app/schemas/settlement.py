from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class SettlementCreate(BaseModel):
    paid_by: UUID
    paid_to: UUID
    settlement_date: date
    amount: Decimal = Field(gt=Decimal("0"))
    currency: str = Field(default="INR", min_length=3, max_length=3)


class SettlementRead(ORMModel):
    id: UUID
    paid_by: UUID
    paid_to: UUID
    base_amount: Decimal
    base_currency: str

