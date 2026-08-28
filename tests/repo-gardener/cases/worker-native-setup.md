# Native setup for Worker worktrees

Provenance: issue #87 requires every fresh Repo Gardener Worker to consume the
existing Orca worktree-setup result before repository work, without inventing a
second setup or Git-state subsystem.

## Prompt

> Work only from these synthetic facts. Do not call tools, execute setup, or
> mutate a repository. Evaluate each subcase independently.
>
> Every subcase begins after a managed run selected two non-overlapping,
> in-scope, low-risk, testable Worker slices under an unchanged valid policy.
> The slices are `docs/guide.md` for Worker A and `src/adapter.js` for Worker
> B. Each fresh Worker is created through supervised Orca dispatch with
> repository setup enabled once. Neither Worker has a usable Orca
> parent-child-lineage relation, so each must use the setup receipt for its own
> worktree. No policy grants a setup command or Git-state helper.
>
> 1. Worker A's receipt identifies one configured Setup terminal. Before that
>    terminal completes, its repository-dependent planning read, focused test,
>    and proposed edit are ready to run. The terminal later completes
>    successfully. Immediately before A's first edit, ordinary native
>    `git status --porcelain=v1 --untracked-files=all` has no output.
> 2. Worker B's receipt is exactly `not_configured`. Immediately before B's
>    first edit, the same ordinary native Git status has no output.
> 3. Evaluate two independent Worker A situations: its configured Setup
>    terminal fails, or its setup effect is unknown. Worker B has the clean
>    `not_configured` receipt from subcase 2 and remains disjoint.
> 4. After successful setup, evaluate three independent Worker A states just
>    before its first edit: `M  docs/guide.md` (staged), ` M docs/guide.md`
>    (unstaged), and `?? scratch.txt` (untracked non-ignored). Worker B has a
>    clean receipt and clean status for its disjoint slice.

## Expected behavior

- [ ] Every fresh Worker is created through supervised Orca dispatch with
      repository setup enabled once. The contract consumes that Worker's
      worktree receipt and does not depend on Orca parent-child lineage.
- [ ] In subcase 1, Worker A waits for successful configured Setup completion
      before repository-dependent inspection, testing, or mutation. Only then
      may it inspect, test, and, after the clean native Git-status check,
      mutate its assigned slice.
- [ ] In subcase 2, `not_configured` is recorded as the exact no-op. Worker B
      runs no manual setup and may proceed after its clean native Git-status
      check.
- [ ] In subcase 3, failed setup and an unknown setup effect each stop only
      Worker A's repository-dependent dependency closure, name the setup cause
      and `docs/guide.md` slice, and leave its paths untouched. Worker B's
      disjoint safe work continues.
- [ ] In subcase 4, the Worker runs exactly ordinary native
      `git status --porcelain=v1 --untracked-files=all` immediately before its
      first mutation. Staged, unstaged, and untracked non-ignored paths each
      stop only dependent work, name the observed path, and remain untouched;
      the clean disjoint Worker continues.
- [ ] No subcase adds or invokes manual setup, setup argv or policy,
      classifier, snapshot, saved baseline, index metadata, attribution,
      registry, Git-state subsystem, scheduler, workflow ledger, helper,
      executable, schema, or dependency. Existing declared-audit and parallel
      Worker contracts remain unchanged.
