# An implementation-bound issue with named modules gets a coordinator, executors, and only supplied bounds

Provenance: user feedback — a plan-only route was too limiting; the card must
estimate the pattern and roster for the whole approach and let supplied
authority alone bound how far the coordinator carries it. A later review found
that adding a Reviewer could exceed the five-worker concurrency ceiling.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every card in order.
> Do not ask which item to assess.
>
> 1. GitHub issue `https://github.com/example/parser/issues/97` holds approved
>    requirements for a parser fix and no execution plan. The fix touches the
>    tokenizer module and the error-reporting module, which do not share files.
>    Implementation through an open pull request is authorized. Merge is not.
> 2. The same issue and authority, and the issue also lists three explicit
>    acceptance criteria that a reviewer can check.
> 3. The same authority and criteria, but the issue names five independent
>    modules: tokenizer, error reporting, serializer, diagnostics, and CLI.
>    All five must be implemented; a Reviewer joins the roster.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] All items return a `**Route**` card whose decision line is "Start with
      ce-plan on Opus 5.5 at high" and names no role. Why says planning
      comes first and the coordinator carries the work into implementation.
- [ ] Item 1's Setup lists a coordinator on Opus 5.5 at high and two Executors on
      Opus 5.5 at medium, one per named module, and no Reviewer. It mentions no
      orchestration, worktree isolation, or plan storage.
- [ ] Item 2 adds no Reviewer, because the run implements through `ce-work`,
      which runs its own review, and keeps item 1's roster.
- [ ] Item 3's Setup lists one Executor per named module, five in all, plus the
      Reviewer, with no concurrency cap or queue.
- [ ] Each kickoff starts ce-plan from the issue URL, states the coordinator's model
      and effort, repeats the Reviewer's model and effort where there is one,
      gives the implementation workers' model and effort without a count or
      scheduling,
      treats the issue as the source of truth, and ends its authority text with
      "Don't merge without human approval." No kickoff narrates phases, checkpoints, PR cadence, or a
      stopping point for the coordinator's work; the Reviewer's one-round guardrail
      is expected, not a stopping point.
- [ ] The trace contains only reads of the installed package.
