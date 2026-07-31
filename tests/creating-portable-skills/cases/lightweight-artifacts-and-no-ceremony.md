# Verification leaves lightweight artifacts and asks no ceremony

Provenance: the U5 retune's discriminating contract (PR #19 review rounds) —
the prior doctrine asked a verification-tier question, kept monolithic
evidence records, and routed unrunnable checks through waivers; this case
grades their removal.

## Prompt

> I just finished a substantive revision of my `expense-notes` skill —
> instruction semantics changed, and the graded prior-versus-revised
> comparison is done. Walk me through what happens next: (a) what, if
> anything, you still need to ask me before the change ships; (b) exactly
> which durable artifacts the verification leaves behind, and where they
> live; (c) how you record a required judgment that cannot be run in this
> environment.

## Expected behavior

- [ ] (a) asks no verification-mode or tier question; any remaining
      questions concern content or scope, not a verification ceremony.
- [ ] (b) the durable artifacts are exactly the suite's thin set — case
      files under `tests/expense-notes/cases/` and one log line per graded
      run in `tests/expense-notes/log.md` — with no completed comparison
      record kept as its own evidence document.
- [ ] (c) an unrunnable judgment is logged as not run; it is never waived
      into shipment, assigned an evidence label, or capped with a Claim
      Ceiling.
