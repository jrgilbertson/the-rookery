# Report-only agent mode

Use this entrypoint only when the leading invocation is `mode:agent`. It is an
assessment for an unattended Worker, not an owner decision. Route here before
the interactive workflow, then return after the structured output below.

## Exact subject

Require a repository, pull request number, current full head OID, authorized
base ref and exact base commit OID, the Worker's assigned path slice, and the
applicable protected-path policy. The repository is one certified full
host/owner/name identity, the pull request number must be positive, and the
head and base commit must be full object IDs. The protected-path policy must
carry its identity, policy revision, and complete protected-path set; without
that binding, actionability is `UNKNOWN`. Read the native pull request for that
repository and number, then require it to be OPEN, non-draft, and unmerged and
require its current head and base tuple exactly match the supplied subject. A
terminal state, unavailable read, or ambiguous identity is `UNKNOWN`; do not
infer a subject, reuse evidence, or retry a provider write.

Before every agent-mode provider read, including subject validation, gather, and
final comparison, set `GH_HOST` to the certified subject host and keep it set
for the inherited history helper. Use `[HOST/]OWNER/REPO` selectors where
commands support them; a default-host substitution cannot pass the certified
exact-subject binding. Gather and grade the same read-only
evidence as the ordinary assessment. In agent mode, every owner-dependent
intent-baseline branch becomes a fail-closed unverifiable-intent cap and never
prompts. Bind all evidence to the exact repository, pull request number, head,
authorized base tuple, Worker slice, and protected-path policy identity,
revision, and complete set. Capture one gathered snapshot of the history
fingerprint, exact identity, authorized base ref and exact base commit OID,
OPEN/non-draft/unmerged state, live merge/check state, host policy,
protected-path policy identity/revision/complete set, and linked-issue digests.
Immediately before return, read and compare those same facts and require the
PR to remain OPEN, non-draft, and unmerged and the same base tuple still
matches the supplied subject: a terminal-state change returns `UNKNOWN`. A base
mismatch, unavailable read, or unapproved base movement returns `UNKNOWN`.
On other movement, including a protected-path policy change, rebuild from the
changed policy or return `UNKNOWN`; an unavailable comparison or movement that
cannot be rebuilt must return `UNKNOWN`. A later head change discards this
result and requires a fresh assessment.

## Structured output

Return one structured result with these fields:

```json
{
  "repository": "host/owner/name",
  "pull_request_number": 0,
  "head_oid": "full object ID",
  "protected_path_policy": {
    "identity": "certified policy identity",
    "revision": "exact policy revision",
    "paths": []
  },
  "recommendation": "merge | debug | do_not_merge | unknown",
  "caps": [],
  "process_only_findings": [],
  "material_findings": [],
  "actionable_in_slice_findings": []
}
```

Every finding names its stable fingerprint, evidence, classification, and the
exact head. Every actionable in-slice finding also names its exact affected and
proposed repair paths. `process_only_findings` records conditions such as missing human
approval or incomplete review history; it never requests source work.
`material_findings` names proven diff, test, intent, or durable-record
problems. A material finding belongs in `actionable_in_slice_findings` only
when its repair is safe, does not cross a protected path, and is contained by
the supplied Worker slice. Do not manufacture an actionable classification
when the slice or protected-path policy is unavailable or a finding crosses its
boundary.

The process-only findings are recorded, never chased. The material findings
are evidence-backed problems. The actionable in-slice findings are the strict
safe subset the owning Worker may receive after fresh authorization.

This mode is report-only. It cannot present an owner choice, perform a forge
write, mutate tracker or pull-request state, alter a branch, or modify local
source. The owning Worker may repair an actionable in-slice finding only after
the Orchestrator validates a fresh exact-head result and grants that Worker a
new bounded authorization.
