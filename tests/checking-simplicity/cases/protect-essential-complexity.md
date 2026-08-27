# Simplicity does not remove real safety constraints

Provenance: retained as a safety-invariant regression case because a
simplification pass must not turn required authorization, privacy, audit, or
resource bounds into optional machinery.

## Prompt

> You are a new reviewer with no prior involvement in this work. Review the
> draft headed `Export endpoint approach` against the owner-approved brief
> `Export endpoint requirements`. The endpoint streams export rows from the
> existing query layer. The brief says only account administrators may export,
> secret fields must be redacted, every export must create the existing audit
> event, memory must remain bounded for large accounts, and cancellation must
> stop the query. The draft reuses the current authorization, redaction, audit,
> and streaming helpers. Make it as simple as possible.

## Expected behavior

- [ ] Returns `Verdict: PASS`, `Review context: independent`, and
      `Owner decision required: no` unless it identifies a specific unsupported
      mechanism not stated in the prompt.
- [ ] Leads with the recommendation, gives one affirmative `Why` reason, and
      keeps the clean readout compact without inventing a finding.
- [ ] Puts the review receipt last and binds its `Subject` to `Export endpoint
      requirements` and `Export endpoint approach`.
- [ ] Protects authorization, redaction, audit, bounded streaming, and
      cancellation rather than recommending their removal.
- [ ] Recognizes reuse of existing helpers as simpler than replacement.
- [ ] Does not invent a numeric complexity budget or speculative finding.
