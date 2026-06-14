from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.schemas.balance import GroupBalanceResponse, MemberBalance, SettlementSuggestionRead
from app.services.balance_service import BalanceService

router = APIRouter(prefix="/groups/{group_id}/balances", tags=["balances"])


@router.get("", response_model=GroupBalanceResponse)
def get_group_balances(group_id: UUID, db: Session = Depends(db_session)) -> GroupBalanceResponse:
    service = BalanceService(db)
    balances = service.group_balances(group_id)
    suggestions = service.simplified_settlements(balances)
    return GroupBalanceResponse(
        group_id=group_id,
        balances=[MemberBalance(user_id=user_id, net_balance=amount) for user_id, amount in balances.items()],
        suggested_settlements=[
            SettlementSuggestionRead(
                from_user_id=suggestion.from_user_id,
                to_user_id=suggestion.to_user_id,
                amount=suggestion.amount,
            )
            for suggestion in suggestions
        ],
    )

