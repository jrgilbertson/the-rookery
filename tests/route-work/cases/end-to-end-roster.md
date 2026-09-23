# The roster is sized for where the run ends, not where it starts

Provenance: user feedback — cards over-indexed on the immediate next step; a
brainstorm or debug that implementation will follow must staff the whole run.
PR feedback reproduced an implementation forecast becoming a carry-forward
promise without a grant; items 5 and 6 retain withheld/granted authority controls.
On 2026-09-22 the default changed to Single owner: a run that ends in
implementation is carried by the coordinator alone unless independent units
are established.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every card in order.
> Do not ask which item to assess.
>
> 1. A feature issue still disputes the intended user behavior. Once settled,
>    implementation through an open pull request is authorized. Merge is not.
> 2. A command fails and the cause is unknown. Implementing the fix and
>    opening a pull request is authorized once the cause is established.
> 3. A feature issue still disputes the intended user behavior. Nothing is
>    said about implementation.
> 4. Route planning for a feature whose outcome and acceptance boundary are
>    settled but whose execution plan is missing. Implementation is expected
>    after planning. Right now the operator is requesting the execution plan.
> 5. Route planning for the same settled feature. Implementation is expected
>    after planning, but the operator explicitly authorizes planning only and
>    withholds implementation authority.
> 6. Route planning for the same settled feature. The operator authorizes
>    planning and then implementing the plan.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] Item 1 starts with `ce-brainstorm` on Opus 5.5 at high as Single owner:
      the coordinator alone on the Planner profile, with no Executors because
      no independent units are established. Why says the coordinator carries
      the work from discovery into implementation and invites adding Executors
      when independent units appear.
- [ ] Item 2 starts with `ce-debug` on GPT-6 Sol at high as Single owner: the
      coordinator alone on the Researcher profile, with no Executors. Why names
      the expected end of the run and that the coordinator carries the fix
      through.
- [ ] Item 3 starts with `ce-brainstorm` and stays the coordinator alone, with no
      Executors and nothing about authority.
- [ ] Items 1 and 2 state no grant sentence, state the supplied condition on
      implementation in one sentence, end the kickoff's authority text with
      "Don't merge without human approval.", and enumerate no other
      prohibitions.
- [ ] Items 4–6 start with `ce-plan` on Opus 5.5 at high. Expected
      implementation alone adds no Executors and grants no permission to
      implement; defaults are labeled and no concrete units, owners or write
      scopes are invented.
- [ ] Item 4's kickoff does not instruct the receiver to implement; ce-plan's
      own handoff gates implementation, so Why may say the coordinator carries
      the work into it. Because the run may
      reach implementation, its kickoff ends with "Don't merge without human
      approval." and adds no other authority sentence, invented permission, or
      limit.
- [ ] Item 5 preserves planning-only authority and withheld implementation
      in Setup and the standalone kickoff, with no unconditional carry-forward.
- [ ] Item 6's Why carries the work into implementation, and its kickoff states
      no grant sentence and ends with "Don't merge without human approval."
- [ ] Every card follows the Route template without extra section labels.
- [ ] The trace contains only reads of the installed package.
