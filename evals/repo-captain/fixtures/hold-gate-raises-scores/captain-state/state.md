# State: acme/ledger-app

Holder: sess-cap-4

## In-flight briefs

### #545 · worker w-1 · dispatch d-1 · sent 2026-11-19

Leaf: move invoice number formatting into app/lib/format.ts
Files: app/lib/format.ts, app/views/invoice-header.tsx, tests/lib/format.test.ts
Verification: id 42 formats as INV-000042; the header renders the same text
Model: gpt-5.5-codex

### #546 · worker w-2 · dispatch d-2 · sent 2026-11-19

Leaf: record a dunning level per invoice
Files: db/migrations/, app/models/dunning.ts, tests/models/dunning.test.ts
Verification: a new invoice is at level 0
Model: gpt-5.5-codex

### #547 · worker w-3 · dispatch d-3 · sent 2026-11-19

Leaf: let customers choose a billing contact
Files: app/views/billing-contact.tsx, tests/views/billing-contact.test.ts
Verification: a test saves a chosen billing contact
Model: gpt-5.5-codex

### #548 · worker w-4 · dispatch d-4 · sent 2026-11-19

Leaf: cache the pnpm store in CI
Files: .github/workflows/ci.yml
Verification: a second CI run restores the cache
Model: gpt-5.5-codex

## Open decisions

None.
