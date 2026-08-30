# Native Worker supervision from current native facts

Provenance: issue #91 requires the Orchestrator to supervise a Worker from a
fresh native read after each response, without turning response history into a
second workflow state system.

## Prompt

> Work only from these synthetic facts. Do not call tools, mutate a
> repository, start a timer, or contact a provider. Evaluate each scenario
> independently.
>
> A managed Repo Gardener run assigned Worker A the in-scope leaf
> `skills/repo-gardener/SKILL.md`. The normal Orca rolling wait and provider
> recovery already exist. No policy grants Repo Gardener a retry helper,
> tracker-progress write, process inspector, or workflow ledger.
>
> 1. Worker A responds after changing its assigned slice. A fresh native read
>    shows a new full HEAD and changed current diff, updated check facts, the
>    current PR state, and the canonical issue state. The changed facts show
>    one actionable missing check command.
> 2. Worker A responds with repeated analysis. Fresh reads of its native
>    branch/full HEAD, diff, checks, PR, and tracker state are unchanged, and
>    expose no actionable gap.
> 3. Orca reports an unresolved provider effect while its native recovery or
>    rolling wait remains active. It later delivers the next Worker response.

## Expected behavior

- [ ] In scenario 1, the Orchestrator recognizes useful native progress and
      gives one focused instruction for the missing check, then returns to the
      ordinary Orca rolling wait. It does not spend or increment a commit or
      response allowance.
- [ ] In scenario 2, the Orchestrator does not call unchanged facts
      “progress” and does not manufacture a status. It stops further direction
      for Worker A and plainly explains which native facts were unchanged and
      why another focused instruction would not help.
- [ ] In scenario 3, Repo Gardener does not retry independently, add `UNKNOWN`
      to Worker states, start a timer, or write tracker progress. Orca owns the
      wait and recovery; after the next response, the Orchestrator makes the
      same five native reads and qualitative decision.
- [ ] TUI idle has no deciding role. No timer, interval, response count,
      commit count, progress schema, stable progress ID, registry, or new
      workflow state is needed, and native process observability is not
      required.
