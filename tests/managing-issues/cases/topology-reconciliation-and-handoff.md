# Topology effects reconcile native facts without rollback or dispatch

Provenance: accepted managing-issues contract R4 and R8, plus AE5 and AE10 —
topology effects preserve verified partial success and return fresh tracker
facts. Behavioral grade not yet run.

## Prompt

> Work only from this synthetic approved Linear batch; do not contact a
> provider. Before approval, complete previews showed these ordered effects:
>
> 1. Create leaf `ENG-13`.
> 2. Set `ENG-10` as `ENG-13`'s parent, dependent on effect 1.
> 3. Remove the independent relation `ENG-12 blocks ENG-11`.
>
> Fresh pre-reads stayed valid. Effect 1 was attempted once, returned canonical
> ID `ENG-13`, and matched readback. Effect 2 was attempted once but failed
> provider validation. Effect 3 was attempted once and both endpoint readbacks
> prove the native `blocks`/`blocked-by` relation is absent. An exhausted
> reconciliation now shows open ready leaves `ENG-11` and `ENG-12` with no
> unresolved blockers. `ENG-13` exists but has no parent.
>
> Report effects and the current handoff.

## Expected behavior

- [ ] Keeps the verified `ENG-13` creation as `Applied` and does not delete,
      retry, or semantically rematch it after the parent failure.
- [ ] Reports the parent effect as `Failed`, while preserving and reporting
      the successful independent relation removal in its exact native
      direction.
- [ ] Uses both endpoint readbacks and the exhausted affected-family read to
      reconcile current topology after the attempts.
- [ ] Derives Ready Frontier as `ENG-11` and `ENG-12` from current canonical
      facts, and separately reports unparented `ENG-13` as unresolved.
- [ ] Returns nodes, edges, coverage, blockers, effect outcomes, and
      Verification gaps only; it starts no worker and stores no schedule,
      claim, retry record, or recommended execution topology.
