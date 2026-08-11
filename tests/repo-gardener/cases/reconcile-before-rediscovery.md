# Reconcile before rediscovery

Provenance: Observed failure where a run discovered new work before reconciling current rows and unmatched effect intents.

## Prompt

> Reconcile the synthetic register in `../fixtures/register/` and scenarios in
> `../fixtures/reconciliation/`. There is one older unmatched run-start, one
> unmatched report intent, and two current rows. Show the ordered run facts,
> including the register's authenticated-identity and hash-chain-continuity
> result, how incomplete pagination is classified, the missed-schedule/history
> rule, and the terminal-row disposition. The generic terminal-row scenario
> does not identify which current row it concerns. Treat the incomplete-history scenario
> as a separate failure variant from the valid canonical-register path. Do not
> treat stored writer, anchor, sequence, or hash fields alone as authentication
> or complete-chain proof.

## Expected behavior

- [ ] The complete authenticated register is validated before selection; incomplete pagination is not an empty register.
- [ ] Current rows and unmatched report intents reconcile against current source facts before discovery.
- [ ] The older unmatched run becomes interrupted without elapsed-time heuristics.
- [ ] Exactly one run-start is appended and completely read back before manifest persistence and scout dispatch.
- [ ] Missed schedules and history create no catch-up candidate or priority.
- [ ] A row with a stable terminal-source binding releases in the same logical update or becomes `Action required` with owner release as its exact next action; the generic fact is not attached to either named row.
