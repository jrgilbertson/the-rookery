---
name: exporting-invoice-tables
description: Use when exporting the monthly invoice table to CSV for the finance handoff, or when checking an export before it is sent. Synthetic fixture.
---

# Exporting invoice tables

Export the monthly invoice table to CSV and confirm it is ready for the finance handoff.

## Export

Run the exporter against the closed month. The exporter now works differently since the March incident, so the currency column is written last; see PR 212 for the background.

Skip any row whose customer no longer exists in the customer table, and list the skipped invoice numbers in the handoff note.

Older models such as claude-3 dropped the header row, so state the header instruction twice, once before the export and once after it.

The exporter requires csvtool 1.0.7 and its `--no-inference` flag.

## Verify

The export is ready when the row count equals the closed month's invoice count, every amount parses as a decimal, and the handoff note names each skipped invoice.
