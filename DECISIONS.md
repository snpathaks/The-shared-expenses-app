# Decision Log

## 1. Using UUIDs for Primary Keys
* **Options Considered:** Auto-incrementing Integers vs. UUIDv4.
* **Decision:** UUIDv4.
* **Rationale:** Predictable integer IDs in a financial/group application expose the system to Insecure Direct Object Reference (IDOR) enumeration attacks. UUIDs make endpoints secure by default and facilitate easier merging of distributed data if offline support is added later.

## 2. Separating Expenses from Settlements
* **Options Considered:** 1. Treat everything as an `Expense` and use negative amounts for settlements.
    2. Create a completely separate `Settlements` table.
* **Decision:** Separate `Settlements` table.
* **Rationale:** Treating settlements as negative expenses inherently distorts the group's "Total Spending" metrics. A payment between two users does not mean the group spent less money overall. Separating them allows clean calculation of both total aggregate spending and individual debt balances.

## 3. The Import Staging Pattern
* **Options Considered:** 1. Parse CSV and insert directly into live `expenses` tables, skipping bad rows.
    2. Parse CSV, insert into staging tables (`imports`, `import_rows`), and require approval.
* **Decision:** Staging and Approval (Option 2).
* **Rationale:** Financial data cannot be "guessed." Our anomaly detector found 40 issues, including mathematically impossible splits (110%) and dates outside of user membership windows. Forcing a direct import would permanently corrupt user balances. Staging allows partial approvals and leaves a paper trail.

## 4. Handling Expense Payers and Splits via Child Tables
* **Options Considered:** 1. Store `paid_by` and `split_with` as JSON columns on the `expenses` table.
    2. Create normalized `expense_payers` and `expense_splits` tables.
* **Decision:** Normalized child tables.
* **Rationale:** While JSON is easier to write, it is terrible for querying. Calculating a user's total balance requires indexing and joining their payments and liabilities. Normalized tables allow the database to easily run aggregate `SUM()` queries for balance resolution.

## 5. Explicit Membership Timelines
* **Options Considered:** Simple `is_active` boolean vs. `joined_at` and `left_at` timestamps.
* **Decision:** Timestamps (`joined_at`, `left_at`).
* **Rationale:** If a user leaves a group, their historical expenses must remain intact. If we only use a boolean, we lose the context of *when* they were allowed to participate in splits. Timestamps allow the service layer to block expenses dated outside a user's active window.
