# Later run appends without touching the pending proposal

Provenance: 2026-07-22 baseline. The bare model handled the split but never
named the append-only invariant, both dispositions, or an explicit ending.

## Prompt

> Earlier in this conversation you proposed Meeting A from source `synthetic`
> with native ID `meeting-pending-a`, and I have not reviewed it. A later
> completed Meeting B with ID `meeting-new-b` is now available. Meeting B
> ended on 2026-07-21, started at `2026-07-21T15:00:00-07:00`, has the title
> `Synthetic product review`, the source URL
> `https://example.invalid/meetings/meeting-new-b`, and generated notes with
> enough grounded context, discussion, decisions, and next steps. The
> configured live meeting template and naming convention are readable.
> Approved-note searches return zero exact source-and-ID matches for A and B,
> Meeting B's intended filename is unoccupied, and this conversation has no
> dismissal for either pair. Run the next post-meeting check.

## Expected behavior

- [ ] Classifies Meeting A as **Already pending** from the retrievable exact
      source-and-ID proposal.
- [ ] Presents only Meeting B as **Newly proposed** — Meeting A is not
      repeated, recomputed, or renumbered.
- [ ] Ends **Ready for review** reporting one newly proposed and one already
      pending.
