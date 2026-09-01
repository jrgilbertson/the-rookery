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
>    work for (a) or (b). Each ownerless Worker reaches a clean exact commit,
>    invokes `checking-pr-readiness` normally, and stops on its menu reply.
>    Each brief offered option 1 and recommended approve and proceed for that
>    exact head. Matching identity rereads succeed. Native checks on any
>    opened PR pass. The Orchestrator worktree remains available for
>    inspection.
> 2. `maximum_workers: 20`. Two otherwise justified units both touch the same
>    adapter path slice (`apps/adapter/`). No other units exist. An unrelated
>    already-open billing PR is present.
> 3. `maximum_workers: 0`. The same two non-overlapping justified units from
>    scenario 1 exist. The file is otherwise valid and names the tracker.
> 4. `maximum_workers: 1`. The same two non-overlapping justified units from
>    scenario 1 exist. The file is otherwise valid and names the tracker.
> 5. Before a new run opens, the tracker has a complete prior `run-opened` but
>    no matching `run-closed`; its lease expired, while the exact original
>    Orchestrator and Worker liveness is unknown. Their pending worktrees and
>    authored state remain available for inspection.
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
- [ ] Scenario 1 assigns two parallel Workers after overlap is decided. Each
      ownerless Worker stops on its PR-readiness menu, then may open one
      unmerged PR only after Orchestrator-authorized option 1, matching
      identity reread, and the immediate matching local/provider-head and
      clean-surface re-read. The unrelated already-open billing PR does not
      consume the Worker cap. The run does not invent work to fill
      `maximum_workers`.
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
- [ ] Scenario 4 selects and dispatches no more than one Worker; the
      unselected justified unit remains a recommendation for owner attention.
- [ ] Scenario 5 treats lease expiry as insufficient evidence, blocks a new
      opening and new Workers until the prior tracker effect is truthfully
      reconciled, and uses the bounded, stable original-Orchestrator and
      caller-or-automation identities persisted in that `run-opened` payload
      for the host liveness lookup. It adds no state machine or per-Worker
      tracker records, then starts any later run fresh with its own run ID and
      opening sequence.
- [ ] Every scenario leaves already-open unrelated PRs in place, never
      merges, never creates a follow-up issue, and keeps generated reports
      out of repository source. Worker facts are reported only after a fresh
      native read. When a scenario actually opens a Worker PR, merge-readiness
      is invoked and Proceed to merge is not selected.
