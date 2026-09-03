---
name: checking-simplicity
description: 'Use when the user asks to simplify, right-size, identify overengineering, compare with a stated smaller alternative, choose the smallest viable approach, or test whether reuse removes the need for change on a named architecture, design, area, plan, technical choice, or code-level approach. General architecture comparison or product brainstorming without that simplification intent stays with planning. Without that request, use only when an approach, plan, or immediate build decision adds durable machinery without tying it to the user''s stated need and is about to enter implementation planning, execution, or continued building. Completion of a brief or plan alone is not a trigger. Direct behavior-preserving cleanup of settled code stays with implementation. An unchanged subject with a clean result continues without another check.'
license: MIT
compatibility: Requires a named area, question, or reviewable subject, enough accessible evidence to identify the current need and protected boundaries, and a harness that can dispatch a subagent.
---
# Checking Simplicity

Find opportunities to safely simplify a system design, architecture, technical
area, plan, question, or code-level approach against the current need. This is
a read-only assessment, not a planning, editing, or approval workflow.

Dispatch one subagent to run the assessment rather than assessing in the
current context. Tell it that it is the dispatched reviewer and give it the
subject in full and the available decision frame. If you were dispatched as
that reviewer, perform the assessment here and do not dispatch another
reviewer. Use the current model unless the caller names a different one. The
reviewer must not have authored or implemented the subject. Do not add extra
review process for this skill. Do not create tracking files, extra reviewers,
or a separate workspace used only to prove the review. If a caller wants a
stronger evidence trail or a repeated-review rule, that caller owns it. A
reviewer may assess a revision it previously reviewed as long as it did not
author or implement the revision.

## Review boundary

Build the decision frame from the best available evidence:

- the user's stated goal and desired outcome;
- explicit requirements, hard constraints, and verification criteria when
  present;
- behavior and boundaries that must be preserved, including authorization,
  security, privacy, accessibility, compatibility, bounded resource use, and
  operability; and
- actual consumers and observed use.

Formal requirements are useful but not required.

Review the subject named in the request. That can be an area or question, a
proposed or existing architecture, design, or technical choice, a planning
or in-build decision, or code and its relevant surrounding implementation.
If the request already includes the decision frame and the complexity-bearing
decisions, start from that material. If it points to a repository area,
inspect the relevant current implementation. Do not require a separate
document, path, or replay. Use the requirements and constraints the user
stated as required. Do not recommend dropping or weakening those. Treat
unverified additions as proposals and ask when they conflict with that
required set. When the subject includes implementation, read the relevant
current code and uncommitted work. Do not assess from a description, a
summary, or one convenient diff.

## Necessity test

Compare viable approaches and ask whether each boundary, responsibility, data
path, and operating surface serves a current consumer or protected constraint.
When a documentation or search tool is available, check current official docs
for platforms and libraries already named in the subject so a smaller native
capability is not missed or invented from memory. Current best-practice
articles may inform a smaller approach. They do not justify a new stack or
extra machinery unless a current consumer or protected constraint requires it.
Before accounting for individual concepts, summarize the current shape and the
smallest viable shape as whole systems.

Separate the needed outcome from the mechanisms proposed to reach it. Then
climb this ladder and stop at the first rung that completely satisfies the
current need:

1. Remove the need for a change.
2. Reuse the codebase's existing mechanism.
3. Use the native platform, standard library, or an installed dependency.
4. Add the smallest clear implementation that works.

Inspect each extra part of the proposed or existing subject, including product
code and process machinery. Keep it only when the evidence shows a current
need or a protected correctness, safety, security, privacy, or operating
boundary that requires it. Do not keep it for a hypothetical future caller.
Do not keep a variation nobody has asked for. Cover every part; group related
ones when that makes the comparison clearer.

Start with what can be removed. Prefer removal or reuse over renaming the
same machinery. Recommend a smaller working slice, not a backlog of deferred
follow-ups. Judge simplicity by the ladder, not by line count, file count, or
a numeric complexity budget. Reuse or a single source of truth can add lines
and still be simpler. Do not claim an existing mechanism unless the evidence
identifies it.

## Return the assessment

Lead with the recommendation when the evidence already supports one. If a
user decision is the only blocker, lead with that question. If some
reductions are safe under every remaining answer, lead with those
reductions, then ask. Do not present a dependent shape as settled.

If a user decision or missing evidence would change the recommendation, apply
the reductions the evidence already allows, then ask the smallest batch of
independent questions that would change the remaining recommendation. If two
behaviors both fit the evidence but need different machinery, ask which is
required. If the result cannot be assessed, name what appears missing and ask
for the evidence that would let the assessment continue. Include the existing
mechanism being compared when that is the gap. Defer questions that depend on
those answers. Keep any dependent recommendation conditional. Do not invent
certainty. Asking is not settling. Ask the question even when the user has
said the decision stays open.

For each question, including a yes or no question, give four options and
mark one as recommended. For a decision, recommend the smallest safe option
the evidence supports. For missing evidence, recommend the smallest set of
evidence that would settle the question.

Keep the readout compact and concrete. A clean result is the recommendation,
one affirmative reason when useful, and what must remain. It has no reasons
list, shapes, tests section, or next action. Do not invent a concern.

When simplification is needed, give the smallest safe alternative, at most
three grouped reasons with each reason's essential evidence in the same
sentence, one sentence on protected behavior and the observable tests that
prove it, and the next action. Name reuse in the recommendation or reasons.
Each removal reason must connect the proposed machinery or scope to the
current need it does not serve. For a system design or architecture, name
the current and smaller whole-system shapes and their decision-driving
contrast before the reasons.

Write in plain language that reads well as unrendered text. Use a short
list when it makes the readout easier to scan. Use a colon for a label and
its description. Do not use em dashes. Do not narrate the process: do not
mention the ladder, a rung, this skill, whether a decision was needed, or
your reasons for producing or omitting a comparison page. When you produce
one, give its path and nothing more.

When the two shapes differ in structure and not only in part count, produce
an HTML page of them in a temporary folder outside the repository so it is
not added to git, and return its path with the assessment. Use an installed
explainer if one is present. Otherwise write the page yourself.

A materially changed need, protected boundary, consumer, observed use, or
complexity decision warrants a new review.

Do not print a tracking header, a replay of the subject, a reviewer roster, a
commit hash, or an internal status code. Offer detailed evidence only if the
caller asks. Return the assessment without revising the subject, editing
repository files, committing, or approving shipping.

## Boundaries

- Use code review for bugs, regressions, tests, and standards.
- Use document review when the job is plan completeness or writing quality
  rather than unnecessary implementation complexity.
- Use PR and merge readiness for shipping decisions. They may consume this
  assessment and add their own evidence requirements, but this skill never
  makes those decisions.
