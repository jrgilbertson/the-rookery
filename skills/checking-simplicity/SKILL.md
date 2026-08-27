---
name: checking-simplicity
description: 'Use when complete requirements and one supplied, reviewable subject are at a simplicity checkpoint: a completed requirements draft or approach before implementation planning; a finished implementation plan before execution or its first edit; or a concrete in-build decision before it adds an abstraction, dependency, configuration, persisted state, adapter, hook, queue, or background workflow. Do not invoke it for subjectless simplification, reuse, or behavior-change requests, or when an independent PASS with no owner decision already covers the unchanged subject; route onward. Review that subject''s proposed scope or machinery against the current requirements and find the smallest safe alternative. For requirements-only drafts, assess scope without inventing implementation details. Route settled-code cleanup, bugs, and shipping decisions to their owners. Read-only; does not plan, edit, implement, or approve.'
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
an unchanged subject already has an independent `PASS` with
`Owner decision required: no`, continue the workflow instead of checking it
again.

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
owner question instead of silently removing or protecting it, and label the
review `unverified`. Make any related recommendation conditional: `Conditional
— remove or defer <capability> only if the owner says it is not required.` Do
not present that removal as settled before the owner answers. Keep this source
authority when reviewing a later approach, implementation plan, or in-build
decision; the latest draft does not erase the originating objective.

When multiple plausible requirements sources conflict, label the review
`unverified`, set `Owner decision required: yes`, and ask which source is
authoritative. Keep findings affected by that answer conditional.

An approach, implementation plan, or in-build decision cannot establish owner
authority for its own requirement summary. Bind it to an originating
owner-authoritative requirements source supplied by the caller or repository
evidence. If that source is absent or unresolved, label the review `unverified`,
set `Owner decision required: yes`, and ask which source governs the subject.

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
write `Review context: unverified`; never infer the missing binding from the
decision document.

When a caller supplies subject-binding fields, repeat them in `Subject`
without weakening them to a prose summary. A missing repository, branch, full
`HEAD`, or surface category makes an implementation review unverified even if
the available subset looks clean. Spell out `committed paths`, `staged paths`,
`unstaged paths`, and `untracked paths` separately, including when each is
unavailable; never collapse them into "all paths" or "all surfaces."

The result describes the observed subject; it is not a durable receipt. A
caller that needs to consume it as a gate must use an uninterrupted handoff:
supply the complete current subject, allow no implementation or surface-changing
work before the result returns, then re-read the full subject content. Matching
paths alone do not prove that staged, unstaged, untracked, or plan content stayed
unchanged.

The reviewer must have no prior involvement with the subject: it must not have
planned, authored, implemented, reviewed an earlier version, applied review
fixes, or produced findings or decisions that shaped it. Independence also
requires complete requirement and subject evidence. Label incomplete evidence
or reviewer provenance, and a result from anyone whose earlier findings or
decisions shaped the current subject, `unverified`. A same-context review with
no unverified condition may still find useful reductions, but label it
`same-context (advisory)` and never claim it satisfies another workflow's
independent simplicity check. A `PASS` with an advisory or unverified context
means only that the available evidence exposed no material issue; it does not
complete an independent checkpoint.

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
budget into the verdict.

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
materially different smaller outcomes would each be valid, set the
owner-decision flag and ask the one question that separates them. The flag is
independent of the verdict. An approach can need changes and an owner decision
at the same time.

When the subject changes behavior, name in `Protected complexity` the
proportionate tests that must continue to prove each protected boundary.

## Return the assessment

Return exactly one verdict:

- `PASS` when no material unnecessary complexity is evidenced; or
- `CHANGES_NEEDED` when at least one named concept can be removed, reused, or
  deferred while preserving the protected requirements.

Use a compact Minto-shaped readout: lead with the conclusion and recommended
action, group the reasons that justify it, and put only the evidence each
reason needs inline after the claim. Keep the review receipt last so it remains
available to consuming workflows without burying the decision.

```text
Verdict: PASS | CHANGES_NEEDED — <plain-language conclusion>
Recommendation: <continue with the current subject or adopt the smallest safe revised subject>

Why:
- <Remove, reuse, defer, or keep conclusion>. Evidence: <requirement and subject pointer>.

Protected complexity: <required behavior, constraints, and proportionate tests that must remain, or none>
Next: <boundary crossed, or blocked boundary + recovery + required recheck>
Owner decision required: no | yes — <one exact question>
Review receipt:
Review context: independent | same-context (advisory) — <reason> | unverified — <missing evidence or provenance>
Subject: <requirements source + objective + required behavior + hard constraints + verification criteria + current requirements draft, approach, or plan; for implementation, also include decision text + repository + branch + full HEAD + separate committed, staged, unstaged, and untracked path inventories + supplied current-content summary for every relevant surface category>
```

Write verified context exactly as `Review context: independent`, with no
suffix. Only advisory and unverified values take a reason.

On a clean `PASS`, use one affirmative `Why` reason and keep everything before
the receipt to about seven nonblank lines. Expand only for decision-driving
reasons, protected boundaries, or missing-evidence recovery. Do not turn the
receipt into the opening or repeat its fields elsewhere.

A caller may cross into implementation planning or execution only when the
current subject receives `PASS`, `Review context: independent`, and
`Owner decision required: no`. Any other result leaves that boundary blocked.
After any other result, state which planning or execution boundary remains
blocked, why, and what new decision, revision, or evidence is required. Then
state that the current resulting subject needs a new uninvolved reviewer's
independent `PASS` with no owner decision before crossing that boundary. For an
advisory or unverified implementation result, the recovery evidence must include
both the path inventory and the complete current contents of every relevant
surface category. Call any advisory or unverified `PASS` tentative and state
that it does not complete the checkpoint or satisfy PR readiness.
For every advisory or unverified result, state in `Next` that any change to the
reviewed draft, `HEAD`, or working surface makes the result stale.

On a clean pass, do not invent a concern. When reuse of an existing mechanism
is part of the smallest safe approach, name it in the recommendation or
affirmative `Why` reason and state under `Protected complexity` which required
constraints it preserves. On `CHANGES_NEEDED`, every reason needs a pointer to
both the proposed mechanism or scope choice and the current objective or
requirement it fails to serve. Return the assessment to the caller. Do not
revise the plan, edit files, configure hooks, commit, or approve shipping.

## Boundaries

- Use behavior-preserving code cleanup for settled, recently changed code
  instead of this skill.
- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment, but this skill never makes those decisions.
