# Portable Worker preparation

Provenance: the portable mutation interface requires an isolated Worker
worktree from the authoritative base and repository-native setup only when the
host provides it. Setup gates repository work; PR readiness uses its normal
brief, numbered options, and later reply.

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
> 3. Immediately before its first mutation, Worker A's ordinary native
>    `git status --porcelain=v1 --untracked-files=all` independently reports
>    `M  docs/guide.md` (staged), ` M docs/guide.md` (unstaged), or
>    `?? scratch.txt` (untracked non-ignored). Worker B remains clean and
>    disjoint.
> 4. Worker A's host cannot provide an isolated worktree at the authoritative
>    base. Worker B has a valid isolated worktree but no Worker-owned branch.
> 5. Both Workers meet the interface, complete one coherent commit, and each
>    can own at most one unmerged PR. A later provider read for A's PR is
>    unknown while B's PR facts remain current.
> 6. Both Workers have clean exact commits. A invokes `checking-pr-readiness`
>    normally, stops at its menu, and the brief offered option 1 with an
>    approve-and-proceed recommendation for that exact head. A later turn
>    occurs. B's checker is unavailable.

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
- [ ] In subcase 3, each dirty status stops only A's dependent work, names its
      observed path, and leaves it untouched without restoring, staging, or
      committing it. B's clean disjoint work may continue.
- [ ] In subcase 4, each affected Worker falls back to read-only reporting
      because a required mutation capability is missing. Repo Gardener does
      not synthesize a worktree, branch, setup command, startup configuration,
      receipt, or alternate lifecycle protocol.
- [ ] In subcase 5, each Worker retains ownership of its own branch and one
      unmerged PR. A's unknown provider fact stops only A's affected action;
      it is never reconciled as success and does not alter B's current facts.
- [ ] In subcase 6, A cannot publish in its menu turn and does not choose
      option 1. It may continue only if the Orchestrator authorizes option 1;
      the checking skill then rereads identity. B preserves its commit
      without a fallback and names unavailable checking as the blocking gap.
- [ ] No subcase creates host adapters, setup commands, wait or recovery
      choreography, progress state, registries, schemas, receipts, or a
      second Git-state system.
