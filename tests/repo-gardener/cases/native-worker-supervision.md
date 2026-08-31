# Worker supervision from current facts

Provenance: the portable mutation interface requires supervised completion, but
leaves host waiting, recovery, and progress mechanics to the host adapter.

## Prompt

> Work only from these synthetic facts. Do not call tools, mutate a repository,
> start a timer, or contact a provider. Evaluate each scenario independently.
>
> A managed Repo Gardener run assigned Worker A the in-scope leaf
> `skills/repo-gardener/SKILL.md`. The host supervises A and reports its
> completion events. No policy grants Repo Gardener a retry helper,
> tracker-progress write, process inspector, or workflow ledger.
>
> 1. A completion event follows a changed assigned slice. Fresh native reads
>    show a new full head and diff, updated checks, current PR state, and
>    current issue authority. Those facts reveal one missing check command.
> 2. A completion event follows repeated analysis. Fresh reads of A's branch,
>    full head, diff, checks, PR, and authority are unchanged and expose no
>    actionable gap.
> 3. The host reports an unknown provider operation for A. A later supervised
>    completion event provides new native facts.

## Expected behavior

- [ ] In scenario 1, the Orchestrator recognizes the specific current gap and
      gives A one focused instruction. It bases that instruction on the fresh
      facts, not a response count or synthetic progress state.
- [ ] In scenario 2, the Orchestrator does not call unchanged facts progress
      or manufacture a status. It stops direction for A and plainly explains
      why another instruction would not help.
- [ ] In scenario 3, the unknown provider operation stops the affected action
      and is not success. Repo Gardener leaves waiting and recovery to the
      host; after the later completion it makes the same fresh-fact judgment.
- [ ] No scenario adds a timer, interval, response or commit count, progress
      schema, stable progress ID, receipt, registry, state machine, or native
      process-observation requirement.
