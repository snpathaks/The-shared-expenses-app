# Anomaly Summary

## Counts By Severity

| Severity | Count |
|---|---:|
| Critical | 20 |
| Warning | 18 |
| Info | 2 |
| Total | 40 |

## Counts By Category

| Category | Count | Rows |
|---|---:|---|
| Duplicate/conflict candidate | 4 | 5, 23, 24 |
| Non-canonical amount format | 2 | 6, 28 |
| Inconsistent name | 3 | 8, 10, 26 |
| Currency precision violation | 1 | 9 |
| Split type alias/conflict | 3 | 11, 21, 41 |
| Missing required value | 2 | 12, 27 |
| Settlement/payment recorded as expense | 2 | 13, 37 |
| Split mismatch | 2 | 14, 31 |
| Ambiguous or invalid date | 12 | 15, 16, 17, 18, 19, 20, 21, 22, 26, 33 |
| Currency conversion required | 5 | 19, 20, 22, 25 |
| Unknown participant | 1 | 22 |
| Negative amount/refund | 1 | 25 |
| Zero amount | 1 | 30 |
| Membership event hint | 1 | 32 |
| Member left before expense | 1 | 35 |
| Member joined after expense | 3 | 37, 38, 39 |

Some rows have multiple anomalies, so category counts do not equal row counts.

## Highest Risk Rows

| Row | Reason |
|---:|---|
| 13 | Settlement mixed into expenses. Importing as expense would distort spending and balances. |
| 14 | Percentages total 110%, making the split mathematically invalid. |
| 22 | Unknown participant plus USD conversion. Cannot safely assign liability. |
| 25 | Negative USD refund. Needs explicit refund policy. |
| 33 | Date ambiguity is acknowledged in the notes. |
| 35 | Meera included after likely leaving the group. |
| 37 | Deposit/payment and Sam membership violation. |
| 38 | Sam membership violation before assumed join date. |
| 39 | Sam membership violation before assumed join date. |

## Finance Application Risk Assessment

The CSV is not safe for direct import. It contains enough ambiguity to materially change user balances:

- Wrong date interpretation can place expenses before or after membership changes.
- Wrong settlement classification can double-count payments as spending.
- Wrong currency conversion can misstate INR balances.
- Wrong duplicate handling can overcharge users.
- Wrong split percentages can create non-zero-sum balances.

Final import should require user review and produce an immutable audit trail.

