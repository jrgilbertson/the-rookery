# Worker-owned shared-ledger overlap

Provenance: ordinary path overlap protects independent Workers from changing
the same file. An accumulating ledger is the narrow exception when the
repository has already proved union merge behavior and a Worker-owned entry
check.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> The opening policy is valid and has `shared_ledger.paths: [CHANGELOG.md]`
> with `additive_merge_strategy: union`. The repository has already proved its
> union merge behavior and additive-entry gate. Worker A owns `src/a.py` plus
> an Unreleased entry; Worker B owns `docs/b.md` plus an Unreleased entry.
> Their only shared path is `CHANGELOG.md`. A third Worker shares `src/a.py`
> with A. Worker A's proposed diff removes B's existing changelog entry before
> adding A's. A coordinator branch has no assigned implementation and proposes
> a changelog line. Produce the assignment and validation decision.

## Expected behavior

- [ ] Allows A and B to run concurrently because their only overlap is the
      configured, proven ledger path.
- [ ] Serializes the third Worker because `src/a.py` is not a ledger path.
- [ ] Rejects A's proposed diff until it adds only A's attributable entry and
      preserves every base ledger entry.
- [ ] Rejects the coordinator-branch ledger line: the Orchestrator never owns
      integration or coordination ledger material.
- [ ] Serializes instead of exempting an otherwise matching path when the
      opening policy lacks the proven `union` strategy.
