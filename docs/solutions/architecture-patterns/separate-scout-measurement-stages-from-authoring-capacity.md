---
title: Separate scout measurement stages from authoring capacity
date: 2026-08-12
last_updated: 2026-09-04
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
records inspected, evidence-qualified lane candidates, and normalized
cross-lane candidates are different populations. Read-only sensing and depth
are not authored work, so unrelated already-open PRs do not consume the Worker
cap (`skills/repo-gardener/references/reconciliation.md:64-85`).

Assign each kind of truth to the system that can own it: the model owns
qualitative judgment, the live repository file owns mutation permission, the
provider owns authored-work status, and deterministic code owns only
mechanically falsifiable tracker consistency
(`skills/repo-gardener/SKILL.md:10-18`).

## Guidance

### Keep qualitative judgment with the model

Run every installed lane. Qualify current evidence and normalize overlapping
candidates. Let the model compare the survivors qualitatively, and do not
manufacture work to consume capacity
(`skills/repo-gardener/SKILL.md:58-69`,
`skills/repo-gardener/references/reconciliation.md:64-75`).

Depth is also a judgment, with no count. After breadth, deepen while further
investigation would change assignments or recommendations. Stop when it would
not, or when the run must close. Prefer credible critical-flow risks,
independent corroboration, measurement defects, overdue coverage with a
current signal, and then the strongest remaining finding
(`skills/repo-gardener/references/reconciliation.md:70-75`).

Keep data trust cross-cutting. It contributes evidence to the nine lanes
rather than becoming a tenth lane. Product-behavior evidence supports a
conclusion only after the relevant metric slice has an explicit grain and
authority and reconciles against durable truth. Blank reporting data is not
zero activity
(`skills/repo-gardener/references/measurement-integrity.md:3-6`,
`skills/repo-gardener/references/measurement-integrity.md:17-23`,
`skills/repo-gardener/references/measurement-integrity.md:50-55`,
`skills/repo-gardener/references/measurement-integrity.md:74-79`).

### Give deterministic checks a narrow claim ceiling

Persist exactly two managed records for each run ID: one `run-opened` before
sensing and one consolidated `run-closed` after supervision or an honest
no-Worker close. Do not add managed manifest, lane, decision, checker, or
per-Worker comments
(`skills/repo-gardener/references/tracker-records.md:24-43`).

After closing, deterministic code may verify only structural facts: the two
records are unique and ordered, their identities agree, and the complete
final snapshot reads the close back exactly
(`skills/repo-gardener/scripts/release_a_contract.py:545-573`). The public
fixture rejects candidates, plans, scores, PR readiness, policy, authority,
and register-quality claims as checker outputs
(`tests/repo-gardener/fixtures/run-records/check_run_records.py:280-292`).
`register_closed_consistently` is not a production result. Never present a
two-comment check as a quality, safety, permission, or readiness verdict
(`tests/repo-gardener/fixtures/run-records/check_run_records.py:147-158`,
`skills/repo-gardener/references/tracker-records.md:89-92`).

### Reread live policy at mutation boundaries

Worker authoring requires, on the opening file, exact
`repository.identity` match, every planned path inside the effective
include/exclude scope, `maximum_workers` greater than zero, owning lane
`mutation: true`, and no protected path. The live gardener file that first-use
writes on the target repository is always protected. Missing or false
permission, scope mismatch, or a current overlap denies that unit
(`skills/repo-gardener/references/policy-and-entry-modes.md:185-200`).

At open, read the durable file from the refreshed default branch and record
that revision. Mid-run, re-read it only to detect that it changed,
immediately before each declared audit, Worker dispatch, push, PR creation,
and `run-closed`. A revision change stops further source mutation, push, and
PR-open for every Worker. In contrast, an unchanged-policy authoring or
overlap denial remains local to that Worker's dependents. If the file still
names the tracker, the Orchestrator still writes the closed comment
(`skills/repo-gardener/references/policy-and-entry-modes.md:3-13`,
`skills/repo-gardener/references/policy-and-entry-modes.md:197-208`,
`skills/repo-gardener/references/reconciliation.md:79-95`,
`skills/repo-gardener/references/reconciliation.md:146-166`).

Never fall back to the bundled starter. It is fail-closed:
`maximum_workers: 0` and all authoring-lane mutations disabled
(`skills/repo-gardener/assets/policy-template.yaml:43-44`,
`skills/repo-gardener/assets/policy-template.yaml:64-98`).

### Let native artifacts own authored work

Create a persistent Worker worktree only for work intended to become one PR.
The Worker owns planning, implementation, simplification, review, repository
verification, its coherent commit, and its branch through at most one unmerged
PR. Every unattended Worker invokes `checking-pr-readiness` on its exact head,
then stops after its menu reply. On a distinct later turn, the Orchestrator
authorizes the Worker to reply 1 only when Approve was offered and recommended
for that exact head. The checking skill then performs its identity reread
before the evidence enters the publication path. Named Worker-owned gaps from
that brief all go back to the same Worker; owner-needed briefs stop without a
PR. An existing same-repository update PR with a Worker-owned gap is itself a
unit: the Worker adopts its branch at the captured head, pushes under the
old-OID lease, and keeps one unmerged PR. Overlap is changed-path
intersection; an open PR in the same directory or lane reserves nothing
(`skills/repo-gardener/references/reconciliation.md`,
`skills/repo-gardener/SKILL.md`).

The Orchestrator owns breadth, depth, selection, tracker writes, supervision,
and the morning report. After PR creation, it reports native PR, check, and
review facts; required pending work makes closure partial. The ownerless
scheduled run invokes `checking-merge-readiness` and never selects Proceed to
merge
(`skills/repo-gardener/references/reconciliation.md`,
`skills/repo-gardener/references/tracker-records.md`).

Freshly read the native repository, PR number, branch, head SHA, state,
checks, and review status before reporting the Worker. Do not mirror that
lifecycle into a custom ownership ledger. Follow-up issues stay outside the
gardening run as owner proposals for Managing Issues. The run never merges,
and the retained
Orchestrator report carries issue-ready recommendations for owner review
(`skills/repo-gardener/SKILL.md:63-67`,
`skills/repo-gardener/references/policy-and-entry-modes.md:119-145`).

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
several lanes converged on one problem. Separating read-only capacity from
authoring capacity lets the gardener keep finding and explaining useful work
when unrelated PRs already exist.

Finally, giving each justified unit its own Worker makes responsibility
legible. One Worker owns one PR-sized unit through at most one unmerged PR;
the Orchestrator coordinates and reports. Helpers scout, simplify, review, and
assess readiness; they do not own a PR. The durable morning summary stays in
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
  -> model surveys nine lanes and deepens while it would change assignment
  -> Orchestrator assigns non-overlapping Workers in parallel up to maximum_workers
  -> each Worker owns one PR-sized unit through at most one unmerged PR
run-closed
  -> deterministic two-comment identity check
  -> no register-quality claim
```

The close still contains nine lane rows, depth results, bounded data-trust
evidence, native Worker facts or a no-Worker reason, owner attention,
recommendations, and run outcome. Less durable ceremony does not mean less
operating coverage.

### Stop only the mutation whose permission changed

If a run opens against revision A of the durable file and the default branch
later holds a different revision:

- an opening-policy denial, such as a disabled owning lane or
  `maximum_workers: 0`, prevents that Worker but not unrelated reporting;
- a later revision change before PR creation preserves saved Worker work
  without opening the PR across the affected run; and
- a denied tracker write before close prevents a false structural-closure
  claim and becomes an interrupted caller handoff.

The active behavioral cases pin revision-change, local-overlap, two-record,
unrelated-PR, and cap behavior
(`tests/repo-gardener/cases/policy-tightening-during-run.md:65-94`,
`tests/repo-gardener/cases/parallel-nightly-orchestration.md:51-70`).

### Keep measurement yield separate from capacity

If nine lanes inspect 107 records, emit two evidence-qualified candidates, and
deduplicate them to one underlying problem, report all three values. If
`maximum_workers` is zero or unrelated PRs already exist, the run may still
sense, deepen, and recommend; those leftover PRs do not consume the Worker
cap. Evidence the host can already read needs no file grant: a runtime lane
that reports `unavailable` because the durable file lacks a key has invented
a permission system on top of a fact the host holds.

## Related

- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-skills.md)
- [Ship bundled skill helpers with an executable falsifiability contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
- [Make skill safe stops local and observable](../workflow-issues/make-skill-safe-stops-local-and-observable.md)
