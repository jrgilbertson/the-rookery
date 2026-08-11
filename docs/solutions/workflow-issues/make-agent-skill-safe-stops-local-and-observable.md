---
title: "Make agent-skill safe stops local and observable"
date: 2026-08-11
category: workflow-issues
module: "skills/repo-gardener"
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "A workflow can block one effect while independent allowed work remains"
  - "Scheduling, invocation liveness, and executor ownership can change independently"
  - "A lifecycle transition can invalidate a one-shot terminal report"
tags: [agent-skills, safe-stops, blocker-locality, caller-lifecycle, receipts]
---

# Make agent-skill safe stops local and observable

## Context

Automation often has several independent stop conditions. Future scheduling can
pause while the current invocation remains live. A live invocation may still
lack exclusive write ownership. One report effect can become ambiguous while
independent read-only work remains safe. Treating any one of those facts as
proof of another either stops too much work or grants authority that was never
proven.

A second failure appears at completion. A workflow can name its blocker yet
omit independent work, or settle its own assignment while it still needs the
assignment's one-shot terminal-report capability. Both paths look finished in
prose while leaving the caller without a complete, accepted result.

## Guidance

### Keep caller lifecycle facts independent

Read separate caller evidence for:

1. whether another invocation may be scheduled;
2. whether the current invocation is live or cancelled; and
3. whether it owns the repository-scoped executor.

No receipt substitutes for another. Paused scheduling does not cancel a live
run. Cancellation does not prove ownership release. Executor ownership does not
prove future scheduling is enabled.

### Stop only the dependency closure

For each missing proof, unavailable role, or ambiguous report effect, identify
the exact work that depends on it. Put that operation and its dependents in
`affected_work`. Continue independent reads and separately authorized work.
Escalate to all report writes only when a global write boundary is missing.

### Make completion a disjoint partition

Return `affected_work` and `remaining_unblocked_work` together. Every named work
item appears exactly once. Each unblocked remainder has one observable
disposition:

```text
remaining_unblocked_work:
  <item>: continued
  <item>: delegated — durable handoff read back from <destination>; authorized executor <executor>; exact work <work>
  <item>: gated — <named prerequisite>
```

Delegation requires readback of destination, authorized executor, and exact
work. Without it, the item is gated. Whole-run completion is unavailable while
any independent item lacks a disposition.

### Report before caller-managed settlement

Treat a caller-supplied one-shot terminal-report capability as the final
ordered operation. Carry pending decision requests in exactly one terminal
report for the caller to persist. Keep the current assignment active until the
caller accepts that report, then stop. Do not create a conflicting lifecycle
transition first.

## Why this matters

Blocker locality preserves safe progress without weakening the uncertain
effect. The completion partition makes omissions testable. Report-first
ordering preserves the only capability that can tell the caller what happened
and what decisions remain.

## Example

If a report write is ambiguous, its dependent recommendation stops while an
unrelated read-only audit continues:

```text
last_safe_stage: Verify
missing_proof_or_role: authoritative register post-read
affected_work: report write; dependent recommendation
remaining_unblocked_work:
  unrelated read-only audit: continued
attention_state: Action required
```

The operation keeps its original identity. A retry waits for authoritative
absence proof. The independent audit does not become affected merely because
the report effect is uncertain.

## Related

- [Verify disposition claims before landing a prune](verify-disposition-claims-before-landing-a-prune.md)
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md)
