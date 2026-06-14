from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.expenses import ExpenseRepository
from app.repositories.settlements import SettlementRepository


@dataclass(frozen=True)
class SettlementSuggestion:
    from_user_id: UUID
    to_user_id: UUID
    amount: Decimal


class BalanceService:
    def __init__(self, db: Session) -> None:
        self.expenses = ExpenseRepository(db)
        self.settlements = SettlementRepository(db)

    def group_balances(self, group_id: UUID) -> dict[UUID, Decimal]:
        balances: dict[UUID, Decimal] = {}

        for expense in self.expenses.list_active_for_group(group_id):
            for payer in expense.payers:
                balances[payer.user_id] = balances.get(payer.user_id, Decimal("0.00")) + payer.base_amount
            for split in expense.splits:
                balances[split.user_id] = balances.get(split.user_id, Decimal("0.00")) - split.base_amount

        for settlement in self.settlements.list_active_for_group(group_id):
            balances[settlement.paid_by] = balances.get(settlement.paid_by, Decimal("0.00")) + settlement.base_amount
            balances[settlement.paid_to] = balances.get(settlement.paid_to, Decimal("0.00")) - settlement.base_amount

        return balances

    def simplified_settlements(self, balances: dict[UUID, Decimal]) -> list[SettlementSuggestion]:
        debtors = [(user_id, -amount) for user_id, amount in balances.items() if amount < 0]
        creditors = [(user_id, amount) for user_id, amount in balances.items() if amount > 0]
        debtors.sort(key=lambda item: item[1], reverse=True)
        creditors.sort(key=lambda item: item[1], reverse=True)

        suggestions: list[SettlementSuggestion] = []
        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt = debtors[i]
            creditor_id, credit = creditors[j]
            amount = min(debt, credit)
            if amount > 0:
                suggestions.append(SettlementSuggestion(debtor_id, creditor_id, amount))
            debtors[i] = (debtor_id, debt - amount)
            creditors[j] = (creditor_id, credit - amount)
            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1
        return suggestions

