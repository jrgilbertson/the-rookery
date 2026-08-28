# Review Bundle

Use this shape as a flexible writing aid, not a fixed form. Omit headings that
do not improve clarity, except the required **Source Access Audit** heading, and
do not create actions merely to fill the bundle.

**State the most important conclusion in a complete, content-first sentence.**
Follow with the evidence, interpretation, uncertainty, and consequence needed
to support it. Group related claims together and keep unrelated claims
separate.

After that synthesis, render the current response's **Source Access Audit**.
Place it before separately approvable actions and before the run ending. Use
the semantics and relevant-source set in `references/source-behavior.md`. Both
surfaces below are required.

Under that heading, print the capsule first, then wrap the recovered table in
HTML `<details>`. The capsule is the default-visible path. The table is the
complete current-response role census. Do not print a spoken caption that
says so.

**Capsule.** For a discovery-bearing response, state overall coverage as
Sufficient, Partial, or Insufficient. An action-only response has no review
coverage verdict. Then name every material limitation with the claim category
it limits and the exact access result that produced it. Include attempted
failures, partial or truncated reads, unconfigured or declined roles, Partial
or Insufficient coverage, and failed post-write readbacks. Include
**Accessed — no relevant evidence** only when that empty result is why a claim
is omitted, qualified, or an absence claim is made. **Not needed** stays in
the table only. Complete, non-truncated **Accessed — evidence found**
discovery stays in the table only.

Print separate compact lines for the **Pre-write target or destination reread**
and the **Post-write verification readback** only when those reads ran. A
failed or missing required reread or readback is a material limitation in the
capsule. Successful reread and readback still appear as those compact lines
and as distinct table rows. Do not add a second mini-table. Do not put Phase
in the capsule.

**Table.** The same response still contains today's GFM table inside HTML
`<details>` with a short summary such as `Full source receipt`. Leave the
element closed unless the capsule includes an attempted failure, a partial
or truncated read, **Not configured**, **Declined**, Partial or Insufficient
coverage, a failed required reread or readback, or a claim-changing
**Accessed — no relevant evidence** row. In those cases add the `open`
attribute. Put a blank line after `</summary>` and before `</details>` so
the table still parses as GFM.

The table reports actual access, not intended retrieval, claim provenance,
or action success.

| Source or role | Result | Scope or window | Effect on claim categories |
| --- | --- | --- | --- |
| [generic source family or canonical role] | [exact access result] | [bounded safe scope] | [claim categories supported or limited] |

Use only these exact results: **Accessed — evidence found**, **Accessed — no
relevant evidence**, **Attempted — unavailable or failed**, **Not configured**,
**Declined**, and **Not needed**. For a response combining an action with either
a review or non-mode context request, add a first **Phase** column. Label action
rows **Action access**; label discovery rows **Review discovery** for a review
request or **Context discovery** for a non-mode context request. Do not add the
Phase column to other responses.

Keep source labels generic and role-based. Bound every scope or window, marking
a returned slice partial when needed and coarsening precision when it could
identify sensitive activity. Do not expose people, projects, counterparties,
private configured names, account identifiers, source URLs, note or event
titles, sensitive event types, content excerpts, credentials, raw queries, or
tool telemetry. Use separate safe rows for mixed bounded slices whose results
differ. Include every source in the relevant-source set, but do not enumerate
irrelevant connectors. Each relevant discovery role appears once as a table
row unless mixed bounded slices of that role have different results or safe
scopes, in which case those slices stay separate rows. Pre-write reread and
post-write readback stay separate rows even when they share a source. The
capsule may name a role that also has a table row.

In the effect column, name the category of claim the result supports, narrows,
or prevents. Do not imply complete coverage from a partial scope and do not use
an access result as evidence that an external action succeeded. Mention a
source limitation again in prose only where it changes a material conclusion.

For action access, make the access purpose independently recoverable in the
scope cell. Use one row for the **Pre-write target or destination reread** and,
when performed, a separate row for the **Post-write verification readback**.
Never combine those rows because their source, scope, or result happens to
match, and never add a row for the mutation itself. In a combined table, those
reread and readback rows stay **Action access** under the unchanged Phase
column.

For each material claim:

- state why it matters now;
- point to the authoritative source and its native timestamp when available,
  otherwise the current response and query time;
- distinguish observed fact from inference;
- name a source gap only when it limits this claim.

When coverage is partial, identify the omitted or qualified conclusions. When
it is insufficient, stop before presenting a weak conclusion as reliable.

Write intentions as natural prose. For each independent future outcome,
recommendation, priority, plan, coaching intervention, experiment, boundary,
strategy or learning proposal, action effect, or recommendation to preserve
the current state, let a reader recover the current authoritative basis (or an
explicitly user-supplied, unverified premise), the outcome the user owns or has
approved, and the future observable evidence that would show closure. These
meanings may be woven into one or two sentences; use literal `Current`,
`Desired`, or `Evidence` labels only when they materially improve clarity. Do
not turn factual synthesis, procedural acknowledgment, or an honest null into
an intention, and do not invent a missing outcome or finish line to fill the
shape. Preserve exact incomplete user wording only as visibly nonconforming
input. When the agent proposes a new outcome, phrase it as a candidate for the
user's approval rather than as the user's Desired; call it user-owned or
complete only after acceptance.

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
>
> Closure evidence: [future observable readback or other finish line for this
> effect]

Invite the user to approve, edit, defer, or skip each number independently.
Each action needs its own closure evidence. Changing that evidence after
approval creates a revised proposal that needs new approval.
After any approved action, report its result as applied, already satisfied,
failed, indeterminate, manual, deferred, or skipped. Close with one explicit
run ending and a short recap of what changed and what remains unapplied.
