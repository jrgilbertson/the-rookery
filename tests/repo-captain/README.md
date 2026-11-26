# Repo Captain checks

`fixtures/run-standin-checks.py` checks the synthetic GitHub, Orca, and git
that the [Repo Captain Skill Eval](../../evals/repo-captain/README.md) runs
against: the shared `gh` stand-in in `evals/reviewing-prs/stand-ins/`, the
`orca` stand-in in `evals/repo-captain/stand-ins/`, the staging script, and
every fixture in `evals/repo-captain/fixtures/`. It stages each fixture and
calls the stand-ins and git the way an agent would.

It confirms that every staged world answers the Captain's discovery: pull
requests, the tracker with its four scores, the default-branch policy, and
Orca's sessions, workers, hosts, and worktrees, and that each pull request's
head is the same commit in gh and in the staged git remote. It also confirms
that:

- the Orca stand-in refuses an unknown verb or flag with exit 3 and traces
  it, and rejects an unsafe or missing configuration
- `worker-release` refuses a worker that has not sent `worker_done`, and a
  retry of an unverifiable worker's dispatch fails
- a head that moves between turns moves in gh and git together, an earlier
  head can still be fetched by SHA, and `git range-diff` shows the fixture's
  quiet revert
- the merge queue enqueues, ejects, and merges, an admin merge cannot bypass
  it, and check runs on the merge commit are served
- a merge pinned to a stale head fails
- a revert branch can be pushed and opened as a pull request, a push to an
  existing pull request branch is refused, and tracker score and body edits
  read back
- the [Reviewing PRs checks](../reviewing-prs/README.md) still pass, since
  both Skill Evals share the `gh` stand-in

Run it through the complete repository gate:

```sh
lefthook run pre-push --force
```

The gate tests the stand-ins, which the Eval Records' evidence depends on. It
does not show that an agent obeys the skill, and nothing here runs a model.
