# Backend Increment 2 - Alembic Migrations

## Purpose

This increment adds migration infrastructure and the first schema migration. It follows the model layer and does not add repositories, services, routes, or tests yet.

## Files

### `alembic.ini`

Purpose: Alembic configuration file.

Design decisions:

- Uses PostgreSQL URL format.
- Keeps the database URL local and replaceable through environment-specific configuration later.
- Enables standard Alembic logging.

Edge cases:

- Production should not hardcode credentials. The next infrastructure increment should load the URL from environment variables.

### `alembic/env.py`

Purpose: Connects Alembic to SQLAlchemy metadata.

Design decisions:

- Imports `Base.metadata` from the model layer.
- Enables `compare_type=True` so Alembic detects column type changes.
- Supports online and offline migration modes.

Edge cases:

- If a model import fails, migrations fail early instead of silently drifting from models.

### `alembic/versions/20260614_0001_initial_schema.py`

Purpose: Creates the first production schema.

Design decisions:

- Creates PostgreSQL enum types explicitly.
- Creates staging/import tables before anomaly-driven final import flow.
- Uses foreign keys for relational integrity.
- Uses check constraints for money positivity, currency code length, and membership interval validity.
- Uses indexes on balance-heavy and import-heavy access patterns.

Edge cases:

- Cross-row rules such as "sum of splits equals expense amount" are not database check constraints because they require aggregate validation. They belong in the service layer.
- Overlapping membership intervals should be handled by service validation or a later PostgreSQL exclusion constraint.
- Final import must be transactional because `expenses`, `expense_payers`, `expense_splits`, `settlements`, `import_rows`, `anomalies`, and `audit_logs` are linked.

