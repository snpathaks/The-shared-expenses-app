# Backend Increment 6 - Tests

## Purpose

Tests cover the highest-risk financial logic first.

## Design Decisions

- Split tests are pure unit tests and do not need a database.
- Balance simplification is tested without a database by constructing the service object directly.
- Anomaly tests use representative rows from `expenses_export.csv`.
- Import staging test verifies bad rows become review-required instead of crashing.

## Edge Cases Covered

- Equal split rounding.
- Exact split mismatch.
- Percentage split mismatch.
- Share split weighting.
- Settlement row detected in expense import.
- Unknown participant detection.
- Review-required import status.

## Files

- `backend/app/tests/test_split_calculator.py`
- `backend/app/tests/test_balance_service.py`
- `backend/app/tests/test_anomaly_service.py`
- `backend/app/tests/test_import_service.py`

