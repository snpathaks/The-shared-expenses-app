# Backend Increment 5 - API Routes

## Purpose

The API layer exposes FastAPI endpoints and delegates business rules to services.

## Design Decisions

- Routes are thin and do not contain finance logic.
- Pydantic schemas validate request shape and response shape.
- `X-User-Id` is a temporary development dependency standing in for JWT auth.
- Service validation errors map to HTTP 422.
- Routes commit after successful service calls and roll back on validation errors.

## Edge Cases

- Production auth should replace `X-User-Id` with JWT decoding.
- Import upload decodes `utf-8-sig` to handle BOM-prefixed CSV files.
- Final import approval is not exposed yet because it needs explicit review decisions and audit logging.

## Files

- `backend/app/main.py`
- `backend/app/api/deps.py`
- `backend/app/api/v1/router.py`
- `backend/app/api/v1/expenses.py`
- `backend/app/api/v1/settlements.py`
- `backend/app/api/v1/balances.py`
- `backend/app/api/v1/imports.py`
- `backend/app/schemas/*.py`

