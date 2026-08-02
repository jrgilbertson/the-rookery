# Missing access degrades honestly instead of inventing

Provenance: U1 regression contract. Folds the source-unavailable,
waiting-for-source, missing-convention, missing-template, and
fresh-conversation variants. Graceful degradation was undefined without the
skill.

## Prompt

> For each scenario below, state the disposition (or run outcome) and what the
> run explicitly does not do.
>
> 1. The required meeting-source query fails outright.
> 2. A meeting has ended but its generated notes are still processing; the
>    source exposes no stable ID yet.
> 3. A genuinely new candidate remains after all suppression checks, but the
>    approved-note source exposes no unambiguous folder, filename format, time
>    basis, or extension.
> 4. A genuinely new candidate remains, but the configured live meeting
>    template cannot be read through its supported interface.
> 5. Approved-note access works, but current conversation history is not
>    retrievable.

## Expected behavior

- [ ] 1 → run ends **Unable to prepare**; it does not infer there were no
      meetings.
- [ ] 2 → **Waiting for source**; no approved-note query, template read,
      filename check, or review bundle.
- [ ] 3 → **Unable to prepare**; no path is invented and no collision check
      runs against a guessed filename.
- [ ] 4 → **Unable to prepare**, not Newly proposed; no invented note shape,
      no durable write.
- [ ] 5 → approved-note suppression still runs; the run discloses that
      pending/dismissed suppression is unavailable and does not claim a
      duplicate-free result.
