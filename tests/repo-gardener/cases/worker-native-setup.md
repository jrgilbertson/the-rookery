# Portable Worker preparation

Provenance: the portable mutation interface requires an isolated Worker
worktree from the authoritative base and repository-native setup only when the
host provides it. Repo Gardener must not recreate host lifecycle machinery.

## Prompt

> Work only from these synthetic facts. Do not call tools, prepare a worktree,
> or mutate a repository. Evaluate each subcase independently.
>
> A managed run selected two non-overlapping, in-scope, low-risk, testable
> slices: `docs/guide.md` for Worker A and `src/adapter.js` for Worker B. The
> opening policy is valid and unchanged. The host can supervise Workers and
> reports the authoritative base, each isolated worktree, each Worker branch,
> and whether repository-native setup is supplied.
>
> 1. Worker A has an isolated worktree at the authoritative base, a
>    Worker-owned branch, and host-provided repository setup that completes
>    successfully. Worker B has the same worktree and branch facts, and its
>    host supplies no setup.
> 2. Worker A's host-provided setup fails or has an unknown outcome. Worker B
>    remains disjoint and has no host-provided setup.
> 3. Worker A's host cannot provide an isolated worktree at the authoritative
>    base. Worker B has a valid isolated worktree but no Worker-owned branch.
> 4. Both Workers meet the interface, complete one coherent commit, and each
>    can own at most one unmerged PR. A later provider read for A's PR is
>    unknown while B's PR facts remain current.

## Expected behavior

- [ ] A Worker mutates only after the host provides its isolated worktree from
      the authoritative base, any host-provided repository setup is complete,
      supervision is available, and the Worker owns a branch and at most one
      unmerged PR.
- [ ] In subcase 1, A may proceed after the supplied setup succeeds. B may
      proceed without setup because its host does not provide one; Repo
      Gardener does not add a manual setup step for either Worker.
- [ ] In subcase 2, A's dependent mutation is stopped and reported without
      treating the failed or unknown setup as success. B's disjoint safe work
      may continue.
- [ ] In subcase 3, each affected Worker falls back to read-only reporting
      because a required mutation capability is missing. Repo Gardener does
      not synthesize a worktree, branch, setup command, startup configuration,
      receipt, or alternate lifecycle protocol.
- [ ] In subcase 4, each Worker retains ownership of its own branch and one
      unmerged PR. A's unknown provider fact stops only A's affected action;
      it is never reconciled as success and does not alter B's current facts.
- [ ] No subcase creates host adapters, setup commands, wait or recovery
      choreography, progress state, registries, schemas, receipts, or a
      second Git-state system.
