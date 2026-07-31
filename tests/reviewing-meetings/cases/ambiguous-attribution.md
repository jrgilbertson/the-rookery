# Generic speaker labels do not become a named owner

Provenance: 2026-07-22 baseline — the bare model asked for confirmation but
did not define selective transcript use or the run outcome.

## Prompt

> The configured source's summary says Alex owns a consequential follow-up,
> but the only transcript labels are `Speaker` and `Microphone`. The completed
> meeting has the stable ID `meeting-attribution-01`, started at
> `2026-07-21T13:00:00-07:00`, has the title `Synthetic planning discussion`,
> and has the source URL
> `https://example.invalid/meetings/meeting-attribution-01`. Its generated
> notes contain enough grounded context, discussion, decisions, and next
> steps; only the owner attribution is ambiguous, and the relevant transcript
> turns are available for selective inspection. The configured live meeting
> template and naming convention are readable. The approved-note search
> returns zero exact source-and-ID matches, the intended filename is
> unoccupied, and this conversation contains no pending proposal or dismissal
> for the pair. Prepare a grounded meeting proposal and resolve only what the
> evidence supports.

## Expected behavior

- [ ] Uses the transcript selectively, only to test the named ownership
      ambiguity.
- [ ] Does not map the generic labels to Alex; ownership stays unresolved
      unless independent meeting evidence is unambiguous.
- [ ] Omits downstream actions that would depend on the unsupported
      attribution.
- [ ] Classifies the meeting **Newly proposed** and ends **Ready for review**.
