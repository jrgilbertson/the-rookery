---
title: "Stop only the work a missing fact blocks"
date: 2026-10-09
category: workflow-issues
module: "skills/repo-gardener"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "An automated workflow reads several independent sources or runs several independent units"
  - "One source is unreachable or one unit is blocked while other work could still proceed"
  - "Someone proposes receipts, partitions, or schemas to prove that a stop stayed local"
tags: [repo-gardener, safe-stops, blocker-locality, gaps, readiness]
supersedes: [make-skill-safe-stops-local-and-observable.md]
---

# Stop only the work a missing fact blocks

## Context

An automated workflow can fail at a missing fact in two opposite ways. It can
treat one unreachable source or one blocked unit as a reason to stop the whole
run, so independent work never happens. Or it can build machinery to prove the
stop stayed local: affected-work and remaining-work partitions, lifecycle
receipts, and ordering rules for the final report. Repo Gardener once carried
that machinery. PR #153 removed it, because proof that nobody consumes turns
ordinary uncertainty into silent no-ops and ceremony.

## Guidance

- Stop only the work that depends on the missing fact. Keep independent reads
  and units going.
- Name every gap in the report: which source was unavailable, which unit
  stopped, and why.
- Keep what a stopped unit already produced, such as its authored commit, and
  say so in the report.
- Treat a run that authors nothing but reports as complete. The report is the
  result.
- Do not encode locality as receipts, partitions, or schemas unless a current
  machine consumer reads them. Plain prose in the report is enough.

## Why This Matters

A whole-run stop throws away safe work and hides how much was possible. Proof
machinery fails differently: when a receipt is missing or ambiguous, the run
does nothing and says little, and a quiet report is worse than a loud failure.
A named gap in prose keeps progress and tells the reader what to fix.

## When to Apply

- A sensing pass reads several providers, trackers, or scanners.
- A coordinator dispatches several independent units of work.
- A readiness check depends on optional companion tooling.

## Examples

`skills/repo-gardener/SKILL.md` states the rule directly:

- Lines 94 to 95: "Do not stop the whole pass because one source is
  unavailable. Name the gap and continue." Each of the five areas still gets
  a status, and the report names each unavailable source (lines 205 to 206).
- Lines 227 to 228: "Preserve a blocked unit's authored commit and name the
  unit in the report." The other units keep shipping.
- Lines 21 to 22: "Treat a run that authors nothing but reports as a complete
  run."

The readiness skills follow the same rule. In
`skills/checking-merge-readiness/SKILL.md` lines 110 to 111, a failed read of
another tracker "is a named gap that does not cap." In
`skills/checking-pr-readiness/SKILL.md` lines 165 to 168, a missing companion
skill makes that check skipped while the rest of the checks run.

## Related

- [Reuse the shipping pipeline instead of a managed-run protocol](../architecture-patterns/reuse-the-shipping-pipeline-instead-of-a-managed-run-protocol.md)
- [Keep qualitative agent reviews qualitative](../best-practices/keep-qualitative-agent-reviews-qualitative.md)
