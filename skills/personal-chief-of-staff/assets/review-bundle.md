# Review Bundle

Use this shape as a flexible writing aid, not a fixed form. Omit headings that
do not improve clarity and do not create actions merely to fill the bundle.

**State the most important conclusion in a complete, content-first sentence.**
Follow with the evidence, interpretation, uncertainty, and consequence needed
to support it. Group related claims together and keep unrelated claims
separate.

After that synthesis, render the current response's **Source Access Audit**.
Place it before separately approvable actions and before the run ending. Use
the semantics and relevant-source set in `references/source-behavior.md`; the
table reports actual access, not intended retrieval, claim provenance, or
action success.

| Source or role | Result | Scope or window | Effect on claim categories |
| --- | --- | --- | --- |
| [generic source family or canonical role] | [exact access result] | [bounded safe scope] | [claim categories supported or limited] |

Use only these exact results: **Accessed — evidence found**, **Accessed — no
relevant evidence**, **Attempted — unavailable or failed**, **Not configured**,
**Declined**, and **Not needed**. For a combined action-and-review response,
add a first **Phase** column and label each row **Action access** or **Review
discovery**. Do not add the Phase column to other responses.

Keep source labels generic and role-based. Bound every scope or window, marking
a returned slice partial when needed and coarsening precision when it could
identify sensitive activity. Do not expose people, projects, counterparties,
private configured names, account identifiers, source URLs, note or event
titles, sensitive event types, content excerpts, credentials, raw queries, or
tool telemetry. Use separate safe rows for mixed bounded slices whose results
differ. Include every source in the relevant-source set, but do not enumerate
irrelevant connectors.

In the effect column, name the category of claim the result supports, narrows,
or prevents. Do not imply complete coverage from a partial scope and do not use
an access result as evidence that an external action succeeded. Mention a
source limitation again in prose only where it changes a material conclusion.

For action access, make the access purpose independently recoverable in the
scope cell. Use one row for the **Pre-write target or destination reread** and,
when performed, a separate row for the **Post-write verification readback**.
Never combine those rows because their source, scope, or result happens to
match, and never add a row for the mutation itself. In a combined
action-and-review table, both remain **Action access** rows under the unchanged
Phase column; discovery rows remain **Review discovery**.

For each material claim:

- state why it matters now;
- point to the authoritative source and its native timestamp when available,
  otherwise the current response and query time;
- distinguish observed fact from inference;
- name a source gap only when it limits this claim.

State overall coverage as sufficient, partial, or insufficient. When coverage
is partial, identify the omitted or qualified conclusions. When it is
insufficient, stop before presenting a weak conclusion as reliable.

When action is warranted, append one numbered proposal per independent effect:

> **1. [Complete sentence describing the proposed effect.]**
>
> Acting identity: [account or identity]
>
> Destination and exact target: [authoritative system and record, recipients,
> event, note, or repository target]
>
> Visibility: [include for repository actions when relevant]
>
> Proposed content or effect: [the full content or precise change]
>
> Evidence and reason: [why this change follows from the review]

Invite the user to approve, edit, defer, or skip each number independently.
After any approved action, report its result as applied, already satisfied,
failed, indeterminate, manual, deferred, or skipped. Close with one explicit
run ending and a short recap of what changed and what remains unapplied.
