# Worker-owned shared-ledger overlap

Provenance: ordinary path overlap protects independent Workers from changing
the same file. An accumulating ledger is the narrow exception when the path
carries the git `merge` attribute `union` at the authoritative base and a
Worker-owned entry check applies.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> The opening policy is valid. `CHANGELOG.md` has the git `merge` attribute
> `union` at the authoritative base, and an additive-entry gate applies.
> Worker A owns `src/a.py` plus an Unreleased entry;
> Worker B owns `docs/b.md` plus an Unreleased entry.
> Their only shared path is `CHANGELOG.md`, and the same assignment decision
> selected both Workers. Their original approved briefs bind each Worker
> identity, branch, and slice. After A has saved its pushed branch but
> immediately before creating its PR, the mandatory native branch/PR reread
> finds B's same branch or PR under B's same brief identity, with exactly B's
> known `docs/b.md` slice plus the same additive `CHANGELOG.md` entry. Variants:
> an unrelated native branch or PR has the same `docs/b.md` plus `CHANGELOG.md`
> path shape but is not B's approved branch or PR; B newly overlaps A's
> `src/a.py` path or scope; a third
> Worker shares `src/a.py` with A; a coordinator branch has no assigned
> implementation and proposes a changelog line; and the same shared path has
> no `merge` attribute at the base. Worker A's
> proposed diff removes B's existing changelog entry before adding A's. Produce
> separate decisions for the proved and missing-proof variants, including the
> handling of any later native merge or rebase conflict.

## Expected behavior

- [ ] Allows A and B to run concurrently because their only overlap is the
      union-merged ledger path.
- [ ] Allows A to reach PR creation after the mandatory native reread when B is
      identified by B's original approved brief identity and same native branch
      or PR, and comparison against both original assigned slices shows B has
      only its known disjoint slice plus that same union-merged ledger
      path.
- [ ] Denies the unrelated branch or PR with that same path shape because it
      is not B's originally approved branch or PR; preserves A's saved
      pushed state while reporting that exact overlap.
- [ ] Denies PR creation and preserves A's saved pushed state when B newly
      overlaps A's path or scope; reports the exact new overlap rather than
      carrying the assignment-time exemption forward.
- [ ] Serializes the third Worker because `src/a.py` is not a ledger path.
- [ ] Rejects A's proposed diff until it adds only A's attributable entry and
      preserves every base ledger entry.
- [ ] Rejects the coordinator-branch ledger line: the Orchestrator never owns
      integration or coordination ledger material.
- [ ] Serializes the otherwise matching ledger path when that path has no
      `merge` attribute at the base.
- [ ] Surfaces a later native merge or rebase conflict for human handling; it
      never hides or auto-resolves that conflict.
