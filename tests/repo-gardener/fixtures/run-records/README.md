# Run record fixtures

`check_run_records.py` exercises the public `effect-v1` and `run-records-v1`
interfaces against synthetic, live-shaped GitHub issue snapshots. It proves
that the closing checker recognizes only an exact `run-opened` / `run-closed`
pair for one run after a complete readback. The checker takes the durable run
ID, prepared closing effect, and final snapshot; recovery does not require the
ephemeral prepared opening effect or its pre-body fingerprint.

The positive case appends the pair to a two-page legacy history. Negative
cases independently exercise identity, history-head, receipt lineage,
sequence, operation, canonical comment, receipt-hash, pagination, count,
duplicate, missing, and interrupted-state rejection paths. Recovery-positive
cases bind the opening receipt directly from durable history and allow the
current open-state body to differ before the exact closing effect is prepared.
