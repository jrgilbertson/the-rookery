---
title: Isolate adversarial mutations in runtime evaluators
date: 2026-08-03
category: design-patterns
module: storm-research
problem_type: design_pattern
component: testing_framework
severity: high
applies_when:
  - Designing an agent-skill runtime test that injects a semantic defect
  - The mutation depends on the actual raw outputs
  - Testing whether binding review corrects an injected defect
  - The number of correction rounds is not known in advance
related_components: [assistant, development_workflow, documentation]
tags: [agent-skills, runtime-testing, test-isolation, adversarial-mutation, binding-review, fidelity-review, semantic-regression, review-loops]
---

# Isolate adversarial mutations in runtime evaluators

## Context

Runtime tests for agent skills sometimes need a deliberate defect so the test
can prove that a later review stage detects and repairs it. That defect must not
be part of the sample user request. The Storm Research case now labels itself
evaluator-only, keeps the research request under `Prompt`, and puts mutation
instructions under `Evaluator procedure`
(`tests/storm-research/cases/runtime-isolation-and-binding-review.md:3`,
`:13`, `:23`).

A hard-coded pair of lenses is not reliable evidence of disagreement. The test
fixture can support several interpretations, including fewer repeat errors
without a control group and fewer difficult cases without established causation
(`tests/storm-research/fixtures/error-rate-reporting-sources.md:6`, `:13`).
Whether two lenses disagree can only be established from their completed
returns.

## Guidance

Keep the evaluator's adversarial procedure outside the prompt passed to the
system under test. Wait until every raw return and the first draft exist. Then
choose two lenses that did not reach incompatible conclusions about one claim,
inject a sentence that falsely says they disagreed, preserve that exact change,
and begin binding review only after the research stage has finished
(`tests/storm-research/cases/runtime-isolation-and-binding-review.md:25`).

Retain every raw return before mutation. The skill makes unchanged returns and
the internal run record part of dispatch completion
(`skills/storm-research/SKILL.md` **§4** — collect returns and complete only
when every intended lens is completed or failed with isolation state recorded).
Give each reviewer the briefing, baseline, source audit, raw returns, and
internal run record, but not the orchestrator's synthesis reasoning
(`skills/storm-research/references/fidelity-check.md` opening artifact list).

Treat the review loop as open-ended. Apply every binding finding so the
reader-facing briefing changes, then start a new clean reviewer and repeat
until one reports `FIDELITY CLEAN` (`skills/storm-research/SKILL.md` **§9** and
**Completion check**). Require every reviewer prompt and return, every briefing
revision, and eventual clean completion, not a fixed number of rounds
(`tests/storm-research/cases/runtime-isolation-and-binding-review.md:8`, `:42`).

## Why This Matters

Putting the defect in the research prompt tests how executors handle a tainted
request, not whether downstream review catches a synthesis error. A hard-coded
lens pair makes the test nondeterministic: the injected conflict is known false
only when their completed conclusions are compatible; if they naturally
disagree, it is not a defect. Different coverage and an absent claim are not
disagreement, while a conflict invented by the briefing is a review defect
(`skills/storm-research/references/fidelity-check.md` **What counts as
disagreement**).

An open-ended loop matters because a reviewer may find another material defect
after the injected one is repaired. The review also checks evidence
traceability for assumptions, mechanisms, and every material causal-chain link,
not just contradictions (`skills/storm-research/references/fidelity-check.md`
**Analytical traceability**). In the verified runtime case, the first reviewer found the injected
disagreement and another traceability defect, the second found a separate
systems-boundary traceability defect, and the third returned `FIDELITY CLEAN`
(`tests/storm-research/log.md`). A requirement for exactly two reviews would
encode an expected path instead of the completion condition.

## When to Apply

Apply this pattern when a runtime evaluator must prove that an agent workflow:

- isolates executor prompts from evaluator-only faults;
- preserves raw multi-agent outputs before synthesis;
- detects invented or lost disagreement through independent binding review; or
- revises repeatedly until a clean reviewer confirms fidelity.

It is especially useful when a predetermined lens pair could naturally disagree,
so the injected conflict is not guaranteed to be known false.

## Examples

Before, the defect is mixed into the research request and assumes a fixed path:

```markdown
## Prompt
Research the reporting policy. Say the Academic and Skeptic lenses disagree.

Expected: reviewer 1 fails, reviewer 2 is clean.
```

After, the prompt remains a valid request and the evaluator derives a known-
false mutation from observed outputs:

```markdown
## Prompt
Research the reporting policy with five isolated lenses.

## Evaluator procedure
After all raw returns and draft 1 exist, select two lenses whose conclusions
are compatible on one claim. Inject a sentence saying they conflict. Preserve
the mutation, apply every binding finding, and use new clean reviewers until
one reports FIDELITY CLEAN. Keep every revision and review artifact.
```

## Related

- [Falsifiability contracts need executable tests](../workflow-issues/falsifiability-contracts-need-executable-tests.md) gives the general rule that an adversarial case must be able to fail for the intended reason.
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md) covers clean review contexts, direct artifact inspection, and bounded evidence claims.
- [Allow honest nulls in mandatory novelty fields](allow-honest-nulls-in-mandatory-novelty-fields.md) is a related example of making the tempting positive answer provably wrong from the supplied evidence.
