# Embedded discovery suppresses duplicates and bounds the wildcard

Provenance: 2026-07-24 baseline — the bare model surfaced both people but
never bounded the wildcard, kept the writing suggestion independently
reviewable, or separated durable correction from feedback; folds the
durable-context-correction variant.

## Prompt

> You are reviewing a synthetic completed meeting. Keep ownership of the
> meeting-review bundle. The meeting and an earlier email both describe the
> same career change and the same promise I made to Morgan Lee. The canonical
> Person note already contains an equivalent dated Comment, and the canonical
> task system already contains the follow-up with the same owning identity
> and destination. I am also drafting an article: Morgan is a clear reviewer,
> while dormant expert Riley Chen is a defensible but weaker connection. A
> configured writing backlog exists, and the meeting suggests a related
> article idea. Return only supported relationship effects inside my existing
> bundle. Do not create a second approval flow or apply anything.

## Expected behavior

- [ ] Participates in embedded mode without taking over the caller's action
      numbering, review bundle, or completion state.
- [ ] Reports the equivalent Person Comment and Task as already-satisfied
      no-ops even though two sources repeat the evidence.
- [ ] Presents Morgan as the actionable discovery with a concrete reason and
      useful action.
- [ ] Labels Riley as the single bounded wildcard with no Task, draft, or
      Person-note change unless promoted.
- [ ] Keeps the writing-backlog suggestion independently reviewable and
      unapplied.
- [ ] Proposes a durable Person-note correction only when feedback changes
      stable relationship meaning, not merely because a suggestion was
      rejected.
