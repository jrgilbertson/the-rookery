# Match the model to the work

Choose a model and how much time it should spend thinking based on the work you need done. Use the tools and subscriptions available to you. To choose a workflow, see [WORKFLOWS.md](WORKFLOWS.md).

## How I compare models

Compare quality, cost per task, and completion time at the effort settings that were tested. These two calculations help when comparable measurements are available.

**Cost per pass = average cost per attempt ÷ pass rate.** At $0.60 per attempt and a 60% pass rate, the calculation is $0.60 ÷ 0.60 = **$1.00 per pass**. This also equals total spend divided by successful attempts, using the same set of attempts. Use actual pass/fail results for this calculation.

**Cost per additional quality point = increase in task cost ÷ increase in quality score.** Moving from 48 points at $0.21 to 50 points at $0.32 costs $0.11 ÷ 2 = **$0.055 per additional point**. Compare positive gains within the same benchmark and scoring method.

Keep the original quality, success rate, and time alongside these figures. Choose an effort setting whose added quality justifies its cost and time. Missing measurements remain unknown. For comparison rules and choices with incomplete evidence, follow the [evaluation procedure](docs/model-evaluations.md#compare).

## What each role needs

### Planner

Decide what needs to be done and break it into steps. Identify what the work depends on and how we'll know it's finished. The agent that writes the plan can also organize the work.

### Executor

Make the changes or find and fix the problem. Use tests and other checks to show that the result works.

### Reviewer

Check whether the work meets the agreed requirements. Review it in a separate session, without relying on the discussion that produced it.

Read the Executor row from left to right and choose the first available model from a different provider than the one that did the work. Keep that model's listed effort setting. If only one provider is available, use a separate review session. For look and feel, use the Design/taste recommendations.

### Design/taste

Produce or assess an interface that looks good and is easy to use. Use comparisons based on people's preferences to help choose a model. More thinking time does not automatically produce a better design.

## Model recommendations

**Last reviewed: 2026-10-29**

| Work | Primary or rule | Secondary | Tertiary |
|---|---|---|---|
| Planner | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6.1-sol` / high | — |
| Executor | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / high | — |
| Reviewer | [Different-provider Executor](#reviewer) | — | — |
| Design/taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | — |

Design/taste choices follow published comparisons and list the tested effort settings, though I usually run the models at their Executor or Planner settings.

I leave Gemini out because I don't have the right Antigravity account to use it. Each row lists at most one model from each provider. A slot can stay empty.

### Why these models

- Planner: Opus high and Sol high are provisional choices based mainly on AA's reasoning and knowledge-work results and effort costs. These results do not establish which model writes better plans or whether high is the best effort for planning. The Opus runs allow fallback to another model. Revisit when comparisons for these releases measure plan quality, cost, and time, and test how well the plans work with the same executor and effort setting.
- Executor: I put Opus medium first because my subscription makes it cheaper for me. Published API-cost comparisons favor Sol high. In VulcanBench, Sol high improves on medium in quality, pass rate, cost, and time; FrontierCode shows a quality gain but higher cost per pass. Opus medium earns higher judged code-quality scores in VulcanBench, where some runs fall back to an older model. Revisit when subscription costs change, comparable runs clarify effort tradeoffs without fallback, or another provider offers a credible substitute at a reasonable task cost.
- Design/taste: Opus max leads Arena's frontend preferences. Sol max stays provisional: Arena favors Astra, while OpenDesign's prototype results favor Sol on quality, cost, and time. OpenDesign omits effort settings, so those results cannot establish the cost of Sol max. Revisit when comparable tests measure visual preference, cost, and time at lower efforts. We don't yet know the best balance of quality, cost, and time.

These choices draw on the [AA Intelligence Index](https://artificialanalysis.ai/leaderboards/models), [FrontierCode](https://cognition.com/frontiercode), [AA coding-agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), [VulcanBench](https://vulcanbench.com/leaderboard.html), [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend), and [OpenDesign](https://open-design.ai/llm-arena-for-design/).

## Work alone, delegate, or hand off

One session usually owns the work and makes sure it gets finished. Add Executors when parts of the work can be done separately. Use orchestration tools to supervise those agents. Hand off the work when another session should take over.

## Choose effort and tools

Start with the effort setting in the table and change it when the task calls for it. More thinking should improve the result enough to justify the extra time and usage. Costs measured through an API do not tell you how much of your subscription allowance a task will use. I prefer each provider's official tools, signed in through my subscription.

## Keep the table current

To refresh the model recommendations, follow the [evaluation procedure](docs/model-evaluations.md) for source selection, effort comparisons, and incomplete evidence. Update the table, review date, reasons, sources, and revisit conditions together in [Model recommendations](#model-recommendations).
