# New meeting classified and kept read-only

Provenance: 2026-07-22 baseline — the bare model proposed a note but never
named the canonical source identity, exact disposition, or an explicit ending.

## Prompt

> Check the completed meeting from source `synthetic` with native ID
> `meeting-new-01` and prepare what should happen next. It ended on
> 2026-07-21, started at `2026-07-21T10:00:00-07:00`, has the title
> `Synthetic customer follow-up`, and has the source URL
> `https://example.invalid/meetings/meeting-new-01`. Its generated notes
> contain enough grounded context, discussion, decisions, and next steps for a
> meeting-note proposal and one follow-up, but the follow-up's owner and
> recipient are unclear. The configured live meeting template and naming
> convention are readable. The approved-note search returns zero exact
> source-and-ID matches, the intended filename is unoccupied, and this
> conversation contains no pending proposal or dismissal for the pair. Do not
> write anything yet.

## Expected behavior

- [ ] Classifies the meeting as **Newly proposed**, keyed on the stable
      source-and-ID pair and ended state.
- [ ] Prepares a preview against the configured live meeting template while
      leaving the follow-up's owner and recipient unresolved.
- [ ] Performs no durable write.
- [ ] Ends **Ready for review** with an exact disposition count.
