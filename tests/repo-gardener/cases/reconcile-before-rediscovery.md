# Reconcile before rediscovery

Provenance: Observed failure where a run discovered new work before reconciling current rows and unmatched report intents.

## Prompt

> Reconcile the synthetic register in `../fixtures/register/` and scenarios in
> `../fixtures/reconciliation/`. There is one older unmatched run-start, one
> unmatched report intent, and two current rows. Show the ordered run facts,
> including the register's authenticated-identity and hash-chain-continuity
> result, how incomplete pagination is classified, the missed-schedule/history
> rule, and the terminal-row disposition. The generic terminal-row scenario
> does not identify which current row it concerns. For the
> `effect_reconciled: true` fact, show the terminal effect disposition and how
> it is recorded. Treat the incomplete-history scenario
> as a separate failure variant from the valid canonical-register path. Do not
> treat stored writer, anchor, sequence, or hash fields alone as authentication
> or complete-chain proof.

## Expected behavior

- [ ] The complete register is validated before selection with separate provider-authenticated identity and hash-chain continuity proof results; incomplete pagination is not an empty register.
- [ ] Current rows and unmatched report intents reconcile against current source facts before discovery; `effect_reconciled: true` is idempotently recorded as an `observed` effect disposition, never reported as lacking a terminal outcome.
- [ ] The older unmatched run becomes interrupted without elapsed-time heuristics.
- [ ] Exactly one run-start is appended and completely read back before manifest persistence and scout dispatch; every supplied Scout Receipt is persisted and read back before decisions are appended.
- [ ] Missed schedules and history create no catch-up candidate or priority.
- [ ] Every reconciliation response states the general rule that a Current Portfolio row with a stable terminal-source binding releases in the same logical update or becomes `Action required` with owner release as its exact next action; the generic unbound fact remains unattached to either named row.
