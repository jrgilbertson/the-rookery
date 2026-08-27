---
name: checking-simplicity
description: Use when a current draft software plan or proposed implementation approach needs a simplicity check before coding, including requests to simplify a plan, avoid overengineering, choose the smallest reliable approach, or reuse an existing mechanism. Also use at an in-build decision point before adding abstractions, dependencies, configuration, persisted state, adapters, hooks, or background workflows. Skip read-only work and prescribed mechanical edits with no design choice. Returns a read-only verdict; it does not plan, edit, review correctness, clean up settled code, or decide shipping readiness.
license: MIT
compatibility: Requires access to the complete requirements and current plan or implementation surface. A verified result requires a fresh context; a caller consuming it as a gate also needs an uninterrupted handoff.
---
# Checking Simplicity

Review the current approach before avoidable machinery hardens into code. Find
only complexity that the stated outcome does not require, and name the
smallest safe alternative. This is an assessment, not a planning, editing, or
approval workflow.

Run after requirements are clear and a draft approach exists, before the first
implementation edit. Run again only when the required behavior or the
implementation shape materially changes. During a build, use it at the
decision point before adding another module, interface, dependency, persisted
state or schema, configuration surface, adapter or provider layer, hook, queue,
cache, state machine, or background workflow.

When configuring how a caller schedules this checkpoint, or when the harness
cannot dispatch a fresh context, read
[references/activation.md](references/activation.md).

## Review boundary

Bind the review to both:

- the current objective, required behavior, hard constraints, and verification
  criteria; and
- one current subject: the draft plan or proposed approach, or the complete
  in-progress implementation surface.

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

When a caller supplies subject-binding fields, repeat them in `Subject`
without weakening them to a prose summary. A missing repository, branch, full
`HEAD`, or surface category makes an implementation review unverified even if
the available subset looks clean.

The result describes the observed subject; it is not a durable receipt. A
caller that needs to consume it as a gate must use an uninterrupted handoff:
supply the complete current subject, allow no implementation or surface-changing
work before the result returns, then re-read the full subject content. Matching
paths alone do not prove that staged, unstaged, untracked, or plan content stayed
unchanged.

The reviewer must have no prior involvement with the subject: it must not have
planned, authored, implemented, reviewed an earlier version, applied review
fixes, or produced findings or decisions that shaped it. Independence also
requires complete requirement and subject evidence. When either the evidence
or reviewer provenance is incomplete, label the review `unverified`. A
same-context review may still find useful reductions, but label it
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

## Protect essential complexity

Never simplify away required behavior, authorization boundaries, security,
privacy, data integrity, accessibility, compatibility, bounded resource use,
operability, or proportionate tests for real failure modes. Call these out as
protected complexity when they could otherwise look removable.

Do not reduce the requested scope. When materially different smaller outcomes
would each be valid, set the owner-decision flag and ask the one decision that
separates them. The flag is independent of the verdict: an approach can need
changes and an owner decision at the same time.

## Return the assessment

Return exactly one verdict:

- `PASS` when no material unnecessary complexity is evidenced; or
- `CHANGES_NEEDED` when at least one named concept can be removed, reused, or
  deferred while preserving the protected requirements.

Use this compact shape:

```text
Verdict: PASS | CHANGES_NEEDED
Review context: independent | same-context (advisory) | unverified
Subject: <requirements source + current plan, or requirements source + repository + branch + full HEAD + complete path inventory>
Owner decision required: no | yes — <one exact question>

Findings:
- Evidence: <requirement and subject pointer>
  Remove, reuse, or defer: <unnecessary concept>
  Smallest safe alternative: <replacement>

Protected complexity: <what must remain, or none>
```

On a clean pass, keep `Findings` to `none`; do not invent a concern. When reuse
of an existing mechanism is part of the smallest safe approach, name it under
`Protected complexity` with the required constraints it preserves. On
`CHANGES_NEEDED`, every finding needs a pointer to both the proposed mechanism
and the current requirement it fails to serve. Return the assessment to the
caller. Do not revise the plan, edit files, configure hooks, commit, or approve
shipping.

## Boundaries

- Use behavior-preserving code cleanup for settled, recently changed code
  instead of this skill.
- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment, but this skill never makes those decisions.
