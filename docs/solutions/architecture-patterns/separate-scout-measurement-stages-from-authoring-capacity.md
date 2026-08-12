---
title: Separate scout measurement stages from authoring capacity
date: 2026-08-12
category: architecture-patterns
module: skills/repo-gardener/reconciliation
problem_type: architecture_pattern
component: development_workflow
severity: high
applies_when:
  - "An autonomous workflow scouts many source records before qualifying recommendations"
  - "Several scouts can emit overlapping findings"
  - "Read-only analysis and authoring have different capacity limits"
  - "A report exposes counts used to judge coverage or candidate yield"
tags:
  - autonomous-scouts
  - candidate-count
  - source-census
  - cross-scout-deduplication
  - execution-parallelism
  - ephemeral-recommendations
  - read-only-depth
---

# Separate scout measurement stages from authoring capacity

## Context

An autonomous scouting pipeline observes three different populations:

1. the source records inspected during breadth sensing;
2. the evidence-qualified candidates emitted by each scout; and
3. the normalized candidates remaining after cross-scout deduplication.

These counts answer different questions. Collapsing them exaggerates candidate
yield or hides deduplication. A related category error occurs when execution
parallelism is treated as a global semaphore: occupied authoring capacity then
suppresses safe read-only investigation and recommendations.

This pattern was captured while revising `repo-gardener` on an unmerged branch.
Its candidate evidence shape requires stable source identity and revision,
scope, impact, urgency, confidence, risk, effort, conflicts, a verification
path, and capability needs
(`skills/repo-gardener/references/lane-contracts.md:14-17`).

## Guidance

Name and report every transformation independently:

- **Source census** measures coverage: issues, alerts, files, events, signals,
  or other records inspected. Census entries are not candidates merely because
  a scout read them.
- **Scout `candidate_count`** counts distinct records emitted by that scout
  after they satisfy the common candidate evidence contract. It is recorded in
  the Scout Receipt before cross-scout normalization
  (`skills/repo-gardener/references/reconciliation.md:37-47`).
- **Normalized candidate count** is computed after combining scout output and
  deduplicating by verified stable source identity. Preserve every contributing
  receipt and lane in the executable result, and report this count separately
  rather than deriving it by summing receipt counts
  (`tests/repo-gardener/fixtures/reconciliation/check_decisions.py`).

Apply each capacity limit only to the effect it governs. Portfolio occupancy
and execution parallelism constrain claiming and authoring. They do not consume
provider-enforced read-only sensing, qualification, bounded deepening, or
ephemeral recommendation capacity
(`skills/repo-gardener/references/reconciliation.md:101-109`).

Give depth its own explicit budget. Finish breadth first, then select zero to
the configured maximum evidence-justified deep targets. Keep deepening inside
the parent read-only invocation; it creates neither portfolio ownership nor a
child authoring worktree
(`skills/repo-gardener/references/reconciliation.md:52-73`).

## Why This Matters

The separation makes pipeline yield auditable:

```text
source census
  -> evidence qualification per scout
  -> cross-scout stable-identity normalization
  -> qualitative recommendation
  -> separately authorized claim and authoring
```

It also prevents an execution constraint from silently becoming a coverage
constraint. A run can continue finding and explaining useful work while its one
authoring slot is occupied, without claiming that work or weakening mutation
authority.

## When to Apply

- Scheduled or autonomous agents fan out across several sources or lanes.
- More than one scout can discover the same underlying work.
- Report capacity, analysis budget, authoring concurrency, and mutation
  serialization are distinct limits.
- Owners use reported counts to evaluate breadth, selectivity, or recommendation
  quality.

## Example

Suppose nine scouts enumerate 90 open issues and 17 repository-health signals,
only two observations satisfy their scouts' evidence contracts, and those two
hypothetical records have different stable identities:

```text
source_census: 107
aggregate_scout_candidate_count: 2
normalized_candidate_count: 2
```

If both scouts instead refer to the same stable source identity, the emitted
counts may still total two while normalization returns one. That is useful
information, not an inconsistency.

Likewise, one retained Merge-ready row consumes portfolio and report capacity,
while execution parallelism of one bounds later authoring. Neither suppresses
eligible recommendations in otherwise free report slots or evidence-justified
read-only depth.

Test these distinctions directly. The matched case uses a census of
107, two emitted candidates, occupied execution capacity, and free report slots
(`tests/repo-gardener/cases/nightly-depth-and-measurement-integrity.md:10-52`).
The fresh-context baseline passed 1/8 behaviors; the skilled variant passed 8/8
after the evidence artifact separately rendered census, emitted, and normalized
counts (`tests/repo-gardener/log.md`). Mechanical checks pin the contract phrases
and configured depth limit
(`tests/repo-gardener/fixtures/reconciliation/check_decisions.py`).

## Related

- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-agent-skills.md)
- [Ship bundled skill helpers with an executable falsifiability contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
