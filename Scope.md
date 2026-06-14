# Project Scope

## 1. Anomaly Log & Handling Strategy
During the CSV import phase, we identified 40 distinct anomalies across the data. Because financial data requires strict integrity, we implemented a staging-and-approval workflow rather than a direct import. 

Here are the data problems identified and how they are handled:

| Anomaly Category | Count | Example Rows | Handling Strategy |
| :--- | :---: | :--- | :--- |
| **Missing Required Value** | 2 | 12, 27 | **Blocked.** Row cannot be processed. Requires manual correction of missing payer or currency before import. |
| **Currency Precision / Format** | 3 | 6, 9, 28 | **Warning/Blocked.** Row 6 & 28 require explicit approval to normalize non-canonical amounts. Row 9 (precision violation) is blocked until corrected. |
| **Inconsistent Names / Unknowns** | 4 | 8, 10, 22, 26 | **Warning/Blocked.** Rows 8, 10, 26 require approval to map aliases to canonical users. Row 22 contains a completely unknown participant + USD conversion and is blocked until the user is registered. |
| **Split Type / Mismatch** | 5 | 11, 14, 21, 31, 41 | **Blocked/Warning.** Rows 14 & 31 are blocked due to invalid math (e.g., percentages totaling 110%). Rows 11, 21, 41 require approval to map aliases like `share` to canonical types. |
| **Duplicate / Conflict Candidate** | 4 | 5, 23, 24 | **Warning.** Requires explicit user review to confirm whether they are genuine duplicates or distinct expenses. |
| **Ambiguous/Invalid Dates** | 12 | 15-22, 26, 33 | **Warning/Blocked.** Rows 15-18 require explicit approval of the date interpretation. Row 33 is blocked until the date ambiguity is manually resolved. |
| **Settlement as Expense** | 2 | 13, 37 | **Blocked.** Row 13 & 37 mix settlements into expenses. Handled by migrating these rows to the `settlements` flow after user approval to prevent double-counting spending. |
| **Membership Violations** | 5 | 32, 35, 37-39 | **Blocked.** Users are listed in expenses before joining or after leaving. Blocked until the membership timeline or expense date is corrected. |
| **Negative Amount / Refund** | 1 | 25 | **Blocked.** Negative USD refund requires an explicit refund policy mapping before it can be imported. |

## 2. Database Schema
The database is built on PostgreSQL using SQLAlchemy ORM. The core schema focuses on immutable auditability and separating logical entities.

* **`users`**: Stores authentication identity, unique email, and preferred currency.
* **`groups`**: Stores expense groups, linking to a creator and a base currency for reporting.
* **`memberships`**: Tracks `joined_at` and `left_at` timelines for users within groups to prevent invalid expense allocations.
* **`expenses`**: The core transaction record. Stores `original_amount`, `base_amount`, and `split_type`.
* **`expense_payers`**: Child table of `expenses`. Allows an expense to be paid by multiple people.
* **`expense_splits`**: Child table of `expenses`. Records the exact divided liability for each participant.
* **`settlements`**: Distinct from expenses. Records direct debt repayments (`paid_by`, `paid_to`).
* **`exchange_rates`**: Historical ledger of currency conversion rates used at the time of transaction.
* **`imports` & `import_rows`**: Staging tables that preserve raw CSV data and track approval status.
* **`anomalies`**: Stores the findings for each import row (rule code, severity, JSONB details).
* **`audit_logs`**: Append-only ledger recording all state mutations with before/after JSON snapshots.
