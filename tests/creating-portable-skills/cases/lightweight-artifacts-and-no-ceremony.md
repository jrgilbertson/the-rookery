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
- [ ] (b) names the case files and one log line per graded run as the
      durable artifacts, located at `tests/expense-notes/cases/` and
      `tests/expense-notes/log.md` or the host's own test convention.
      Also naming the trigger contract or commit message is fine.
- [ ] (b) keeps no completed comparison record, evidence document, or run
      ledger as a separate durable file.
- [ ] (c) an unrunnable judgment is recorded as not run or unverified and
      never counted as a pass; it is not waived into shipment, given an
      evidence label, or capped with a Claim Ceiling.
