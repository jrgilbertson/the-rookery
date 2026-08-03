---
title: Allow honest nulls in mandatory novelty fields
date: 2026-08-02
category: design-patterns
module: storm-research
problem_type: design_pattern
component: assistant
severity: medium
applies_when:
  - An agent schema requires a unique insight, contribution, connection, or similar novelty field
  - A labeled output slot can be filled by paraphrasing findings instead of adding a material conclusion
  - A prompt revision needs behavioral proof that an honest null remains available
related_components:
  - testing_framework
  - documentation
tags:
  - agent-skills
  - prompt-schema
  - forced-novelty
  - null-output
  - materiality-threshold
  - anti-paraphrase
  - matched-comparison
---

# Allow honest nulls in mandatory novelty fields

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

## Guidance

Make the contribution field explicitly nullable and define the null exactly.
The current charter uses `Lens-specific contribution` and requires the literal
`none beyond the findings` unless a proposed contribution is all three of:

- evidence-backed;
- absent from **Findings**; and
- capable of changing the answer, confidence, or next action.

Those conditions are the charter's operative contract
(`skills/storm-research/references/lens-charter.md:62-65`). The third uses the
same materiality definition as the executor's research questions and the main
workflow (`skills/storm-research/references/lens-charter.md:32-34`,
`skills/storm-research/SKILL.md:12`).

Do not allow an executor to paraphrase, combine, rename, or reframe existing
findings merely to populate the field. A neutral label alone is insufficient:
an intermediate revision changed the heading but still restated a finding as a
contribution (session history). The anti-paraphrase rule and exact null made the
behavior observable.

Keep the field in the ordered return schema. An explicit null communicates that
the executor completed the judgment; omission is ambiguous. Carry the rule into
the orchestrator's completion check so downstream synthesis cannot reintroduce
the novelty that an executor correctly declined to manufacture
(`skills/storm-research/SKILL.md:224-225`).

Test the null branch with evidence designed to make novelty incorrect. The case
should fail a response that merely renames a finding and should retain the rest
of the output contract: questions, sources, findings, unresolved items, bias,
and confidence
(`tests/storm-research/cases/lens-contribution-can-be-null.md:17-27`).

## Why This Matters

A duplicate summary can acquire the rhetorical status of a new insight even
though the evidence has not changed. That distortion then compounds: the
synthesizer may overweight it, call it cross-lens agreement, or present it as a
non-obvious connection.

An explicit null preserves the evidence boundary without weakening the
research. The executor still asks material questions, retrieves permitted
sources, answers from evidence, names unresolved issues and bias, and calibrates
confidence (`skills/storm-research/references/lens-charter.md:30-52`). The null
applies only to the extra contribution slot.

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

## When to Apply

Use this pattern when:

- a structured executor or reviewer asks for a unique insight, hidden
  connection, novel contribution, or similar delta after substantive findings;
- the evidence may legitimately add no separate conclusion;
- downstream synthesis could mistake a renamed finding for independent support;
  or
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

## Related

- [Operationalize abstract qualifiers in instruction review](../best-practices/operationalize-abstract-qualifiers-in-instruction-review.md) defines observable thresholds for vague agent-facing language. This pattern extends that guidance to a required schema field whose valid result may be null.
- [Falsifiability contracts need executable tests](../workflow-issues/falsifiability-contracts-need-executable-tests.md) explains why distinct semantic states need distinct, adversarially tested outcomes.
