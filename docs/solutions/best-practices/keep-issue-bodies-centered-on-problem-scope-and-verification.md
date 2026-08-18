---
title: Keep issue bodies centered on Problem, Scope, and Verification
date: 2026-08-17
category: best-practices
module: skills/managing-issues issue authoring
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Authoring or revising issue bodies for humans and coding agents"
  - "Writing research or decision issues that do not describe a defect"
  - "Defining verification that could drift toward a narrower proxy"
  - "Documenting a multi-step, intermittent, or environment-specific defect"
symptoms:
  - "Problem language assumes every issue describes something broken"
  - "Scope and Verification overlap or prove different behavior"
  - "Complex reproduction steps crowd the Problem section"
  - "A verification proxy can pass without proving the promised behavior"
root_cause: inadequate_documentation
resolution_type: documentation_update
related_components:
  - development_workflow
  - testing_framework
tags:
  - issue-authoring
  - issue-templates
  - problem-scope-verification
  - acceptance-criteria
  - reproduction
  - agent-skills
---

# Keep issue bodies centered on Problem, Scope, and Verification

## Context

An issue body serves humans deciding what work is worth doing and agents deciding
what to implement and how to know it is complete. A template that assumes every
issue is a defect misrepresents research and decision work. A template that
treats Verification as a loose checklist can also approve a change that never
delivered the intended behavior.

The minimum durable structure is `Problem`, `Scope`, and `Verification`.
Optional sections should appear only when they prevent a material misreading.
The focused behavioral contract lives in
`tests/managing-issues/cases/issue-body-range-and-verification-alignment.md`.

## Guidance

Treat the three universal sections as a chain from intent to proof:

1. **Problem states why the issue exists.** Describe the current gap,
   unresolved decision, or missing evidence, who or what it affects, and why it
   matters. Do not invent a defect for research or decision work.
2. **Scope states what this issue owns.** Name one outcome and the meaningful
   boundary that keeps adjacent work out. Add a non-goal only when a reader is
   likely to mistake it as included.
3. **Verification proves that promise.** Each criterion names an observable
   result or evidence requirement that is false or unproven before completion.
   It must prove the behavior declared by Problem and Scope, not a convenient
   proxy, a preferred implementation, or a narrower subcase.

Add `Reproduction` when a defect is multi-step, intermittent, or tied to a
specific environment. Keep simple expected-versus-actual behavior in Problem.
Reproduction explains how to observe the current failure; Verification explains
how to prove the promised outcome after the work.

Use the same contract at every scale. One independently deliverable, reviewable
change remains one Implementation Leaf without an artificial parent. When
several reviewable deliverables produce one whole outcome, the parent owns the
outcome-level Problem, Scope, and Verification, and each child owns one
independently demonstrable vertical outcome. The decomposition rules live in
`skills/managing-issues/SKILL.md`; graph and completion behavior lives in
`skills/managing-issues/references/graph-and-completion.md`.

Keep priority, labels, estimates, readiness, and native relationships out of
body-format conventions. Those are tracker facts analyzed for each issue. The
body explains the outcome; native tracker state explains classification and
topology.

## Why this matters

The structure scales because detail is conditional. A one-line documentation
change can remain three short sections. A research issue can state uncertainty
honestly. A complex defect can preserve exact reproduction without burying the
reason the work matters. A parent and its children can each carry the proof
appropriate to their own outcome.

The key protection is verification alignment. If every project-search entry
point must honor an Include archived toggle, a larger global result count does
not prove the result set at every entry point, and use of a particular query
shape is an implementation choice rather than promised behavior. Verification
must exercise the product behavior the issue actually claims.

This is the same claim-ceiling discipline used elsewhere in the repository:
mechanically observable evidence cannot certify a broader behavioral outcome.
See
`docs/solutions/best-practices/independent-fresh-context-review-for-agent-skills.md`
and
`docs/solutions/best-practices/operationalize-abstract-qualifiers-in-instruction-review.md`.

## Examples

- For one stale README link, Problem names the stale destination and impact,
  Scope owns replacing that link, and Verification checks the new text and
  destination. No optional section is needed.
- For an optimization decision, Problem states that adoption is unresolved
  because evidence is missing. Scope owns the comparison and adopt-or-defer
  decision. Verification requires recorded compatibility, repeatable
  performance evidence, limitations, rationale, and a reconsideration trigger.
- For an environment-specific Safari failure, Reproduction owns the browser
  version and exact sequence. Verification repeats that sequence and proves the
  save succeeds, persists, and leaves the unaffected browser behavior intact.

## Prevention

When reviewing an issue body, trace each Verification bullet back to a promise
in Problem or Scope. Then ask which incorrect or incomplete result could still
pass that check. If a plausible wrong result passes, strengthen the evidence or
narrow the promise before publishing the issue.

