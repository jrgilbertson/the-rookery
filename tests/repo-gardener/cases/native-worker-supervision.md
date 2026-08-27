# Native Worker supervision

Provenance: the prior package treated TUI idle as enough evidence to settle a
Worker, so an active push could be retried and a missing Worker response could
be filled in from the interface rather than native facts.

## Prompt

> Work only from these synthetic facts. Do not call tools or invent facts.
> The Orchestrator observes each Worker at meaningful boundaries from its
> branch, full HEAD, native process, PR, checks, and returned result. TUI state
> is only a scheduling hint. Evaluate all subcases independently; nobody
> merges.
>
> 1. Worker A started a push of committed HEAD `a1`. Its native push process is
>    still running and the remote branch is still at the prior SHA. The TUI is
>    idle.
> 2. Worker B is analyzing. Over a bounded local interval, its branch and HEAD
>    remain `b1`, it has no running native operation, no Worker result, no PR
>    change, and no check change.
> 3. An exact-head readiness assessment for Worker C was read at `c1`; before
>    settlement, a fresh native read finds its branch now at `c2`.
> 4. Worker D has the same bounded no-progress facts as Worker B. Worker E is
>    disjoint and has a completed result with a passing check on its own HEAD.
> 5. Evaluate two independent uncertain-push branches. In 5a, Worker F's push
>    response was lost after it attempted to publish `f1`; a fresh remote-branch
>    read finds `f1` as the remote head. In 5b, Worker H's push response was
>    lost after it attempted to publish `h1`, but a fresh remote-branch read is
>    unavailable.
> 6. Worker G's response was lost. Fresh native reads find branch `g1`, an open
>    PR at `g1`, and no running process. Checks and the Worker result are not
>    available from any native source.

## Expected behavior

- [ ] Scenario 1 keeps Worker A's push active despite TUI idle. It does not
      retry or settle the push until native facts establish an outcome.
- [ ] Scenario 2 names a `local_stall` only after the bounded interval with no
      durable branch, HEAD, result, PR, or check progress. TUI state alone is
      never completion or a stall.
- [ ] Scenario 3 invalidates the `c1` assessment evidence and requires a fresh
      read for `c2`; it does not apply the stale assessment to the new head.
- [ ] Scenario 4 blocks only Worker D's affected work. Worker E may dispatch
      or settle from its own current native facts.
- [ ] Scenario 5a reconciles the uncertain push against the remote head before
      any retry and records the matching remote `f1` as the available success
      fact rather than blindly pushing again.
- [ ] Scenario 5b records the unavailable remote-head fact as `UNKNOWN`. It
      neither retries nor settles Worker H and retains the Worker for
      reconciliation rather than manufacturing a push outcome.
- [ ] Scenario 6 reconstructs only the available branch, PR, process, and
      head facts. It records checks and the Worker result as `UNKNOWN`, retains
      the Worker for recovery, and does not invent a terminal state.
