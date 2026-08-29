# Native setup gates repository verification

Provenance: issue #89 requires native Orca setup to gate repository-dependent
work without turning verification gates into setup or creating an environment
subsystem.

## Prompt

> You may read the installed Repo Gardener package. Otherwise work only from
> these synthetic facts: do not inspect a live repository or provider, run
> commands, or change state. Evaluate each subcase independently.
>
> One authorized Worker slice. A fresh supervised Orca dispatch has setup
> enabled once. Policy authorizes only source change. Verification documents
> contain only named commands.
>
> 1. Setup succeeds. Implementation, simplification, and review are complete.
>    `python3 verify_policy.py` exits zero. `npx --no-install verify-contract`
>    exits nonzero.
> 2. The receipt is exactly `not_configured`. Implementation, simplification,
>    and review are complete. Starting `missing-verifier --check` returns
>    `executable-not-found` before it runs.
>
> Provide a table with one row per command and these columns: subcase, setup
> disposition, command, reported result, additional action, and next Worker
> step. Use installed skill terms and do not assume facts not given here.

## Expected behavior

- [ ] Separate subcase-1 rows report the Python command as `pass` and the npx
      command as `failure`, unchanged and not setup or environment outcomes.
- [ ] Subcase 2 keeps `not_configured` as the exact no-op and reports the
      missing command as unavailable, with no install, replacement, or
      environment synthesis.
