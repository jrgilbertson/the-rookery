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

Produce or assess an interface that looks good and is easy to use. Use comparisons based on people's preferences to help choose a model. This role is more subjective than the others, so I also use my own judgment when a release has no preference results yet. More thinking time does not automatically produce a better design.

## Model recommendations

**Last reviewed: 2026-11-09**

| Work | Primary or rule | Secondary | Tertiary |
|---|---|---|---|
| Planner | Anthropic / `claude-fable-5-2` / high | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6-astra` / high |
| Executor | Anthropic / `claude-opus-5-5` / high | Anthropic / `claude-fable-5-2` / high | OpenAI / `gpt-6.1-sol` / high |
| Reviewer | [Different-provider Executor](#reviewer) | — | — |
| Design/taste | Anthropic / `claude-fable-5-2` / high | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max |

Design/taste choices follow published comparisons and list the tested effort settings, though I usually run the models at their Executor or Planner settings. No comparison has tested Fable 5.2, so its Design/taste entry shows the high setting I run.

I leave Gemini out because I don't have the right Antigravity account to use it. Each row lists at most one model from each provider. Fable is the exception. Claude's [help center](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) caps Fable at half of a plan's weekly limit, and its usage counts against the limit the other Claude models share. A row can therefore name the Claude model to use once the Fable cap is reached. A slot can stay empty.

### Why these models

- Planner: Fable 5.2 high becomes first. This is a provisional planning judgment, not a measured improvement in plans. Its Intelligence Index is 9.99 points above Opus high, and it scores above Astra and Sol on ARC-AGI-3. AA-Briefcase v1.1 gives Fable high and Opus high about the same overall Elo, with Fable ahead on rubric coverage and Opus ahead on analytical quality. I accept Fable's higher benchmark task cost and about 8 more minutes of estimated inference time. Its weekly cap bounds that cost, and Opus high takes over when the cap is reached. I chose high for its 5.41-point index gain over medium; xhigh adds only 0.39 more. Opus high moves to second and remains the better choice for analysis-heavy plans, where Briefcase favors it. Astra high stays the OpenAI choice for stronger general reasoning than Sol at moderate effort, despite its higher benchmark task cost. Fable and Opus results allow fallback to another model. Sol remains a credible cheaper planner, especially at xhigh or max; Astra high offers a stronger overall index than Sol xhigh and a similar index to Sol max with less estimated inference time. Revisit when exact-release comparisons measure plan quality and downstream success with the same executor, or subscription usage changes the tradeoff.
- Executor: Opus 5.5 stays first and moves from medium to high. Fable 5.2 high joins as second, for the hardest work and for when Opus high falls short. Opus is first on cost and time. On FrontierCode 2.0, Opus high costs $6.40 per pass against $17.01 for Fable high, and AA estimates about half the inference time per task. Both models draw on the same weekly limit, so that cost counts against my allowance too. The stronger pass rate puts Fable second: 49.39% of FrontierCode tasks, against 37.88% for Opus high and 33.03% for Opus medium, at about 20 minutes per rollout. AA's Terminal-Bench 4.0 run shows a smaller gap in the same direction. The claude.dev [model guide](https://claude.dev/blog/which-claude-model-should-you-build-with/) gives the same order. It is provider guidance and does not decide the order here, and it starts Opus at medium where I run high. High is Fable's largest step. Xhigh costs $2.44 per additional quality point, and max scores below xhigh. I base Opus high on the same two tests. VulcanBench does not support it: high passed 22/23 against medium's 23/23, and Opus 4.8 wrote more of the replies. Sol high stays the OpenAI choice. FrontierCode 2.0 gives Astra high a modest quality gain at much higher cost per pass; Sol max exceeds Astra high's quality and pass rate for less money. VulcanBench finds almost identical quality and correctness for Astra high and Sol high, with Astra faster but more expensive. Sol high improves on medium in every listed VulcanBench measure; higher efforts bring little extra quality there and no extra passes. Revisit when VulcanBench tests Fable 5.2, fallback-free comparisons change the result, or subscription costs change.
- Design/taste: Fable 5.2 high becomes first as a judgment call. Arena, Design Arena, and OpenDesign had not listed it as of 2026-11-09, so its rank and its effort are unmeasured. I put it first for two reasons. Arena [ranked Fable 5 first on frontend](https://x.com/arena/status/2064858698582040693) when it arrived, and [Fable 5.1 max gained 137 points on Fable 5](https://x.com/arena/status/2095544323622551802). One early [screenshot-to-HTML comparison](https://news.ycombinator.com/item?id=50429906) also judged Fable 5.2 truer to the source design than Opus 5.5, though readers found layout mistakes in the Fable build. Neither a predecessor's rank nor one comparison establishes this release's quality. Opus max moves to second and remains the measured leader on Arena's frontend preferences, 85 points ahead of Fable 5.1 max. Sol max stays provisional: Arena favors Astra, while OpenDesign's prototype results favor Sol on quality, cost, and time. OpenDesign omits effort settings, so those results cannot establish the cost of Sol max. Revisit when Arena lists Fable 5.2; if it ranks below Opus 5.5 max, Opus returns to first. Also revisit when comparable tests measure visual preference, cost, and time at lower efforts. We don't yet know the best balance of quality, cost, and time.

These choices draw on the [AA Intelligence Index](https://artificialanalysis.ai/leaderboards/models), [FrontierCode](https://cognition.com/frontiercode), [AA coding-agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), [VulcanBench](https://vulcanbench.com/leaderboard.html), [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend), and [OpenDesign](https://open-design.ai/llm-arena-for-design/).

### Planning and execution tradeoffs

AA Intelligence Index v5.0.1 results, observed 2026-11-09. Cost is AA's weighted API-equivalent task cost; time is estimated inference time, not measured completion time for a planning session. The index combines knowledge work, coding, science, and general knowledge; it is not a pass rate. Values below are rounded; effort gains use the underlying precision.

| Model / effort | Intelligence Index | $ / task | Minutes / task |
|---|---:|---:|---:|
| Sol 6.1 / high | 50.33 | 0.59 | 6.6 |
| Sol 6.1 / xhigh | 52.46 | 0.76 | 9.3 |
| Sol 6.1 / max | 54.61 | 1.27 | 20.2 |
| Astra / medium | 51.55 | 2.73 | 6.9 |
| Astra / high | 54.85 | 3.24 | 9.9 |
| Astra / xhigh | 55.31 | 3.66 | 11.6 |
| Astra / max | 56.85 | 6.24 | 22.6 |
| Opus 5.5 / medium | 48.21 | 2.45 | 7.1 |
| Opus 5.5 / high | 51.84 | 3.46 | 9.5 |
| Opus 5.5 / xhigh | 57.44 | 6.05 | 16.3 |
| Opus 5.5 / max | 59.11 | 10.04 | 25.1 |
| Fable 5.2 / low | 53.92 | 3.10 | 6.5 |
| Fable 5.2 / medium | 56.41 | 3.80 | 8.3 |
| Fable 5.2 / high | 61.82 | 9.08 | 17.7 |
| Fable 5.2 / xhigh | 62.22 | 14.83 | 26.3 |
| Fable 5.2 / max | 64.56 | 26.54 | 45.0 |

For Fable 5.2, medium → high adds 5.41 index points for $5.28 (+139%) and 9.37 minutes (+113%): $0.97 and 1.73 minutes per point. High → xhigh adds only 0.39 points for $5.75 (+63%) and 8.63 minutes (+49%): $14.56 and 21.85 minutes per point. Xhigh → max adds 2.35 points for $11.71 (+79%) and 18.76 minutes (+71%): $4.99 and 8.00 minutes per point. High is the balance because it is the last large step. Compared with Opus high, Fable high costs $5.61 more per task, about 2.6 times as much, for 9.99 points and 8.11 extra minutes. It also scores 2.72 points above Opus max for less cost and time.

For Astra, medium → high adds 3.30 index points for $0.51 (+19%) and 2.95 minutes (+43%): $0.15 and 0.90 minutes per point. High → xhigh adds only 0.46 points for $0.42 (+13%) and 1.75 minutes (+18%): $0.92 and 3.84 minutes per point. Xhigh → max adds 1.55 points for $2.59 (+71%) and 10.96 minutes (+95%): $1.67 and 7.08 minutes per point. High is the provisional balance. Compared with Sol high, Astra high costs $2.65 more per task, bringing its total cost to about 5.5 times as much, for 4.52 points and 3.29 extra minutes.

For Opus, high → xhigh adds 5.61 points for $2.58 (+75%) and 6.72 minutes (+70%): $0.46 and 1.20 minutes per point. Xhigh is a credible upgrade; high uses less estimated inference time. Actual planning-time and quality gains remain unmeasured.

The planning proxies disagree. [AA-Briefcase v1.1](https://artificialanalysis.ai/evaluations/aa-briefcase) analytical-quality Elo is 1968 for Opus high, 1845 for Fable high, 1672 for Astra high, and 1652 for Sol high; Astra and Sol's confidence intervals overlap. Sol xhigh reaches 1691 and max 1764. Fable high and Opus high have about the same combined Briefcase Elo, 1677 and 1682, with overlapping intervals. Fable passes more rubric criteria, 62.9% versus 58.9%. Opus leads analytical quality by 123 Elo. Fable high's Briefcase tasks cost $15.49 against Opus high's $6.27. GDP.pdf also slightly favors Sol high, 32% versus Astra high's 31%; Opus high scores 28.8% and Fable high 21.8%. These AA components are not independent confirmations. [ARC Prize's Astra results](https://arcprize.org/results/openai-gpt-6) and [Sol 6.1 results](https://arcprize.org/results/openai-gpt-6-1-sol) favor Astra high on ARC-AGI-3: 54.8% versus 26.7% under the Standard harness, narrowing to 99.9% versus 95.0% with the Provider Adapter. [Fable 5.2 high](https://arcprize.org/results/anthropic-claude-fable-5-2) reaches 79.3% under the Standard harness and 97.7% with the Provider Adapter; ARC lists no ARC-AGI-3 result for Opus 5.5. Puzzle performance does not establish repository plan quality.

For execution, [FrontierCode 2.0](https://cognition.com/frontiercode) reports Sol high at 34.82 quality points, 38.03% passing, and $0.647 per rollout: **$1.70 per pass**. Astra high reaches 38.31 points and 41.36% passing at $4.277: **$10.34 per pass**. Sol max reaches 38.95 points and 42.27% passing at $1.029: **$2.43 per pass**. High → max buys 4.13 points for $0.382 (+59%), or $0.093 per point. Binary pass rates and blended quality scores are separate measures.

On the same benchmark, Fable 5.2 high reaches 45.29 quality points and 49.39% passing at $8.402 per rollout: **$17.01 per pass**. Opus high reaches 34.53 points and 37.88% passing at $2.423: **$6.40 per pass**. Opus medium reaches 30.10 points and 33.03% passing at $1.699: **$5.14 per pass**. Opus medium → high buys 4.43 points for $0.724 (+43%), or $0.163 per point. Fable medium → high buys 7.70 points for $5.299 (+171%) and 10.8 minutes (+113%): $0.69 and 1.40 minutes per point. Fable high → xhigh buys 3.82 points for $9.332 (+111%) and 16.9 minutes (+83%): $2.44 and 4.42 minutes per point. Fable max scores 3.46 points below xhigh at about three times the cost. Fable high matches Opus max, 45.45 points and 49.70% passing, for 34% less. Cognition publishes runtime only for Fable 5.2, which takes 20.4 minutes per rollout at high. AA's own FrontierCode 2.0 runs show the same ordering and are not an independent benchmark. AA's Terminal-Bench 4.0 component gives Fable high 59.6% at $13.47 per task and Opus high 56.6% at $5.12, a gap of two of its 66 tasks.

[VulcanBench's Sol report](https://vulcanbench.com/benchmarks/swe-v4-gpt61-sol-v318.html) gives high 23/23 passes at $0.33 and 10.22 minutes per task. Xhigh adds 0.55 combined-score points for $0.10 (+32%) and 5.15 minutes (+50%), with no additional passes. [Astra high](https://vulcanbench.com/benchmarks/swe-v4-astra-fable51-v34.html) also passes 23/23 with nearly identical combined quality, at $1.71 and 4.90 minutes. Its cost estimate has a $3.22 upper bound for unresolved long-context charges. This small suite mixes correctness with model-judged quality; [Opus medium](https://vulcanbench.com/benchmarks/swe-v4-opus55-v315.html) includes older-model replies in 3/23 runs. Opus high passes 22/23 at $3.27 and 21.4 minutes. Older-model replies appear in 7/23 of its runs and make up 20.9% of replies, against 6.4% at medium. VulcanBench had no Fable 5.2 report as of 2026-11-09. AA's coding-agent comparison covers Sol and Astra only at max, with an older FrontierCode component, so cannot establish high-effort performance. API-equivalent costs do not measure subscription allowance use.

## Work alone, delegate, or hand off

One session usually owns the work and makes sure it gets finished. Add Executors when parts of the work can be done separately. Use orchestration tools to supervise those agents. Hand off the work when another session should take over.

## Choose effort and tools

Start with the effort setting in the table and change it when the task calls for it. More thinking should improve the result enough to justify the extra time and usage. Costs measured through an API do not tell you how much of your subscription allowance a task will use. I prefer each provider's official tools, signed in through my subscription.

## Keep the table current

To refresh the model recommendations, follow the [evaluation procedure](docs/model-evaluations.md) for source selection, effort comparisons, and incomplete evidence. Update the table, review date, reasons, sources, and revisit conditions together in [Model recommendations](#model-recommendations).
