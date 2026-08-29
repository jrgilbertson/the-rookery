---
title: Keep qualitative agent reviews qualitative
date: 2026-08-28
last_updated: 2026-08-28
category: best-practices
module: skill-instruction-review
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "A user points to an area, question, plan, technical choice, existing architecture, or current code and asks for opportunities to simplify safely"
  - "Formal requirements are absent but the current goal, protected boundaries, consumers, or observed use provide a sufficient decision frame"
  - "A component-by-component review could miss that the whole-system shape is unnecessary"
  - "Some complexity can be removed immediately while one owner decision controls the minimum safe final shape"
  - "A qualitative review is being converted into parsers, schemas, receipts, reviewer quotas, or proof workspaces"
tags: [skills, simplicity, qualitative-review, system-design, architecture, decision-frame, model-judgment, process-machinery]
---

# Keep qualitative agent reviews qualitative

## Context

A simplicity review grew into a certification protocol with exact Git binding,
structured receipts, new reviewers after revisions, and repeated proof
environments. The machinery made the output harder to use and consumed reviewer
capacity without improving the qualitative decision. It also exempted the
review process from the necessity test applied to product designs. (session
history)

Its next framing centered formal requirements and named workflow checkpoints.
That excluded a common, valid request: point at an area, question, plan,
technical choice, current implementation, or bounded brainstorming direction
and ask where it can be simplified safely. It also encouraged reviewing
components one by one when the larger architecture was the unnecessary part.
(session history)

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

Apply this necessity test to the review process as well as the product. Build
the decision frame from the best available evidence: the stated goal,
requirements when present, protected behavior and constraints, actual
consumers, and observed use. Formal requirements are useful but not mandatory,
and a named subject with enough inspectable evidence is sufficient. Do not
demand a separate artifact that only replays the same information.

Review the whole-system shape before its individual concepts. Compare the
viable approaches, boundaries, responsibilities, data paths, and operating
surfaces first, and state the current and smaller system shapes before the
component findings. A queue, adapter, registry, or protocol may look defensible
in isolation while composing into an architecture that no current consumer or
protected boundary needs.

When safe reductions and one unresolved owner decision coexist, lead with the
unconditional reductions. Ask the one question that changes the remaining
shape, then state the smallest safe shape for either answer. Do not withhold
known reductions or silently answer the product question.

Preserve precision that serves an observed boundary. For example, activation
language proven necessary by native routing tests is load-bearing even when it
is longer than the skill body would otherwise need.

## Why This Matters

Qualitative review machinery can create the same speculative abstractions it is
supposed to remove. Every extra parser, reviewer, receipt, and proof environment
adds failure modes and coordination cost. Requiring a current consumer or
boundary keeps rigor proportional without weakening real safety constraints.
Starting at the whole-system level also prevents local component justifications
from hiding an unnecessary distributed design.

## When to Apply

- While designing or simplifying an agent-facing review workflow.
- When reviewing a proposed or existing system without a formal requirements
  artifact but with enough evidence to identify its current need.
- During bounded brainstorming whose explicit question is how to simplify a
  named direction safely.
- When a proposed control exists only to make model judgment deterministic.
- When review revisions trigger new reviewers, receipts, or proof environments.
- When an owner decision affects the final design but does not block other safe
  reductions.

## Examples

`checking-simplicity` accepts a named subject and the best available decision
frame, starts with whole-system shape, and names direct judgment as an existing
mechanism (`skills/checking-simplicity/SKILL.md`). Its ordinary assessment can
run in context, while an explicitly independent gate uses one separate-context
non-author, non-implementer without reviewer churn.

The regression cases make these behaviors observable:

- `tests/checking-simplicity/cases/process-machinery-overcomplication.md`
- `tests/checking-simplicity/cases/independent-gate-one-reviewer.md`
- `tests/checking-simplicity/cases/existing-architecture-without-formal-requirements.md`
- `tests/checking-simplicity/cases/brainstorming-simplification-opportunities.md`

## Related

- [Operationalize abstract qualifiers in instruction review](operationalize-abstract-qualifiers-in-instruction-review.md)
- [Use independent contexts for skill grading and review](independent-fresh-context-review-for-skills.md)
- [Answer-first natural prose for owner-facing skill readouts](answer-first-natural-prose-for-owner-facing-skill-readouts.md)
- [Make skill safe stops local and observable](../workflow-issues/make-skill-safe-stops-local-and-observable.md)
