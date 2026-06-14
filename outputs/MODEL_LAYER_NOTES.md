# Backend Increment 1 - Database Models

## Purpose

This increment creates the SQLAlchemy model layer only. It does not create migrations, repositories, services, API routes, or tests yet because the implementation must be incremental.

## Files

### `backend/app/models/base.py`

Purpose: Defines the SQLAlchemy declarative base plus shared UUID primary key and timestamp mixins.

Design decisions:

- UUID primary keys avoid predictable integer IDs.
- Timezone-aware timestamps support auditability.
- Mixins avoid repeating common columns.

Edge cases:

- `updated_at` is handled by the database/ORM layer, but explicit audit logs still record meaningful before/after changes.

### `backend/app/models/enums.py`

Purpose: Centralizes allowed business states.

Design decisions:

- `StrEnum` keeps values readable in API responses and database rows.
- Enums prevent invalid statuses like `deleted`, `done`, or `maybe_duplicate`.

Edge cases:

- Anomaly severity uses `Critical`, `Warning`, and `Info` as requested. Validation errors that block import are represented as `Critical` when unsafe for finance import.

### `backend/app/models/user.py`

Purpose: Stores app users and authentication identity.

Design decisions:

- Email is unique and indexed for login.
- Password hash is stored, never raw password.
- Preferred currency is stored separately from group base currency.

Edge cases:

- Currency length is constrained to 3 characters, but ISO validation should also happen at service/schema layer.

### `backend/app/models/group.py`

Purpose: Stores expense groups.

Design decisions:

- Group has a base currency for reporting.
- Group creator is tracked for ownership and auditability.

Edge cases:

- Users may leave groups later, but the group creator relationship remains historical.

### `backend/app/models/membership.py`

Purpose: Stores group membership timelines.

Design decisions:

- `joined_at` and `left_at` support Sam's mid-April requirement.
- `left_at > joined_at` prevents impossible intervals.
- The unique constraint allows rejoining later with a different `joined_at`.

Edge cases:

- Overlapping memberships for the same user/group should be prevented in the service layer or with an exclusion constraint in a later migration.

### `backend/app/models/expense.py`

Purpose: Stores expenses, expense payers, and expense splits.

Design decisions:

- Payers and splits are separate child tables because one expense can have multiple payers and multiple participants.
- Original and base amounts are both stored for currency auditability.
- Expenses are voided instead of hard-deleted.

Edge cases:

- Sum of payer amounts and split amounts must equal expense amount; this is cross-row validation and belongs in the service layer.

### `backend/app/models/settlement.py`

Purpose: Stores direct payments between users.

Design decisions:

- Settlements are separate from expenses because they reduce debt rather than create shared spending.
- `paid_by <> paid_to` blocks meaningless self-payments.

Edge cases:

- Membership validity for settlement participants should be checked in services because some products may allow former members to settle old balances.

### `backend/app/models/exchange_rate.py`

Purpose: Stores exchange rates used for transaction conversion.

Design decisions:

- Rates are keyed by currency pair, date, and source.
- Historical transactions can be explained with the rate used at import/creation time.

Edge cases:

- Same-currency conversion is handled without a row by using rate `1` in the currency service.

### `backend/app/models/import_batch.py`

Purpose: Stores CSV import batches and raw rows.

Design decisions:

- `raw_data` preserves exactly what was uploaded.
- `normalized_data` can store parsed values without overwriting raw input.
- Row decisions support partial approval.

Edge cases:

- Bad rows are stored with parse errors instead of crashing the importer.

### `backend/app/models/anomaly.py`

Purpose: Stores anomaly findings from imports or validations.

Design decisions:

- Every anomaly has a rule code, severity, message, status, and approval requirement.
- `details` JSONB keeps rule-specific evidence without creating dozens of narrow columns.

Edge cases:

- Some anomalies may relate to an import row before a final entity exists, so `entity_id` is nullable.

### `backend/app/models/audit_log.py`

Purpose: Stores append-only audit events.

Design decisions:

- Before/after JSON makes finance changes reviewable.
- Metadata can include import IDs, request IDs, and rule codes.

Edge cases:

- Logs should not contain passwords, JWTs, or other secrets.

## CSV Analysis Status

No `expenses_export.csv` file is currently visible in the accessible workspace, so row-by-row data quality analysis cannot be completed yet. Once the CSV is available, the importer report should include:

- import report
- anomaly summary
- suggested policies
- SQL records proposed for creation after approval

