# Reconcile before rediscovery

Provenance: Observed failure where a run discovered new work before reconciling current rows and unmatched report intents.

## Prompt

> Reconcile the complete synthetic GitHub snapshots in
> `../fixtures/reconciliation/`. There is one older unmatched run-opened
> receipt, one unmatched prepared report operation, and current rows. Show the
> ordered run facts, how incomplete pagination is classified, the
> missed-schedule/history rule, and terminal-row disposition. Derive the
> report outcome internally from immutable prepared material plus complete
> pre/post snapshots. Reject a serialized `effect_reconciled` label. Treat an
> incomplete-history scenario separately from a structurally valid snapshot.

## Expected behavior

- [ ] A complete GitHub snapshot is structurally normalized before selection; incomplete pagination is not an empty register and provenance remains unverified.
- [ ] Current rows and unmatched prepared report operations reconcile before discovery; `reconciliation-v2` derives the terminal effect internally and rejects `effect_reconciled`.
- [ ] The older unmatched run becomes interrupted without elapsed-time heuristics.
- [ ] Serialized operations remain ordered: `run-opened`, manifest, supplied lane receipts, decisions, and `run-closed`, with exact verification between operations.
- [ ] Missed schedules and history create no catch-up candidate or priority.
- [ ] Every reconciliation response states the general rule that a Current Portfolio row with a stable terminal-source binding releases in the same logical update or becomes `Action required` with owner release as its exact next action; the generic unbound fact remains unattached to either named row.
