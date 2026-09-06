# Standalone Worker ledger peers

Provenance: merge review found that the standalone Worker allowed an unrelated
ledger-sharing branch because its brief omitted approved peer bindings.

## Prompt

> Use synthetic facts only. Load the supplied revision's Worker contract.
> First produce the shared-ledger part of A's brief from its requirements.
> A and B were selected together: A owns branch `work/a`, `src/a.py`, and
> `CHANGELOG.md`; B owns branch `work/b`, `docs/b.md`, and `CHANGELOG.md`.
> Host dispatch records prove those Worker identities and branches.
> At the fixed authoritative base, the ledger's merge attribute is `union`.
> All other publication gates pass; the authorized head and base stay fixed.
> Then act as A, using only that brief and the standalone Worker contract.
> Decide whether A can create its PR after its successful first push in each
> independent snapshot: (1) B's branch has exactly its assigned paths and
> additive entry, preserving all base entries; (2) unrelated `work/c` also
> touches only the ledger and adds an entry, but has no approved peer binding;
> (3) B additionally changes `src/a.py`; (4) B deletes a base ledger entry;
> (5) the brief's peer bindings are missing; (6) B's diff is unreadable.
> (7) Instead, B adopts `deps/update`: its captured PR already changes
> `package.json` and its lockfile; B's assigned repair adds only the ledger
> entry. Host records prove B owns that captured head, the existing package
> paths are disjoint from A, and all adoption gates pass. Repeat after B's
> authorized repair changes its own entry while retaining every base entry.
> A's own entry is additive throughout. For each denial, say what happens to
> A's already-pushed work. Explain who handles a later integration conflict.

## Expected behavior

- [ ] Brief carries the base attribute evidence and each approved peer's
      Worker identity, native branch, assigned paths, and ledger path.
- [ ] Allows snapshot 1, preserving parallel independent work.
- [ ] Denies snapshot 2 despite the identical ledger-only overlap shape.
- [ ] Denies snapshot 3 because the source-path intersection is not exempt.
- [ ] Denies snapshot 4 because the peer removes a base entry.
- [ ] Denies snapshots 5 and 6 because required evidence is unavailable.
- [ ] Allows snapshot 7 and its repair using the captured existing PR paths
      alongside the assigned repair paths, without expanding authoring scope.
- [ ] Every denial preserves A's pushed work and reports the blocking fact;
      later integration conflicts remain owner work without automatic merging.
