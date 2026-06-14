from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import current_user_id, db_session
from app.schemas.settlement import SettlementCreate, SettlementRead
from app.services.errors import ValidationError
from app.services.settlement_service import SettlementService

router = APIRouter(prefix="/groups/{group_id}/settlements", tags=["settlements"])


@router.post("", response_model=SettlementRead, status_code=status.HTTP_201_CREATED)
def record_settlement(
    group_id: UUID,
    payload: SettlementCreate,
    db: Session = Depends(db_session),
    actor_id: UUID = Depends(current_user_id),
) -> SettlementRead:
    try:
        settlement = SettlementService(db).record(
            group_id=group_id,
            paid_by=payload.paid_by,
            paid_to=payload.paid_to,
            settlement_date=payload.settlement_date,
            amount=payload.amount,
            currency=payload.currency,
            created_by=actor_id,
        )
        db.commit()
        db.refresh(settlement)
        return SettlementRead.model_validate(settlement)
    except ValidationError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

