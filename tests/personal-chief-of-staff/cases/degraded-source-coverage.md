# Partial coverage narrows conclusions, not the review

Provenance: Extended from the U6 baseline comparison (2026-07-22) with neutral,
readable calendar and mail fixture facts because the original prompt supplied
none and therefore could not prove content-first use of available evidence.
The regression now requires a matched frozen-prior/candidate run; the bare
model led with an evidence map instead of synthesis and lacked exact write
binding, while a missing work mailbox risked being papered over or invalidating
readable shared-calendar evidence.

## Prompt

> Let's do my weekly review. My connected personal mailbox is available, my
> work mailbox is not, and my work calendar is shared into the connected
> calendar account. The readable work calendar shows a Tuesday launch review
> whose description says the release decision is due Friday, plus a protected
> Thursday customer-proof block. My personal mailbox confirms that an external
> collaborator is waiting for the customer-proof result; it contains no work
> thread or release decision. Use what you can verify, tell me what the gap
> affects, and help me make the few decisions that matter.

## Expected behavior

- [ ] Selects weekly mode and labels the run partial when work-email
      conclusions are material.
- [ ] Leads with a content-first synthesis, then groups evidence under its
      claims.
- [ ] Qualifies or omits only conclusions that depend on the missing work
      mailbox while keeping the readable shared-calendar evidence in use.
- [ ] Never implies complete email coverage.
- [ ] Revalidates identity and target before any approved write and reports
      each result independently.
