# Review Bundle

Lead with the most important conclusion in a complete sentence. Group evidence
under the claim it supports, distinguish fact from inference and uncertainty,
and explain why it matters now. Cite the authoritative source and native
timestamp, or the current response and query time when no native timestamp
exists. Name a gap beside a claim only when it limits that claim.

Use headings when they improve clarity. The **Source Access Audit** heading is
required after the synthesis, before actions and the explicit run ending.

## Source Access Audit

Write exactly one short paragraph, using the relevant-source set and access results in
"Audit the current response's source access" in `references/source-behavior.md`.

- For discovery, lead with **Sufficient**, **Partial**, or **Insufficient**
  coverage. Action-only responses have no review coverage verdict.
- Name every relevant role and its actual result. Group successes when useful;
  connect each stated limit to its consequence with "so": what claim is
  omitted, qualified, or prevented. For example, unresolved calendar identities
  mean combined availability may be known, so separate personal/work coverage
  is unverified. A complete empty read is a limit only when it explains an
  omitted claim or supports an absence claim. Complete successful evidence
  needs no "so" clause.
- Bound the read window or scope. Mark truncated scope partial. Name a role
  once unless its bounded slices have different results or safe scopes.
- Name **Pre-write target or destination reread** and **Post-write verification
  readback** as separate operations when performed, even on the same source.
  A failed or missing required operation is a limit. In combined responses,
  distinguish **Action access** from **Review discovery** or **Context
  discovery** using inline labels within that same paragraph, not separate
  paragraphs or subsections. Mutation outcomes belong in the action narrative.
- Keep labels generic and role-based. Coarsen scopes that could identify
  sensitive activity. Exclude private bindings, people, projects, account
  identifiers, URLs, note or event titles, sensitive event types, excerpts,
  credentials, queries, and tool telemetry.

Use ordinary prose, no table, HTML details, extra census label, or em dashes.
For example:

> Coverage is partial because the mailbox read was attempted and failed, so
> there are no reply-commitment claims from this window. Calendar was accessed
> with evidence for the current day.

## Proposed actions

Apply "Make every intention verifiable" in `references/source-behavior.md` to
recommendations as they appear and to each independent effect. Keep the basis,
outcome, and closure evidence in natural prose; use the following shape when
it helps the user review an external change:

> **1. [Complete sentence describing the proposed effect.]**
>
> Acting identity: [account or identity]
>
> Destination and exact target: [authoritative system and record, recipients,
> event, note, or repository target]
>
> Visibility: [repository visibility when relevant]
>
> Proposed content or effect: [complete content or precise change]
>
> Evidence and reason: [current basis and why this matters]
>
> Closure evidence: [future observable finish line for this effect]

Give each proposed source change its own action number, including a draft
awaiting canonical access; numbers inside its content do not number the action.
Continue action numbering across bundles in the same run. Invite the user to approve, edit, defer, or skip each number. Follow
"Bind approval to the exact action" and "Revalidate, apply, and read back" in
the shared reference, including its action-result labels. End with one run
ending and a recap of what changed and every action still unapplied.
