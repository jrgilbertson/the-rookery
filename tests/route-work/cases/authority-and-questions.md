# Questions, availability, and authority resolve cleanly

Provenance: user feedback — routing asks the smallest independent question
batch, ordered by impact with recommended answers, and copies only supplied
authority.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every card in order.
> Do not ask which item to assess.
>
> 1. An issue-shaped request could mean tracker cleanup or implementing an
>    accepted change. The operator has answered one question so far: the
>    tracker is correct and the work is outside it. Nothing has been said about
>    whether the product outcome is settled.
> 2. The same request. The operator has answered that the tracker is correct
>    and that the outcome and acceptance boundary are settled, with no
>    execution plan yet. Implementation is authorized.
> 3. The same initial request, but the operator says they cannot determine
>    whether tracker truth or source implementation must change.
> 4. A named primary plan cannot be read.
> 5. `ce-plan` is selected and available. Its primary Lead profile is stated
>    unavailable; availability of the other profiles is unknown.
> 6. All three Lead profiles are stated unavailable.
> 7. The selected workflow itself is stated unavailable.
> 8. Two separate invocations. First, a grill of a supplied decision document
>    is requested without document-write authority. Second, an implementation
>    is authorized but commit and publication are unstated.
> 9. Two coequal workstreams, the parser rewrite and the CLI cleanup, have no
>    dependency order. The operator says the work should move to a separate
>    worktree but has not said whether the current agent should supervise it
>    through Orca or fully hand off ownership.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] Item 1 returns a Questions card with exactly one question, whether the
      product outcome is settled, and no route.
- [ ] Item 2 returns a Route starting with ce-plan on Fable 5.1 at medium with
      a roster of Lead plus up to three Executors on Grok 4.6 at high.
- [ ] Items 3, 4, 6, and 7 each return a Questions card that asks for the
      missing fact, artifact, profile, or workflow with a recommended answer
      and names no workflow, model, role profile, or kickoff, including in
      its recommendation.
- [ ] Item 5 keeps ce-plan, selects the secondary Lead profile, GPT-5.6 Sol at
      high, and says the primary is unavailable without calling the secondary
      unverified.
- [ ] Item 8 renders two Route cards. The grill states its supplied
      document-write limit; the implementation grants implementation only and
      lists no unsupplied permissions.
- [ ] Item 9 returns one Questions card with exactly two numbered questions,
      owner order first and orchestration versus handoff second, each with a
      concrete recommended answer that names a workstream or a choice.
- [ ] No item probes availability, persists state outside the visible
      conversation, performs downstream discovery, or escalates effort.
