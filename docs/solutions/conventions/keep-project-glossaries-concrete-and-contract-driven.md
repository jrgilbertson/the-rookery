---
title: "Keep project glossaries concrete and contract-driven"
date: 2026-08-17
last_updated: 2026-08-17
category: conventions
module: "CONCEPTS.md glossary"
problem_type: convention
component: documentation
severity: medium
applies_when:
  - "Adding or revising entries in a project glossary"
  - "A capitalized workflow phrase may be ordinary prose rather than a shared contract"
  - "A persisted schema name needs a human-readable explanation"
tags: [concepts-glossary, plain-language, vocabulary-governance, schema-compatibility, documentation]
---

# Keep project glossaries concrete and contract-driven

## Context

`CONCEPTS.md` had accumulated ordinary workflow steps, internal metaphors, and
capitalized prose alongside the smaller set of terms that carry shared
contracts. The result was harder to scan and encouraged dependent documents to
repeat project-specific labels instead of explaining the work plainly.

The glossary's [admission rule](../../../CONCEPTS.md#concepts) prefers an
established industry term or plain description. Add a project term only when
it describes a precise contract used in more than one place or names persisted
compatibility data. Ordinary workflow phrases do not become concepts merely by
being capitalized.

## Guidance

Treat a project glossary as a vocabulary index, not a specification or an
inventory of every workflow step. Before adding an entry, ask:

1. Does the term identify a project-specific contract used in more than one
   place, or persisted data that callers must keep compatible with?
2. Would an established term or a short plain description communicate the same
   thing without inventing a proper noun?

If the first answer is no, keep the explanation in the workflow or skill that
owns it. If the second answer is yes, use the established or plain term.

When an opaque name already exists, update its live consumers in the same
change. A glossary rename is incomplete while skills, public documentation, or
tests still teach the old vocabulary. Search the live tree for the old term,
update the owning instructions, and run the checks that cover the affected
artifacts.

Keep the owning rule exact while simplifying its name. For a derived set,
equivalence language such as "the issues are exactly..." requires every
qualifying item to appear and every reported item to qualify. A one-way phrase
such as "issues appear only when..." prevents invalid entries but still permits
valid ones to be omitted.

Persisted names are the exception to friendly renaming. Explain them clearly,
but retain the exact field, marker, or receipt-kind identifier unless the work
includes an intentional compatibility migration. [Run
History](../../../CONCEPTS.md#run-history), for example, keeps the exact
pre-version `orchestrator:run-record:v1` marker text so the liveness gate can
still recognize a legacy record.

## Why This Matters

A catch-all glossary hides the few terms readers need to recognize across
skills, documentation, and persisted records. Opaque labels create translation
work and make routine actions look like protocols. Detailed entries for every
step also duplicate the specifications that should remain in their owning
files.

The compatibility exception prevents the opposite mistake. Readable prose must
not silently rename fields or enum-like values that stored data and callers
depend on. Keeping a clear human explanation beside the literal identifier
improves comprehension without breaking interoperability.

## When to Apply

- Adding or revising a `CONCEPTS.md` entry.
- Renaming a workflow, readiness, research, installation, or maintenance term.
- Simplifying a skill that uses capitalized labels for ordinary actions.
- Editing persisted records, JSON fields, markers, or receipt vocabulary.
- Reviewing documentation that repeats a named concept without a concrete,
  reused contract behind it.

## Examples

Keep terms with stable shared meaning.
[Installation Parity](../../../CONCEPTS.md#installation-parity) names the
repository's visitor-equivalent installation invariant.
[Repository Maintenance Run](../../../CONCEPTS.md#repository-maintenance-run)
names the complete `Sense -> Decide -> Act -> Verify -> Learn` contract used by
[`repo-gardener`](../../../skills/repo-gardener/SKILL.md).

Use plain language when the owning workflow can state the rule directly. The
issue-management skill reports which issues are "Ready to start now" and keeps
the exact blocker and readiness rules in its graph reference rather than naming
that set as a separate project concept. Its behavioral comparison checks both
directions of the contract: the rewritten skill still reports every eligible
issue and no ineligible issue.

Remove or demote names that merely label steps. In this cleanup, `Global Pass`,
`Process Residual`, and `Targeted Sweep` stopped being standalone concepts. The
owning skills now say directly that they review the whole change, check whether
review is complete, and run pre-PR review checks. Likewise, `Repository Memory
Current` and `Personal Learning Current` became the more familiar
[Repository Learning Loop](../../../CONCEPTS.md#repository-learning-loop) and
[Personal Learning Loop](../../../CONCEPTS.md#personal-learning-loop).

## Related

- [Loosening a checklist during grading removes the check](../workflow-issues/loosening-a-checklist-during-grading-removes-the-check.md)
- [Operationalize abstract qualifiers in instruction review](../best-practices/operationalize-abstract-qualifiers-in-instruction-review.md)
- [Use answer-first natural prose for owner-facing skill readouts](../best-practices/answer-first-natural-prose-for-owner-facing-skill-readouts.md)
- [Allow honest nulls in mandatory novelty fields](../design-patterns/allow-honest-nulls-in-mandatory-novelty-fields.md)
- [Separate scout measurement stages from authoring capacity](../architecture-patterns/separate-scout-measurement-stages-from-authoring-capacity.md)
