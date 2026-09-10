---
title: Separate scout measurement stages from authoring capacity
date: 2026-08-12
last_updated: 2026-09-10
category: architecture-patterns
module: skills/repo-gardener/reconciliation
problem_type: architecture_pattern
component: development_workflow
severity: high
applies_when:
  - "An autonomous workflow scouts many source records before qualifying recommendations"
  - "Deterministic evaluators are being asked to certify qualitative model decisions"
  - "Read-only analysis and authored work have different capacity limits"
  - "Repository policy may change while an autonomous run is active"
  - "A durable run history is useful but per-step receipts add ceremony without assurance"
related_components:
  - assistant
  - testing_framework
tags:
  - autonomous-agents
  - repository-gardening
  - model-judgment
  - structural-verification
  - two-record-closure
  - live-policy
  - data-trust
  - execution-parallelism
---

# Separate scout measurement stages from authoring capacity

## Context

The first Repo Gardener dogfood made too much of the workflow deterministic.
Durable records accumulated around manifests, lanes, decisions, and effects,
while executable checks were asked to stand in for judgments such as whether
the run chose useful work or produced a good plan. That added ceremony without
the claimed assurance. A script can prove identities, ordering, bytes, and
readback. It cannot prove that a candidate matters or a plan is good.

The same category error appears in measurement and capacity accounting. Source
records inspected, evidence-qualified candidates, and deduplicated
repairs are different populations. Read-only sensing and depth
are not authored work, so unrelated already-open PRs do not consume the
Executor cap ([Decide whether to author](../../../skills/repo-gardener/references/reconciliation.md#decide-whether-to-author)).

Assign each kind of truth to the system that can own it: the model owns
qualitative judgment, the live repository file owns mutation permission, the
provider owns authored-work status, and deterministic code owns only
mechanically falsifiable tracker consistency
([Repo Gardener](../../../skills/repo-gardener/SKILL.md#repo-gardener)).

## Guidance

### Keep qualitative judgment with the model

Complete the quick available-input pass across five areas before dispatch.
Use filtered discovery and share evidence, assigning each repair one owner
under [area-contracts.md](../../../skills/repo-gardener/references/area-contracts.md).
Let the model compare qualified candidates without manufacturing work to
consume capacity
([Lead the run](../../../skills/repo-gardener/SKILL.md#lead-the-run) and
[Declared audits and sensing](../../../skills/repo-gardener/references/reconciliation.md#declared-audits-and-sensing)).

Depth is also a judgment, with no count. After breadth, deepen while further
investigation would change assignments or recommendations. Stop when it would
not, or when the run must close
([Declared audits and sensing](../../../skills/repo-gardener/references/reconciliation.md#declared-audits-and-sensing)).

Keep data trust cross-cutting. It contributes evidence to the five areas.
Product-behavior evidence supports a conclusion only after the relevant metric slice has an explicit grain and
authority and reconciles against durable truth. Blank reporting data is not
zero activity
([Cross-cutting measurement integrity](../../../skills/repo-gardener/references/measurement-integrity.md)).

### Give deterministic checks a narrow claim ceiling

Persist exactly two managed records for each run ID: one `run-opened` before
sensing and one consolidated `run-closed` after supervision or an honest
no-Executor close. Do not add managed manifest, area, decision, checker, or
per-Executor comments
([Tracker records](../../../skills/repo-gardener/references/tracker-records.md)).

After closing, deterministic code may verify only structural facts: the two
records are unique and ordered, their identities agree, and the complete
final snapshot reads the close back exactly
(`verify_run_records` in
[release_a_contract.py](../../../skills/repo-gardener/scripts/release_a_contract.py)). The public
fixture rejects candidates, plans, scores, PR readiness, policy, authority,
and register-quality claims as checker outputs
(the rejected-input assertions in
[check_run_records.py](../../../tests/repo-gardener/fixtures/run-records/check_run_records.py)).
`register_closed_consistently` is not a production result. Never present a
two-comment check as a quality, safety, permission, or readiness verdict
(the exact-result assertion in
[check_run_records.py](../../../tests/repo-gardener/fixtures/run-records/check_run_records.py) and
[Check the closed run](../../../skills/repo-gardener/references/tracker-records.md#check-the-closed-run)).

### Reread live policy at mutation boundaries

Executor authoring requires, on the opening file, exact
`repository.identity` match, every planned path inside the effective
include/exclude scope, `maximum_workers` greater than zero, owning area
`mutation: true`, and no protected path. The live gardener file that first-use
writes on the target repository is always protected. Missing or false
permission, scope mismatch, or a disallowed current overlap denies that unit
([Authoring and hardcoded denies](../../../skills/repo-gardener/references/policy-and-entry-modes.md#authoring-and-hardcoded-denies)).

At open, read the durable file from the refreshed default branch and record
that revision. Mid-run, re-read it only to detect that it changed,
immediately before each declared audit, Executor dispatch, push, PR creation,
and `run-closed`. A revision change stops further source mutation, push, and
PR-open for every Executor. In contrast, an unchanged-policy authoring or
overlap denial remains local to that Executor's dependents. If the file still
names the tracker, the Lead still writes the closed comment
([Revision check points](../../../skills/repo-gardener/references/policy-and-entry-modes.md#revision-check-points) and
[Decide whether to author](../../../skills/repo-gardener/references/reconciliation.md#decide-whether-to-author)).

Never fall back to the bundled starter. It is fail-closed:
`maximum_workers: 0` and all area mutations disabled
(the `maximum_workers` and `areas` fields in
[policy-template.yaml](../../../skills/repo-gardener/assets/policy-template.yaml)).

### Let native artifacts own authored work

Create a persistent Executor worktree only for work intended to become one PR.
The Executor owns planning, implementation, simplification, review, repository
verification, its coherent commit, and its branch through at most one unmerged
PR. Every unattended Executor invokes `checking-pr-readiness` on its exact
head, then stops after its menu reply. On a distinct later turn, the Lead
authorizes the Executor to reply 1 only when Approve was offered and
recommended for that exact head. The checking skill then performs its
identity reread before the evidence enters the publication path. Named
Executor-owned gaps from that brief all go back to the same Executor;
owner-needed briefs stop without a PR. An existing same-repository update
PR with an Executor-owned gap stays a recommendation; this slice does not
dispatch it. Assignment names the files each Executor will touch,
including any shared convention file, so two Executors are not assigned
the same one. The Lead does not run a publication-time overlap inventory
([worker-contract.md](../../../skills/repo-gardener/references/worker-contract.md)).

The Lead owns breadth, depth, selection, tracker writes, supervision,
and the morning report. After PR creation, it reports native PR, check, and
review facts; required pending work makes closure partial. After looks
merge-ready, the Lead dispatches `checking-merge-readiness` to a
fresh uninvolved helper and never selects Proceed to merge
(`skills/repo-gardener/references/reconciliation.md`,
`skills/repo-gardener/references/tracker-records.md`).

Freshly read the native repository, PR number, branch, head SHA, state,
checks, and review status before reporting the Executor. Do not mirror that
lifecycle into a custom ownership ledger. Follow-up issues stay outside the
gardening run as owner proposals for Managing Issues. The run never merges,
and the retained
Lead report carries issue-ready recommendations for owner review
([Lead the run](../../../skills/repo-gardener/SKILL.md#lead-the-run) and
[Authoring and hardcoded denies](../../../skills/repo-gardener/references/policy-and-entry-modes.md#authoring-and-hardcoded-denies)).

## Why This Matters

The boundary removes data that no component can truthfully certify. The
deterministic checker remains valuable where a wrong answer is mechanically
falsifiable. It stops being misleading when structural success no longer
becomes a claim about work selection or plan quality.

Trusting the model with qualitative execution does not grant unbounded
authority. The model explains its evidence and decisions. Hard limits, fresh
policy reads, protected effects, native provider state, and human-only merge
remain outside its discretion.

Separating measurement stages makes a quiet night interpretable. Owners can
see whether little was inspected, much was inspected but little qualified, or
several areas converged on one problem. Separating read-only capacity from
authoring capacity lets the gardener keep finding and explaining useful work
when unrelated PRs already exist.

Finally, giving each justified unit its own Executor makes responsibility
legible. One Executor owns one PR-sized unit through at most one unmerged PR;
the Lead coordinates and reports. Scouts gather evidence. Reviewers judge
readiness. They do not own a PR. The durable morning summary stays in
the tracker or a caller-approved destination, not in public repository source.

## When to Apply

- A scheduled or manual agent surveys several sources and must prioritize work
  rather than execute a predetermined ticket.
- Native systems already own durable work state, such as PRs, branches, heads,
  checks, and reviews.
- Policy may change while a long-running agent is sensing or implementing.
- Read-only breadth, purpose-bounded depth, recommendations, and authored work
  have different limits or risk profiles.
- Analytics can inform work only after schema, identity, grain, freshness, and
  source-of-truth checks make the evidence trustworthy.
- An audit trail is useful, but only some workflow facts have exact structural
  invariants that deterministic code can honestly verify.

Do not apply the pattern by removing evidence or verification. Match each
claim to the narrowest owner capable of proving it, then delete duplicate
representations elsewhere.

## Examples

### Replace per-step receipts with one run pair

```text
run-opened
  -> model completes the quick five-area pass using filtered inputs
  -> Lead assigns non-overlapping Executors in parallel up to maximum_workers
  -> model deepens decision-relevant investigations while Executors progress
  -> each Executor owns one PR-sized unit through at most one unmerged PR
run-closed
  -> deterministic two-comment identity check
  -> no register-quality claim
```

The close still contains five area coverage summaries, depth results, bounded
data-trust evidence, native Executor facts or a no-Executor reason, owner
attention, recommendations, and run outcome. Less durable ceremony does not
mean less operating coverage.

### Stop only the mutation whose permission changed

If a run opens against revision A of the durable file and the default branch
later holds a different revision:

- an opening-policy denial, such as a disabled owning area or
  `maximum_workers: 0`, prevents that Executor but not unrelated reporting;
- a later revision change before PR creation preserves saved Executor work
  without opening the PR across the affected run; and
- a denied tracker write before close prevents a false structural-closure
  claim and becomes an interrupted caller handoff.

The active behavioral cases pin revision-change, local-overlap, two-record,
unrelated-PR, and cap behavior
([Policy tightening expectations](../../../tests/repo-gardener/cases/policy-tightening-during-run.md#expected-behavior) and
[Parallel orchestration expectations](../../../tests/repo-gardener/cases/parallel-nightly-orchestration.md#expected-behavior)).

### Keep measurement yield separate from capacity

If filtered queries return 107 records, 12 are inspected, and two findings
resolve to one qualified repair, keep those counts distinct. State the query
filters and pagination limits; unread work remains unassessed. If
`maximum_workers` is zero or unrelated PRs already exist, the run may still
sense, deepen, and recommend; those leftover PRs do not consume the Executor
cap. Evidence the host can already read needs no file grant: the runtime
reliability area that reports `unavailable` because the durable file lacks a key has invented
a permission system on top of a fact the host holds.

## Related

- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-skills.md)
- [Ship bundled skill helpers with an executable falsifiability contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
- [Make skill safe stops local and observable](../workflow-issues/make-skill-safe-stops-local-and-observable.md)
