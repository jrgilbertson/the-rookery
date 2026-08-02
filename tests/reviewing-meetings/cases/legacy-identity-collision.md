# Legacy notes stop for review instead of duplicating

Provenance: post-review correction gate (2026-07-23). Durable discovery
originally missed URL-only and legacy-ID-only matches, allowing duplicate
proposals.

## Prompt

> For each scenario, state the disposition and what the run refuses to do. The
> retrieved meeting is completed with sufficient notes and current source
> identity (`synthetic`/`meeting-l1`, mapped URL
> `https://example.invalid/meetings/meeting-l1`).
>
> 1. An existing note's identity fields differ, but its exact source URL
>    identifies the same meeting, under a different filename.
> 2. Two distinct existing notes each contain that exact URL.
> 3. A historical note carries only a configured legacy provider ID field
>    matching this meeting; no current source-and-ID pair matches.

## Expected behavior

- [ ] 1 → found by the durable-state search despite the different filename;
      **Collision stop** (not Already approved, no duplicate proposal) unless
      the user explicitly selected it for a reviewed identity correction.
- [ ] 2 → **Collision stop**; more than one exact URL match always stops for
      review.
- [ ] 3 → found via the legacy field; **Collision stop**, may return as a
      reviewed identity correction, never falls through to a new-note
      proposal, and the note is not bulk-rewritten.
