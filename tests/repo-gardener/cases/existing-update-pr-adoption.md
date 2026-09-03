# Adopt an existing update PR as a Worker unit

Provenance: live run `run:corvly:20260901T2117:92` treated open bot update
PRs as reserved surfaces to avoid and opened no dependency work, although
each PR failed a repository gate a Worker could satisfy. An open
same-repository update PR with a Worker-closable gap is a unit.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run opens on a valid durable file with
> `maximum_workers: 20`, matching identity, in-scope paths, and
> `mutation: true` for the dependency lane. `CHANGELOG.md` has the git
> `merge` attribute `union` at the authoritative base. One open pull request
> was created by a provider-marked bot account; its head branch lives in this
> repository, every head commit beyond the base is by that bot, it is not a
> draft, its diff changes `package.json` and `package-lock.json`, and its
> only failing check is a repository gate that requires a changelog entry.
> The native read gives head ref, full head OID `h1`, base ref, full base
> OID, and changed paths. Evaluate these situations independently:
> (1) dispatch for that PR. (2) The Worker adds the changelog entry, runs
> `checking-pr-readiness`, and stops at the menu; on a later turn the
> Orchestrator authorizes 1. (3) Before the push the hosted head has moved to
> `h2` because the bot rebased. (4) A second unit proposes adopting the same
> PR. (5) A variant PR's head branch lives in a fork. (6) The PR's existing
> diff also touches `.github/workflows/ci.yml`, a protected path, while the
> Worker's own commit does not. (7) A separate new dependency unit for an
> unrelated advisory would change `package-lock.json`; another new unit
> changes only `apps/web/src/` files. (8) A variant PR is authored by a human
> collaborator and fails the same check. (9) Immediately before authoring,
> a fresh native read shows the changelog gate now passes. (10) A variant PR's
> only failing check is a runner timeout unrelated to its diff. (11) A second
> open PR targets a different base from the same head branch.

## Expected behavior

- [ ] Situation 1 dispatches one Worker whose unit is the existing PR: the
      worktree is the PR head branch at `h1`; the brief names the PR number,
      head ref, `h1`, base ref and base OID, the changelog gap, and that the
      bot will stop maintaining the branch after the first Worker push.
      Adoption counts against `maximum_workers`.
- [ ] Situation 2 continues into an atomic update of the hosted head under a
      lease expecting `h1`; no second PR opens; the Worker then invokes
      `checking-merge-readiness` on that PR; nothing merges; the report
      names the PR as adopted and owner-maintained from that push.
- [ ] Situation 3 refuses the lease, preserves the local commit, names the
      moved head, and does not recapture or retry.
- [ ] Situation 4 denies the second adoption; one PR has at most one Worker.
- [ ] Situation 5 yields a recommendation only, never adoption.
- [ ] Situation 6 passes the protected-path gate on the Worker's own diff and
      reports the workflow change as native state, not authored.
- [ ] Situation 7 makes the lockfile-only unit a recommendation naming the
      open PR, not a dispatch; the `apps/web/src/` unit is not overlap and may
      dispatch.
- [ ] Situation 8 yields a recommendation; a human-authored head is never
      adopted.
- [ ] Situation 9 stops the unit and reports the closed gap without
      authoring or publishing.
- [ ] Situation 10 yields a recommendation; a transient provider failure is
      not a Worker-closable gap.
- [ ] Situation 11 denies adoption because the head ref is not exclusive to
      the PR, regardless of changed paths.
- [ ] The existence of an open PR is never given as a reason to skip a unit.
- [ ] At most one unmerged PR per Worker; the run never merges.
