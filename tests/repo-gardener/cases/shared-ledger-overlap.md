# Worker-owned shared-ledger overlap

Provenance: ordinary path overlap protects independent Workers from changing
the same file. An accumulating ledger is the narrow exception when the
repository has already proved union merge behavior and a Worker-owned entry
check.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> The opening policy is valid and has `shared_ledger_paths: [CHANGELOG.md]`.
> The repository has already proved conflict-safe additive merge behavior and
> an additive-entry gate. Worker A owns `src/a.py` plus an Unreleased entry;
> Worker B owns `docs/b.md` plus an Unreleased entry.
> Their only shared path is `CHANGELOG.md`, and the same assignment decision
> selected both Workers. After A has saved its pushed branch but immediately
> before creating its PR, the mandatory native branch/PR reread finds B's
> branch or PR with exactly B's known `docs/b.md` slice plus the same additive
> `CHANGELOG.md` entry. Variants: the native work is not that selected sibling;
> B newly overlaps A's `src/a.py` path or scope; a third Worker shares
> `src/a.py` with A; a coordinator branch has no assigned implementation and
> proposes a changelog line; the same path list is empty; and the same path
> list exists but repository proof is missing. Worker A's proposed diff removes
> B's existing changelog entry before adding A's. Produce separate decisions
> for the proved and missing-proof variants, including the handling of any later
> native merge or rebase conflict.

## Expected behavior

- [ ] Allows A and B to run concurrently because their only overlap is the
      configured, proven ledger path.
- [ ] Allows A to reach PR creation after the mandatory native reread when B is
      the sibling selected in that same assignment decision and B's branch or
      PR contains only B's known disjoint slice plus that same configured,
      proven ledger path.
- [ ] Denies PR creation for a branch or PR from unrelated native work, even
      when it touches the ledger, and preserves A's saved pushed state while
      reporting that exact overlap.
- [ ] Denies PR creation and preserves A's saved pushed state when B newly
      overlaps A's path or scope; reports the exact new overlap rather than
      carrying the assignment-time exemption forward.
- [ ] Serializes the third Worker because `src/a.py` is not a ledger path.
- [ ] Rejects A's proposed diff until it adds only A's attributable entry and
      preserves every base ledger entry.
- [ ] Rejects the coordinator-branch ledger line: the Orchestrator never owns
      integration or coordination ledger material.
- [ ] Serializes the otherwise matching ledger path when repository proof is
      missing.
- [ ] Does not exempt an empty `shared_ledger_paths` list.
- [ ] Surfaces a later native merge or rebase conflict for human handling; it
      never hides or auto-resolves that conflict.
