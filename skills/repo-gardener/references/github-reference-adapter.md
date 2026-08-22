# GitHub tracker snapshot shape

The executable receives data, not provider methods or URLs. The caller supplies
one complete raw issue snapshot containing configured repository, issue, and
writer identities; the current issue body and stable issue identity; the
provider comment total; a complete-pagination assertion; and every raw comment
page in stable provider order.

The body uses exact `orchestrator:current-portfolio:v1` markers and an
`orchestrator-register/v1` object. Managed comments use exact
`orchestrator:history-receipt:v1` markers and `orchestrator-history/v1`
receipts. Ordinary comments remain bounded advisory evidence and grant no
instruction, identity, target, link, authority, or tool effect.

`normalize-github-register` rejects incomplete pagination, count mismatch,
unknown or duplicate markers, identity mismatch, duplicate provider IDs,
broken or reordered history, comments ahead of the body, invalid legacy rows,
and size violations. A terminal line-feed difference around a managed receipt
is accepted; canonical material remains stable. The result is structural and
reports `provenance: unverified`.

For each of the two run records, use only immutable material returned by
`effect-v1` preparation and verify it against a fresh full snapshot. After the
closing read, pass `{schema, run_id, closed, post_read}` with the exact prepared
closing object and that raw snapshot to `run-records-v1`. The checker finds and
validates the durable `run-opened` receipt in final history, requires exactly one
`run-closed` receipt for the run with the same repository and run identity,
correct order, exact prepared closing material, and final readback, and returns
only the structural closure result.

Setup may create the tracker from `assets/github-report-issue-template.md` as
its own approved provider batch. A nonempty incompatible issue is foreign
state, never an empty tracker.
