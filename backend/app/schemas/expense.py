from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class EqualExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    expense_date: date
    amount: Decimal = Field(gt=Decimal("0"))
    currency: str = Field(default="INR", min_length=3, max_length=3)
    paid_by: UUID
    participants: list[UUID] = Field(min_length=1)


class ExpenseRead(ORMModel):
    id: UUID
    title: str
    original_amount: Decimal
    original_currency: str
    base_amount: Decimal
    base_currency: str

