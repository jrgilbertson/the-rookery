# Granola URL-less payloads map identity strictly or stop

Provenance: observed failure, fixed in PR #16 (`fix(meetings): recover
Granola source URLs safely`) — URL recovery needed exact-form validation.

## Prompt

> The configured Granola adapter declares a deterministic mapping from a
> canonical lowercase 36-character native ID to a source URL. For each
> returned payload below (each an ended meeting with sufficient notes), state
> whether the meeting continues through the remaining checks, and under what
> identity, or which disposition stops it.
>
> 1. Native ID `123e4567-e89b-42d3-a456-426614174000`, no source URL field.
> 2. Same ID, plus a direct source URL exactly equal to the adapter's mapped
>    URL.
> 3. Native ID `URN:UUID:123E4567-E89B-42D3-A456-426614174000`, no URL.
> 4. Native ID ` 123e4567-e89b-42d3-a456-426614174000 ` (whitespace-padded),
>    no URL.
> 5. Canonical ID, but a direct source URL that differs from the mapped URL.
> 6. A different provider with no declared mapping returns a source-ready
>    meeting without a source URL.

## Expected behavior

- [ ] 1 → continues; the mapped URL counts as adapter-exposed identity.
- [ ] 2 → continues; the equal direct URL confirms the mapped identity.
- [ ] 3 → **Unable to prepare**; no normalization of prefix or case.
- [ ] 4 → **Unable to prepare**; no trimming before interpolation.
- [ ] 5 → **Collision stop**; contradictory identity evidence is recorded.
- [ ] 6 → **Unable to prepare**; no URL guess for an unmapped provider.
