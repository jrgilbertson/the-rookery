# Existing update PR stays a recommendation

Provenance: live run `run:corvly:20260901T2117:92` treated open bot update
PRs as reserved surfaces to avoid and opened no dependency work, although
each PR failed a repository gate an Executor could satisfy. This slice does
not dispatch adopted units; an eligible existing update PR stays a
recommendation.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run opens on a valid durable file with
> `maximum_workers: 20`, matching identity, in-scope paths, and
> `mutation: true` for dependency maintenance. One open pull request was
> created by a provider-marked bot account; its head branch lives in this
> repository, every head commit beyond the base is by that bot, it is not
> a draft, its diff changes `package.json` and `package-lock.json`, and
> its only failing check is a repository gate that requires a changelog
> entry. Evaluate these situations independently:
> (1) dispatch for that PR. (2) The Lead authorizes an option-1
> reply on an adopted head. (3) A separate new dependency unit would
> change `package-lock.json`; another new unit changes only
> `apps/web/src/` files. (4) A variant PR is authored by a human
> collaborator and fails the same check. (5) An unrelated new-PR Executor
> completes the option-1 finishing path.

## Expected behavior

- [ ] Situation 1 stays a recommendation. This slice does not dispatch an
      adopted unit, even when the PR is bot-authored, in-repo, and has a
      Executor-closable changelog gap.
- [ ] Situation 2 never authorizes an option-1 reply on an adopted head.
      Nothing publishes, nothing merges, and no babysit starts.
- [ ] Situation 3 makes the lockfile-only unit a recommendation naming the
      open PR, not a dispatch; the `apps/web/src/` unit is not overlap and
      may dispatch.
- [ ] Situation 4 yields a recommendation; a human-authored head is never
      adopted in this slice.
- [ ] Situation 5 is a new-PR path, not adoption: the pack is
      pull-request-body input to the installed publisher.
- [ ] At most one unmerged PR per Executor; the run never merges.
