# Grok X Source

Read this reference only when authenticated Grok or host X search tools are
available and a material X query is about to run. It adapts X evidence to the
CRM source contract. It does not authorize posting, replies, likes, follows,
or DMs.

This is relationship evidence only. It is not engagement scanning, interesting
posts discovery, or contribute workflows (see repository issue #12).

## Prove read access

Confirm the host can run authenticated read-only X search before relying on
the source. Use whatever authenticated Grok CLI or host X tools the runtime
exposes. On auth failure, missing tools, or error, mark X **unavailable** and
apply Partial coverage only to conclusions that depend on X.

Do not like, follow, reply, post, send DMs, or otherwise mutate X as part of
this skill. CRM or CoS approval of a Person note or Task never authorizes an
X write.

Completion: a successful read proves access, or X is marked unavailable with
the failure named.

## Bound ordinary reads

Query only when X can change a named identity, contact, durable meaning,
relevance, or duplicate decision. Prefer the smallest useful slice: an explicit
result limit and a recent window (or equivalent host bound), not full history.

**Pointer-first.** When evidence already has an X URL, known handle, or named
interlocutor, scope the query to that pointer first. Self-activity may
corroborate when it can change the named conclusion.

**Self-activity-first.** When X is material and no stronger pointer exists,
start from a bounded slice of the user's own recent directed posts and replies.
Identify who those exchanges were directed at. Then apply the previously loaded
identity rules before attaching evidence to a Person note. Known matches may
support contact, durable meaning, or Task proposals under the relationship
contract. Unmatched or ambiguous candidates stay unlinked, or ask only when
ambiguity changes the result.

Treat likes, passive follows, ambient broadcasts, and observing someone else's
update as non-contact under the relationship contract. Substantive direct
replies, DMs, and targeted exchanges may count as contact when identity and
time are reliable.

For each retained interaction, keep enough source context to distinguish
**observed** facts from **inference**, and to support safe use: handle or
profile URL when known, direction, native timestamp, brief meaning, and source
URL when available. Use native times with the previously loaded
time-normalization rules before proposing `date_last_contacted`.

Raw X activity stays in X. Do not copy activity logs into Person notes. Dated
commitments route to Tasks, not Person metadata.

Completion: the query is bounded to a defensible purpose, pointer or
self-activity path, result limit, and time window, with observed evidence kept
separate from inference.
