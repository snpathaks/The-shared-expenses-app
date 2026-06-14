# SQL Records That Would Be Created After Import

This file describes records that should be created. It intentionally does not execute SQL or mutate data.

## Import Staging Records

The importer should first create one `imports` row:

```sql
INSERT INTO imports (
  id,
  group_id,
  file_name,
  file_hash,
  status,
  uploaded_by,
  report
) VALUES (
  :import_id,
  :group_id,
  'expenses_export.csv',
  :sha256_file_hash,
  'review_required',
  :uploaded_by,
  :report_json
);
```

Then create 42 `import_rows` records, one per CSV row:

```sql
INSERT INTO import_rows (
  id,
  import_id,
  row_number,
  raw_data,
  row_hash,
  parse_status,
  parse_errors,
  normalized_data,
  decision
) VALUES (
  :row_id,
  :import_id,
  :row_number,
  :raw_csv_json,
  :sha256_row_hash,
  :parse_status,
  :parse_errors_json,
  :normalized_data_json,
  'pending'
);
```

## Anomaly Records

Create 40 anomaly records matching `CSV_IMPORT_REPORT.md`.

Example:

```sql
INSERT INTO anomalies (
  id,
  import_id,
  import_row_id,
  entity_type,
  rule_code,
  severity,
  message,
  details,
  status,
  requires_approval
) VALUES (
  :anomaly_id,
  :import_id,
  :row_14_id,
  'import_row',
  'RULE_008_SPLIT_MISMATCH',
  'critical',
  'Percentage split totals 110%, expected 100%',
  '{"expected":100,"actual":110}'::jsonb,
  'open',
  true
);
```

## Final Expense Records After Approval

Only approved clean or resolved rows should create final `expenses`, `expense_payers`, and `expense_splits`.

Clean candidates that can create expense records immediately after batch approval:

- Row 1
- Row 2
- Row 3
- Row 7
- Row 29
- Row 34
- Row 36
- Row 40
- Row 42

Rows with warnings can create records only after explicit approval:

- Row 4 or row 5, depending duplicate decision
- Row 6 after amount normalization approval
- Row 8 after name mapping approval
- Row 10 after alias approval
- Row 11 after mapping `unequal` to exact
- Rows 15-18 after date interpretation approval
- Row 21 after mapping `share` to `shares`
- Row 23 or row 24, depending duplicate/conflict decision
- Row 28 after trimming approval
- Row 30 only if zero-amount policy allows it
- Row 41 after resolving split type/details conflict

Rows blocked from final expense creation until corrected:

- Row 9
- Row 12
- Row 13
- Row 14
- Row 19
- Row 20
- Row 22
- Row 25
- Row 26
- Row 27
- Row 31
- Row 33
- Row 35
- Row 37
- Row 38
- Row 39

## Example Final Expense Insert

Row 1 after approval:

```sql
INSERT INTO expenses (
  id,
  group_id,
  title,
  expense_date,
  original_amount,
  original_currency,
  base_amount,
  base_currency,
  exchange_rate,
  split_type,
  status,
  import_batch_id,
  source_row_id,
  created_by
) VALUES (
  :expense_row_1_id,
  :group_id,
  'February rent',
  DATE '2026-02-01',
  48000.0000,
  'INR',
  48000.0000,
  'INR',
  1.00000000,
  'equal',
  'active',
  :import_id,
  :row_1_id,
  :aisha_user_id
);
```

Payer:

```sql
INSERT INTO expense_payers (
  id,
  expense_id,
  user_id,
  amount,
  currency,
  base_amount
) VALUES (
  :payer_id,
  :expense_row_1_id,
  :aisha_user_id,
  48000.0000,
  'INR',
  48000.0000
);
```

Equal splits:

```sql
INSERT INTO expense_splits (
  id,
  expense_id,
  user_id,
  split_amount,
  currency,
  base_amount
) VALUES
  (:split_1, :expense_row_1_id, :aisha_user_id, 12000.0000, 'INR', 12000.0000),
  (:split_2, :expense_row_1_id, :rohan_user_id, 12000.0000, 'INR', 12000.0000),
  (:split_3, :expense_row_1_id, :priya_user_id, 12000.0000, 'INR', 12000.0000),
  (:split_4, :expense_row_1_id, :meera_user_id, 12000.0000, 'INR', 12000.0000);
```

## Example Settlement Insert After Approval

Row 13 should become a settlement only after approval:

```sql
INSERT INTO settlements (
  id,
  group_id,
  paid_by,
  paid_to,
  settlement_date,
  original_amount,
  original_currency,
  base_amount,
  base_currency,
  exchange_rate,
  status,
  import_batch_id,
  source_row_id,
  created_by
) VALUES (
  :settlement_row_13_id,
  :group_id,
  :rohan_user_id,
  :aisha_user_id,
  DATE '2026-02-25',
  5000.0000,
  'INR',
  5000.0000,
  'INR',
  1.00000000,
  'active',
  :import_id,
  :row_13_id,
  :approver_user_id
);
```

## Audit Records

Every final mutation creates an audit log.

```sql
INSERT INTO audit_logs (
  id,
  actor_user_id,
  action,
  entity_type,
  entity_id,
  before_state,
  after_state,
  metadata
) VALUES (
  :audit_id,
  :approver_user_id,
  'IMPORT_ROW_APPROVED',
  'import_row',
  :row_id,
  :before_json,
  :after_json,
  :metadata_json
);
```

