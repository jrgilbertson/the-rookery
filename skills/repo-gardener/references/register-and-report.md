# Tracker and morning report contract

The live GitHub tracker is one issue body plus comments. The issue body is a
mutable morning projection. Native GitHub pull requests, branches, heads,
checks, and states are authoritative for authored work.

## Preserve the existing grammar

The body contains one fenced `orchestrator-register/v1` object between
`orchestrator:current-portfolio:v1` markers, followed by the human projection.
Legacy rows remain parseable for continuity, but they are not claims, a queue,
or an ownership database.

Managed comments contain one exact `orchestrator-history/v1` receipt between
`orchestrator:history-receipt:v1` markers. The sequence remains hash-linked
from `GENESIS`. Preserve all existing receipts byte-for-byte and continue from
the current head. Do not create a new chain or use the chain as proof of
planning quality, authority, or safety.

`normalize-github-register` requires the complete issue and every comment page,
exact configured identities, valid markers, stable provider order, a complete
chain, and a body anchor equal to history or exactly one prepared tail ahead.
Its result has `provenance: unverified` because structural consistency cannot
authenticate how the snapshot was obtained.

## Write exactly two run records

Each run ID owns exactly two managed comments:

1. one `run-opened` record written and read back before sensing; and
2. one consolidated `run-closed` record written and read back after child
   supervision or an honest no-child decision.

Do not write managed manifest, scout, lane, decision, effect, checker, or
per-child comments. Unrelated comments with another run ID do not count.

Use the existing body-and-comment preparation path for each record. The body
may refresh the human projection during those two operations. An ambiguous
write is resolved by a complete read for the exact prepared material before
any retry.

Machine identities are bounded ASCII, not prose, titles, URLs, or elapsed
time. Receipt JSON remains bounded to 16 KiB and the managed issue body to
48 KiB. Keep raw customer identities, event payloads, free text, secrets,
transcripts, recordings, and exported datasets out of both surfaces.

## Render the morning projection

The issue body and retained parent report show:

- a nine-row lane table with status, what happened, terminal event, strongest
  evidence, and room for improvement;
- selected depth targets and findings;
- a bounded data-trust result or exact limitation;
- native child PR facts and terminal state;
- up to seven owner-attention items plus overflow count;
- ranked issue-ready recommendations;
- run outcome and provisional dogfood milestone; and
- after final readback, `register_closed_consistently` in the retained parent
  report or caller result, not in the immutable close record.

Seven is a presentation limit only. It does not constrain sensing, depth, or
native authored work. Never claim persistence without an exact provider read.
