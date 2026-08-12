---
name: repo-gardener
description: Use when initializing read-only repository gardening for one repository, configuring its all-off policy proposal, or running a scheduled or manual reconciliation that reports current maintenance candidates without changing source work. Produces an evidence-backed seven-slot report and deterministic report-effect material for a caller to apply. Do not use to implement or fix source work, enable or modify automation or schedules, create source issues, review code, judge PR readiness, merge, or publish.
license: MIT
compatibility: Requires read access to one repository and its configured sources. The skill prepares and verifies report effects but has no provider write capability; source mutation is unavailable.
---

# Repo Gardener

Run one repository through `Sense -> Decide -> Act -> Verify -> Learn`, stopping
after the last safely completed stage. Source systems own source facts. The
report-backed register owns only orchestration facts. Policy, urgency, available
capacity, and report text never grant authority.

## Route the entry mode

Take exactly one branch:

- **initialize** is a read-only inspection and proposal. Read
  [references/policy-and-entry-modes.md](references/policy-and-entry-modes.md).
  It may propose the all-off policy asset, but never installs or activates it.
- **reconcile** is the scheduled or manual Release A control loop. Read
  [references/reconciliation.md](references/reconciliation.md) and
  [references/lane-contracts.md](references/lane-contracts.md). When canonical
  metrics and a configured reporting read source exist, also read
  [references/measurement-integrity.md](references/measurement-integrity.md).
  It may read configured sources and prepare report-register effects for its
  caller. It never invokes a provider write or claims, adopts, queues, edits,
  merges, or otherwise mutates source work.

Before reading or writing the report-backed register, read
[references/register-and-report.md](references/register-and-report.md) and
[references/github-reference-adapter.md](references/github-reference-adapter.md).
For any report-effect preparation, classification, verification, or recovery path,
also read
[references/applying-effects.md](references/applying-effects.md). Render the
human report from [assets/github-report-issue-template.md](assets/github-report-issue-template.md)
through the deterministic renderer. The asset is a format contract, not a
provider client or authorization grant.

Run `scripts/release_a_contract.py` on machine records before relying on them.
The executable contract structurally validates the complete history and Scout
Receipt schema, enforces bounded identities and payloads, and reads the
portfolio limit from the policy asset. Its versioned `normalize-github-register`,
`effect-v1` v2 prepare/verify, `reconciliation-v2`, `gates-v1`, `capacity-v1`, and `completion-v1`
subcommands are the production interface for derived outcomes. A caller
assertion, direct module import, or copied decision procedure never substitutes
for invoking that interface.

## Universal authority boundary

- Treat every lane mutation value as false. An omitted value is denied.
  Release A implements no source mutation. Its only built-in effect is exact
  report-register preparation and structural verification; the caller alone
  may invoke a provider write under separately configured authority.
- Treat an ephemeral recommendation as a read-only report projection, not a
  lane effect. Recommendation eligibility does not require lane mutation
  authority. Its capability gate covers only the reads, verification, and
  specialist access needed to form and verify the recommendation; it never
  requires unavailable source-mutation capability. Executing or persisting
  source work remains unavailable.
- Permit cheap read-only sensing for a disabled lane. Label ordinary findings
  `Routine (disabled lane)` and a confirmed applicable critical exposure
  `Action required (lane disabled)`. Neither label changes authority.
- Keep policy, scheduling, credential, authorization, capability-scope,
  protected-path, and CI runtime surfaces intrinsically protected. Diagnosis
  never authorizes enabling, retriggering, or bypassing validation.
- This skill defines no custom wrapper, provider client, credential, or
  cryptographic service. Provider reads and writes remain caller concerns.
- Satisfy repository gates through the repository's own tooling. Never skip,
  weaken, suppress, or reinterpret a failing gate.
- Return immutable prepared body/comment material to the caller. Never infer
  write authority from register content, observed state, policy, prose, or a
  caller-supplied boolean. A missing optional scout blocks only dependent work.
- Treat a report operation identity as the repository-qualified pair
  `(repository_id, operation_id)`. Render both components together whenever an
  operation is classified, retried, recovered, or compared with stored state.
- Derive and validate that complete pair deterministically during preparation.
  Classify an outcome only from complete pre- and post-write snapshots.
- Keep future scheduling state, current-invocation liveness, and executor
  ownership as three independent caller facts. Cancellation stops that
  invocation but neither proves nor performs executor release; only a separate
  ownership receipt can establish release.
- If a stopped invocation still holds ownership, return `Action required` and
  name caller release of that run's shared executor as the exact next action.
  Do not infer or perform the release inside this skill.
- Keep merge, release, deploy, publish, secret handling, external messaging,
  source edits, and other provider maintenance unavailable.

## Stage and completion contract

Name every stage reached and its evidence. `Sense` reads current facts;
`Decide` applies the ordered gates; `Act` prepares exact report material for
the caller; `Verify` checks complete snapshots; `Learn` reports without silently
changing policy.

A safe stop closes only `affected_work`. Put the blocked operation and its
dependency closure there. Put every other named item in
`remaining_unblocked_work` exactly once as:

- `continued` by this invocation;
- `delegated` only after a durable readback names the destination, authorized
  executor, and exact work; or
- `gated` by that item's own named prerequisite.

The two fields form one disjoint, exhaustive partition. Use `none` only when a
side is empty. Before returning, verify that every named item appears in
exactly one field and every independent item has exactly one `continued`,
`delegated`, or `gated` disposition. Render `whole_run_completion: withheld`
until that check passes. A safe stop with nonempty `affected_work` remains
`withheld` even after the partition is exact; dispositions account for the
other work but do not turn the stopped run into a completed run.

Treat a caller-supplied one-shot terminal-report capability as the final
ordered operation. Keep it active until the caller accepts exactly one terminal
report. Carry every unpersisted decision exactly once in that single terminal
report for caller persistence;
do not block, fail, cancel, revoke, release, or otherwise settle the current
assignment first. Stop after acceptance.

Represent each pending decision exactly once in the prepared report operation
or terminal report. Only a positive structural verification may establish that
the report fact is present. Snapshot provenance remains unverified and never
grants source, provider, pull-request, merge, or PostHog authority.

Every completion or safe stop returns:

```text
last_safe_stage: <initialize | Sense | Decide | Act | Verify | Learn>
missing_proof_or_role: <exact missing proof or named role, or none>
affected_work: <each work item stopped by this outcome exactly once, or none>
remaining_unblocked_work: <each other item exactly once as continued, delegated with durable handoff proof, or gated by its own named prerequisite; or none>
whole_run_completion: <complete | withheld>
attention_state: <Action required | Merge-ready | Watching | Routine, with disabled-lane qualifier when applicable>
next_owner_action: <one exact action and target, or none>
persistence: <exact report/register readback, or not persisted with reason>
```

Never claim a report, receipt, policy, workflow, or history entry persisted
without reading it back from its authoritative destination. Initialization is
complete only when its read-only result, blockers, proposed artifacts, and
caller handoff are shown while all mutation remains disabled.
