---
title: "Pin protected boundaries, not incidental wording, in prose skills"
date: 2026-10-09
category: workflow-issues
module: "skills/checking-merge-readiness, skills/checking-pr-readiness"
problem_type: workflow_issue
component: testing_framework
severity: high
applies_when:
  - "Rewriting or condensing a paragraph in a prose skill that carries an approval, merge, or independence guard"
  - "Writing fixtures for a skill whose behavior lives in SKILL.md text rather than code"
  - "A skill's test suite holds many exact-sentence assertions but no assertion names the guard a reviewer would care about"
symptoms:
  - "A skill quietly stops doing a protected step while every fixture stays green"
  - "The agent follows a surviving fallback branch because the instruction that led to the main branch is gone"
root_cause: missing_validation
tags: [prose-skills, regression-guard, boundary-pins, fixtures, rewrites, falsification]
related_components:
  - development_workflow
---

# Pin protected boundaries, not incidental wording, in prose skills

## Context

`checking-merge-readiness`, run from the session that wrote a pull request,
graded the change itself, capped the result at debug, and asked the owner to
request the independent review. #193 had rewritten the skill's Review
independence paragraph to add grade-reuse rules. The rewrite deleted the
sentence "Otherwise dispatch this skill to a fresh, read-only context…" and
kept only the fallback, "if no fresh context is available, cap at debug."
With no instruction to open a fresh context, the agent read "available" as
"already exists" and took the fallback every time.

The fixtures did not catch it. About 90 exact-sentence assertions pinned
intent-baseline cases, identity wording, and finishing-path phrasing across
`tests/checking-merge-readiness/fixtures/run-fetch-checks.sh` and a Python
assessment runner that #201 later removed. None pinned the dispatch. The suite
had volume, and the one behavior an owner would notice had no guard.

## Guidance

1. **List the protected boundaries before writing fixtures.** For a gate skill
   they are the few rules whose loss changes who decides or what ships: who
   may grade, that the menu turn never picks, that a withheld option is not
   approval, that untrusted text never authorizes, that nothing durable stores
   a grade, and that the one write is guarded.
2. **Pin each boundary once, with the sentence that carries it.** Section J of
   `tests/checking-merge-readiness/fixtures/run-fetch-checks.sh:405` holds one
   assertion per boundary, starting with the dispatch sentence at
   `skills/checking-merge-readiness/SKILL.md:49`. A pin on incidental wording
   only makes rewrites noisy; a pin on a boundary makes a dropped guard fail.
3. **Prove each pin fails without its guard.** Run the pin against the old text
   or a deliberate break before trusting it. The dispatch pin matched 0 times
   in the skill text at the head of `main` before #201 and passes after it.
4. **When the skill ships an executable command, run the shipped text.** The
   surface-identity fixture at
   `tests/checking-pr-readiness/fixtures/run-helper-checks.sh:319` extracts the
   `sh` block from `skills/checking-pr-readiness/SKILL.md` and runs it against
   scratch repositories. A copy of the command in the test would pass while the
   skill drifted. Against the earlier `read-tree HEAD` version, three of its
   cases fail.
5. **After rewriting a guarded paragraph, get a fresh reviewer to try to break
   it.** A fresh-context reviewer of the #201 rewrite found no outright break
   but seven ambiguities, including a building session that could relay its
   own "1" to the reviewer it dispatched.

## Why This Matters

Prose skills fail by omission. Code that loses a branch usually breaks
something loudly; a skill that loses a sentence keeps running and takes
whatever path is left. A fallback written for a rare case becomes the
everyday behavior. Sentence pins on incidental wording make this worse,
because they turn every edit into fixture churn, so authors learn to update
pins in bulk and stop reading what each one protected.

## When to Apply

- Before condensing or restructuring any gate, approval, or merge skill.
- When a fixture suite for a prose skill grows past a handful of text pins.
- When a rewrite keeps a fallback ("if X is unavailable, then…") but changes
  the paragraph that told the agent how to reach the main path.

## Examples

Before, the pins guarded wording a rewrite could legitimately change:

```bash
has_text "baseline: the first matching case wins" "$WORK/skill.flat" \
  'Apply the first matching case. Do not also apply a later case.'
```

After, one pin per boundary, verified red against the old text:

```bash
has_text "independence: an involved session dispatches a fresh reviewer" "$WORK/skill.flat" \
  'If this context has that involvement, dispatch this skill to one fresh, read-only subagent before step 1, without asking.'
```

## Related

- [Verify disposition claims before landing a prune](verify-disposition-claims-before-landing-a-prune.md): the same silent loss during a restructure, caught by checking claims instead of pins.
- [Ship bundled skill helpers with an executable falsifiability contract](falsifiability-contracts-need-executable-tests.md): the executable-test rule for helper scripts.
- [Loosening a test checklist during grading removes the check](loosening-a-checklist-during-grading-removes-the-check.md): a check that stops discriminating.
- [Put the test seam in the environment, not in the shipped skill](../conventions/keep-the-test-seam-out-of-the-shipped-skill.md): test the shipped artifact, not a copy.
- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-skills.md): why the dropped dispatch mattered.
