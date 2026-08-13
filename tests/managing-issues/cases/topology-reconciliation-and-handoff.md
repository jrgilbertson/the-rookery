# Topology effects reconcile native facts without rollback or dispatch

Provenance: the bare baseline omitted coverage and Verification gaps and added
execution-sequencing and speculative provider guidance, while a later
candidate appended repair choices; accepted contract R4, R8, AE5, and AE10
returns only reconciled tracker facts. The scenario uses GitHub because Release
A intentionally exposes no Linear mutation path.

## Prompt

> Work only from this synthetic approved GitHub batch in `example/project`; do
> not contact a provider. Before approval, complete previews showed these
> ordered effects:
>
> 1. Create leaf `#13`.
> 2. Set `#10` as `#13`'s parent, dependent on effect 1.
> 3. Remove the independent relation `#12 blocks #11`.
>
> Fresh pre-reads stayed valid. Effect 1 was attempted once, returned canonical
> URL `https://github.com/example/project/issues/13`, and matched canonical
> readback. Effect 2 was attempted once but failed
> provider validation. Effect 3 was attempted once and both endpoint readbacks
> prove the native `blocks`/`blocked-by` relation is absent. An exhausted
> reconciliation now shows open ready leaves `#11` and `#12` with no unresolved
> blockers. `#13` exists but has no parent.
>
> Report effects and the current handoff.

## Expected behavior

- [ ] Keeps the verified `#13` creation as `applied` and does not delete,
      retry, or semantically rematch it after the parent failure.
- [ ] Reports the parent effect as `failed`, while preserving and reporting
      the successful independent relation removal in its exact native
      direction.
- [ ] Uses both endpoint readbacks and the exhausted affected-family read to
      reconcile current topology after the attempts.
- [ ] Derives Ready Frontier as `#11` and `#12` from current canonical facts,
      and separately reports unparented `#13` as unresolved.
- [ ] Returns nodes, edges, coverage, blockers, effect outcomes, and
      Verification gaps only; it starts no worker and stores no schedule,
      claim, retry record, or recommended execution topology.
