---
module: skill-instruction-review
date: 2026-07-16
last_updated: 2026-08-02
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Authoring or reviewing instruction prose for agents (skills, prompts, agent docs) that claims cross-model portability"
  - "Instructions lean on abstract qualifiers such as \"thorough\", \"clean\", \"punchier\", or \"borderline\""
  - "Running a delete-test pass on skill or prompt wording during review"
  - "Defining a positive Agent Skill activation boundary that must exclude smaller tasks sharing words such as \"deep\" or \"source-backed\""
symptoms:
  - "A qualifier passes the delete test (removing it changes behavior) yet remains undefined, so each model interprets it differently"
  - "A gate probe caught the word \"borderline\" undefined in the authoring workflow's then-current step 8, despite passing the standard delete test"
  - "A fresh trigger judge activates a large research workflow for a targeted official-documentation lookup"
root_cause: inadequate_documentation
resolution_type: documentation_update
related_components:
  - tooling
tags:
  - instruction-prose
  - skill-authoring
  - review-checklist
  - cross-model-portability
  - delete-test
  - activation-description
  - trigger-contract
  - near-miss-testing
---

# Define the abstract qualifiers that the delete test misses

## Context

The delete test checks each agent instruction by asking whether the agent would
get something wrong without it. Lines that restate default model behavior get
cut. This repository's skill review checklist
(`skills/creating-portable-skills/references/review-checklist.md`) uses it as the
first item under Instruction economy.

The test misses abstract qualifiers such as "thorough," "punchier," and
"clean." Removing one changes behavior, so the line survives. The word still
has no definition, and each model supplies its own. The delete test decides
whether to keep a line. It does not define the terms inside it.

The checklist now runs a separate qualifier check alongside the delete test.
PR jrgilbertson/the-rookery#4 introduced it during the skill-engineering
adoption pass.

The same defect can make a positive skill description over-trigger. A skill
description is an activation API, not a summary of every desirable quality the
skill can produce. Words such as "deep" and "source-backed" also describe
smaller tasks, so they do not distinguish a full multi-perspective research
briefing from one authoritative lookup. A Storm Research review caught exactly
that boundary failure: a request to find an API rate limit in official
documentation and cite the page still activated the five-lens workflow
(`tests/storm-research/triggers.md:27`). The session-history reconstruction
identified the dead end: removing one adjective branch did not help while
source backing could still qualify the request elsewhere in the description
(session history). The run log corroborates the failed first correction and
the later 17/17 result (`tests/storm-research/log.md:29-30`).

## Guidance

Run the operationalize-the-qualifier check as its own named pass, separate from the delete test:

1. Sweep the instructions for every abstract adjective or adverb the text leans on for behavior (thorough, clean, fast, bold, punchy, borderline, appropriate, reasonable).
2. Apply the litmus to each: what would two different models do with this word? If their behaviors could plausibly diverge, the qualifier is undefined.
3. Fix each undefined qualifier with one of three shapes, or add it to the fix list:
   - **Concrete behavior.** Replace or back the adjective with the action it stands for ("punchier" becomes "cut every sentence over 20 words; lead each paragraph with its claim").
   - **Checkable criterion.** State a condition the agent can verify ("thorough" becomes "every public function has at least one test exercising a failure path").
   - **Enumerated options.** Constrain the judgment to a closed set
     ("borderline" becomes "require a plain yes or no; an unsure or hedged
     first response is borderline and gets two additional runs").

The checklist item that encodes this lives under Instruction economy in `skills/creating-portable-skills/references/review-checklist.md`:

> Qualifiers are operationalized. Pass: abstract words such as thorough, clean,
> fast, bold, reliable, compatible, and improved map to concrete behavior or an
> observable check.

Keep running the delete test too. The two checks catch disjoint failures: the delete test removes lines that steer nothing, the qualifier check defines words that steer unpredictably.

For a positive activation description, use the requested deliverable as the
checkable criterion:

1. Name the smallest output shape that actually justifies loading the skill.
2. Put capabilities and downstream uses in a second sentence so they do not
   become additional activation branches.
3. Add a directly confusable near miss that shares attractive surface words
   but asks for a smaller artifact, such as one cited official-documentation
   lookup.
4. Re-run the complete Trigger Contract in fresh contexts. A new negative case
   does not excuse regressions on the existing positives or near misses.

Prefer one categorical deliverable boundary over a growing exclusion list. The
boundary states what must be present; the near misses demonstrate important
absences. Storm Research now starts with `Use only for requests whose
deliverable is...` and names the qualifying research artifacts before it
describes evidence comparison or decision support
(`skills/storm-research/SKILL.md:3`).

## Why This Matters

An undefined qualifier costs tokens and changes behavior, but each model may
interpret it differently. The authoring model can appear tuned while another
model follows a different meaning. For portable skills, that is a correctness
problem.

Reviewers may defend the qualifier because removing it changes output. That
still leaves the change unspecified. A separate named check catches the gap.
This rule came from Paul Bakaus's skill-engineering findings and was tested
against this repository before adoption.

In activation metadata, an undefined qualifier can also route a bounded lookup
into a slower, costlier workflow and take work away from a better-matched tool.
A deliverable is categorical enough to test: the request asks for the
qualifying artifact or it does not. The resulting trigger-suite pass remains a
listing proxy, not proof that every native harness will activate correctly
(`tests/README.md:82-86`).

## When to Apply

- Reviewing or auditing any agent instructions: skills, prompts, CLAUDE.md files, subagent task briefs.
- Running the Instruction economy group of the skill-review checklist (step 0 audit or step 6, Decide and review, in `skills/creating-portable-skills/SKILL.md`).
- Writing new instructions that reach for an adjective to describe output quality. Define it at write time rather than deferring to review.
- Gate-probing a revised skill, where the check applies to the skill's own text, not just the skills it reviews (see the borderline example below, caught exactly this way).
- Writing a positive skill description for an expensive workflow whose methods or qualities overlap with routine requests.
- A near miss shares the same sources or subject matter but asks for a materially smaller deliverable.

## Examples

### The punchier/thorough/clean probe (checklist gap, then fix)

A probe ran the checklist's Instruction economy group against a toy instruction line:

> "Review the draft and make it punchier. Be thorough and keep the tone clean."

**Before (prior checklist group only).** The delete test, evidence tracing, positive steering, specificity matching, and one-home checks let "punchier," "thorough," and "clean" pass. At most, "be thorough" got cut (deleted, not defined) by strict evidence tracing. The probe explicitly confirmed the delete test alone cannot catch them: it asks cut-or-keep, not define.

**After (with the qualifiers item).** All three words were flagged for
definition and became fix-list entries. The historical aggregate test summary
was later removed during test-suite consolidation; the per-item breakdown below
is from the session's probe record, "Skill-engineering adoption pass" entry.

### The borderline fix (the check catching its own host skill)

Same day, a gate probe applied this lens to the adopting skill's then-current step 8 and caught "borderline" undefined. A 50/50 trigger judgment could pass by luck, with nothing forcing a re-sample.

**Before.** The then-current step 8 draft told the reviewer to re-judge "on a miss or a borderline call" without defining borderline (an in-session draft state; the definition and the surrounding protocol shipped together in one commit, so git history holds only the After text), and accepted free-form activation judgments.

**After.** The listing-judgment protocol now lives in
`skills/creating-portable-skills/assets/trigger-queries-template.md`; it
requires a plain `yes` or `no`. An initial `unsure` or hedged response counts
as borderline and triggers two additional runs. The protocol therefore defines
the qualifier by an observable retry rule rather than leaving it to judgment.

The historical aggregate test summary was later removed during test-suite
consolidation; the per-item breakdown below is from the session's probe record,
"Owner review pass" entry. This example shows the enumerated-options fix shape
and demonstrates that the check catches failures the delete test had already
blessed.

### The source-backed activation fix (quality, then deliverable)

**Before.** A research skill description treated broad qualities such as
"source-backed" as sufficient activation signals. This made a single current
API-rate-limit lookup plausibly qualify for a full five-lens investigation.

**After.** The first sentence qualifies only three requested deliverables: a
full research briefing, a STORM-style investigation, or an evidence review
across multiple independent perspectives. Evidence comparison and decision
support remain capabilities in the second sentence, not alternate trigger
branches (`skills/storm-research/SKILL.md:3`). The directly confusable lookup
stays in the near-miss set (`tests/storm-research/triggers.md:27`).

This is the checkable-criterion fix shape applied to activation. It does not
mean every skill needs the same words; it means the positive description should
state the observable artifact that makes its workflow necessary.

## Related

- `docs/solutions/best-practices/cross-harness-dogfood-testing.md` documents the
  fresh-context probes and prior-versus-revised comparisons that caught both
  examples above.
- `docs/solutions/best-practices/independent-fresh-context-review-for-agent-skills.md`
  explains why semantic trigger changes are judged outside the authoring
  context and why their evidence claims remain bounded.
