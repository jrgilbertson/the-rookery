---
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

# Operationalize the Qualifier: The Delete Test's Blind Spot for Abstract Adjectives

## Context

The delete test is the standard instruction-economy check when reviewing agent instructions: for each line, would the agent get this wrong without it? Lines that restate default model behavior get cut. This repo's skill-review checklist (`skills/creating-portable-skills/references/review-checklist.md`) uses it as the first item under Instruction economy.

This session surfaced a blind spot. Abstract qualifiers like "thorough," "punchier," or "clean" survive the delete test, because removing them genuinely changes behavior, so cut-or-keep reasoning keeps them. But the kept word remains undefined, and each model backfills its own meaning. That is precisely the cross-model unpredictability that instruction review exists to prevent. The delete test asks cut-or-keep. It never asks define.

The fix, adopted into the checklist during the skill-engineering adoption pass (PR jrgilbertson/the-rookery#4, open but not merged as of this writing), is a distinct check that runs alongside the delete test rather than replacing it.

## Guidance

Run the operationalize-the-qualifier check as its own named pass, separate from the delete test:

1. Sweep the instructions for every abstract adjective or adverb the text leans on for behavior (thorough, clean, fast, bold, punchy, borderline, appropriate, reasonable).
2. Apply the litmus to each: what would two different models do with this word? If their behaviors could plausibly diverge, the qualifier is undefined.
3. Fix each undefined qualifier with one of three shapes, or add it to the fix list:
   - **Concrete behavior.** Replace or back the adjective with the action it stands for ("punchier" becomes "cut every sentence over 20 words; lead each paragraph with its claim").
   - **Checkable criterion.** State a condition the agent can verify ("thorough" becomes "every public function has at least one test exercising a failure path").
   - **Enumerated options.** Constrain the judgment to a closed set ("borderline" becomes "require a plain yes, no, or unsure; unsure or hedged counts as borderline").

The checklist item that encodes this lives under Instruction economy in `skills/creating-portable-skills/references/review-checklist.md`:

> Qualifiers are operationalized. Pass: every abstract adjective the skill leans on (thorough, clean, fast, bold) is backed by concrete behavior or a checkable criterion; an undefined qualifier becomes a fix-list entry.

Keep running the delete test too. The two checks catch disjoint failures: the delete test removes lines that steer nothing, the qualifier check defines words that steer unpredictably.

## Why This Matters

An undefined qualifier is the worst of both worlds. It costs tokens and passes review because it demonstrably changes behavior, yet the behavior it produces varies by model. On the authoring model it may look tuned; on a weaker or different model it silently means something else. For portable skills, which are explicitly tuned for the floor model they claim, this is a correctness issue, not a style issue.

The blind spot is self-reinforcing. Reviewers trained on the delete test will defend the qualifier ("removing it changes output, so it earns its place") without noticing that what it changes is unspecified. A separate named check breaks that reasoning loop. As the origin source puts it, an adjective with nothing behind it is just a nice apostrophe (Paul Bakaus's skill-engineering findings, evaluated against this repo and adopted).

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

**After (with the qualifiers item).** All three words were flagged for definition and became fix-list entries. Summary recorded in `tests/creating-portable-skills/results.md`; the per-item breakdown below is from the session's probe record, "Skill-engineering adoption pass" entry.

### The borderline fix (the check catching its own host skill)

Same day, a gate probe applied this lens to the adopting skill's then-current step 8 and caught "borderline" undefined. A 50/50 trigger judgment could pass by luck, with nothing forcing a re-sample.

**Before.** The then-current step 8 draft told the reviewer to re-judge "on a miss or a borderline call" without defining borderline (an in-session draft state; the definition and the surrounding protocol shipped together in one commit, so git history holds only the After text), and accepted free-form activation judgments.

**After.** The listing-judgment protocol now lives in `skills/creating-portable-skills/assets/trigger-queries-template.md`; it constrains the judgment to enumerated options and defines the qualifier by criterion:

> "...ask whether it would activate, requiring a plain yes, no, or unsure" and "An unsure or hedged judgment counts as borderline."

Summary recorded in `tests/creating-portable-skills/results.md`; the per-item breakdown below is from the session's probe record, "Owner review pass" entry. This example shows the enumerated-options fix shape and demonstrates that the check catches failures the delete test had already blessed.

## Related

- `docs/solutions/best-practices/cross-harness-dogfood-testing.md` — probing techniques (fresh-context gate probes, prior-vs-revised comparisons) from the same shipping effort; those probes are how both examples above were caught and verified.
