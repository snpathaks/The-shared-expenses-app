# Backend Increment 4 - Services

## Purpose

Services contain business logic: split calculation, membership validation, balances, anomaly detection, import staging, expense creation, and settlement creation.

## Design Decisions

- `SplitCalculator` is pure Python and easy to unit test.
- `MembershipService` enforces temporal membership rules.
- `BalanceService` treats positive balances as receivables and negative balances as payables.
- `AnomalyService` is rule-based so findings are explainable and auditable.
- `ImportService` stages rows and anomalies instead of writing final expenses immediately.
- Expense and settlement services validate domain rules before adding models.

## Edge Cases

- Equal split rounding assigns the remainder deterministically.
- Exact split totals must match the expense amount.
- Percentage splits must total exactly 100.
- Share splits must have total shares greater than zero.
- CSV anomalies are findings, not silent corrections.
- Import approval/finalization should be a later service because it must be transactional and user-approved.

## Files

- `backend/app/services/errors.py`
- `backend/app/services/split_calculator.py`
- `backend/app/services/membership_service.py`
- `backend/app/services/balance_service.py`
- `backend/app/services/anomaly_service.py`
- `backend/app/services/import_service.py`
- `backend/app/services/expense_service.py`
- `backend/app/services/settlement_service.py`

