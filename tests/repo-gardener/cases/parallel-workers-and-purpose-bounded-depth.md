# Parallel Workers and purpose-bounded depth

Provenance: the prior package dispatched at most one child and capped depth at
three, so two non-overlapping justified units could not both get a Worker and
a fourth look that would change assignment was refused.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run has finished the nine-lane survey. The durable
> file has `maximum_workers: 20`, matching identity, in-scope paths, and
> `mutation: true` for code-health and documentation. Opening revision is
> `policy:1`. Its optional `shared_ledger_paths` includes `CHANGELOG.md`, and
> the repository has already proved conflict-safe additive merge behavior and
> an additive-entry check. Two independently deliverable units
> overlap only on that ledger and not on an unrelated already-open billing PR:
> (1) dead-code removal in an adapter plus its own changelog entry, (2)
> documentation drift plus its own changelog entry. A third unit would
> touch a protected path. A fourth seam's next look would change which unit
> to assign; after that look, further investigation would not change
> assignments or recommendations. Variant: use the same proposed assignments
> and path list but omit the repository proof. Produce separate assignment and
> depth decisions for the proved and missing-proof variants.

## Expected behavior

- [ ] Assigns two parallel Workers after overlap is decided, one worktree and
      one unmerged PR each, without inventing work to fill `maximum_workers`.
- [ ] The unrelated already-open PR does not consume the Worker cap.
- [ ] Does not assign a Worker to the protected-path unit; reports it for
      owner attention.
- [ ] Takes the fourth look because it would change assignment, then stops
      deepening because further investigation would not.
- [ ] A Worker does not survey nine lanes or write tracker comments; scout
      helpers stay read-only in the Orchestrator session.
- [ ] Permits the two assignments' `CHANGELOG.md` overlap only after the
      repository proof of conflict-safe additive behavior, while each Worker
      retains its own additive entry.
- [ ] Serializes the otherwise matching `CHANGELOG.md` overlap when that
      repository proof is missing.
