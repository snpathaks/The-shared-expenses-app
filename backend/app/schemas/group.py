from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class GroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    base_currency: str = Field(default="INR", min_length=3, max_length=3)


class GroupRead(ORMModel):
    id: UUID
    name: str
    description: str | None
    base_currency: str


class MembershipCreate(BaseModel):
    user_id: UUID
    role: str = Field(pattern="^(owner|admin|member)$")
    joined_at: date

