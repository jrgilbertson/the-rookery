---
name: checking-simplicity
description: 'For a finished implementation plan described as ready and asked to hand off or continue, select this read-only review before execution or its first edit when no clean simplicity result is supplied or an owner question remains. Subjectless reuse stays with planning. If that result covers the unchanged plan and no owner question remains, do not load this review; execution owns the next step. Also use it for a completed requirements brief or approach before implementation planning, or an in-build decision before it adds an abstraction, dependency, configuration, persisted state, adapter, hook, queue, or background workflow. Review the identified subject against complete requirements to find the smallest safe alternative; for requirements-only drafts, assess scope without inventing implementation details. Exclude unfinished behavior changes, settled-code cleanup, bugs, and shipping. It does not plan, edit, implement, approve, or require a workflow checkpoint.'
license: MIT
compatibility: Requires access to the current requirements and subject under review. An independent gate also requires one reviewer who did not author or implement the subject.
---
# Checking Simplicity

Challenge proposed scope or machinery against the current requirements and
find the smallest safe alternative. This is an assessment, not a planning,
editing, or approval workflow.

Use it when a completed requirements draft or approach is ready for
implementation planning, a finished implementation plan is ready for
execution, or an in-build decision would add product or process machinery. An
unchanged subject with a clean result and no open owner question can continue
without another check.

The ordinary assessment can run in the current context. When the caller
explicitly needs an independent gate, use one reviewer who did not author or
implement the subject and give that reviewer the current owner-authoritative
requirements and complete subject. The caller owns any stronger evidence or
continuity protocol; do not create receipts, reviewer quotas, or proof
environments for this skill. A reviewer may assess a revision it previously
reviewed as long as it did not author or implement the revision.

## Review boundary

Review both:

- the current objective, required behavior, hard constraints, and verification
  criteria; and
- one current subject: the completed requirements draft, proposed approach,
  implementation plan, or concrete in-build decision and its relevant current
  implementation.

A request that states the relevant requirements and complexity-bearing
decisions is a complete subject. Do not require a separate document, path, or
replay of the same information.

Treat owner-approved requirements and hard constraints as requested scope.
Treat capabilities added only by an agent-authored draft as proposals, even
when the draft is marked complete. If available evidence does not establish
whether the owner approved a capability, ask one owner question and make any
dependent recommendation conditional. When plausible requirements sources
conflict, ask which source governs the review.

Infer the subject from the request and available evidence. For implementation,
inspect the relevant current code and uncommitted work rather than one
convenient diff. If missing evidence could change the recommendation, name the
minimum missing evidence, including the existing mechanism being compared,
instead of inventing certainty.

The result covers the subject reviewed. Run another check only when the
requirements or complexity-bearing decisions relevant to the recommendation
change. Copy edits and implementation changes that merely apply the recommended
reduction do not require a new assessment unless a caller's independent gate
sets a stricter rule.

## Necessity test

Separate the requested outcome from the mechanisms proposed to reach it. Then
climb this ladder and stop at the first rung that completely satisfies the
current requirements:

1. Remove the need for a change.
2. Reuse the codebase's existing mechanism.
3. Use the native platform, standard library, or an installed dependency.
4. Add the smallest clear implementation that works.

For qualitative agent-facing work, direct model judgment is an existing
mechanism. Add parsers, schemas, or deterministic protocols only when a current
machine consumer, enforcement boundary, or observed failure requires them.

Inspect each new complexity-bearing concept, including product code and process
machinery. It earns its place only when the current requirement, correctness,
safety, or operating constraint that needs it is named and observable. A
hypothetical future caller or possible later variation is not current evidence.
Account for every proposed concept, grouping related concepts when useful.

Ask four questions:

1. Which stated requirement or hard constraint requires this concept?
2. What existing mechanism or direct judgment was considered, and why is it
   insufficient?
3. Does the interface, schema, protocol, option, or proof environment serve a
   current consumer, responsibility, or observed variation?
4. What smaller alternative preserves behavior, safety, operability, and
   maintainability?

Start with what can disappear. Prefer removal, reuse, or deferral over renaming
the same machinery. Do not turn line count, file count, or a numeric complexity
budget into the verdict. Do not claim an existing mechanism unless the evidence
identifies it. Preserve requirement quantifiers: a maximum is an upper bound,
not required work; a retry capped at two attempts stops after the first success.

At a requirements-only handoff, compare every added capability, variation,
lifecycle state, policy, and operator control with the originating objective
and hard constraints. Name a smaller requirements set when speculative scope
can disappear, and name acceptance tests for that set and every protected
constraint. Do not choose files, APIs, dependencies, or architecture.

## Protect essential complexity

Preserve required behavior, authorization boundaries, security, privacy, data
integrity, accessibility, compatibility, bounded resource use, operability,
and proportionate tests for real failure modes. Call these out as protected
complexity when they could otherwise look removable.

Do not reduce owner-approved scope. When source authority is unclear, or when
materially different smaller outcomes would each be valid, ask the one question
that separates them. An approach can need simplification and an owner decision
at the same time.

Do not treat silence as an answer when two observable behaviors both fit the
stated requirement but need materially different machinery. Ask which behavior
is required before choosing between them. Protect only boundaries stated or
directly implied by current requirements.

When the subject changes behavior, name the proportionate tests that must
continue to prove each protected boundary. Name the observable test, not only
the boundary.

## Return the assessment

Use a compact Minto-shaped readout: lead with the recommendation, group only
the reasons that justify it, and keep each reason's essential evidence in the
same sentence. The response must remain easy to scan as plain text when
Markdown is not rendered.

Start with the one line that fits:

- `Proceed with the current approach.` when no material unnecessary complexity
  is evident.
- `Simplify before proceeding.` when at least one named concept can be removed,
  reused, or deferred while preserving the requirements.
- `Decide before proceeding: <one exact question>` when owner authority is the
  only blocker.
- `Cannot assess yet: <minimum missing evidence>` when the requirements or
  subject cannot support a responsible recommendation.

When evidence and an owner decision are both missing, lead with `Cannot assess
yet` and include the single exact decision question after the evidence gap.
Keep any reduction that depends on that answer explicitly conditional.

```text
Simplify before proceeding.

<smallest safe revised approach>

Why:
- <decision-driving reason with its essential evidence>

Keep <required behavior, constraints, and proportionate tests>.

<next action and any warranted recheck>
```

For a clean result, use three to five short nonblank lines: the recommendation,
one affirmative reason when useful, and what must remain. Do not invent a
concern or print `Why` or next-action sections.

When simplification is needed, aim for eight to twelve short nonblank lines.
Give the smallest safe alternative, at most three grouped `Why` reasons, one
`Keep` sentence for protected behavior and tests, and the next action. Name
reuse in the recommendation or reasons. Each removal reason must connect the
proposed machinery or scope to the current requirement it does not serve.

When the result cannot be assessed, name only the missing evidence that changes
what the caller can do, the recovery action, and any useful conditional
reduction. A materially changed requirement or complexity decision warrants a
new review.

Do not print a review receipt, subject replay, reviewer identity inventory,
commit hash, context label, negative owner-decision field, or internal status
code. Offer detailed evidence only if the caller asks. Return the assessment
without revising the subject, editing files, configuring hooks, committing, or
approving shipping.

## Boundaries

- Use behavior-preserving code cleanup for settled, recently changed code
  instead of this skill.
- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment and add their own evidence requirements, but this skill never
  makes those decisions.
