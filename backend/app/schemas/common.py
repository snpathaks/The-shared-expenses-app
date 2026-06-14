from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MoneyAmount(BaseModel):
    amount: Decimal = Field(gt=Decimal("0"))
    currency: str = Field(min_length=3, max_length=3)


class MessageResponse(BaseModel):
    message: str


class IDResponse(ORMModel):
    id: UUID

