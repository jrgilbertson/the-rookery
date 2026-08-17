# A failed topology effect stops every later effect

Provenance: covers node-before-edge ordering, exact readback, partial success,
and the global batch stop in R3, R13, and R15.

## Prompt

> Work only from this synthetic approved GitHub batch in `example/project`; do
> not contact a provider. Capability checks passed before the preview. The
> displayed order was:
>
> 1. Create ready implementation leaf `#13`.
> 2. Set `#10` as `#13`'s parent.
> 3. Remove the independent native relation `#12 blocks #11`.
>
> Effect 1 ran once, returned exact canonical URL
> `https://github.com/example/project/issues/13`, and its canonical readback
> matched. Fresh endpoint reads for effect 2 matched the preview, but its one
> write failed provider validation and made no relationship change. Effect 3
> has not been attempted. The latest complete family read still shows `#11`
> and `#12` as open, derived-ready, and unblocked. `#13` exists but is not a
> child of `#10`.
>
> Report the batch and current graph facts.

## Expected behavior

- [ ] Reports the verified `#13` creation as `applied` and preserves it without
      deleting, retrying, or matching it by similarity.
- [ ] Reports the parent edge as `failed` and the independent relation removal
      as `unapplied`; it does not continue after the failure.
- [ ] Reports current canonical nodes, edges, blockers, complete coverage, and
      the unresolved intended parent edge from exact reads.
- [ ] Reports `#11` and `#12` in the Ready Frontier for the connected family;
      it does not silently treat unattached `#13` as a child.
- [ ] Requires a fresh complete read, preview, and approval before any
      continuation, without storing a retry schedule or execution handoff.
