<!-- Replace stable identity placeholders during tracker bootstrap. -->
<!-- orchestrator:current-portfolio:v1:begin -->
```json
{"schema":"orchestrator-register/v1","repository_id":"<verified-repository-id>","report_issue_id":"<verified-report-issue-id>","writer_id":"<verified-writer-id>","register_revision":0,"last_operation_id":null,"last_operation_fingerprint":null,"history_anchor":{"sequence":0,"head":"GENESIS","latest_receipt":null},"rows":[]}
```
<!-- orchestrator:current-portfolio:v1:end -->

# Repository gardening report

Native pull requests are authoritative for authored work. This issue is a
morning report and append-only run-history surface.

## Latest run

- Run outcome: no run recorded
- Dogfood milestone: not exercised
- Child result: none

| Lane | Status | What happened | Terminal event | Strongest evidence | Room for improvement |
| --- | --- | --- | --- | --- | --- |
| — | no run recorded | — | — | — | run repository gardening |

## Depth and data trust

No run recorded.

## Owner attention and issue-ready recommendations

None recorded.

## Run history

Each run writes exactly one `run-opened` and one `run-closed` managed comment.
The tracker or caller result is the durable summary. Retain the parent worktree
for source, diff, and terminal-context inspection, not as the destination for
owner-generated reports or supporting files when target repository instructions
prohibit that storage. Put those artifacts in a per-run temporary directory or
a caller-approved external or private destination, as those instructions require.

The structural closure result exists only after final readback and is available
in the caller result or retained parent execution context, not in the immutable
close or this issue body.
