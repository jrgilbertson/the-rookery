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

**Last reviewed: Planner and Executor 2026-11-06; Design/taste 2026-10-29**

| Work | Primary or rule | Secondary | Tertiary |
|---|---|---|---|
| Planner | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6-astra` / high | — |
| Executor | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / high | — |
| Reviewer | [Different-provider Executor](#reviewer) | — | — |
| Design/taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | — |

Design/taste choices follow published comparisons and list the tested effort settings, though I usually run the models at their Executor or Planner settings.

I leave Gemini out because I don't have the right Antigravity account to use it. Each row lists at most one model from each provider. A slot can stay empty.

### Why these models

- Planner: Astra high replaces Sol high as the OpenAI choice. I accept its higher benchmark task cost for stronger general reasoning at moderate effort; this is a provisional planning judgment, not a measured improvement in plans. Opus high stays first: AA-Briefcase v1.1 favors it over Astra high on analytical quality and rubric coverage, despite Astra's higher overall Intelligence Index. Opus results allow fallback to another model. Sol remains a credible cheaper planner, especially at xhigh or max; Astra high offers a stronger overall index than Sol xhigh and a similar index to Sol max with less estimated inference time. Revisit when exact-release comparisons measure plan quality and downstream success with the same executor, or subscription usage changes the tradeoff.
- Executor: Sol high stays the OpenAI choice. FrontierCode 2.0 gives Astra high a modest quality gain at much higher cost per pass; Sol max exceeds Astra high's quality and pass rate for less money. VulcanBench finds almost identical quality and correctness for Astra high and Sol high, with Astra faster but more expensive. Sol high improves on medium in every listed VulcanBench measure; higher efforts bring little extra quality there and no extra passes. I retain Opus medium first for my subscription economics and its higher judged code quality, with some runs falling back to Opus 4.8. Revisit when harder repeated tests justify higher effort, fallback-free comparisons change the result, or subscription costs change.
- Design/taste: Opus max leads Arena's frontend preferences. Sol max stays provisional: Arena favors Astra, while OpenDesign's prototype results favor Sol on quality, cost, and time. OpenDesign omits effort settings, so those results cannot establish the cost of Sol max. Revisit when comparable tests measure visual preference, cost, and time at lower efforts. We don't yet know the best balance of quality, cost, and time.

These choices draw on the [AA Intelligence Index](https://artificialanalysis.ai/leaderboards/models), [FrontierCode](https://cognition.com/frontiercode), [AA coding-agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), [VulcanBench](https://vulcanbench.com/leaderboard.html), [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend), and [OpenDesign](https://open-design.ai/llm-arena-for-design/).

### Planning and execution tradeoffs

AA Intelligence Index v5.0.1 results, observed 2026-11-06. Cost is AA's weighted API-equivalent task cost; time is estimated inference time, not measured completion time for a planning session. The index combines knowledge work, coding, science, and general knowledge; it is not a pass rate. Values below are rounded; effort gains use the underlying precision.

| Model / effort | Intelligence Index | $ / task | Minutes / task |
|---|---:|---:|---:|
| Sol 6.1 / high | 50.33 | 0.59 | 7.0 |
| Sol 6.1 / xhigh | 52.46 | 0.76 | 10.0 |
| Sol 6.1 / max | 54.61 | 1.27 | 22.1 |
| Astra / medium | 51.55 | 2.73 | 6.5 |
| Astra / high | 54.85 | 3.24 | 9.0 |
| Astra / xhigh | 55.31 | 3.66 | 10.5 |
| Astra / max | 56.85 | 6.24 | 20.9 |
| Opus 5.5 / medium | 48.21 | 2.45 | 6.8 |
| Opus 5.5 / high | 51.84 | 3.46 | 9.4 |
| Opus 5.5 / xhigh | 57.44 | 6.05 | 16.2 |
| Opus 5.5 / max | 59.11 | 10.04 | 26.6 |

For Astra, medium → high adds 3.30 index points for $0.51 (+19%) and 2.46 minutes (+38%): $0.15 and 0.75 minutes per point. High → xhigh adds only 0.46 points for $0.42 (+13%) and 1.48 minutes (+16%): $0.92 and 3.25 minutes per point. Xhigh → max adds 1.55 points for $2.59 (+71%) and 10.41 minutes (+99%): $1.67 and 6.73 minutes per point. High is the provisional balance. Compared with Sol high, Astra high costs $2.65 more per task, bringing its total cost to about 5.5 times as much, for 4.52 points and 2.00 extra minutes.

For Opus, high → xhigh adds 5.61 points for $2.58 (+75%) and 6.79 minutes (+72%): $0.46 and 1.21 minutes per point. Xhigh is a credible upgrade; high uses less estimated inference time. Actual planning-time and quality gains remain unmeasured.

The planning proxies disagree. [AA-Briefcase v1.1](https://artificialanalysis.ai/evaluations/aa-briefcase) analytical-quality Elo is 1968 for Opus high, 1672 for Astra high, and 1652 for Sol high; Astra and Sol's confidence intervals overlap. Sol xhigh reaches 1691 and max 1764. GDP.pdf also slightly favors Sol high, 32% versus Astra high's 31%. These AA components are not independent confirmations. [ARC Prize's Astra results](https://arcprize.org/results/openai-gpt-6) and [Sol 6.1 results](https://arcprize.org/results/openai-gpt-6-1-sol) favor Astra high on ARC-AGI-3: 54.8% versus 26.7% under the Standard harness, narrowing to 99.9% versus 95.0% with the Provider Adapter. Puzzle performance does not establish repository plan quality.

For execution, [FrontierCode 2.0](https://cognition.com/frontiercode) reports Sol high at 34.82 quality points, 38.03% passing, and $0.647 per rollout: **$1.70 per pass**. Astra high reaches 38.31 points and 41.36% passing at $4.277: **$10.34 per pass**. Sol max reaches 38.95 points and 42.27% passing at $1.029: **$2.43 per pass**. High → max buys 4.13 points for $0.382 (+59%), or $0.093 per point. Runtime is unpublished. Binary pass rates and blended quality scores are separate measures.

[VulcanBench's Sol report](https://vulcanbench.com/benchmarks/swe-v4-gpt61-sol-v318.html) gives high 23/23 passes at $0.33 and 10.22 minutes per task. Xhigh adds 0.55 combined-score points for $0.10 (+32%) and 5.15 minutes (+50%), with no additional passes. [Astra high](https://vulcanbench.com/benchmarks/swe-v4-astra-fable51-v34.html) also passes 23/23 with nearly identical combined quality, at $1.71 and 4.90 minutes. Its cost estimate has a $3.22 upper bound for unresolved long-context charges. This small suite mixes correctness with model-judged quality; [Opus medium](https://vulcanbench.com/benchmarks/swe-v4-opus55-v315.html) includes older-model replies in 3/23 runs. AA's coding-agent comparison covers Sol and Astra only at max, with an older FrontierCode component, so cannot establish high-effort performance. API-equivalent costs do not measure subscription allowance use.

## Work alone, delegate, or hand off

One session usually owns the work and makes sure it gets finished. Add Executors when parts of the work can be done separately. Use orchestration tools to supervise those agents. Hand off the work when another session should take over.

## Choose effort and tools

Start with the effort setting in the table and change it when the task calls for it. More thinking should improve the result enough to justify the extra time and usage. Costs measured through an API do not tell you how much of your subscription allowance a task will use. I prefer each provider's official tools, signed in through my subscription.

## Keep the table current

To refresh the model recommendations, follow the [evaluation procedure](docs/model-evaluations.md) for source selection, effort comparisons, and incomplete evidence. Update the table, review date, reasons, sources, and revisit conditions together in [Model recommendations](#model-recommendations).
