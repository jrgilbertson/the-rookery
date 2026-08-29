# Native setup gates repository verification

Provenance: issue #89 requires native Orca setup to gate repository-dependent
work without turning verification gates into setup or creating an environment
subsystem.

## Prompt

> Work only from these synthetic facts. Do not call tools, execute setup, or
> mutate a repository. Evaluate each subcase independently.
>
> A managed run has selected one in-scope Worker slice. Its fresh Worker was
> created through supervised Orca dispatch with repository setup enabled once.
> The repository documents the commands exactly as written below. No policy
> grants a setup command, package installation, command replacement, or
> synthesized environment.
>
> 1. The Worker's existing current-Dispatch observation proves configured Setup
>    is still running. Its first documented verification command is ready to
>    run.
> 2. In separate evaluations, Setup fails, or its effect is unknown. The same
>    documented verification command is ready to run.
> 3. Setup succeeds. The documented `python3 verify_policy.py` command exits
>    zero. The documented `npx --no-install verify-contract` command exits
>    nonzero.
> 4. The receipt is exactly `not_configured`. The documented command
>    `missing-verifier --check` is absent.

## Expected behavior

- [ ] In subcases 1 and 2, no verification gate runs. Running, failed, and
      unknown setup each keep the Worker's repository-dependent closure blocked
      and leave its slice untouched.
- [ ] In subcases 3 and 4, successful or no-op setup permits planning, then
      reaches the clean native status immediately before implementation's first
      mutation, then implementation, simplification, and review, before the
      documented PR gates run unchanged.
- [ ] In subcase 3, `python3 verify_policy.py` is reported `pass`; `npx
      --no-install verify-contract` is reported `failure`, not as setup or an
      environment problem.
- [ ] In subcase 4, `not_configured` is the exact no-op. The absent command is
      reported `unavailable`; the Worker does not install a package, replace
      the command, or synthesize another environment.
- [ ] No subcase adds a setup command, prerequisite or health model,
      optional-environment model, setup machinery, Git-state manager,
      scheduler, ledger, taxonomy, stable identity, JSON schema, receipt
      bundle, or state machine.
