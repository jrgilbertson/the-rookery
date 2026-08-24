# Tracker and morning report contract

The live GitHub tracker is one issue body plus comments. The issue body is a
mutable morning projection. Native GitHub pull requests, branches, heads,
checks, and states are authoritative for authored work.

## Two plain comments are the production records

Each run ID owns exactly two managed comments. Comments do not need a
hash-linked register, Current Portfolio JSON, exclusive-writer lock, or
structural checker to be valid production records.

Managed comments contain one exact `orchestrator-run-record/v1` object between
`orchestrator:run-record:v1` markers. Hash fields are not required. Unrelated
comments with another run ID, and ordinary comments without those markers, do
not count.

`normalize-github-tracker` requires the complete issue and every comment page,
exact configured identities, valid markers, and stable provider order. It does
not require a hash chain or a body register. Its result has
`provenance: unverified` because structural identity cannot authenticate how
the snapshot was obtained.

## Write exactly two run records

The caller-owned exclusive tracker-writer precondition in
`applying-effects.md` precedes the first write. That is a behavioral rule the
caller owns. This skill ships no lock or exclusive-writer checker. A successful
exact readback does not replace that precondition.

Each run ID owns exactly two managed comments:

1. one `run-opened` record written and read back before sensing; and
2. one consolidated `run-closed` record written and read back after Worker
   supervision or an honest no-Worker decision.

Do not write managed manifest, scout, lane, decision, effect, checker, or
per-Worker comments. Workers never comment on the tracker.

Use the existing body-and-comment preparation path for each record. The body
may refresh the human projection during those two operations. An ambiguous
write is resolved by a complete read for the exact prepared material before
any retry.

Machine identities are bounded ASCII, not prose, titles, URLs, or elapsed
time. Record JSON remains bounded to 16 KiB and the managed issue body to
48 KiB. Keep raw customer identities, event payloads, free text, secrets,
transcripts, recordings, and exported datasets out of both surfaces.

## Render the morning projection

The issue body and retained Orchestrator report show:

- a nine-row lane table with status, what happened, terminal event, strongest
  evidence, and room for improvement;
- selected depth targets and findings;
- a bounded data-trust result or exact limitation;
- native Worker PR facts, checks, review state, current Worker state, and
  in-run merge-readiness lights when that review ran;
- up to seven owner-attention items plus overflow count;
- ranked issue-ready recommendations; and
- run outcome.

The in-run merge-readiness review is not the owner's later merge gate. Say
that in the closed comment and the morning projection.

Do not include a dogfood milestone or a “behavioral during this pilot”
disclosure. Exact readback of the two comments is required before treating the
run as recorded. That verification is not a planning-quality, safety, or
register-consistency claim.

Seven is a presentation limit only. It does not constrain sensing, depth, or
native authored work. Never claim persistence without an exact provider read.
When native checks or required review remain pending at bounded closure, render
the retained Worker as `pending` and the run as `partial`; still render all nine
lane results.
