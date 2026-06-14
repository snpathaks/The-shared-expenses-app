# CSV Import Report

Source file: `C:\Users\hp\Downloads\expenses_export.csv`

Rows read: 42

Columns read:

- `date`
- `description`
- `paid_by`
- `amount`
- `currency`
- `split_type`
- `split_with`
- `split_details`
- `notes`

## Assumptions Used For Data Quality Review

- Known users: Aisha, Rohan, Priya, Meera, Dev, Sam.
- Base reporting currency: INR.
- Aisha, Rohan, Priya, and Meera are regular household members from February 2026.
- Meera appears to leave after Sunday, 2026-03-29 based on row 32.
- Sam joins mid-April; for validation, Sam is treated as active from 2026-04-15.
- Dev is a known user, but Dev's guest/trip membership intervals should be explicitly approved.
- Date format policy should prefer ISO `YYYY-MM-DD`.
- Finance import must not silently trim, normalize, convert, or delete data.

## Row Read Register

| Row | Status | Notes |
|---:|---|---|
| 1 | Clean candidate | Equal INR rent split. |
| 2 | Clean candidate | Equal INR grocery split. |
| 3 | Clean candidate | Equal INR wifi split. |
| 4 | Warning | Possible duplicate with row 5; Dev guest membership should be confirmed. |
| 5 | Warning | Possible duplicate of row 4. |
| 6 | Warning | Amount contains thousands separator: `1,200`. |
| 7 | Clean candidate | Equal INR maid salary split. |
| 8 | Warning | Payer casing mismatch: `priya`. |
| 9 | Critical | INR amount has 3 decimal places: `899.995`. |
| 10 | Warning | Payer alias: `Priya S`. |
| 11 | Warning | Split type `unequal` should map to exact split only with approval. |
| 12 | Critical | Missing payer. |
| 13 | Critical | Settlement/payment recorded in expense file. |
| 14 | Critical | Percentages total 110%, not 100%. |
| 15 | Warning | Ambiguous non-ISO date: `01/03/2026`. |
| 16 | Warning | Ambiguous non-ISO date: `03/03/2026`. |
| 17 | Warning | Ambiguous non-ISO date: `05/03/2026`. |
| 18 | Warning | Ambiguous non-ISO date: `08/03/2026`; Dev trip membership should be confirmed. |
| 19 | Critical | USD expense requires approved exchange rate; ambiguous date. |
| 20 | Critical | USD expense requires approved exchange rate; ambiguous date. |
| 21 | Warning | Split type `share` should map to `shares` only with approval; ambiguous date. |
| 22 | Critical | Unknown participant `Dev's friend Kabir`; USD exchange rate required. |
| 23 | Warning | Possible duplicate/conflict with row 24; ambiguous date. |
| 24 | Warning | Possible duplicate/conflict with row 23; note says another log may be wrong. |
| 25 | Critical | Negative USD amount/refund; should not import as normal expense. |
| 26 | Critical | Date `Mar 14` has no year; payer has case/whitespace mismatch. |
| 27 | Critical | Missing currency. |
| 28 | Info | Amount has trailing whitespace: `1450 `. |
| 29 | Clean candidate | Equal INR maid salary split. |
| 30 | Warning | Zero amount expense, likely correction placeholder. |
| 31 | Critical | Percentages total 110%, not 100%. |
| 32 | Info | Meera farewell note implies membership change. |
| 33 | Critical | Explicitly ambiguous date: `04/05/2026`. |
| 34 | Clean candidate | Valid shares split if Meera has left. |
| 35 | Critical | Meera included after likely leaving. |
| 36 | Clean candidate | Equal INR wifi split after Meera left. |
| 37 | Critical | Deposit/payment likely settlement; Sam before assumed join date. |
| 38 | Critical | Sam included before assumed join date. |
| 39 | Critical | Sam included before assumed join date. |
| 40 | Clean candidate | Sam active on join date under inclusive join policy. |
| 41 | Warning | Equal split type conflicts with share details, although all shares are equal. |
| 42 | Clean candidate | Equal INR maid salary split after Sam joined. |

## Detailed Anomalies

| ID | Row | Issue type | Severity | Description | Detection logic | Recommended action | Approval required |
|---|---:|---|---|---|---|---|---|
| ANOM-001 | 5 | Duplicate candidate | Warning | Row 5 appears to duplicate row 4 with normalized description and same date, payer, amount, currency, participants, and split type. | Normalize description by lowercasing/removing punctuation; compare business fingerprint. | Show row 4 and row 5 side by side; approve one, reject one, or keep both with reason. | Yes |
| ANOM-002 | 6 | Non-canonical amount format | Warning | Amount contains comma thousands separator. | Numeric field contains comma. | Parse only after user approves normalization from `1,200` to `1200`. | Yes |
| ANOM-003 | 8 | Inconsistent name | Warning | Payer `priya` differs from canonical `Priya` by case. | Case-insensitive match exists but exact match fails. | Map to Priya after approval; optionally create approved alias. | Yes |
| ANOM-004 | 9 | Currency precision violation | Critical | INR amount `899.995` has more than two decimal places. | Currency INR supports 2 decimal places; value has 3. | Require correction or rejection. | Yes |
| ANOM-005 | 10 | Inconsistent name | Warning | Payer `Priya S` is not an exact user name. | Exact user match fails; fuzzy match suggests Priya. | User must approve alias mapping to Priya or reject row. | Yes |
| ANOM-006 | 11 | Split type alias | Warning | Split type `unequal` is not canonical but split details are exact amounts summing to total. | `split_type` not in canonical enum; exact split details parse and sum to 1500. | Map to `exact` after approval. | Yes |
| ANOM-007 | 12 | Missing payer | Critical | `paid_by` is blank. | Required field empty. | Require payer selection or reject row. | Yes |
| ANOM-008 | 13 | Settlement recorded as expense | Critical | Description and notes indicate Rohan paid Aisha back. | Keywords: `paid back`, `settlement`; split type blank; one payee in `split_with`. | Convert to settlement after approval: Rohan pays Aisha INR 5000. | Yes |
| ANOM-009 | 14 | Split mismatch | Critical | Percentages total 110%, not 100%. | Sum percentages in split_details: 30+30+30+20=110. | Require corrected percentages or reject row. | Yes |
| ANOM-010 | 15 | Ambiguous date format | Warning | `01/03/2026` can mean 1 Mar or 3 Jan depending locale. | Date format is not ISO and day/month are both <= 12. | Require file-level date format approval. | Yes |
| ANOM-011 | 16 | Ambiguous date format | Warning | `03/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Require file-level date format approval. | Yes |
| ANOM-012 | 17 | Ambiguous date format | Warning | `05/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Require file-level date format approval. | Yes |
| ANOM-013 | 18 | Ambiguous date format | Warning | `08/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Require date format approval. | Yes |
| ANOM-014 | 19 | Currency conversion required | Critical | USD expense cannot be imported into INR group without an approved exchange rate. | `currency != group.base_currency` and no exchange-rate evidence in row. | Provide/approve USD-INR rate for transaction date. | Yes |
| ANOM-015 | 19 | Ambiguous date format | Warning | `09/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Approve interpreted date before selecting exchange rate. | Yes |
| ANOM-016 | 20 | Currency conversion required | Critical | USD expense requires exchange rate. | Currency differs from base currency. | Approve USD-INR rate for transaction date. | Yes |
| ANOM-017 | 20 | Ambiguous date format | Warning | `10/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Approve interpreted date. | Yes |
| ANOM-018 | 21 | Split type alias | Warning | Split type `share` should map to canonical `shares`. | Non-canonical split_type with parseable numeric shares. | Map to `shares` after approval. | Yes |
| ANOM-019 | 21 | Ambiguous date format | Warning | `10/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Approve interpreted date. | Yes |
| ANOM-020 | 22 | Unknown participant | Critical | `Dev's friend Kabir` is not one of the known users. | Participant name has no exact, case-insensitive, or approved alias match. | Create user and temporary membership, map to existing user, or reject row. | Yes |
| ANOM-021 | 22 | Currency conversion required | Critical | USD expense requires exchange rate. | Currency differs from base currency. | Approve USD-INR rate. | Yes |
| ANOM-022 | 22 | Ambiguous date format | Warning | `11/03/2026` is ambiguous. | Non-ISO date with day/month <= 12. | Approve interpreted date. | Yes |
| ANOM-023 | 23 | Duplicate/conflict candidate | Warning | Row 23 may duplicate row 24 but has different payer and amount. | Same date, similar merchant text, same participants, close amount. | Review both rows; keep one or both with reason. | Yes |
| ANOM-024 | 24 | Duplicate/conflict candidate | Warning | Row note says Aisha also logged this and hers may be wrong. | Notes explicitly indicate duplicate/conflict. | Review against row 23. | Yes |
| ANOM-025 | 25 | Negative amount | Critical | Amount `-30` cannot be imported as normal expense. | Amount < 0. | Treat as refund/adjustment with explicit policy or reject. | Yes |
| ANOM-026 | 25 | Currency conversion required | Critical | Negative USD refund still requires exchange-rate policy if imported as adjustment. | Currency differs from base currency. | Approve refund handling and exchange rate. | Yes |
| ANOM-027 | 26 | Invalid partial date | Critical | `Mar 14` has no year. | Parser cannot determine full transaction date without external context. | Require user to select full date. | Yes |
| ANOM-028 | 26 | Inconsistent name | Warning | Payer `rohan ` has lowercase and trailing whitespace. | Trim/case-insensitive match exists. | Map to Rohan after approval. | Yes |
| ANOM-029 | 27 | Missing currency | Critical | Currency is blank. | Required currency field empty. | Require currency selection or reject row. | Yes |
| ANOM-030 | 28 | Non-canonical amount format | Info | Amount contains trailing whitespace. | Numeric field changes after trim. | Preserve raw value; parse normalized amount only with audit metadata. | Yes |
| ANOM-031 | 30 | Zero amount | Warning | Zero amount likely represents correction placeholder. | Amount == 0. | Reject or import as no-op adjustment only with reason. | Yes |
| ANOM-032 | 31 | Split mismatch | Critical | Percentages total 110%, not 100%. | Sum percentages: 30+30+30+20=110. | Require corrected percentages or reject. | Yes |
| ANOM-033 | 32 | Membership event hint | Info | Notes imply Meera moved out after this expense. | Natural-language note contains `moving out`. | Create or confirm Meera `left_at` membership date. | Yes |
| ANOM-034 | 33 | Ambiguous date | Critical | Notes explicitly say the date may be April 5 or May 4. | Non-ISO `04/05/2026` plus note confirms uncertainty. | User must choose exact date before import. | Yes |
| ANOM-035 | 35 | Member left before expense | Critical | Meera appears in split on 2026-04-02 after likely leaving 2026-03-29. | Membership timeline check fails. | Remove Meera from split or adjust membership with approval. | Yes |
| ANOM-036 | 37 | Settlement/deposit recorded as expense | Critical | Sam paid Aisha deposit share; this is a payment, not shared spending. | Keywords `deposit`, `paid Aisha`; split_with only Aisha. | Convert to settlement or deposit transaction after approval. | Yes |
| ANOM-037 | 37 | Member joined after expense | Critical | Sam paid before assumed join date 2026-04-15. | Sam active_on_date false for 2026-04-08. | Confirm Sam join date or reject/convert with explanation. | Yes |
| ANOM-038 | 38 | Member joined after expense | Critical | Sam included on 2026-04-10 before assumed join date. | Split participant/payer active_on_date false. | Confirm earlier join date or remove/reject row. | Yes |
| ANOM-039 | 39 | Member joined after expense | Critical | Sam included on 2026-04-12 before assumed join date. | Split participant active_on_date false. | Confirm earlier join date or remove Sam from split. | Yes |
| ANOM-040 | 41 | Split type/details conflict | Warning | `split_type` says equal, but `split_details` contains shares. | Equal split has non-empty share-style split details. | Since all shares are 1, import as equal after approval or canonicalize to shares. | Yes |

## Proposed Import Decision

Do not perform final import automatically.

Recommended batch status: `review_required`.

Rows that can be imported only after approval of warnings: 4, 5, 6, 8, 10, 11, 15, 16, 17, 18, 21, 23, 24, 28, 30, 32, 41.

Rows blocked until corrected or explicitly transformed: 9, 12, 13, 14, 19, 20, 22, 25, 26, 27, 31, 33, 35, 37, 38, 39.

Clean candidates: 1, 2, 3, 7, 29, 34, 36, 40, 42.

