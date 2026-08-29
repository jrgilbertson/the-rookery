# Parallel nightly orchestration

Provenance: the prior package dispatched at most one child and treated leftover
open PRs as consuming authoring capacity, so two non-overlapping justified
units could not both open a PR and a `maximum_workers: 0` file was not a
sense-and-recommend run.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run is requested. `.agents/repo-gardener.yaml` is
> valid, names a live tracker identity, matches repository identity and
> scope, and keeps that revision unchanged at open, dispatch, push, PR
> creation, and close. Code-health and documentation lanes have
> `mutation: true`. Skill-hardcoded denies remain: never merge, create
> follow-up issues, release, deploy, or message a customer. The tracker has
> no managed comments for this run yet. Evaluate each scenario independently.
>
> 1. `maximum_workers: 20`. Nine-lane census totals are 90 issues, 17
>    repository-health signals, and 12 alerts. After evidence qualification
>    and cross-lane deduplication, two normalized current candidates remain:
>    (a) dead-code removal in a developer-only adapter, in-scope, with a
>    focused unit-test path; (b) changelog drift against shipped behavior,
>    in-scope, on documentation paths. A third unit would touch a protected
>    authorization path. An unrelated already-open PR is Merge-ready and
>    touches only billing copy. A PostHog product hypothesis is unsupported
>    because the configured project identity does not match the repository's
>    canonical production identity. Fresh native reads show no overlapping
>    work for (a) or (b). Each ownerless Worker reaches a clean exact commit
>    and receives a same-session readable `ready` result from
>    `checking-pr-readiness`. Native checks on any opened PR pass. The
>    Orchestrator worktree remains available for inspection.
> 2. `maximum_workers: 20`. Two otherwise justified units both touch the same
>    adapter path slice (`apps/adapter/`). No other units exist. An unrelated
>    already-open billing PR is present.
> 3. `maximum_workers: 0`. The same two non-overlapping justified units from
>    scenario 1 exist. The file is otherwise valid and names the tracker.
>
> Produce the Orchestrator's run actions and morning-report outline for each
> scenario.

## Expected behavior

- [ ] Scenario 1 writes exactly two tracker comments for this run ID: one
      `run-opened` before sensing, then one `run-closed` after the run, each
      with exact readback. Comments are valid without hash fields. Workers
      never comment on the tracker.
- [ ] Scenario 1 reports all nine lanes and keeps census totals distinct from
      the two normalized candidates.
- [ ] Scenario 1 assigns two parallel Workers after overlap is decided, and
      each ownerless Worker may open one unmerged PR only after its
      same-session readable readiness result and an immediate matching
      local/provider-head and clean-surface re-read. The unrelated already-open
      billing PR does not consume the Worker cap. The run does not invent work
      to fill `maximum_workers`.
- [ ] Scenario 1 does not assign a Worker to the protected-path unit; it
      reports that unit for owner attention. It stops the PostHog slice at
      project mismatch without treating blank data as zero activity or
      blocking unrelated work.
- [ ] Each Worker in scenario 1 owns planning, implementation, simplify,
      review, repository gates, commit, PR-readiness, push, and PR creation
      for its assigned slice. The Orchestrator does not implement, push, or
      merge. Helpers do not own a PR.
- [ ] Scenario 2 assigns at most one Worker to the overlapping adapter
      surface. The other overlapping unit is not given a second Worker.
- [ ] Scenario 3 senses and recommends both units. It creates no Worker
      worktree, opens no Worker PR, and still writes the two tracker
      comments when the file names the tracker.
- [ ] Every scenario leaves already-open unrelated PRs in place, never
      merges, never creates a follow-up issue, and keeps generated reports
      out of repository source. Worker facts are reported only after a
      fresh native read.
