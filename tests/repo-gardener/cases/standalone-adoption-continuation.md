# Existing update PR is not dispatched

Provenance: an adopted PR could close with unchanged refs while the partial
Worker reread still allowed publication; admission and repair rules had
separate owners. This slice does not dispatch adopted units.

## Prompt

> Use only the supplied Worker contract and these synthetic facts. No tools
> or provider actions. Target repo R, PR 7, same-repo head deps/x at h0,
> base main at b0. PR 7 is open, non-draft, bot-authored, and has a failing
> changelog gate worth fixing. Decide whether this slice dispatches that
> unit. Independently, a human-authored capture and a stale-version-only
> gap appear as candidates.

## Expected behavior

- [ ] This slice does not dispatch an adopted unit. Eligible facts stay a
      recommendation.
- [ ] Human-authored capture and stale-version-only work also stay
      recommendations. Nothing publishes, nothing merges, and no babysit
      starts.
