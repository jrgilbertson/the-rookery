# Grok X Source

Read this reference when an X query is about to run, or when judging X
evidence a caller already retrieved. Use it for relationship evidence from X.
Do not post, reply, like, follow, or send DMs.

Finding posts to read or contribute to is out of scope (repository issue #12).

## Prove read access

This check applies when this skill needs its own X query. Confirm the host can
run authenticated read-only X search before treating X as available. Use the
Grok CLI or host X tools the runtime already exposes.

If tools are missing, auth fails, or the query errors, mark X **unavailable**.
Apply **Partial** coverage only to conclusions that need X.

X evidence a caller already retrieved needs no local X tool. Judge it under the
identity, direction, and time rules below, and mark X unavailable only for a
further conclusion this skill would have to query for itself.

Do not mutate X in this skill. Approving a Person note or Task never authorizes
an X write.

Completion: a successful read proves access, or X is unavailable with the
failure named.

## Bound ordinary reads

Query X only when it can change a named identity, contact, durable meaning,
relevance, or duplicate decision. Cap results in every case and do not pull
full history.

**Pointer first.** If evidence already has an X URL, known handle, or named
person, search that first. For an exact URL, bound the read around the
referenced item rather than a recent window — a pointer to an older exchange
is still the evidence that was asked for. For a handle or named person with no
exact item, use a recent window (or the host's equivalent bound). Use the
user's own recent posts only when they can change that same conclusion.

**Own activity first when there is no pointer.** Read a short slice of the
user's recent directed posts and replies, using a recent window (or the host's
equivalent bound). See who those were to. Apply the
loaded identity rules before attaching anything to a Person note. A clear match
may support contact date, durable meaning, or a Task under the relationship
contract. Leave unmatched or ambiguous people unlinked. Ask only when the
ambiguity changes the result.

Likes, passive follows, broadcasts, and watching someone else's update do not
count as contact. Direct replies, DMs, and targeted exchanges may count when
identity and time are reliable.

For each kept interaction, separate **observed** facts from **inference**. Keep
handle or profile URL when known, direction, native timestamp, a short meaning
line, and source URL when available. Normalize native times with the loaded
time rules before proposing `date_last_contacted`.

Leave raw X history on X. Do not paste activity logs into Person notes. Put
dated commitments on Tasks, not in Person metadata.

Completion: the query has a clear purpose, a pointer or own-activity path, a
result limit, a time bound, and observed facts kept separate from inference.
