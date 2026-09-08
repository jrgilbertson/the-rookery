# The roster is sized for where the run ends, not where it starts

Provenance: user feedback — cards over-indexed on the immediate next step; a
brainstorm or debug that implementation will follow must staff the whole run.
PR feedback reproduced an implementation forecast becoming a carry-forward
promise without a grant; items 5 and 6 retain withheld/granted authority controls.

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
- [ ] Item 1 starts with `ce-brainstorm` on Fable 5.1 at medium and its Setup
      lists a Lead on Fable 5.1 at medium plus Executors on Grok 4.6 at high,
      up to three, with the pattern Lead + Executors. Why says the lead carries
      the work from discovery into implementation, so the roster covers that
      work rather than only the brainstorm.
- [ ] Item 2 starts with `ce-debug` on GPT-5.6 Sol at high as the lead and
      its Setup lists up to three Executors on Grok 4.6 at high. No supplied
      evidence establishes a single bounded fix. Why names the expected end
      of the run and that the lead carries the fix through.
- [ ] Item 3 starts with `ce-brainstorm` and stays the lead alone, with no
      Executors and nothing about authority.
- [ ] Items 1 and 2 state the supplied merge or pull-request authority in one
      sentence and enumerate no other prohibitions.
- [ ] Items 4–6 start with `ce-plan` on Fable 5.1 at medium. Expected
      implementation may size a Lead + Executors roster without granting
      permission to implement; defaults are labeled and no concrete units,
      owners or write scopes are invented.
- [ ] Item 4 does not promise unconditional implementation by this lead or
      instruct a receiver to implement without a grant. It adds no authority
      sentence, invented permission or limit when authority is unstated.
- [ ] Item 5 preserves planning-only authority and withheld implementation
      in Setup and the standalone kickoff, with no unconditional carry-forward.
- [ ] Item 6 preserves planning and implementation authority in Setup and the
      standalone kickoff and permits carry-forward into implementation.
- [ ] Every card follows the Route template without extra section labels.
- [ ] The trace contains only reads of the installed package.
