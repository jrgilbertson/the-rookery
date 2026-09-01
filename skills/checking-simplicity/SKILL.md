---
name: checking-simplicity
description: 'Use when the user explicitly requests a simplicity assessment of a named system architecture, system design, technical area, plan, technical choice, or code-level approach by asking to simplify, right-size, identify overengineering, compare with a stated smaller alternative, choose the smallest viable approach, or test whether reuse removes the need for change. General architecture comparison or product brainstorming without that simplification intent stays with planning. Without that request, use only when an approach, plan, or immediate build decision adds durable machinery without tying it to the user''s stated need and is about to enter implementation planning, execution, or continued building. Completion of a brief or plan alone is not a trigger. Direct behavior-preserving cleanup of settled code stays with implementation. An unchanged subject with a clean result continues without another check. It assesses; it does not plan, edit, implement, approve, or require a checkpoint.'
license: MIT
compatibility: Requires a named area, question, or reviewable subject and enough accessible evidence to identify the current need and protected boundaries. An independent gate also requires a separate-context reviewer who did not author or implement the subject.
---
# Checking Simplicity

Find opportunities to safely simplify a system design, architecture, technical
area, plan, question, or code-level approach against the current need. This is
a read-only assessment, not a planning, editing, or approval workflow.

The ordinary assessment can run in the current context. When the caller
explicitly needs an independent gate, dispatch one reviewer in a separate
context, such as a subagent, separate session, or other model invocation. That
reviewer must not have authored or implemented the subject. Give the reviewer
the complete subject and available decision frame. Keep the review lightweight:
do not create receipts, reviewer quotas, or proof environments for this skill.
A reviewer may assess a revision it previously reviewed as long as it did not
author or implement the revision. The caller owns any stronger evidence or
continuity protocol.

## Review boundary

Build the decision frame from the best available evidence:

- the user's stated goal and desired outcome;
- explicit requirements, hard constraints, and verification criteria when
  present;
- behavior and boundaries that must be preserved; and
- actual consumers and observed use.

Formal requirements are useful but not required. Ask only when ambiguity would
change what can safely disappear.

Review one named subject. It may be an area or question, a proposed or existing
architecture, design, or technical choice, a planning or in-build decision, or
code and its relevant surrounding implementation. A request that supplies the
decision frame and complexity-bearing decisions is a complete subject; when it
points to a repository area instead, inspect the relevant current
implementation. Do not require a separate document, path, or replay.

Treat owner-approved requirements and hard constraints as controlling when
available. Treat capabilities added only by an agent-authored draft as
proposals, even when the draft is marked complete. If the evidence does not
establish whether the owner approved a capability, ask one owner question and
make any dependent recommendation conditional. When plausible evidence sources
conflict, ask which source governs the review.

Infer the subject from the request and available evidence. For implementation,
inspect the relevant current code and uncommitted work rather than one
convenient diff. If missing evidence could change the recommendation, name the
minimum missing evidence, including the existing mechanism being compared,
instead of inventing certainty.

The result covers the subject reviewed. Do not repeat the assessment when that
subject already received `Proceed with the current approach.` and no relevant
goal, protected boundary, consumer, observed use, or complexity-bearing
decision has changed. Copy edits and implementation changes that merely apply a
recommended reduction do not require a new assessment unless a caller's
independent gate sets a stricter rule.

## Necessity test

Start with the whole-system shape. Compare viable approaches and ask whether
each boundary, responsibility, data path, and operating surface serves a
current consumer or protected constraint. Before accounting for individual
concepts, summarize the current shape and the smallest viable shape as whole
systems.

Separate the needed outcome from the mechanisms proposed to reach it. Then
climb this ladder and stop at the first rung that completely satisfies the
current need:

1. Remove the need for a change.
2. Reuse the codebase's existing mechanism.
3. Use the native platform, standard library, or an installed dependency.
4. Add the smallest clear implementation that works.

For qualitative agent-facing work, direct model judgment is an existing
mechanism. Add parsers, schemas, or deterministic protocols only when a current
machine consumer, enforcement boundary, or observed failure requires them.

Inspect each complexity-bearing concept in the proposed or existing subject,
including product code and process machinery. It earns its place only when the
current need or a protected correctness, safety, or operating boundary is named
and observable. A hypothetical future caller or possible later variation is
not current evidence. Account for every concept, grouping related concepts when
useful.

Ask four questions:

1. Which part of the current need or protected boundary requires this concept?
2. What existing mechanism or direct judgment was considered, and why is it
   insufficient?
3. Does the interface, schema, protocol, option, or proof environment serve a
   current consumer, responsibility, or observed variation?
4. What smaller alternative preserves behavior, safety, operability, and
   maintainability?

Start with what can disappear. Prefer removal, reuse, or deferral over renaming
the same machinery. Do not turn line count, file count, or a numeric complexity
budget into the verdict. Do not claim an existing mechanism unless the evidence
identifies it. Preserve stated sequencing and quantifiers: a completion audit
occurs only after success; a maximum is an upper bound, not required work; a
retry capped at two attempts stops after the first success.

When reviewing a requirements-only subject, compare every added capability,
variation, lifecycle state, policy, and operator control with the originating
objective and hard constraints. Name a smaller requirements set when
speculative scope can disappear, and name acceptance tests for that set and
every protected constraint. Do not choose files, APIs, dependencies, or
architecture.

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
available decision frame but need materially different machinery. Ask which
behavior is required before choosing between them. Protect only boundaries
stated or directly supported by the decision frame.

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
  reused, or deferred while preserving the current need and protected
  boundaries.
- `Decide before proceeding: <one exact question>` when owner authority is the
  only blocker.
- `Cannot assess yet: <minimum missing evidence>` when the decision frame or
  subject cannot support a responsible recommendation.

When evidence and an owner decision are both missing, lead with `Cannot assess
yet` and include the single exact decision question after the evidence gap.
Keep any reduction that depends on that answer explicitly conditional.

When unconditional reductions and an owner decision coexist, lead with
`Simplify before proceeding.`, give those reductions first, then ask the one
exact question and end with two short sentences: `If no, <smallest safe
shape>.` and `If yes, <smallest safe shape>.`

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
proposed machinery or scope to the current need it does not serve.
For a system design or architecture, the alternative must name both the current
and smaller whole-system shapes and their decision-driving contrast before the
component reasons.

When the result cannot be assessed, name only the missing evidence that changes
what the caller can do, the recovery action, and any useful conditional
reduction. A materially changed need, protected boundary, consumer, observed
use, or complexity decision warrants a new review.

Do not print a review receipt, subject replay, reviewer identity inventory,
commit hash, context label, negative owner-decision field, or internal status
code. Offer detailed evidence only if the caller asks. Return the assessment
without revising the subject, editing files, configuring hooks, committing, or
approving shipping.

## Boundaries

- Use general brainstorming or planning when the outcome itself is still open;
  this skill joins only when the task is to find safe simplification
  opportunities.
- Use behavior-preserving code cleanup for settled, recently changed code
  instead of this skill.
- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment and add their own evidence requirements, but this skill never
  makes those decisions.
