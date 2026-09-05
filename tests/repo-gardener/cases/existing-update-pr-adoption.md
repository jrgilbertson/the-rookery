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
> OID, and changed paths. Current native facts identify `main` as the
> configured default branch and prove the PR head `deps/update` is not
> provider-protected; the Worker can independently reread those facts.
> Existing host dispatch and supervision records prove no other live Worker
> can mutate that head, except where a situation below changes those facts.
> Evaluate these situations independently:
> (1) dispatch for that PR. (2) The Worker adds the changelog entry, runs
> `checking-pr-readiness`, and stops at a menu offering option 1 with an
> approve-and-proceed recommendation bound to the exact Worker head and base;
> on a distinct later turn the Orchestrator authorizes 1 for that head. All
> publication rereads still match. (3) Before the push the hosted head has moved to
> `h2` because the bot rebased. (4) A second unit proposes adopting the same
> PR. (5) A variant PR's head branch lives in a fork. (6) The PR's existing
> diff also touches `.github/workflows/ci.yml`, a protected path, while the
> Worker's own commit does not. (7) A separate new dependency unit for an
> unrelated advisory would change `package-lock.json`; another new unit
> changes only `apps/web/src/` files. (8) A variant PR is authored by a human
> collaborator and fails the same check. (9) Immediately before authoring,
> a fresh native read shows the changelog gate now passes. (10) A variant PR's
> only failing check is a runner timeout unrelated to its diff. (11) A second
> open PR targets a different base from the same head branch. (12) The
> otherwise eligible all-bot PR has head `main` and base `release`.
> (13) Its head is not `main` but is protected by a provider ruleset,
> although its classic branch-protection rule is absent.
> (14) The configured default branch or head-protection state is unavailable
> or unknown. (15) After dispatch, before the first mutation, the captured
> head becomes the default branch or provider-protected, or the native read
> becomes unavailable. (16) Those same changes occur after the Worker commits
> but before its first push or a repaired-head update; head and base OIDs
> have not moved. (17) Situation 2 holds, but an owner edits the adopted
> PR's title and bot-generated body while the Worker runs; head and base
> remain unchanged. (18) An unrelated new-PR Worker completes the same
> readiness and later-1 sequence with matching publication gates.
> (19) The same bot-authored PR was created by a Worker retained after a
> prior run closed partial. Existing host dispatch and supervision records
> show that Worker is still live and can mutate the head. Repeat with proven
> termination of that Worker, and with unavailable or unknown liveness.
> (20) Two candidates exist: the retained-Worker PR from situation 19 and an
> otherwise eligible bot PR whose existing host records prove no other live
> Worker can mutate its head.

## Expected behavior

- [ ] Situation 1 dispatches one Worker whose unit is the existing PR: the
      worktree is the PR head branch at `h1`; the brief names the PR number,
      head ref, `h1`, base ref and base OID, the current default branch ref,
      native proof the head is not provider-protected, the changelog gap,
      and that bot updates may stop after the first Worker push, while later bot or manual
      rebases may overwrite Worker edits.
      Adoption counts against `maximum_workers`.
- [ ] Situation 2 continues into an atomic update of the hosted head under a
      lease expecting `h1`; no second PR opens; the Worker then invokes
      `checking-merge-readiness` on that PR; nothing merges; the report
      names the PR as adopted with the risk of stopped bot updates or overwritten
      Worker edits.
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
- [ ] Situations 12 and 13 deny adoption despite bot-only commits, an
      exclusive same-repository head, and a Worker-closable gap.
- [ ] Situation 14 denies adoption; missing evidence is not permission.
- [ ] Situation 15 stops before mutation on the Worker's independent reread.
- [ ] Situation 16 stops publication and preserves the local commit even
      with an unchanged OID lease; it never recaptures authorization or retries.
- [ ] Situations 1 and 2 remain eligible with a known unprotected non-default
      head and matching native rereads; no new branch-name convention is required.
- [ ] Situations 2 and 17 update only the leased head and preserve the
      adopted PR's current title and body, including the concurrent owner
      edit. The evidence pack goes to the Orchestrator report; no metadata
      write or owner publisher is dispatched.
- [ ] Situation 18 supplies the evidence pack to the new PR description.
- [ ] The existence of an open PR is never given as a reason to skip a unit.
- [ ] At most one unmerged PR per Worker; the run never merges.

- [ ] Situation 19 refuses duplicate ownership even though the earlier run
      closed and its Worker created rather than adopted the PR. Proven
      termination permits adoption under the ordinary gates; historical
      Worker authorship does not permanently reserve the PR.
- [ ] Unknown or unavailable ownership/liveness makes only that candidate a
      recommendation. Situation 20 may adopt the independent eligible PR.
      Evidence comes from existing host dispatch and supervision records,
      never a new ownership registry or an inference from bot authorship.
