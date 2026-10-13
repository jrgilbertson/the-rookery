# Match the model to the work

Choose a model and how much time it should spend thinking based on the work you need done. Use the tools and subscriptions available to you. [WORKFLOWS.md](WORKFLOWS.md) explains the workflows.

## What each role needs

### Planner

Decide what needs to be done, what it depends on, and how we'll know it's finished. The agent that writes the plan can also organize the work.

### Executor

Make the changes or find and fix the problem. Use tests and other checks to show that the result works.

### Reviewer

Check whether the work meets the agreed requirements. Review it in a separate session, without relying on the discussion that produced it.

### Design/taste

Check how the finished interface looks and whether it's easy to use. Use comparisons based on people's preferences to help choose a model. More thinking time does not automatically produce a better design.

## Model recommendations

**Last reviewed: 2026-10-13**

| Work | Primary or rule | Secondary | Tertiary |
|---|---|---|---|
| Planner | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6.1-sol` / high | Google / `gemini-4-argon` / high |
| Executor | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / medium | — |
| Reviewer | [Different-provider Executor](#reviewer) | — | — |
| Design/taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | Google / `gemini-4-argon` / high |

Design/taste choices follow published comparisons and list the tested effort settings, though I usually run the models at their Executor or Planner settings.

Treat Argon as a tentative choice for planning and design. Each row lists at most one model from each provider. A slot can stay empty.

## Work alone, delegate, or hand off

One session usually owns the work and makes sure it gets finished. Add Executors when parts of the work can be done separately. Use orchestration tools to supervise those agents. Hand off the work when another session should take over.

To check correctness, read the Executor row from left to right and choose the first available model from a different provider than the one that did the work. Keep that model's listed effort setting. If only one provider is available, use a separate review session. For look and feel, use the Design/taste recommendations.

## Choose effort and tools

Choose for the result you need. A planning model should work through decisions and break the work into clear steps. An Executor should make changes that work. A Reviewer should judge the result independently. A design model should produce an interface that looks good and is easy to use.

Start with the effort setting in the table and change it when the task calls for it. More thinking should improve the result enough to justify the extra time and usage. Costs measured through an API do not tell you how much of your subscription allowance a task will use. I prefer each provider's official tools, signed in through my subscription.

## Why these models

- Planner: Opus high and Sol high balance reasoning quality and cost. Argon high gives another provider to choose from. Few results directly measure how well these models plan.
- Executor: Opus medium and Sol medium balance the quality of code changes, cost, and time. Argon's measured coding cost is too high to recommend it as a regular backup.
- Design/taste: Published comparisons based on people's preferences tested Opus and Sol at max. Early results support Argon high for interface work. We still lack comparisons that measure quality, cost, and time at different effort settings under the same conditions.

These choices draw on [FrontierCode](https://cognition.com/frontiercode), [AA coding-agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), and [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend).

## Keep the table current

Check results for the exact model release and the kind of work it will do. Use independent comparisons and consider quality, cost per task, and time together. Missing results mean we don't know yet. Maximum effort is not automatically the best choice.

Update the table, review date, and reasons together. The [evaluation procedure](docs/model-evaluations.md) explains which sources to use, how to compare effort settings, and how to recommend a model when the evidence is incomplete.
