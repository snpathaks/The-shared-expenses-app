from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import ExpenseStatus, SplitType
from app.models.expense import Expense, ExpensePayer, ExpenseSplit
from app.services.membership_service import MembershipService
from app.services.split_calculator import SplitCalculator


class ExpenseService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.memberships = MembershipService(db)
        self.splits = SplitCalculator()

    def create_equal_expense(
        self,
        *,
        group_id: UUID,
        created_by: UUID,
        title: str,
        expense_date,
        amount: Decimal,
        currency: str,
        paid_by: UUID,
        participants: list[UUID],
    ) -> Expense:
        self.memberships.assert_all_active(group_id, [paid_by, *participants], expense_date)
        split_amounts = self.splits.calculate(split_type=SplitType.EQUAL, amount=amount, participants=participants)
        expense = Expense(
            group_id=group_id,
            title=title,
            expense_date=expense_date,
            original_amount=amount,
            original_currency=currency,
            base_amount=amount,
            base_currency=currency,
            exchange_rate=Decimal("1"),
            split_type=SplitType.EQUAL,
            status=ExpenseStatus.ACTIVE,
            created_by=created_by,
        )
        expense.payers.append(ExpensePayer(user_id=paid_by, amount=amount, currency=currency, base_amount=amount))
        for user_id, split_amount in split_amounts.items():
            expense.splits.append(
                ExpenseSplit(user_id=user_id, split_amount=split_amount, currency=currency, base_amount=split_amount)
            )
        self.db.add(expense)
        return expense

