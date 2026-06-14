from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import current_user_id, db_session
from app.schemas.expense import EqualExpenseCreate, ExpenseRead
from app.services.errors import ValidationError
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_equal_expense(
    group_id: UUID,
    payload: EqualExpenseCreate,
    db: Session = Depends(db_session),
    actor_id: UUID = Depends(current_user_id),
) -> ExpenseRead:
    try:
        expense = ExpenseService(db).create_equal_expense(
            group_id=group_id,
            created_by=actor_id,
            title=payload.title,
            expense_date=payload.expense_date,
            amount=payload.amount,
            currency=payload.currency,
            paid_by=payload.paid_by,
            participants=payload.participants,
        )
        db.commit()
        db.refresh(expense)
        return ExpenseRead.model_validate(expense)
    except ValidationError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

