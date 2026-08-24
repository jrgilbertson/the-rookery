# Repository gardening report

Native pull requests are authoritative for authored work. This issue is a
morning report and append-only run-history surface.

## Latest run

- Run outcome: no run recorded
- Worker result: none

| Lane | Status | What happened | Terminal event | Strongest evidence | Room for improvement |
| --- | --- | --- | --- | --- | --- |
| — | no run recorded | — | — | — | run repository gardening |

## Depth and data trust

No run recorded.

## Owner attention and issue-ready recommendations

None recorded.

## Run history

Each run writes exactly one `run-opened` and one `run-closed` managed comment.
The tracker or caller result is the durable summary. Retain the Orchestrator
worktree for source, diff, and terminal-context inspection, not as the
destination for owner-generated reports or supporting files when target
repository instructions prohibit that storage. Put those artifacts in a
per-run temporary directory or a caller-approved external or private
destination, as those instructions require.

Exact readback of the two managed comments is required before treating the run
as recorded. That verification is not a planning-quality, safety, or
register-consistency claim, and it does not belong in this issue body.
