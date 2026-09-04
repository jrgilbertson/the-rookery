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
the semantics and relevant-source set in `references/source-behavior.md`.

Under that heading, write a short paragraph of a few sentences. That
paragraph is the complete current-response role census. Do not use a table,
HTML details, or em dashes. Do not print a spoken caption that says so.

Lead with coverage. For a discovery-bearing response, state overall coverage
as Sufficient, Partial, or Insufficient. An action-only response has no
review coverage verdict. Then name every relevant role that was in play and
how the read finished. Use these ordinary-word results: **accessed with
evidence**, **accessed with no relevant evidence**, **attempted and failed**,
**not configured**, **declined**, and **not needed**. Successful reads may
share one sentence. A limit gets its own clause or sentence, with a "so"
only when that result omits, qualifies, or prevents a claim. If the roster
is long, use two or three sentences: coverage and limits first, then the
remaining successes.

Classify internally with the six access results in
`references/source-behavior.md`. Render them as the ordinary-word forms
above. **Accessed — evidence found** renders **accessed with evidence**.
**Accessed — no relevant evidence** renders **accessed with no relevant
evidence**. **Attempted — unavailable or failed** renders **attempted and
failed**. **Not configured**, **Declined**, and **Not needed** render as
**not configured**, **declined**, and **not needed**.

Include attempted failures, partial or truncated reads, unconfigured or
declined roles, Partial or Insufficient coverage, and failed post-write
readbacks as limits. Include **accessed with no relevant evidence** as a
limit only when that empty result is why a claim is omitted, qualified, or
an absence claim is made. Complete, non-truncated **accessed with evidence**
discovery does not get a "so" clause.

When a **Pre-write target or destination reread** or **Post-write
verification readback** ran, say so in the paragraph. A failed or missing
required reread or readback is a limit. Keep those two operations as
separate clauses even when they share a source. Do not add a mini-table.
For a response combining an action with a review or non-mode context
request, distinguish action access from review discovery or context
discovery in the same paragraph. Do not use a Phase column.

The paragraph reports actual access, not intended retrieval, claim
provenance, or action success. Example:

```text
Coverage is partial because the mailbox read was attempted and failed, so
there are no reply-commitment claims from this window. Calendar was accessed
with evidence for the current day.
```

Keep source labels generic and role-based. Bound every scope or window, marking
a returned slice partial when needed and coarsening precision when it could
identify sensitive activity. Do not expose people, projects, counterparties,
private configured names, account identifiers, source URLs, note or event
titles, sensitive event types, content excerpts, credentials, raw queries, or
tool telemetry. Name mixed bounded slices separately when their results
differ. Include every source in the relevant-source set, but do not enumerate
irrelevant connectors. Each relevant discovery role appears once unless mixed
bounded slices of that role have different results or safe scopes, in which
case those slices stay separate. Pre-write reread and post-write readback stay
separate even when they share a source.

Name the category of claim a result supports, narrows, or prevents only when
that result limits a claim. Do not imply complete coverage from a partial
scope and do not use an access result as evidence that an external action
succeeded. Mention a source limitation again in later prose only where it
changes a material conclusion.

For action access, make the access purpose independently recoverable. Name the
**Pre-write target or destination reread** and, when performed, the
**Post-write verification readback** as separate operations. Never combine
them because their source, scope, or result happens to match, and never treat
the mutation itself as an access result. In a combined paragraph, keep those
operations as action access, distinct from later discovery.

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
