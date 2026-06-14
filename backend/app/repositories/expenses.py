from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.enums import ExpenseStatus
from app.models.expense import Expense
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Expense)

    def list_active_for_group(self, group_id: UUID) -> list[Expense]:
        stmt = (
            select(Expense)
            .options(selectinload(Expense.payers), selectinload(Expense.splits))
            .where(Expense.group_id == group_id, Expense.status == ExpenseStatus.ACTIVE)
            .order_by(Expense.expense_date, Expense.created_at)
        )
        return list(self.db.scalars(stmt))

