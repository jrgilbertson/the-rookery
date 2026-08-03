# Unverifiable isolation degrades

Provenance: 2026-08-02 final package review — the contract restored degradation
when clean executor contexts cannot be verified, but existing evidence covered
only contexts that were known to be unavailable.

## Prompt

> Read the project-local Storm Research skill. The harness offers separate
> executor contexts but cannot report whether they inherited task conversation
> or sibling work; no leak is currently visible. Prepare only the pre-dispatch
> isolation decision and execution-manifest state. Do not run research or
> assume that lack of a visible leak proves cleanliness.

## Expected behavior

- [ ] Does not describe the available contexts as verified clean or claim
      independent multi-perspective research can proceed normally.
- [ ] If work continues, selects the best available separation and labels the
      planned result a `single-context synthesis`.
- [ ] Marks the run degraded and lowers confidence because cleanliness cannot
      be verified, even though contexts are technically available.
- [ ] Records the isolation mechanism and its unverified state in the manifest.
- [ ] Names a concrete upgrade path, such as a harness signal that confirms no
      inherited task conversation or sibling work entered each executor.
