# Match the model to the work

Choose a model and how long it should think based on the work you need done. Use the tools and subscriptions you have. To choose a workflow, see [WORKFLOWS.md](WORKFLOWS.md).

## What each role needs

### Captain

Act as the product, design, and engineering player-coach. Own the outcome: decide what needs doing, in what order, and how we'll know it's finished. Think through the hard parts yourself, hand separable work to Executors or Domain Leads, and answer for the quality of what they produce. A solo session with no workers that plans or works a hard problem uses this row too. For a persistent per-repository fleet in Orca, [`repo-captain`](skills/repo-captain/SKILL.md) runs the Captain and its workers.

### Executor

Make the changes or find and fix the problem. Use tests and other checks to show that the result works.

### Design/taste

Produce or assess an interface that looks good and is easy to use. People's preferences decide this role, so rankings of what people preferred help choose a model. More thinking time does not automatically produce a better design.

### Writing

Draft or edit prose that people will read, such as documentation, posts, and messages. Readers judge it by preference, as with design.

## Model recommendations

**Last reviewed: 2026-11-25**

![Recommendations reviewed 2026-11-25. Captain: Gemini 4 Neon (gemini-4-neon) at high, then Claude Fable 5.2 (claude-fable-5-2) at medium, then GPT-6.2 Astra (gpt-6.2-astra) at high. Executor: Claude Opus 5.5 (claude-opus-5-5) at high, marked as my judgment, then Gemini 4 Neon (gemini-4-neon) at high, marked as my judgment, then GPT-6.2 Sol (gpt-6.2-sol) at medium. Design/taste: Claude Fable 5.2 (claude-fable-5-2) at medium, then GPT-6.2 Astra (gpt-6.2-astra) at high, then Gemini 4 Neon (gemini-4-neon) at high. Writing: Claude Fable 5.2 (claude-fable-5-2) at medium, then Gemini 4 Neon (gemini-4-neon) at high, then GPT-6.2 Astra (gpt-6.2-astra) at high.](docs/assets/routing-table.svg)

Each row names one model from each of three providers, best first, with its effort setting, so take the first one you can run. The same picks, with model ids for tools and agents, are in [`recommendations.csv`](docs/routing/recommendations.csv), and the figure is drawn from that file.

A pick marked \* is my judgment over the method, and the reasons below say why and what would change my mind. This review has two marks, both on the Executor row, and both change only the order: the models and efforts there follow the method.

Claude plans that include Fable let it use up to half of the weekly limit, which the other Claude models share, according to Claude's [help center](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan). When that half runs out, use `claude-opus-5-5` at high in Fable's place.

The recommendations cover four providers: Anthropic, OpenAI, Google, and xAI. The suites also test models from other companies, such as DeepSeek, Qwen, and Mistral, and their results stay in `results.csv`, but this page charts and recommends only these four.

Grok 4.7 comes fourth in every row, so it has no slot. In the base, GPT-6.2 Sol at medium scores higher than Grok at any effort and costs less, and Grok scores lowest among the charted models on the combined Design/taste and Writing scores.

If you only need a model for the task in front of you, stop here; the rest of this page covers the benchmark charts, evidence tables, and [update method](#how-i-update-the-table).

### What each model gains as you raise its effort

![One chart of combined quality against relative cost per task for eight models from four providers, each drawn as a line joining its efforts from lowest to highest. On data read 2026-11-25, Gemini 4 Neon at high scores about 55 at 1.2 times the cost of a typical charted setting, and Gemini 4 Carbon at high about 58 at 1.9 times. Fable 5.2 at high scores about 60 at 2.6 times. GPT-6.2 Astra's best value is high, about 54 at 0.9 times. GPT-6.2 Sol reaches about 49 at medium for a fifth of a typical setting's cost. Gemini 4 Carbon's line doubles back because its low effort costs more than its medium. A soft ring in the line's own color marks each model's best-value effort.](docs/assets/routing-base.svg)

The chart puts five benchmark suites on one scale, so every model shares the same axes. Color names the provider, a dash tells one provider's models apart, and each marker's shape names the effort, as the key above the chart shows. The chart covers coding and general work, and it shows the current models from the four providers, whether or not I can run them today.

A soft ring in the line's own color marks each model's best-value effort, the last step up that costs at most 20% more per point of quality. [The rules](#the-rules) define it.

### Where the frontier sits among the top models

![One chart of combined quality against relative cost for the 15 highest-scoring current models that at least two of the five suites scored, on the same scale as the chart above. On data read 2026-11-25, the frontier runs from Haiku 5.5 at low, medium, and high, through GPT-6.2 Sol at every effort, GPT-6.2 Astra at high and xhigh, Fable 5.2 at medium, Gemini 4 Neon at high, GPT-6.2 Astra at max, and Gemini 4 Carbon at medium and high, to Fable 5.2 at high, xhigh, and max. Opus 5.5 and Sonnet 5.5 sit below it at every effort. Colored lines are the models this page routes, gray dotted lines are the rest, an outlined marker sits on the frontier, and a bold name has at least one setting on it.](docs/assets/routing-frontier.svg)

This chart widens the view beyond the four providers to every maker the suites score, so a cheaper or stronger model elsewhere shows up. A setting is on the [Pareto Frontier](GLOSSARY.md#pareto-frontier) when it scores higher than every cheaper setting among the models shown. It shows the 15 highest-scoring models that at least two suites scored, and leaves out releases a newer one in the same family replaces. Near-free models far below these, such as GPT-6 Luna at low, would otherwise join the frontier at its cheap end.

### Why these models

[How I update the table](#how-i-update-the-table) explains the method. The base table shows each charted model at its best-value effort, in the price order. Relative cost is a multiple of a typical charted setting's cost, and fewer suites means a less certain position.

| Model | Best value | Combined quality | Relative cost | Suites |
|---|---|---|---|---|
| GPT-6.2 Sol | medium | 49.0 | 0.20 | 3 of 5 |
| GPT-6.2 Astra | high | 53.9 | 0.88 | 4 of 5 |
| Gemini 4 Carbon | high | 58.1 | 1.85 | 4 of 5 |
| Gemini 4 Neon | high | 55.2 | 1.23 | 4 of 5 |
| Fable 5.2 | medium | 54.8 | 1.20 | 4 of 5 |
| Gemini 4 Hydrogen | high | 51.5 | 0.79 | 3 of 5 |
| Opus 5.5 | high | 52.6 | 1.26 | 5 of 5 |
| Grok 4.7 | medium | 46.2 | 1.66 | 3 of 5 |

#### Captain

The row starts from each vendor's flagship and goes by quality. Gemini 4 Neon at high gives Google's slot a better sibling: it beats Carbon at high on the suites that tested both, 59.9 to 58.1, for about two thirds of the cost. By quality the row reads Neon (55.2), Fable 5.2 at medium (54.8), then GPT-6.2 Astra at high (53.9). AA-Briefcase, the closest measure of leading work, puts Neon at high (1631) and Fable at medium (1623) within each other's intervals of about 10 points, and Astra at high lower (1570), so it agrees with the order.

Revisit when a suite measures plan quality and downstream success for these releases with the same Executor.

#### Executor

The row starts from each vendor's everyday model and follows the price order. Neon takes Google's slot: at medium it beats Hydrogen at high on the suites that tested both, 53.5 to 51.5, for about 85% of the cost, and it is listed at its best-value effort, high. Fable 5.2 scores higher than Opus for less, but Anthropic rations it, so Opus keeps Anthropic's slot.

Two adjustments, both to the order:

- **Opus 5.5 moves to first \*.** The method puts Sol first, then Neon, then Opus. Opus is the worker I rely on day to day, and the coding suites split: VulcanBench puts Opus at high above Sol at medium (91.1 against 88.9), and FrontierCode puts it below (36.3 against 38.3). This reverses if a suite tests Opus at high beside Sol and Neon at medium and Opus falls behind, or if my own sessions stop bearing it out.
- **Gemini 4 Neon at high moves to second \*.** It scores 6.2 points more than Sol at medium (55.2 against 49.0) at about six times the API cost. On subscriptions that gap is smaller, and the quality is worth it. This reverses if the Coding Agent Index or Terminal-Bench by effort tests Neon at high beside Sol at medium and Sol matches or beats it, or if my own sessions stop bearing it out.

Revisit when the Coding Agent Index tests Opus 5.5 at high, or when Terminal-Bench by effort adds Sol or Neon.

#### Design/taste

Four sources score this row, weighted equally, and each provider's best-scoring model takes its slot. Each source is standardized over the current models it lists, where 50 is their average and 10 points is one standard deviation, and a model's score is the mean of its source scores. That mean isn't rescaled, so its spread can be narrower than 10 points per standard deviation.

| Model | Arena WebDev | Design Arena | 21st.dev Design System Bench | Frontier Design | Score |
|---|---|---|---|---|---|
| Fable 5.2 | 1822 | 1377 | 85.2 | 1710 | 60.6 |
| Opus 5.5 | 1820 | 1454 | 73.7 | 1684 | 58.4 |
| GPT-6.2 Astra | 1761 | 1322 | not listed | 1755 | 54.1 |
| GPT-6.2 Sol | 1755 | 1292 | not listed | 1631 | 49.8 |
| Gemini 4 Neon | 1765 | 1339 | not listed | 1430 | 49.7 |
| Gemini 4 Carbon | 1769 | 1316 | 82.9 | 1337 | 49.7 |

The margins are small: Astra leads Sol by 4 points, and Neon and Carbon are tied to one decimal, with Neon ahead by 0.03. Neon's Design Arena score fell from 1392 to 1339 on 2026-11-25 as its comparisons grew from 212 to 340, so Google's slot could pass to Carbon on the next read. WebDev tested Fable at xhigh and Astra at max, so raise the effort when a design calls for more.

Revisit when Design System Bench lists the GPT-6.2 models or Neon, or when Frontier Design's GPT-6.2 and Neon entries reach several hundred votes.

#### Writing

Two sources score this row, weighted equally. Arena counts once, through creative writing.

| Model | Arena creative writing | Lechmazur score | Score |
|---|---|---|---|
| Fable 5.2 | 1525 | 3.56 | 58.5 |
| Opus 5.5 | 1518 | 3.35 | 56.9 |
| Gemini 4 Neon | 1504 | not listed | 55.0 |
| GPT-6.2 Astra | 1471 | 4.30 | 53.6 |
| Gemini 4 Hydrogen | 1492 | not listed | 51.7 |
| Gemini 4 Carbon | 1518 | 1.62 | 51.3 |

Neon leads Astra by 1.4, and Neon's score rests on Arena alone. No benchmark scores current models on non-fiction such as documentation or reports, so this row rests on creative writing.

Revisit when Lechmazur lists Neon, when Surge AI's Hemingway-bench lists current models, or when EQ-Bench Creative Writing lists Fable 5.2, the GPT-6.2 models, and Neon.

## Choose effort and tools

Start with the effort setting in the table and change it when the task calls for it. API costs don't tell you how much of a subscription allowance a task will use, and time per task is often the better guide. I prefer each provider's official tools, signed in through my subscription.

## How I update the table

The method runs in four steps, from what is measured to what is judged. A refresh covers every row unless I name specific roles, and it considers every current model from the four providers.

1. **The base.** Five suites from five operators measure quality and cost at several effort settings, across coding and general work. A script puts them on one scale, finds each model's best-value effort, and lists the models in order.
2. **Role inputs.** Each role also has its own sources. Vendor guidance sets where the Executor and Captain rows start, related benchmarks check those rows, and preference sources score Design/taste and Writing. I record each with its source and the date I read it.
3. **The practitioner view.** I scan the last 30 days of public posts for what people who use these models report. A report doesn't change a row by itself. It informs my judgment, and an adjustment that rests on one says so.
4. **My judgment.** I make the final call. Suites can be gamed or badly built, and my own use is evidence. My judgment can override the measurements. When it does, the cell carries an asterisk (\*), and the reasons say what would change my mind.

Each change to a row is an **adjustment**: one line that says from what, to what, which input or judgment justifies it, and what would reverse it. A row with no adjustment follows the method.

### The rules

- **Compare settings.** A setting is one model at one effort. A model is better when its listed setting scores higher, whatever it could reach at another effort.
- **Standardize every source.** Each suite and preference source is put on its own scale over the current charted models it tested: 50 is their average and 10 points is one standard deviation. A setting's score averages the sources that tested that setting, and no source is a reference for the others.
- **A point of quality is worth up to 20% more cost.** This one figure sets both the best-value effort and the price order. A point is a tenth of a standard deviation among the charted settings.
- **The best-value effort is the last step worth its extra cost.** First drop any effort that a cheaper effort of the same model beats. Then climb from the cheapest and stop before the first step that costs more than 20% extra for each added point. Each model is listed at its best-value effort unless a rule below names another.
- **The Executor row starts from each vendor's everyday model, and the Captain row from its flagship.** Vendors name these in their own guidance. When a vendor's sources disagree, the everyday model is the one its own coding tool runs by default to do the work.
- **A better sibling takes the slot.** If another current model from the same vendor scores higher for less at any effort, compared on the base suites that tested both settings, its cheapest such setting earns the slot. The sibling is listed at that setting or at its own best-value effort, whichever is higher. Comparing only shared suites keeps a model from losing ground for having been tested more widely. A rationed model never takes a slot this way. A vendor rations a model when its plans cap the model's use, count it faster against the allowance, or bill it to credits.
- **The Executor row follows the price order.** A setting at least as good for no more cost goes first. Otherwise the better-scoring setting goes first only when it costs at most 20% more for each point it adds. Past that, the cheaper one goes first. If every remaining setting is beaten by another, the best-scoring one goes next. The base table uses the same order.
- **The Captain row goes by quality.** The higher combined score goes first, and the cheaper setting breaks a tie. A Captain's decisions carry the outcome, so cost only sets each model's effort and decides whether a sibling takes a slot.
- **Preference rows weigh their sources equally.** Design/taste and Writing each have their own sources, since cost doesn't measure taste, and each operator counts once. Each source is standardized across the current models it lists, taking a model's best score at any effort, and a model's score is the mean over the sources that list it. Each provider's best-scoring model takes its slot, best first, at its best-value effort.
- **Three providers per row, one model each.** A row takes the first three providers in its order.

### Where the evidence comes from

| Source | Operator | Feeds | Kind of evidence | What it is and how it's used |
|---|---|---|---|---|
| [FrontierCode](https://cognition.com/frontiercode) | Cognition | The base | Measured | Coding tasks run in each model's own tool, scored on merge quality with a pass rate and cost. One of the five base suites. |
| [VulcanBench](https://vulcanbench.com/leaderboard.html) | VulcanBench | The base | Measured | 23 coding tasks scored on tests passed and code quality, which models judge, with cost and time. One of the five base suites. |
| [CursorBench](https://cursor.com/cursorbench) | Cursor | The base | Measured | Ambiguous multi-file coding tasks, with a score and cost per task. One of the five base suites; it tests no current OpenAI model. |
| [AA Index without coding](https://artificialanalysis.ai/methodology/intelligence-benchmarking) | Artificial Analysis | The base | Measured | The AA Intelligence Index without its Coding category: seven evaluations of knowledge work, science, and general reasoning, with cost per task. It leaves out FrontierCode-AA 2.0, which runs FrontierCode's tasks, and Terminal-Bench 4.1, which the Vals Index also contains. One of the five base suites. |
| [Vals Index](https://www.vals.ai/benchmarks/vals_index) | Vals AI | The base | Measured | A composite of eight evaluations, including legal, tax, and finance work, with cost per test. One of the five base suites, read from its per-effort results and, for models without them, its leaderboard. |
| Each vendor's model guidance | Anthropic, OpenAI, Google, xAI | Executor and Captain starting models | Vendor guidance | Which model each vendor recommends for everyday work and for its hardest work, and which it rations. Sets the model each of those rows starts from. |
| [AA Coding Agent Index](https://artificialanalysis.ai/agents/coding) | Artificial Analysis | Executor check | Measured | Each model in its maker's coding tool, scored on three coding suites with cost and time. Read beside the base when judging the Executor row. |
| [Vals Terminal-Bench](https://www.vals.ai/benchmarks/terminal-bench-4) | Vals AI | Executor check | Measured | Terminal tasks with every model in one shared harness, with a separate by-effort chart. Read beside the base when judging the Executor row. |
| [AA-Briefcase](https://artificialanalysis.ai/evaluations/aa-briefcase) | Artificial Analysis | Captain check | Proxy | Elo on long, multi-step knowledge-work tasks, the closest published match to leading work. Read beside the base when judging the Captain row. |
| [Arena WebDev](https://arena.ai/leaderboard/code/webdev) | Arena | Design/taste | Preference | People vote between finished web apps. One of four equal sources for Design/taste. |
| [Design Arena](https://www.designarena.ai/leaderboard) | Design Arena | Design/taste | Preference | People vote between generated interfaces, read from its overall agentic board. One of four equal sources for Design/taste. |
| [21st.dev Design System Bench](https://21st.dev/benchmarks/leaderboard) | 21st.dev | Design/taste | Measured | Agents build interfaces in a real repository, scored on how well they use its design system. One of four equal sources for Design/taste. |
| [Frontier Design](https://contralabs.com/frontierdesign/leaderboard) | Contra Labs and BenchFlow | Design/taste | Preference | Professional designers vote blind between websites built from real client briefs. One of four equal sources for Design/taste. |
| [Arena Creative Writing](https://arena.ai/leaderboard/text/creative-writing) | Arena | Writing | Preference | People vote between pieces of creative writing. One of two equal sources for Writing. |
| [Lechmazur Writing](https://github.com/lechmazur/writing) | Lechmazur | Writing | Proxy | Short stories scored by a panel of models; Epoch rated it "Flawed". One of two equal sources for Writing. |
| Public posts from the last 30 days | Many | Any row | Report | What practitioners report from their own use, often second-hand. Informs judgment but never changes a row by itself. |
| My own use | Me | Any row | Judgment | What I have seen these models do. The basis for any pick marked \*. |

Measured means the suite reports quality and cost for the same model, effort, and tasks. Vendor guidance is the vendor's own recommendation, which I take as a statement of what it tuned each model for. Proxy means it measures related work. Preference means people chose between results. Report and Judgment are the last two steps of the method.

A suite joins the base only when it publishes quality and cost at more than one effort per model, a different operator runs it, and it doesn't rerun a suite already there. When a composite contains a suite the base already counts, the base uses the composite without that part. Each operator counts once, so a second suite from the same operator becomes a role input. Cognition and Cursor sell coding products, and the other three operators are independent evaluators.

Every score and cost from these sources is a row in [`results.csv`](docs/routing/results.csv), so you can check the figures on this page against one table. Counts such as comparisons, ranks, and fallback attempts, and everything a source says in words, are in [`role-inputs.csv`](docs/routing/role-inputs.csv).

[Epoch's benchmark reviews](https://epoch.ai/data/benchmark-reviews-documentation/included-benchmarks) flag known problems with a suite. Check that a finding applies to the version tested before acting on it.

### Names and effort labels

Sources name some models and efforts differently. [`models.csv`](docs/routing/models.csv) maps every name a source uses to one model, with its maker and whether a newer release has replaced it. [`efforts.csv`](docs/routing/efforts.csv) maps each source's effort labels to the seven efforts the charts use. Two names become one model only when the sources show they are the same release; otherwise they stay apart, and the note column says why. FrontierCode's "Muse Wonder 1.0" stays separate for that reason. An effort label with no row stops the import, so a numeric scale such as Inkling's "0.99" is left out rather than guessed.

| Model | Maker | Other names the sources use |
|---|---|---|
| Beam 1.0 | Reflection | Reflection Beam |
| DeepSeek V4.1 Flash | DeepSeek | DeepSeek V4.1 Flash 1017 |
| GLM-5.2 | Zhipu | GLM 5.2 |
| GLM-5.3 | Zhipu | GLM 5.3 |
| GLM-5.3-Flash | Zhipu | GLM 5.3 Flash |
| Hy4 | Tencent | Tencent Hy4 |
| Ling 3.1 Flash | Ant Group | Ling-3.1-flash |
| MiMo-V2.6-Flash | Xiaomi | MiMo V2.6 Flash |
| MiMo-V2.6-Pro | Xiaomi | MiMo V2.6 Pro |
| MiniMax-M2.7 | MiniMax | MiniMax M2.7 |
| MiniMax-M3 | MiniMax | MiniMax M3 |
| MiniMax-M3.1-Flash | MiniMax | MiniMax M3.1 Flash |
| Muse Wonder | Meta | Wonder |
| Muse Wonder Full | Meta | Wonder Full |
| Qwen3.8 Max (0902) | Alibaba | Qwen 3.8 Max 0902 |
| Qwen4 Max | Alibaba | Qwen 4 Max, Qwen4-Max |

| Effort | Labels the sources use |
|---|---|
| none | na (FrontierCode); none (FrontierCode, AA, Vals, Design Arena) |
| minimal | minimal (FrontierCode) |
| low | low (every base suite) |
| medium | medium (every base suite) |
| high | high (every base suite) |
| xhigh | xhigh (FrontierCode, AA (Xhigh), Vals, Arena (xHigh)); extra-high (VulcanBench); extra high (CursorBench) |
| max | max (every base suite) |

### How I compare

The script standardizes each base suite over the settings it tested for the current charted models. A setting's combined score averages the suites that tested that setting, where 50 is an average charted setting and 10 points is one standard deviation. Each suite's costs are taken as a multiple of its typical charted setting, the geometric mean of those settings' costs, and combined cost is the geometric mean across the same suites. The page shows it as relative cost, so a relative cost of 2 means twice a typical charted setting. It compares settings with each other and is not a bill. Time per task is each suite's own figure in minutes, where it publishes one.

These rules prevent the easiest mistakes:

- **Judge each release on its own results.** A predecessor's score doesn't establish a new release's score or its best effort. A missing result means untested, not poor.
- **Use third-party suites for measurement.** A provider's launch claims don't count as measurements. A provider's guidance on which model to use for which work is a role input.
- **Don't rule a provider out before looking.** Whether I can run a model doesn't remove it from the chart or the rows.
- **Read the page's data before calling a figure missing.** Several suites keep efforts, per-effort results, and errors in the page's embedded data, which the visible text leaves out.
- **Compare settings, not models.** A ranking that tested two models at different efforts compares those two settings, not the models. Say which efforts were tested before saying one leads, and don't read a ranking that names an effort for one model and not the other as comparing them.
- **Note when another model could have answered.** Some runs fall back to another model, and those replies count in the score.
- **Don't read API cost as subscription cost.** Benchmark dollars don't show how much of a plan's allowance a task uses.
- **Choose even when evidence is thin.** Name the gap and what would change the choice.

### Running a refresh

Everything the script needs is in [`docs/routing/`](docs/routing/). `results.csv` holds every read of every suite in use. `role-inputs.csv` holds what each role input says beyond its figures. `chart.json` names the base suites, the sources each preference row weighs, and the models the charts draw. It also records each vendor's everyday model, flagship, and rationed models, and the frontier chart's settings: how many models it draws and how many suites must score each one. `models.csv` and `efforts.csv` map the names and effort labels the sources use, as [Names and effort labels](#names-and-effort-labels) describes. The script reads local files only.

`results.csv` is append-only while a source is in use. An import adds a read and leaves earlier reads alone, and the report and charts use each suite's latest read. Importing a suite twice on one date replaces that day's read. To retire a source, delete its rows, its `chart.json` entry, and its `role-inputs.csv` row, so it can't be counted by accident.

1. **Import the base.** Download FrontierCode's `data.json` and VulcanBench's leaderboard CSV and import each. For the other three, copy the results from the page's data into a plain table of model, effort, score, pass rate, cost, and minutes, and import that.

   For the Vals Index, take each model's per-effort results where the page's data has them. For every other leaderboard entry, take the effort its model page states as "Reasoning Effort" or "Compute Effort", so the read covers the whole leaderboard.

   The AA Index without coding is derived from AA's own figures for every setting AA lists, so the frontier chart can place models beyond the routed ones. Its score is the published Intelligence Index minus 15 times the FrontierCode-AA 2.0 score and 10 times the Terminal-Bench 4.1 score (each a fraction from the leaderboard's page data), divided by 0.75.

   Its cost is the index cost per task minus those two evaluations' weighted cost per task, divided by 0.75. Each model's page lists every evaluation's weighted cost per task under `intelligenceIndexCostPerTask`, and they sum to the index cost. AA publishes no time per task for the subset, so leave minutes empty. If AA changes the index's weights or components, update the formula from its methodology page.
2. **Import the role inputs** the same way, each as a suite outside the base. Update what `role-inputs.csv` says about each one, with the date read.

   Most sources can be fetched as plain pages or files. The two Arena boards (WebDev and creative writing) cannot: arena.ai refuses automated requests, so read them in a real browser, such as Orca's built-in browser, and say so in `role-inputs.csv`. A summarizing reader is not a substitute. On the 2026-11-19 read one gave the wrong page date and dropped the efforts the page names.
3. **Re-read each vendor's model guidance.** Update `chart.json` with each vendor's everyday model, flagship, and rationed models, and record the sources in `role-inputs.csv`. The script looks for a better sibling only among the models `chart.json` lists, so list any current model that could beat a vendor's everyday model or flagship.
4. **Check names and effort labels.** If a suite names a model differently, add a row to `models.csv` that points the new name at the model, once the sources confirm they are the same release. Give a new model its own row with its maker. When a new release replaces an older one in its family, set the older one's status to superseded. If an import stops on an effort label, add the label to `efforts.csv`, or leave those rows out when the label has no named equivalent. Then copy the report's `names` section into [Names and effort labels](#names-and-effort-labels).
5. **Run `changes`** to see what moved since the previous read.
6. **Run the report.** Its `candidates` section lists the charted models at their best-value efforts in order. Its `rows` section builds the Executor and Captain rows, and its `preference` section scores the Design/taste and Writing rows.
7. **Regenerate the charts** and look at each one. Run it again after the rows are final so the recommendations figure matches `recommendations.csv`.
8. **Write the rows** in `recommendations.csv`. Take the Executor and Captain rows from the report's `rows` section, and Design/taste and Writing from its `preference` section. Apply any adjustment a role input supports, and write each one as a line. The routing checks fail when a pick names a different model or effort from the report, unless its `judgment` column says `yes`.
9. **Scan the last 30 days** for what practitioners report about the settings in the rows. Record what bears on a row in `role-inputs.csv` as a report.
10. **Apply judgment.** Change any pick I disagree with, set its `judgment` column to `yes`, and write the adjustment with what would change my mind.
11. **Update the page:** the recommendations figure's alt text, which must name every pick, the base table, each role's evidence tables, the chart alt text, the revisit conditions, and the review date.

```bash
python3 scripts/routing/evidence.py import --format frontiercode --file data.json --version 2.0 --date YYYY-MM-DD --url https://cognition.com/data/frontier-code-2.0/data.json
python3 scripts/routing/evidence.py import --format vulcanbench --file swe-v4-board.csv --version v4 --date YYYY-MM-DD --url https://vulcanbench.com/assets/data/swe-v4-board.csv
python3 scripts/routing/evidence.py import --format table --suite "Vals Index" --file vals.csv --version 2.2 --date YYYY-MM-DD --url https://www.vals.ai/benchmarks/vals_index
python3 scripts/routing/evidence.py import --format table --suite "AA Index without coding" --file aa.csv --version v5.0.2 --date YYYY-MM-DD --url https://artificialanalysis.ai/leaderboards/models
python3 scripts/routing/evidence.py changes
python3 scripts/routing/evidence.py report
python3 scripts/routing/evidence.py charts
```

The repository checks fail when a committed chart no longer matches the data, when `recommendations.csv` drifts from the method without a `judgment` mark, when the [Names and effort labels](#names-and-effort-labels) tables diverge from `models.csv` and `efforts.csv`, or when the recommendations figure's alt text misses a pick or review date. Nothing checks the other figures typed into this page, so step 11 is still manual.
