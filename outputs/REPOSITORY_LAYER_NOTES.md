# Backend Increment 3 - Repositories

## Purpose

Repositories isolate SQLAlchemy query details from business services.

## Design Decisions

- `BaseRepository` provides common `get`, `require`, and `add` operations.
- Domain repositories expose only queries the services need.
- Balance-heavy queries load expense payers and splits with `selectinload` to avoid N+1 access.
- Import repositories keep staging separate from final expense creation.

## Edge Cases

- `NotFoundError` is repository-level and can be mapped to HTTP 404 in routes.
- Cross-row financial validation does not live in repositories; it belongs in services.
- Repositories do not commit transactions. Service/API orchestration controls commit/rollback.

## Files

- `backend/app/repositories/base.py`
- `backend/app/repositories/users.py`
- `backend/app/repositories/groups.py`
- `backend/app/repositories/memberships.py`
- `backend/app/repositories/expenses.py`
- `backend/app/repositories/settlements.py`
- `backend/app/repositories/imports.py`
- `backend/app/repositories/anomalies.py`
- `backend/app/repositories/audit_logs.py`

