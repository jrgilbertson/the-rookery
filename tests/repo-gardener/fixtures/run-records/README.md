# Run record fixtures

`check_run_records.py` exercises the public `effect-v1` and `run-records-v1`
interfaces against synthetic, live-shaped GitHub issue snapshots. It proves
that the closing checker recognizes only an exact `run-opened` / `run-closed`
pair for one run after a complete readback.

The positive case appends the pair to a two-page legacy history. Negative
cases independently exercise identity, history-head, body-lineage, sequence,
operation, canonical comment, receipt-hash, pagination, count, duplicate,
missing, and interrupted-state rejection paths.
