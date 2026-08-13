---
title: Separate scout measurement stages from authoring capacity
date: 2026-08-12
last_updated: 2026-08-12
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
adding the claimed assurance. A script can prove identities, ordering, bytes,
and readback. It cannot prove that a candidate matters or a plan is good.

The same category error appears in measurement and capacity accounting. Source
records inspected, evidence-qualified lane candidates, and normalized
cross-lane candidates are different populations. Read-only sensing and depth
are not authored work, so an occupied PR slot must not suppress them
(`skills/repo-gardener/references/reconciliation.md:48-58`,
`skills/repo-gardener/references/reconciliation.md:80-84`).

Assign each kind of truth to the system that can own it: the model owns
qualitative judgment, the live repository policy owns mutation permission,
native GitHub PR state owns authored-work status, and deterministic code owns
only mechanically falsifiable tracker consistency
(`skills/repo-gardener/SKILL.md:10-13`).

## Guidance

### Keep qualitative judgment with the model

Run all nine breadth lanes. Qualify current evidence and normalize overlapping
candidates by stable identity. Let the model compare the survivors by impact,
urgency, confidence, risk, effort, verification quality, and conflict cost.
Do not compute a master score or manufacture work to consume capacity
(`skills/repo-gardener/references/reconciliation.md:41-58`,
`skills/repo-gardener/references/reconciliation.md:78-91`).

Depth is also a judgment within a hard policy bound. Finish breadth first, then
select zero through the installed `maximum_deep_targets_per_run`. Choosing fewer
is correct when the evidence does not justify more. Prefer critical-flow risk,
multi-signal convergence, and measurement defects that block trusted decisions,
but reassess after each result instead of treating the maximum as a quota
(`skills/repo-gardener/references/reconciliation.md:60-76`).

Keep data trust cross-cutting. It contributes evidence to the nine lanes rather
than becoming a tenth lane. Product-behavior evidence supports a conclusion only
after the relevant metric slice has an explicit grain and authority and
reconciles against durable truth. Blank reporting data is not zero activity
(`skills/repo-gardener/references/measurement-integrity.md:3-23`,
`skills/repo-gardener/references/measurement-integrity.md:45-66`).

### Give deterministic checks a narrow claim ceiling

Persist exactly two managed records for each run ID: one `run-opened` before
sensing and one consolidated `run-closed` after supervision or an honest
no-child decision. Do not add managed manifest, lane, decision, checker, or
per-child comments (`skills/repo-gardener/references/register-and-report.md`).

After closing, deterministic code may verify only structural facts: the two
records are unique and ordered, their identities agree, history is contiguous,
the prepared material matches, and the complete final snapshot reads the close
back exactly (`skills/repo-gardener/scripts/release_a_contract.py:1050-1105`).
The public fixture explicitly rejects candidates, plans, scores, PR readiness,
policy, authority, and effect safety as checker inputs
(`tests/repo-gardener/fixtures/run-records/check_run_records.py:287-295`).

Report `register_closed_consistently` outside the immutable close. Never present
it as a quality, safety, permission, or readiness verdict
(`skills/repo-gardener/SKILL.md:126-134`).

### Reread live policy at mutation boundaries

Child authoring requires both a positive
`boundaries.maximum_new_child_prs_per_run` and `mutation: true` for the owning
lane. Missing or false permission denies authoring. Compare the exact installed
policy revision with the opening revision immediately before parent dispatch,
child PR creation, and parent closing. A change stops that mutation and its
dependents, not unrelated read-only work
(`skills/repo-gardener/references/policy-and-entry-modes.md:3-24`).

Never fall back to the bundled starter. It intentionally has zero child
capacity and all lane mutations disabled
(`skills/repo-gardener/assets/policy-template.yaml`).

### Let native artifacts own authored work

Create a persistent child worktree only for work intended to become one PR.
The child owns planning, implementation, simplification, code review,
repository gates, PR readiness, commit, push, and PR creation. The parent owns
breadth, depth, selection, policy checks, tracker writes, supervision, and the
morning report (`skills/repo-gardener/SKILL.md:73-84`).

Freshly read the native repository, PR number, branch, head SHA, state, and
checks before reporting the child. Do not mirror that lifecycle into a custom
ownership ledger. The automation does not merge or create follow-up issues;
the retained parent report carries issue-ready recommendations for owner review
(`skills/repo-gardener/SKILL.md:82-89`).

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
when another PR already exists.

Finally, delegating one actual PR to one child makes responsibility legible.
The child completes its workflow once; the parent coordinates and reports it
once. This reduces duplicated review, excess worktrees, and bespoke state while
preserving a full morning inspection surface.

## When to Apply

- A scheduled or manual agent surveys several sources and must prioritize work
  rather than execute a predetermined ticket.
- Native systems already own durable work state, such as PRs, branches, heads,
  checks, and reviews.
- Policy may change while a long-running agent is sensing or implementing.
- Read-only breadth, bounded depth, recommendations, and authored work have
  different limits or risk profiles.
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
  -> model surveys nine lanes and deepens 0..policy maximum
  -> optional child owns one complete PR workflow
run-closed
  -> deterministic two-record structural check
  -> result reported outside the immutable close
```

The close still contains nine lane rows, depth results, bounded data-trust
evidence, native child facts or a no-child reason, owner attention,
recommendations, and run outcome. Less durable ceremony does not mean less
operating coverage.

### Stop only the mutation whose permission changed

If a run opens under `policy:1` and the owner installs `policy:2`:

- a disabled owning lane before dispatch prevents child creation but not
  unrelated reporting;
- a zero child limit before PR creation preserves saved child work without
  opening the PR; and
- a denied tracker write before close prevents a false structural-closure
  claim and becomes an interrupted caller handoff.

The active behavioral case pins all three boundaries
(`tests/repo-gardener/cases/policy-tightening-during-run.md`).

### Keep measurement yield separate from capacity

If nine lanes inspect 107 records, emit two evidence-qualified candidates, and
deduplicate them to one underlying problem, report all three values. If the
single authoring slot is occupied, the run may still sense, deepen, and
recommend; it simply may not dispatch another child.

Fresh-context dogfood passed 10/10 one-child behaviors, 6/6 policy-tightening
behaviors, and 8/8 depth/data-trust behaviors. The structural suite also
covered a two-page legacy history and adversarial identity, lineage, sequence,
operation, comment, hash, pagination, count, duplicate, missing, and
interrupted mutations (`tests/repo-gardener/log.md:41-48`).

## Related

- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-agent-skills.md)
- [Ship bundled skill helpers with an executable falsifiability contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
- [Make agent skill safe stops local and observable](../workflow-issues/make-agent-skill-safe-stops-local-and-observable.md)
