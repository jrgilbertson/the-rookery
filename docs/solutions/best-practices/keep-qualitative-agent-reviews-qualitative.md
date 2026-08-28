---
title: Keep qualitative agent reviews qualitative
date: 2026-08-28
category: best-practices
module: skill-instruction-review
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "A qualitative review is being converted into parsers, schemas, receipts, reviewer quotas, or proof workspaces"
  - "A skill adds verification machinery without a current machine consumer or enforcement boundary"
  - "An independent review loop replaces its reviewer after every revision"
tags: [skills, simplicity, qualitative-review, model-judgment, process-machinery, evidence]
---

# Keep qualitative agent reviews qualitative

## Context

A simplicity review grew into a certification protocol with exact Git binding,
structured receipts, new reviewers after revisions, and repeated proof
environments. The machinery made the output harder to use and consumed reviewer
capacity without improving the qualitative decision. It also exempted the
review process from the necessity test applied to product designs. (session
history)

## Guidance

Treat direct model judgment as the existing mechanism for qualitative,
agent-facing work. Add a parser, schema, receipt, or deterministic protocol
only when a current machine consumer, enforcement boundary, or observed
failure requires it.

Separate an ordinary advisory assessment from a caller-owned independent gate:

- The ordinary assessment can run in the current context.
- A gate needs one reviewer who did not author or implement the subject.
- That reviewer may assess a later revision; prior review is not authorship.
- The caller owns any stronger continuity or evidence requirement.

Apply this necessity test to the review process as well as the product. A
request that supplies the relevant requirements and decisions is enough; do
not demand a separate artifact that only replays the same information.

Preserve precision that serves an observed boundary. For example, activation
language proven necessary by native routing tests is load-bearing even when it
is longer than the skill body would otherwise need.

## Why This Matters

Qualitative review machinery can create the same speculative abstractions it is
supposed to remove. Every extra parser, reviewer, receipt, and proof environment
adds failure modes and coordination cost. Requiring a current consumer or
boundary keeps rigor proportional without weakening real safety constraints.

## When to Apply

- While designing or simplifying an agent-facing review workflow.
- When a proposed control exists only to make model judgment deterministic.
- When review revisions trigger new reviewers, receipts, or proof environments.

## Examples

`checking-simplicity` now names direct judgment as an existing mechanism and
requires evidence before adding deterministic protocols
(`skills/checking-simplicity/SKILL.md`). Its ordinary assessment can run in
context, while an explicitly independent gate uses one non-author,
non-implementer without reviewer churn.

The regression cases make both outcomes observable:

- `tests/checking-simplicity/cases/process-machinery-overcomplication.md`
- `tests/checking-simplicity/cases/independent-gate-one-reviewer.md`

## Related

- [Operationalize abstract qualifiers in instruction review](operationalize-abstract-qualifiers-in-instruction-review.md)
- [Use independent contexts for skill grading and review](independent-fresh-context-review-for-skills.md)
- [Answer-first natural prose for owner-facing skill readouts](answer-first-natural-prose-for-owner-facing-skill-readouts.md)
- [Make skill safe stops local and observable](../workflow-issues/make-skill-safe-stops-local-and-observable.md)
