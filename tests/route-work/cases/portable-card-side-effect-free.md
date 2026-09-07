# A plan-only authorization produces a lead-alone route without side effects

Provenance: user feedback — the route must include a plain-text statement a
receiver can paste to start work without duplicating its source artifact or
making the router perform downstream work.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Route this synthetic request from the
> supplied facts. GitHub issue
> `https://github.com/example/parser/issues/97` contains approved requirements
> for a parser fix but no execution plan. The issue is the source of truth.
> Planning is authorized. No implementation, issue mutation, commit, push, pull
> request, or publication is authorized. Model availability is unknown.

## Expected behavior

- [ ] The final answer is exactly one card beginning with the bold line `**Route**`.
      The decision line is "Start with ce-plan on Fable 5.1 at medium" and
      names no role. Bold `**Why**`, `**Setup**`, and `**Copy/paste kickoff**`
      labels follow, each with a blank line after it; no headings or fences.
- [ ] Setup lists the Lead on Fable 5.1 at medium and no other role, since
      implementation is not authorized, and states that boundary. It mentions
      no worktree, orchestration, availability, or plan storage.
- [ ] The kickoff starts ce-plan from the supplied issue URL, states the lead's
      model and effort, treats the issue as the source of truth, and withholds
      implementation, issue mutation, commit, push, pull request, and
      publication in one sentence. It does not restate the issue.
- [ ] The trace contains only reads of the installed package: no attempted issue fetch,
      downstream invocation, planning, mutation, scheduling, monitoring, or
      persisted route state.
