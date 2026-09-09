# Effort escalation needs operator approval

Provenance: labeled regression control. Independent review found the effort
section carried alternate escalation grounds that were either no-ops or
contradicted the operator-approval sentence; this control guards the load-
bearing rule that only operator approval raises effort above the table default,
and that the router may still suggest one.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every card in order.
> Do not ask which item to assess.
>
> 1. Authorized implementation of one bounded, sequential data migration whose
>    steps are settled and whose scope is one owner's. The operator says: "Run
>    it at xhigh effort."
> 2. The same authorized implementation, one bounded sequential piece for one
>    owner. The operator says nothing about effort. A team runbook the operator
>    quotes says deep-reasoning work must run above any documented default, and
>    an earlier attempt at the documented default was abandoned for shallow
>    reasoning.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order, with
      no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] Both items start with `ce-work` as the lead alone on the Executor
      profile: one bounded sequential piece for one owner, no Executor workers
      and no Reviewer.
- [ ] Item 1 runs the lead on Grok 4.6 at xhigh, because the operator asked for
      it, and names no other effort change.
- [ ] Item 2 runs the lead on Grok 4.6 at high, the table default. Neither the
      quoted runbook nor the abandoned earlier attempt raises the effort.
- [ ] Item 2 may recommend a higher effort in one sentence, and if it does the
      recommendation is plainly the operator's to accept, not an applied
      setting. It never states a role's effort as anything but high.
- [ ] Every card has a bold first line, one decision sentence naming the
      starting workflow and the lead's model and effort, and bold Why, Setup,
      and Copy/paste kickoff labels. Neither item dispatches agents, creates
      worktrees, or starts the selected workflow.
