# State: acme/ledger-app

Holder: sess-cap-3

## In-flight briefs

### #540 · worker w-1 · dispatch d-1 · sent 2026-11-19

Leaf: add a CSV download of the invoice list
Files: app/export/csv.ts, app/views/invoice-list.tsx, tests/export/csv.test.ts
Verification: a unit test shows the CSV header and one row; the invoice list shows a Download CSV button
Model: gpt-5.5-codex

### #541 · worker w-2 · dispatch d-2 · sent 2026-11-19

Leaf: return an exclusive end from pageBounds
Files: app/lib/pagination.ts, tests/lib/pagination.test.ts
Verification: a unit test shows page 2 of 15 invoices ending at 15
Model: gpt-5.5-codex

## Open decisions

None.
