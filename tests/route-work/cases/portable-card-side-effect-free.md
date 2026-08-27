# A request-only route produces a pasteable side-effect-free kickoff

Provenance: user feedback — the route must include a plain-text statement a
receiver can paste to start work while the router remains side-effect-free.

Input file: [`../fixtures/parser-fix.md`](../fixtures/parser-fix.md), installed
in the test project as `docs/requirements/parser-fix.md`.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package and the named input file; call no other tools. Route this synthetic
> request using only the text below.
> The team has approved requirements for a parser fix but no execution plan.
> Start from `docs/requirements/parser-fix.md`. The plan may be written in the
> repository, but no implementation, issue mutation, commit, push, pull
> request, or publication is authorized. Workflow and model availability are
> unknown.

## Expected behavior

- [ ] Returns exactly one response beginning `## Route`, with plain `Workflow`
      and `Setup` labels and no Markdown bold labels; the workflow is `ce-plan`
      and the topology is Single owner.
- [ ] Setup includes its reason, the primary orchestrator/planner tuple,
      availability `unverified`, Orca `None`, and current-worktree placement.
- [ ] `## Copy/paste kickoff` contains one fenced plain-text block beginning
      `Start this work with ce-plan.`, repeats the complete selected setup, and
      contains no Markdown delimiters.
- [ ] The fenced block gives the objective, done condition, stable supplied
      locator and first action, facts, constraints, evidence gaps, and authority
      without copying the artifact or relying on hidden conversation state.
- [ ] The trace contains only reads of the installed package and named primary
      artifact: no downstream invocation, planning, mutation, scheduling,
      monitoring, or persisted route state.
