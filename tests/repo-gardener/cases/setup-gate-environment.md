# Host-provided setup gates repository work

Provenance: host-provided repository setup must gate dependent work without
turning verification into setup or creating an environment subsystem.

## Prompt

> You may read the installed Repo Gardener package. Otherwise work only from
> these synthetic facts: do not inspect a live repository or provider, run
> commands, or change state. Evaluate each subcase independently.
>
> One authorized Worker slice. Policy authorizes only source change.
> Verification documents contain only named commands.
>
> 1. The host provides setup and it succeeds. Implementation, simplification,
>    and review are complete.
>    `python3 verify_policy.py` exits zero. `npx --no-install verify-contract`
>    exits nonzero.
> 2. The host provides setup and it fails before repository-dependent work.
> 3. The host provides no setup. Implementation, simplification, and review
>    are complete. Starting `missing-verifier --check` returns
>    `executable-not-found` before it runs.
>
> Provide a table with one row per command and these columns: subcase, setup
> disposition, command, reported result, additional action, and next Worker
> step. Use installed skill terms and do not assume facts not given here.

## Expected behavior

- [ ] Subcase 1 reports the Python command as `pass` and the npx
      command as `failure`, unchanged and not setup or environment outcomes.
- [ ] Subcase 2 stops dependent work without running a repository command.
- [ ] Subcase 3 reports the missing command as unavailable, with no setup task,
      install, replacement, or environment synthesis.
