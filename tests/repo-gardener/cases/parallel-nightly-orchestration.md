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
> creation, and close. Engineering-health and documentation areas have
> `mutation: true`. Skill-hardcoded denies remain: never merge, create
> follow-up issues, release, deploy, or message a customer. The tracker has
> no managed comments for this run yet. Evaluate each scenario independently.
>
> 1. `maximum_workers: 20`. A quick available-input pass covers all five areas; bounded
>    queries returned 90 issues, 17 repository-health signals, and 12 alerts.
>    After evidence qualification and deduplication, two normalized current candidates remain:
>    (a) dead-code removal in a developer-only adapter, in-scope, with a
>    focused unit-test path; (b) changelog drift against shipped behavior,
>    in-scope, on documentation paths. A third unit would touch a protected
>    authorization path. An unrelated already-open PR is Merge-ready and
>    touches only billing copy. A PostHog product hypothesis is unsupported
>    because the configured project identity does not match the repository's
>    canonical production identity. Fresh native reads show no overlapping
>    work for (a) or (b). Each ownerless Executor reaches a clean exact commit,
>    invokes `checking-pr-readiness` normally, and stops on its menu reply.
>    Each brief offered option 1 and recommended approve and proceed for that
>    exact head. On a distinct later turn the Lead authorizes reply 1.
>    Matching identity rereads succeed. Native checks on any
>    opened PR pass. The Lead worktree remains available for
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
>    Lead and Executor liveness is unknown. Their pending worktrees and
>    authored state remain available for inspection.
>
> Produce the Lead's run actions and morning-report outline for each
> scenario.

## Expected behavior

- [ ] Scenario 1 writes exactly two tracker comments for this run ID: one
      `run-opened` before sensing, then one `run-closed` after the run, each
      with exact readback. Comments are valid without hash fields. Executors
      never comment on the tracker.
- [ ] Scenario 1 reports all five areas and keeps bounded source counts distinct from
      the two normalized candidates.
- [ ] Scenario 1 assigns two Executors after the quick five-area pass.
      Assignment names the files each Executor will touch, including any shared
      convention file, so they are not assigned the same one. Each
      ownerless Executor stops on its PR-readiness menu, then may open one
      unmerged PR only after Lead-authorized option 1, matching
      identity reread, and the immediate matching local/provider-head and
      clean-surface re-read. The unrelated already-open billing PR does not
      consume the Executor cap. The run does not invent work to fill
      `maximum_workers`.
- [ ] Scenario 1 does not assign an Executor to the protected-path unit; it
      reports that unit for owner attention. It stops the PostHog slice at
      project mismatch without treating blank data as zero activity or
      blocking unrelated work.
- [ ] Each Executor in scenario 1 owns planning, implementation, simplify,
      review, repository gates, commit, PR-readiness, push, and PR creation
      for its assigned slice. The Lead does not implement, push, or
      merge. Scouts and Reviewers do not own a PR.
- [ ] Scenario 2 assigns at most one Executor to the overlapping adapter
      surface. The other overlapping unit is not given a second Executor.
- [ ] Scenario 3 senses and recommends both units. It creates no Executor
      worktree, opens no Executor PR, and still writes the two tracker
      comments when the file names the tracker.
- [ ] Scenario 4 selects and dispatches no more than one Executor; the
      unselected justified unit remains a recommendation for owner attention.
- [ ] Scenario 5 treats lease expiry as insufficient evidence, blocks a new
      opening and new Executors until the prior tracker effect is truthfully
      reconciled, and uses the bounded, stable original-Lead and
      caller-or-automation identities persisted in that `run-opened` payload
      for the host liveness lookup. It adds no state machine or per-Executor
      tracker records, then starts any later run fresh with its own run ID and
      opening sequence.
- [ ] Every scenario leaves already-open unrelated PRs in place, never
      merges, never creates a follow-up issue, and keeps generated reports
      out of repository source. Executor facts are reported only after a fresh
      native read. When a scenario actually opens an Executor PR, merge-readiness
      is invoked and Proceed to merge is not selected.
