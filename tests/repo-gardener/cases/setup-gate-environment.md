# Setup gate environment

Provenance: the setup lifecycle previously required one exact argv and a
byte-clean worktree, but did not make gate-prerequisite health an observable
setup result. A finite setup exit alone must not let a Worker run or assess a
gate against an unhealthy or substituted environment.

## Prompt

> Work only from these synthetic facts. Do not call tools or invent host
> capabilities. An opening policy pins one approved direct setup argv. Each
> fresh Worker has a byte-clean worktree and an assigned path slice. Required
> gate prerequisites and optional gate environments are declared by the
> repository's documented gates; neither setup output nor a harness profile can
> change them. Evaluate the independent subcases.
>
> 1. The finite setup command returns successfully. Its required local service
>    is healthy in the Worker worktree, and the Worker later reaches a clean
>    exact commit for `checking-pr-readiness`.
> 2. The finite setup command returns successfully, but required service
>    `local-api` never becomes healthy. A separate Worker has an unchanged
>    healthy required service and an unrelated non-browser verification gate.
> 3. The required local service is healthy, but optional browser infrastructure
>    is unavailable. The Worker has both a browser gate and an independent
>    non-browser repository gate.

## Expected behavior

- [ ] In subcase 1, setup records `local-api` as healthy before dependent work
      begins. The Worker runs documented gates in that worktree, and the
      exact-head readiness helper rechecks the required prerequisite for the
      same exact subject and full HEAD OID before assessment. Neither helper
      owns the PR, a tracker write, a merge, or environment repair.
- [ ] In subcase 2, the Worker names `local-api` and blocks only its dependent
      gate and work. A successful finite setup exit does not count as health,
      and the Worker does not retry setup, skip or weaken the gate, prompt for
      repair, or substitute an environment. The separate Worker and its
      independent verification continue under their unchanged envelope.
- [ ] In subcase 3, unavailable browser infrastructure names and blocks only
      the browser gate. The non-browser gate continues when its own required
      prerequisites are healthy; no browser substitute, implicit environment,
      or broad Worker block is permitted.
