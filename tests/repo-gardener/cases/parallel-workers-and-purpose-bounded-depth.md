# Parallel Workers and purpose-bounded depth

Provenance: the prior package dispatched at most one child and capped depth at
three, so two non-overlapping justified units could not both get a Worker and
a fourth look that would change assignment was refused.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run has finished the quick available-input pass across five areas. The durable
> file has `maximum_workers: 20`, matching identity, in-scope paths, and
> `mutation: true` for engineering health and documentation. Opening revision is
> `policy:1`. `CHANGELOG.md` has the git `merge` attribute `union` at the
> authoritative base and an additive-entry check applies. Two independently
> deliverable units
> overlap only on that ledger and not on an unrelated already-open billing PR:
> (1) dead-code removal in an adapter plus its own changelog entry, (2)
> documentation drift plus its own changelog entry. A third unit would
> touch a protected path. A fourth seam's next look would change which unit
> to assign; after that look, further investigation would not change
> assignments or recommendations. Variant: use the same proposed assignments
> but the ledger path has no `merge` attribute at the base. Produce separate
> assignment and depth decisions for the attributed and unattributed variants.

## Expected behavior

- [ ] Assigns two parallel Workers after overlap is decided, one worktree and
      one unmerged PR each, without inventing work to fill `maximum_workers`.
- [ ] The unrelated already-open PR does not consume the Worker cap.
- [ ] Does not assign a Worker to the protected-path unit; reports it for
      owner attention.
- [ ] Deepens the fourth seam while independent selected Workers progress because
      it would change assignment, then stops
      deepening because further investigation would not.
- [ ] A Worker does not perform the five-area breadth pass or write tracker comments; scout
      helpers stay read-only in the Orchestrator session.
- [ ] Does not assign two Workers the same `CHANGELOG.md` file. Assignment
      names that shared convention file on at most one Worker.
- [ ] A later merge collision on that file is owner work at merge-readiness,
      not a publication-time exception.
