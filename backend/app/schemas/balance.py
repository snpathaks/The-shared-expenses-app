from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class MemberBalance(BaseModel):
    user_id: UUID
    net_balance: Decimal


class SettlementSuggestionRead(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    amount: Decimal


class GroupBalanceResponse(BaseModel):
    group_id: UUID
    balances: list[MemberBalance]
    suggested_settlements: list[SettlementSuggestionRead]

