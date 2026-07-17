---
title: "Cross-harness dogfood runs are the cheapest honest test of a skill's degradation paths"
date: 2026-07-16
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: medium
applies_when:
  - "Shipping any agent skill that claims multi-harness portability"
  - "Before marking a degradation path done in a skill's verification plan"
  - "When a skill's authoring environment differs from its users' environments"
symptoms:
  - "Scripted tests only exercise the degradation paths the skill author already anticipated"
  - "Author-only runs never surface destination ambiguities because the author's own environment answers them implicitly"
tags: [cross-harness, dogfood-testing, agent-skills, portability, degradation-paths, fresh-context, validator-fallback]
related_components:
  - development_workflow
  - documentation
---

# Cross-harness dogfood runs are the cheapest honest test of a skill's degradation paths

## Context

While shipping the `creating-portable-skills` skill (PR jrgilbertson/the-rookery#4, open but not merged as of this writing), the acceptance plan required running the skill end-to-end in three harnesses: Codex CLI, Grok CLI, and a Claude Code visitor session in a clean repo. The recorded evidence lives in `tests/creating-portable-skills/results.md` (Run log section).

The pattern that emerged: scripted or self-run tests exercise the failure modes the author anticipated. Real runs in differently-constrained harnesses exercise the ones the author didn't, because each harness's constraints — sandbox policies, missing tools, bare environments — fire the skill's degradation paths organically, without anyone having to fake the failure.

## Guidance

Before shipping a skill that claims portability:

1. Run the skill end-to-end from a clean install in each harness the portability claim names. Not a review of the text against each harness's docs — an actual run.
2. Use a bare repo the author didn't configure. The author's own environment answers questions implicitly (where files go, what "install" means, which companions exist); a clean repo forces the skill text to answer them.
3. Treat each harness's constraint differences as free test fixtures. A network-denied sandbox tests the validator-unavailable fallback. A missing user-level home tests install-destination logic. A fresh-context baseline tests the skill's own comparison discipline. None of these need to be scripted — they fire on their own.
4. Record what each run exercised in the evidence file, per run, so the coverage each harness bought is auditable later.

Fixes surfaced this way tend to be cheap: every destination ambiguity the clean-repo visitor run exposed became a one-clause edit to the skill text.

## Why This Matters

Degradation paths are the hardest part of a skill to test honestly. If the author scripts the failure (mocks the network error, deletes the tool), the test only confirms the path the author already imagined. A differently-constrained harness produces the failure for real, and produces failures the author never imagined at all. The cost is one dogfood run per harness; the alternative — shipping and letting the first real visitor hit the ambiguity — is strictly worse and lands on someone else.

## When to Apply

- A skill's description or docs claim it works across harnesses or models.
- A skill has explicit fallback or degradation instructions (validator unavailable, tool missing, network denied) that have only ever been tested by the author simulating the failure.
- A skill was authored and tested entirely inside the author's own configured environment.
- An adversarial reviewer demands proof that a fallback path actually fires.

## Examples

All three from the Run log in `tests/creating-portable-skills/results.md`:

1. **Codex CLI, network-denied sandbox.** `npx skills-ref` failed with `ENOTFOUND` mid-run. The executing agent followed the skill's manual-fallback checks and declared the validator skipped — exactly the degradation path an adversarial reviewer had demanded, verified in the wild with no one scripting the network failure.
2. **Claude Code visitor run, clean repo.** Surfaced three destination ambiguities the author's own runs never hit: where the new skill directory goes, where filled test templates go, and what "install" means when the user-level home is unreachable. The author's environment had answered all three implicitly. Each became a one-clause fix, applied and re-validated same-day.
3. **Grok CLI run.** A real double-bucketing defect in the skill it produced was surfaced by its fresh-context baseline and resolved in the subtract pass — a bug the author's own context would have carried right past.

## Related

- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` — same shipping evidence, different lesson: the skills CLI's `@ref` targeting clones but does not check out the requested ref, so remote install probes must run against the default branch post-merge.
