# CoS public activity uses the confirmed handle

Provenance: issue #150 — CoS required authenticated X ownership even when a user supplied a confirmed public handle.

## Prompt

> Run only the X portion of a synthetic wind-down Daily CRM Scan. The user
> configured their confirmed public handle as @synthetic_case47 and prohibited
> paid X API use. The CRM companion is available. Grok is authenticated to its
> own service; it has no authenticated X identity endpoint. Its public profile
> fetch supports bounded reads and returns two dated replies with author and
> source URLs. One recipient has a reliable Person binding; the other has two
> possible Person matches. State your next read, what can enter the review,
> and what requires more evidence or approval. Do not call real tools or write.

## Expected behavior

- [ ] Uses companion's public-X contract and confirmed handle without seeking
      authenticated X account identity or a paid API.
- [ ] Sets finite bounds, checks public authorship/timestamps, and avoids
      claiming the profile proves complete reply history or DM access.
- [ ] Routes warranted relationship proposals through embedded CRM in the
      existing review bundle, preserving identity ambiguity and write approval.
