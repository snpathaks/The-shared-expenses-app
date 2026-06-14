# Suggested Import Policies

## Policy 1: No Silent Mutation

Raw CSV values must be stored exactly as received in `import_rows.raw_data`.

Examples:

- Do not silently trim `rohan `.
- Do not silently convert `1,200` to `1200`.
- Do not silently map `Priya S` to `Priya`.
- Do not silently infer `Mar 14` as `2026-03-14`.

Approved normalized values may be stored separately in `import_rows.normalized_data`.

## Policy 2: Date Parsing

Accepted without approval:

- ISO date: `YYYY-MM-DD`

Requires approval:

- `DD/MM/YYYY`
- `MM/DD/YYYY`
- textual dates like `Mar 14`
- any date where notes indicate uncertainty

For this file, the likely intended interpretation is Indian `DD/MM/YYYY`, but finance import should still ask for approval because many March rows have day and month values <= 12.

## Policy 3: Duplicate Handling

Duplicate candidates must be shown to the user.

The system should never delete duplicates automatically because similar rows may represent separate real-world transactions.

Recommended duplicate fingerprint:

```text
group_id
normalized_description
transaction_date
amount
currency
paid_by
split_type
participant_set
```

## Policy 4: Settlement Classification

Rows that describe repayment, deposit transfer, refund, or payback must not be imported as normal expenses.

They should be routed to one of:

- settlement
- refund/adjustment
- rejected row

All transformations require approval.

## Policy 5: Currency Conversion

If row currency differs from group base currency:

- require transaction date first
- require exchange rate for that date
- store original currency amount
- store exchange rate source
- store converted INR amount

No USD row in this file should be finalized without an approved USD-INR exchange rate.

## Policy 6: Membership Timeline Validation

Use:

```text
joined_at <= transaction_date
AND (left_at IS NULL OR transaction_date < left_at)
```

Rows involving Sam before 2026-04-15 require correction or an approved membership date change.

Rows involving Meera after her confirmed leaving date require correction or membership review.

## Policy 7: Split Validation

For every expense:

- exact splits must sum to total amount
- percentage splits must sum to 100%
- share splits must have total shares > 0
- equal splits must not contain conflicting split details unless approved

## Policy 8: Severity Mapping

Critical:

- cannot safely import as-is
- would affect balances incorrectly
- requires correction, rejection, or explicit transformation

Warning:

- parseable but suspicious
- requires approval before final import

Info:

- does not block import, but should be audited

