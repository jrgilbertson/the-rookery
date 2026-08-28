---
name: checking-simplicity
description: 'For a finished implementation plan described as ready and asked to hand off or continue, select this read-only review before execution or its first edit when no clean independent simplicity result is supplied or an owner question remains. If that result covers the unchanged plan and no owner question remains, do not load this review; execution owns the next step. Also use it for a completed requirements brief or approach before implementation planning, or an in-build decision before it adds an abstraction, dependency, configuration, persisted state, adapter, hook, queue, or background workflow. Review the identified subject against complete requirements to find the smallest safe alternative; for requirements-only drafts, assess scope without inventing implementation details. Exclude subjectless simplification or reuse, unfinished behavior changes, settled-code cleanup, bugs, and shipping. It does not plan, edit, implement, approve, or require a workflow checkpoint.'
license: MIT
compatibility: Requires access to the complete requirements and current plan or implementation surface. A verified result requires a fresh context; a caller consuming it as a gate also needs an uninterrupted handoff.
---
# Checking Simplicity

Challenge proposed scope or machinery against the current requirements and
find the smallest safe alternative. This is an assessment, not a planning,
editing, or approval workflow.

Run after requirements are clear and a current reviewable draft exists. A
completed requirements-only draft is a valid early subject. Assess its scope
without proposing implementation details. Run again before a finished
implementation plan hands off to execution, or before its first code edit. If
an unchanged subject already has a clean independent result and no open owner
question, continue the workflow instead of checking it again.

Schedule another checkpoint when required behavior, a protected constraint, or
one of the implementation concepts under review changes. Copy edits alone do
not need a new review, but any subject-content change makes an earlier result
stale for a caller that consumes it as a gate. During a build, run at the
decision point before adding another module, interface, dependency, persisted
state or schema, configuration surface, adapter or provider layer, hook, queue,
cache, state machine, or background workflow.

For an independent checkpoint, dispatch the complete subject to a fresh
context. When the harness cannot do that:

1. Stop at the planning or execution boundary.
2. Prepare a separate-session handoff with the complete requirements and exact
   subject.
3. Before consuming the returned assessment, re-read the complete subject and
   its binding.
4. If either differs, dispatch the current subject through a new checkpoint
   instead of crossing the boundary.

## Review boundary

Bind the review to both:

- the current objective, required behavior, hard constraints, and verification
  criteria; and
- one current subject: the completed requirements draft, proposed approach,
  implementation plan, or, for an in-build decision, both the decision text
  and the complete current implementation surface.

Treat owner-approved requirements and hard constraints as requested scope.
Treat capabilities added only by an agent-authored draft as proposals, even
when the planning workflow marked the draft complete or ready for handoff. If
the available evidence does not establish who approved a capability, ask one
owner question instead of silently removing or protecting it. Make any related
recommendation conditional and do not present the removal as settled before
the owner answers. Keep this source authority when reviewing a later approach,
implementation plan, or in-build decision; the latest draft does not erase the
originating objective.

When multiple plausible requirements sources conflict, ask which source is
authoritative. Keep findings affected by that answer conditional.

An approach, implementation plan, or in-build decision cannot establish owner
authority for its own requirement summary. Bind it to an originating
owner-authoritative requirements source supplied by the caller or repository
evidence. If that source is absent or unresolved, ask which source governs the
subject.

Infer the subject from the request and available evidence. Plan and
implementation are input shapes, not separate modes. For implementation,
inspect the whole relevant surface rather than one convenient diff: committed,
staged, unstaged, and untracked work when a Git worktree is available. Name any
missing evidence and do not invent certainty around it. Bind an implementation
subject to the repository, branch, full `HEAD` commit OID, and the path
inventory in each surface category. Bind a plan to the current draft supplied
in this context, naming its path or heading when one exists and the requirements
source used to judge it. A changed draft, `HEAD`, or working surface makes an
older result stale.

Every concrete in-build decision is an implementation subject. Its decision
text cannot substitute for the current implementation surface. If a required
Git identity or inventory read fails, or any surface category is unavailable,
the review cannot be verified. Never infer the missing binding from the
decision document.

Retain the exact subject binding while assessing it, but do not replay that
inventory in the normal readout. A missing repository, branch, full `HEAD`, or
surface category makes an implementation review unverifiable even when the
available subset looks clean. Track committed, staged, unstaged, and untracked
paths separately; never assume that "all paths" or one pasted diff covers the
whole surface.

The result describes the observed subject; it is not a durable receipt. A
caller that needs to consume it as a gate must use an uninterrupted handoff:
supply the complete current subject, allow no implementation or surface-changing
work before the result returns, then re-read the full subject content. Matching
paths alone do not prove that staged, unstaged, untracked, or plan content stayed
unchanged.

The reviewer must have no prior involvement with the subject: it must not have
planned, authored, implemented, reviewed an earlier version, applied review
fixes, or produced findings or decisions that shaped it. Independence also
requires complete requirement and subject evidence. Incomplete evidence,
unknown reviewer provenance, or prior influence prevents a verified result. A
same-context review may still find useful reductions, but it is advisory and
never satisfies another workflow's independent simplicity check.

## Necessity test

Separate the requested outcome from the mechanisms proposed to reach it. Then
climb this ladder and stop at the first rung that completely satisfies the
current requirements:

1. Remove the need for a change.
2. Reuse the codebase's existing mechanism.
3. Use the native platform, standard library, or an installed dependency.
4. Add the smallest clear implementation that works.

Inspect each new complexity-bearing concept. It earns its place only when the
current requirement, correctness, safety, or operating constraint that needs
it is named and observable. A hypothetical future caller or possible later
variation is not current evidence.

Ask four questions:

1. Which stated requirement or hard constraint requires this concept?
2. What existing mechanism was considered, and why is it insufficient?
3. Does the interface or option represent a real responsibility or an observed
   variation, with a current caller or operator?
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

Never simplify away required behavior, authorization boundaries, security,
privacy, data integrity, accessibility, compatibility, bounded resource use,
operability, or proportionate tests for real failure modes. Call these out as
protected complexity when they could otherwise look removable.

Do not reduce owner-approved scope. When source authority is unclear, or when
materially different smaller outcomes would each be valid, ask the one question
that separates them. An approach can need simplification and an owner decision
at the same time.

Do not treat silence as an answer when two observable behaviors both fit the
stated requirement but need materially different machinery. Ask which behavior
is required before choosing between them. Whether request-scoped work must
survive a client disconnect is such a decision; hypothetical future flexibility
is not.

When the subject changes behavior, name the proportionate tests that must
continue to prove each protected boundary.

Protect only boundaries stated or directly implied by current requirements.
Do not fill the readout with generic authorization, concurrency, logging, or
test obligations that the evidence does not establish.

## Return the assessment

Use a compact Minto-shaped readout: lead with the recommendation, group only
the reasons that justify it, and put each reason's essential evidence in the
same sentence. The response must remain easy to scan as plain text when
Markdown is not rendered.

Start with the one line that fits:

- `Proceed with the current approach.` when no material unnecessary complexity
  is evident.
- `Simplify before proceeding.` when at least one named concept can be removed,
  reused, or deferred while preserving the requirements.
- `Decide before proceeding: <one exact question>` when owner authority is the
  only blocker.
- `Cannot verify yet: <missing evidence or reviewer independence>` when the
  subject or reviewer cannot support a verified result.

When evidence and an owner decision are both missing, lead with `Cannot verify
yet` and include the single exact decision question after the evidence gap.
Keep any reduction that depends on that answer explicitly conditional.

```text
Simplify before proceeding.

<smallest safe revised approach>

Why:
- <decision-driving reason with its essential evidence>

Keep <required behavior, constraints, and proportionate tests>.

<next action and any required recheck>
```

For a clean result, use three to five short nonblank lines: the recommendation,
one affirmative reason when useful, and what must remain. Do not invent a
concern or print empty sections.

When simplification is needed, aim for eight to twelve short nonblank lines.
Give the smallest safe alternative, at most three grouped `Why` reasons, one
`Keep` sentence for protected behavior and tests, and the next action. Name
reuse in the recommendation or reasons. Each removal reason must connect the
proposed machinery or scope to the current requirement it does not serve.
Fold proportionate tests into the `Keep` sentence rather than adding a separate
test inventory. When that sentence already names the protected behaviors, say
`focused tests for those behaviors` instead of listing each test case unless a
specific case drives the decision.

When the result cannot be verified, name only the missing evidence or
provenance that changes what the caller can do, the recovery action, and any
useful advisory reduction. For implementation, recovery requires both the four
path categories and the complete current contents of every relevant surface.
End with this staleness rule: `A changed draft, HEAD, or working surface
requires a new review.`

Do not print a review receipt, subject replay, reviewer identity inventory,
commit hash, clean-run context label, negative owner-decision field, or internal
status code. Offer detailed evidence or trace only if the caller asks. Return
the assessment to the caller without revising the plan, editing files,
configuring hooks, committing, or approving shipping.

## Boundaries

- Use behavior-preserving code cleanup for settled, recently changed code
  instead of this skill.
- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment, but this skill never makes those decisions.
