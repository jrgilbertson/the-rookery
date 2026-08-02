Tax was rounded per line item and then summed, so multi-line invoices
could disagree with the tax authority's invoice-level calculation by a
cent or two. This sums unrounded line tax and rounds once at the invoice
level, with a backfill migration recomputing stored totals.

## Evidence pack

**Plan vs delivered:** delivered — invoice-level tax rounding, backfill
migration for stored totals. Not delivered — none.

**Checks:** code review: verified — all findings applied (receipt:
review rounds 1–2). tests: verified — suite green (receipt: CI run
8817). simplification: not run.

**Not verified / attested:** none.

**Sweep findings:** duplicate-knowledge: pass. evidence-freshness: pass.
oversized-diff: pass.

**Owner decision:** approved.
