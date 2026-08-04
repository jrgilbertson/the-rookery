---
title: Allow honest nulls in mandatory analytical fields
date: 2026-08-02
last_updated: 2026-08-02
category: design-patterns
module: storm-research
problem_type: design_pattern
component: assistant
severity: medium
applies_when:
  - An agent schema requires a unique insight, contribution, connection, or similar analytical field
  - A labeled output slot can be filled by paraphrasing findings or inventing unsupported structure
  - Optional analytical concepts are useful only when the shared evidence record supports them
  - A prompt revision needs behavioral proof that an honest null remains available
related_components:
  - testing_framework
  - documentation
tags:
  - agent-skills
  - prompt-schema
  - evidence-gating
  - null-output
  - materiality-threshold
  - systems-thinking
  - causal-inference
  - binary-tests
---

# Allow honest nulls in mandatory analytical fields

## Context

Research executors often return findings followed by a field such as `Unique
insight`. When that field requires a positive answer, the schema turns novelty
into a completion obligation even when the evidence supports no distinct
contribution. The Storm Research regression case records this failure mode: the
prior charter required `Unique insight` when the permitted facts could support
only the findings already returned
(`tests/storm-research/cases/lens-contribution-can-be-null.md:3-15`).

The case deliberately removes legitimate room for novelty. It asks whether a
filename-only dataset rename changes the available scientific conclusions while
holding the URL redirect, schema, contents, update schedule, and API constant.
Effects outside those facts may not be inferred. In that setting, a required
novelty statement measures willingness to fill a slot, not research quality.

The same pressure appears inside qualitative analysis. A section that names
feedback, delays, nonlinearities, path dependence, emergence, stocks, flows,
spillovers, and higher-order effects can look like a checklist. An early
systems-thinking revision permitted unsupported dynamics as low-confidence
hypotheses; review found that the label exposed speculation without supplying
the missing causal evidence (session history).

## Guidance

Make the contribution field explicitly nullable and define the null exactly.
The current charter uses `Lens-specific contribution` and requires the literal
`none beyond the findings` unless a proposed contribution is all three of:

- evidence-backed;
- absent from **Findings**; and
- capable of changing the answer, confidence, or next action.

Those conditions are the charter's operative contract under **Return →
Lens-specific contribution**
(`skills/storm-research/references/lens-charter.md`). The third uses the same
materiality definition as the executor's research questions and the main
workflow (`skills/storm-research/references/lens-charter.md` **Research** step 1;
`skills/storm-research/SKILL.md` opening “Material means…”).

Do not allow an executor to paraphrase, combine, rename, or reframe existing
findings merely to populate the field. A neutral label alone is insufficient:
an intermediate revision changed the heading but still restated a finding as a
contribution (session history). The anti-paraphrase rule and exact null made the
behavior observable.

Keep the field in the ordered return schema. An explicit null communicates that
the executor completed the judgment; omission is ambiguous. Carry the rule into
the orchestrator's completion check so downstream synthesis cannot reintroduce
the novelty that an executor correctly declined to manufacture
(`skills/storm-research/SKILL.md` **Completion check** — lens-specific
contribution must be evidence-backed or `none beyond the findings`).

Test the null branch with evidence designed to make novelty incorrect. The case
should fail a response that merely renames a finding and should retain the rest
of the output contract: questions, sources, findings, unresolved items, bias,
and confidence
(`tests/storm-research/cases/lens-contribution-can-be-null.md:17-27`).

Apply the same pattern to optional analytical concepts:

- Treat each concept as evidence-triggered, not required. For systems thinking,
  feedback, delays, nonlinearities, path dependence, and emergence appear only
  when the shared analytical record supports the mechanism and its materiality
  (`skills/storm-research/references/analysis-methods.md` **System context**).
- Trace causal effects link by link. A supported start and endpoint do not
  verify an unsupported intermediate link, although a bounded inference may be
  labeled with calibrated confidence
  (`skills/storm-research/references/analysis-methods.md` **Foundations** and
  **System context**).
- Discuss accumulation, depletion, capacity, or rate limits only when supported.
  Name what accumulates and the evidenced inflows or outflows; do not invent a
  dynamic to fill a checklist
  (`skills/storm-research/references/analysis-methods.md` **System context**).
- Keep causal-loop diagrams, stock-and-flow models, equations, simulations, and
  other formal models as separate, user-requested deliverables
  (`skills/storm-research/references/analysis-methods.md` formal-models paragraph).
- When no material dynamic or higher-order effect is supported, omit it unless
  the null itself changes the answer; then state the limit next to the claim or
  in the Overview
  (`skills/storm-research/references/analysis-methods.md` **Presentation and
  degradation**; honest-no-material-effect case).

Do not treat `Low confidence` as an evidence gate. Confidence calibrates a claim
that has a grounded chain; it does not legitimize inventing the chain itself.

## Why This Matters

A duplicate summary can acquire the rhetorical status of a new insight even
though the evidence has not changed. That distortion then compounds: the
synthesizer may overweight it, call it cross-lens agreement, or present it as a
non-obvious connection.

Unsupported analytical structure compounds similarly. A plausible loop or
stock-and-flow story can make a qualitative briefing look more rigorous while
quietly changing observations into causal claims. Using formal system-dynamics
vocabulary without the required structure also blurs the boundary between
systems thinking and a separately requested model.

An explicit null preserves the evidence boundary without weakening the
research. The executor still asks material questions, retrieves permitted
sources, answers from evidence, names unresolved issues and bias, and calibrates
confidence (`skills/storm-research/references/lens-charter.md` **Research** and
**Return**). The null applies only to the extra contribution slot.

The matched evidence is discriminating. With the same Academic lens and
four-part seed, the prior charter scored 3/5 after manufacturing a renamed
summary under `Unique insight`; the revised charter scored 5/5 after returning
exact `none beyond the findings` (`tests/storm-research/log.md:32`). A separate
exact-final run read the byte-identical charter and no other file, returned the
same null, and received an independent 5/5 grade
(`tests/storm-research/log.md:35`).

The repository retains those bounded outcomes in the run log, not the private
raw transcripts. Do not describe temporary evaluation artifacts as tracked
evidence (`tests/storm-research/log.md:5`).

The systems-thinking regression case makes the broader rule executable. It
requires an honest null for every unsupported feedback, delay, nonlinearity,
path-dependence, emergence, stock-or-flow detail, spillover, or higher-order
relationship, while separately checking that supported accumulation or rate
limits do not require a formal model
(`tests/storm-research/cases/systems-thinking-scope.md:30-37`). Enumerating the
optional concepts matters: a catch-all such as “and related effects” cannot
prove that each unsupported slot remains nullable.

## When to Apply

Use this pattern when:

- a structured executor or reviewer asks for a unique insight, hidden
  connection, novel contribution, or similar delta after substantive findings;
- the evidence may legitimately add no separate conclusion;
- downstream synthesis could mistake a renamed finding for independent support;
- a qualitative analysis names optional mechanisms that the evidence may not
  establish;
- an uncertainty label is being used to justify otherwise unsupported causal
  structure; or
- the schema needs a mechanically observable distinction between material
  contribution and no contribution.

Do not use the null as permission to skip research. Return a positive
contribution when it passes the evidence, distinctness, and materiality gates.
Otherwise, return the exact null.

## Examples

Before, the schema forces a superficially distinct statement:

```text
Findings — The filename changed, but the URL behavior, schema, contents,
schedule, and API did not; no change in scientific conclusions is supported.

Unique insight — The rename is administrative rather than scientific.
```

The second line only reframes the finding.

After, the schema permits the honest result:

```text
Findings — The filename changed, but the URL behavior, schema, contents,
schedule, and API did not; no change in scientific conclusions is supported.

Lens-specific contribution — none beyond the findings
```

This version reports exactly what the evidence establishes and nothing more.

For analytical concepts, avoid filling a taxonomy with softened speculation:

```text
The growing onboarding backlog may form a low-confidence reinforcing loop:
slower onboarding could raise support demand, further slowing onboarding.
```

If the record establishes backlog growth and flat staffing but not support
demand or a return path, report the boundary instead:

```text
The backlog grew while staffing remained flat, which supports describing
accumulation and a possible capacity constraint. The record does not establish
the inflows or outflows, a feedback return path, or additional delayed and
higher-order effects. Those dynamics remain unclaimed pending evidence about
onboarding completion rates, support demand, and customer behavior over time.
```

## Related

- [Operationalize abstract qualifiers in instruction review](../best-practices/operationalize-abstract-qualifiers-in-instruction-review.md) defines observable thresholds for vague agent-facing language. This pattern extends that guidance to a required schema field whose valid result may be null.
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md) describes the isolation needed to verify semantic instruction changes without allowing author context to leak into grading.
- [Falsifiability contracts need executable tests](../workflow-issues/falsifiability-contracts-need-executable-tests.md) explains why distinct semantic states need distinct, adversarially tested outcomes.
