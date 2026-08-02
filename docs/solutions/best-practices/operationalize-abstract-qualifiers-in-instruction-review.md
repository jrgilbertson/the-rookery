---
title: "Define the abstract qualifiers that the delete test misses"
category: best-practices
module: skill-instruction-review
date: 2026-07-16
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Authoring or reviewing instruction prose for agents (skills, prompts, agent docs) that claims cross-model portability"
  - "Instructions lean on abstract qualifiers such as \"thorough\", \"clean\", \"punchier\", or \"borderline\""
  - "Running a delete-test pass on skill or prompt wording during review"
symptoms:
  - "A qualifier passes the delete test (removing it changes behavior) yet remains undefined, so each model interprets it differently"
  - "A gate probe caught the word \"borderline\" undefined in the authoring workflow's then-current step 8, despite passing the standard delete test"
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

## Guidance

Run the operationalize-the-qualifier check as its own named pass, separate from the delete test:

1. Sweep the instructions for every abstract adjective or adverb the text leans on for behavior (thorough, clean, fast, bold, punchy, borderline, appropriate, reasonable).
2. Apply the litmus to each: what would two different models do with this word? If their behaviors could plausibly diverge, the qualifier is undefined.
3. Fix each undefined qualifier with one of three shapes, or add it to the fix list:
   - **Concrete behavior.** Replace or back the adjective with the action it stands for ("punchier" becomes "cut every sentence over 20 words; lead each paragraph with its claim").
   - **Checkable criterion.** State a condition the agent can verify ("thorough" becomes "every public function has at least one test exercising a failure path").
   - **Enumerated options.** Constrain the judgment to a closed set ("borderline" becomes "require a plain yes, no, or unsure; unsure or hedged counts as borderline").

The checklist item that encodes this lives under Instruction economy in `skills/creating-portable-skills/references/review-checklist.md`:

> Qualifiers are operationalized. Pass: abstract words such as thorough, clean, fast, bold, reliable, compatible, and improved map to concrete behavior or an observable check.

The fix-list clause moved to that checklist's preamble, which routes any failed item into the fix list.

Keep running the delete test too. The two checks catch disjoint failures: the delete test removes lines that steer nothing, the qualifier check defines words that steer unpredictably.

## Why This Matters

An undefined qualifier costs tokens and changes behavior, but each model may
interpret it differently. The authoring model can appear tuned while another
model follows a different meaning. For portable skills, that is a correctness
problem.

Reviewers may defend the qualifier because removing it changes output. That
still leaves the change unspecified. A separate named check catches the gap.
This rule came from Paul Bakaus's skill-engineering findings and was tested
against this repository before adoption.

## When to Apply

- Reviewing or auditing any agent instructions: skills, prompts, CLAUDE.md files, subagent task briefs.
- Running the Instruction economy group of the skill-review checklist (step 0 audit or step 6, Decide and review, in `skills/creating-portable-skills/SKILL.md`).
- Writing new instructions that reach for an adjective to describe output quality. Define it at write time rather than deferring to review.
- Gate-probing a revised skill, where the check applies to the skill's own text, not just the skills it reviews (see the borderline example below, caught exactly this way).

## Examples

### The punchier/thorough/clean probe (checklist gap, then fix)

A probe ran the checklist's Instruction economy group against a toy instruction line:

> "Review the draft and make it punchier. Be thorough and keep the tone clean."

**Before (prior checklist group only).** The delete test, evidence tracing, positive steering, specificity matching, and one-home checks let "punchier," "thorough," and "clean" pass. At most, "be thorough" got cut (deleted, not defined) by strict evidence tracing. The probe explicitly confirmed the delete test alone cannot catch them: it asks cut-or-keep, not define.

**After (with the qualifiers item).** All three words were flagged for definition and became fix-list entries. Summary recorded in `tests/creating-portable-skills/log.md`; the per-item breakdown is in git history at `cc66ee8`, which retired the evidence-ledger files this originally cited.

### The borderline fix (the check catching its own host skill)

Same day, a gate probe applied this lens to the adopting skill's then-current step 8 and caught "borderline" undefined. A 50/50 trigger judgment could pass by luck, with nothing forcing a re-sample.

**Before.** The then-current step 8 draft told the reviewer to re-judge "on a miss or a borderline call" without defining borderline (an in-session draft state; the definition and the surrounding protocol shipped together in one commit, so git history holds only the After text), and accepted free-form activation judgments.

**After.** The listing-judgment protocol now lives in `skills/creating-portable-skills/assets/trigger-queries-template.md`; it constrains the judgment to enumerated options and defines the qualifier by criterion:

> "Show it only the skill name, description, and one query; require a plain yes or no." and "A first judgment that is `unsure` or hedged is borderline: run that query twice more."

The enumerated set has since narrowed from {yes, no, unsure} to {yes, no}, with `unsure` handled as the trigger for re-sampling rather than as a third option (the same fix shape, tightened). `tests/README.md` (Running → Trigger suite) now carries this as the in-repo canonical statement alongside the template. Summary recorded in `tests/creating-portable-skills/log.md`; the per-item breakdown is in git history at `cc66ee8`.

## Related

- `docs/solutions/best-practices/independent-fresh-context-review-for-agent-skills.md`
  documents the fresh-context probes and prior-versus-revised comparisons that
  caught both examples above, and why a judgment from the context that wrote
  the prose is not evidence.
