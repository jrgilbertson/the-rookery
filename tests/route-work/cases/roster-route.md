# An implementation-bound issue gets a lead, executors, and only supplied bounds

Provenance: user feedback — a plan-only route was too limiting; the card must
estimate the pattern and roster for the whole approach and let supplied
authority alone bound how far the lead carries it. A later review found
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
      ce-plan on Fable 5.1 at medium" and names no role. Why says planning
      comes first and the lead carries the work into implementation.
- [ ] Item 1's Setup lists a Lead on Fable 5.1 at medium and two Executors on
      Grok 4.6 at high, one per named module, and no Reviewer. It states that
      merge authority was not supplied and mentions no orchestration or plan
      storage. Isolation may be named for concurrent Executor writes.
- [ ] Item 2's Setup adds a Reviewer on GPT-5.6 Sol at high, hands it the
      acceptance criteria, and keeps the rest of item 1's roster.
- [ ] Item 3 budgets at most five concurrent workers including the Lead and
      Reviewer: at most three Executors, with the remaining modules queued
      rather than dropped. Setup and kickoff agree on the complete roster.
- [ ] Each kickoff starts ce-plan from the issue URL, states the lead's model
      and effort, repeats every other role with model, effort, and count,
      treats the issue as the source of truth, and withholds merge in one
      sentence. No kickoff narrates phases, checkpoints, PR cadence, or a
      stopping point for the lead's work; the Reviewer's one-round guardrail
      is expected, not a stopping point.
- [ ] The trace contains only reads of the installed package.
