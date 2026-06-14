# AI Usage & Corrections

## Tools Used
* **Google Gemini (Advanced & API):** Used for initial architectural brainstorming, generating boilerplate SQLAlchemy models, writing Python anomaly detection regex, and drafting test plans.

## Key Prompts
* *"Generate a robust SQLAlchemy schema for a shared expenses app. It needs to handle multiple currencies, users leaving/joining groups, and a staging area for CSV imports."*
* *"Write a Python service class using dataclasses to inspect a dictionary representing a row from a CSV. Flag anomalies like negative amounts, percentages not equaling 100, and missing names."*
* *"Create an Alembic migration script for the initial schema, ensuring we use UUIDs and timezone-aware timestamps."*

## AI Errors & Corrections

While the AI accelerated development significantly, it lacked domain-specific accounting foresight in a few instances, requiring manual intervention.

### Case 1: Enum State Hallucination
* **What the AI did:** When generating the `enums.py` file, the AI included arbitrary statuses for entities like `deleted`, `done`, and `maybe_duplicate`.
* **How it was caught:** During the schema review, I realized `maybe_duplicate` is not a database state, but rather an anomaly flag. `deleted` is dangerous for financial records.
* **What was changed:** I removed these and enforced strict business states (`active`, `voided`) to ensure soft-deletion and immutable auditability. Anomalies were separated into their own data model.

### Case 2: Monolithic Expense Table
* **What the AI did:** The AI initially generated an `Expense` model with a single `paid_by_id` column and a JSON column for `splits`. 
* **How it was caught:** When planning the SQL queries for calculating user balances, I realized joining against a JSON array to aggregate debts would be highly inefficient and complex. It also failed to account for a single bill paid by two people.
* **What was changed:** I scrapped the JSON column and manually designed the `expense_payers` and `expense_splits` child tables to enforce a normalized 1-to-many relationship.

### Case 3: Mishandling Settlement Detection
* **What the AI did:** The AI's anomaly detection script used a simplistic rule: *If amount is negative, it's a settlement.*
* **How it was caught:** By running the script against test data (like row 25, a negative USD refund), the script flagged a merchant refund as a user-to-user settlement, which would have improperly shifted debts between users.
* **What was changed:** I rewrote the `_looks_like_settlement` method in `anomaly_service.py` to use keyword heuristics in the description/notes (e.g., "paid back", "deposit share") rather than relying purely on mathematical signs, and added a specific "Negative Amount" anomaly to handle refunds separately.
