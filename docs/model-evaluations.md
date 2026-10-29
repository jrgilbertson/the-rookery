# Maintaining the routing model table

Use this procedure when the maintainer asks to update the recommendations in
[ROUTING.md](../ROUTING.md). A general refresh covers Planner, Executor, and
Design/taste; a narrower request covers only the named roles. Reviewer keeps
its [selection rule](../ROUTING.md#reviewer). Adding a role is a separate
maintainer decision. This procedure does not start a workflow.

## Gather

Start with affected roles, current selections, candidates, and explicit
maintainer constraints. Use the [role guidance](#choose-by-role) to choose
relevant evidence from the [evaluation sources](#evaluation-sources).
All supported efforts, including max, are eligible
unless the maintainer excludes them. Use third-party evaluations rather than
provider launch claims or direct model trials. Product defaults, account access,
and CLI availability are outside this analysis; the user chooses available
tools when starting work.
Consult provider documentation only to resolve ambiguous identifiers or settings.

**Release coverage.** Treat each release independently: evidence for a
predecessor or successor does not establish its scores or effort choice.
Recheck exact-release coverage and prior gaps on every run after a launch.
Missing results mean unevaluated, not poor performance; keep superseded results
as history rather than filling slots solely because those results exist.
Cross-check against independent sources without requiring a fixed number of sources,
every effort level, or a waiting period. A partial sweep informs the steps it
measures; max-only evidence establishes neither a lower effort's quality nor
the best effort.

Before comparing a candidate, record its source details and missing measurements
using the [source checks](#check-each-source).

## Compare

Use the same benchmark version, scoring rule, and comparable harness conditions
for each comparison. Keep quality, cost, and available completion time visible together.
Prefer primary sources for calculations. Use secondary sources to check task
fit and challenge the choices; use them for a calculation only when they
publish the required matched inputs. Compare conclusions rather than averaging
incompatible scores or assigning numeric weights to sources.
Count overlapping aggregates, components, and republished results once.

**Cost per pass.** Pass rate is the fraction of attempts or tasks meeting the
benchmark's pass/fail rule. Use cost and success measured for the same tasks
and attempt budget:

    cost per pass = average cost per attempt ÷ pass rate as a fraction

At $0.60 per attempt and 60% passing, cost per pass is $1.00. Zero observed
passes gives no finite estimate. Pass@4 measures success within four attempts;
pair it with the cost of that attempt budget, not one attempt's cost.
Indices, preference scores, and partial-credit
percentages are not pass rates. This measures spend across evaluated work,
not a guarantee that retries solve a hard task. Retain raw success alongside
cost/pass; neither automatically takes priority.
See [Cost-of-Pass](https://arxiv.org/abs/2504.13359).

**Rule out worse settings.** Set aside a setting when another has at least
as much quality, costs no more, takes no longer, and improves at least one
measure. Missing time data leaves that dimension unresolved; note unique
capabilities separately.
Compare the remaining settings within and across models for the role's work.

**Compare effort gains.** For successive remaining effort settings, show
quality gain, absolute and percentage cost/time increases, and
additional dollars and minutes per point. For a positive gain:

    cost per additional point = (higher-effort cost − lower-effort cost)
                                ÷ (higher-effort score − lower-effort score)

Moving from 48 points at $0.21 to 50 at $0.32 costs $0.055 per additional point.
Name the metric and distinguish percentage points from relative percentages;
compare increments only within that metric. If added cost brings no quality
gain, report that outcome rather than calculating a cost per additional point.
If cost is missing, report the quality result and leave the calculation unknown.

**Choose a balance.** Prefer a setting before extra cost and time buy too
little useful quality for the role. Keep measured costs unchanged and explain
why any further upgrade is worth its cost and time. Neither the highest score
nor maximum score/dollar establishes suitability.

Explain disagreements between evaluations rather than automatically taking higher effort.
Use no fixed point gap, quality floor, statistical gate, or marginal-cost
threshold.

## Choose by role

Use the comparison rules above for each role. Without comparable results at
multiple effort settings, make a provisional effort choice for Planner and
Executor from the available evidence and the role's needs. Do not default to
the highest effort or leave the choice unresolved. Design/taste follows the
rule below.

### Planner

Look for reasoning, decomposition, and repository comprehension. Prefer direct
plan-quality comparisons when available; general reasoning and coding results
remain indirect evidence. Explain what the results suggest about planning and
what they do not measure.

### Executor

Look for repository repair, debugging, and terminal correctness. Prefer
test-verified correctness.

### Design/taste

Choose using relevant human visual preference and compare measured task
cost/time where available. Keep visual preference separate from implementation
correctness.
Image-generation rankings inform image-model selection, not the coding LLM's
design ability.

Without comparable results at multiple effort settings, retain the
configuration supporting the selection, including its effort. If effort is
undisclosed, choose it provisionally without attributing it to that result.
Change that configuration only for an explicit workload, budget, or latency
reason. Label unmeasured assumptions about quality and savings. A result at
max does not tell us whether max is needed or whether a lower effort preserves
quality. When cost or time is missing, the best balance is still unknown.

## Recommend

Propose Primary, Secondary, and Tertiary provider/model/effort slots for each
affected role. Each ranked row may contain at most one model per provider.
Show before-to-after choices and a short reason for each change
or retention, comparing alternatives in the row. Where measured, state why
the next upgrade's quality gain is or is not worth its cost and time.

- **Fallback fit:** choose credible substitutes for the role and disclose their
  main weakness. Apply the same balanced-setting rule as for the primary,
  including the [Design/taste rule](#designtaste). Covering a fallback's weakest task
  category alone does not justify higher effort. Before paying that premium,
  compare the upgrade with other models' role-relevant quality, cost, and time.
  They need not be proven equivalent to the primary. Keep
  specialists that require a narrower task separate from general-purpose slots.
  An already-paid subscription may retain a usable fallback despite weaker API
  economics. Benchmark dollars do not tell you a task's extra subscription cost
  or how much allowance it uses.
- **Provisional choices:** use incomplete or indirect evidence to make the best
  justified choice, separating observations from model/effort judgment. Name
  the evidence date, material gap, and revisit trigger. Missing evaluations
  reduce confidence but do not rule out a model. Leave a slot empty when no candidate seems
  suitable for the role, not merely because evaluations are incomplete.

**Deliver:** a compact evidence comparison followed by the proposed table and
rationale for every affected role. Show which sources cover the candidates,
gaps in release or effort coverage, where sources agree or disagree, measured
upgrade tradeoffs, and revisit triggers alongside the choices they inform.

Repeated runs may confirm existing choices; change them only when evidence or
constraints justify it. Apply only when authorized: update the table, review
date, affected rationale, sources, and revisit triggers together in
[Model recommendations](../ROUTING.md#model-recommendations).

## Evaluation sources

Start with primary sources for cost and effort comparisons, then use secondary
sources to check the choice against the role's work. These groups describe
how to use the evidence. Reclassify a source when its published data changes,
and replace stale or saturated benchmarks. No source needs to cover every
dimension or support both calculations.

### Primary sources: cost and effort comparisons

Look for quality, cost, and available completion time for the same model,
effort, and tasks. Calculate cost per pass when matched binary success and
cost are available. Compare effort gains when comparable quality and cost
are available at multiple efforts. State which calculations the evidence
supports and leave missing inputs unknown.

- [AA's Intelligence evaluations](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
  report quality and task cost across model and effort settings, including
  analytical and document-reasoning work. Inspect the current components;
  the overall index reflects AA's task mix and is not a pass rate.
- [AA coding-agent results](https://artificialanalysis.ai/agents/coding-agents)
  include repository Q&A and provide component scores and agent task cost/time,
  distinct from the general Intelligence Index. Match a component's success
  rate to its own costs before calculating cost per pass.
- [VulcanBench](https://vulcanbench.com/leaderboard.html)
  separates tasks passed, code quality, cost, and runtime at tested efforts.
  Check its model reports for the populations and exclusions behind each figure.
- [FrontierCode](https://cognition.com/frontiercode) reports merge quality,
  binary pass rates, and cost per rollout across effort settings. Keep its
  quality score separate from its pass rate and check overlap with AA's runs.

### Secondary sources: task fit and corroboration

Use these to test capabilities the primary suites miss and investigate
disagreements. For Design/taste, human visual preference supplies the relevant
quality evidence even when cost or effort data is missing. A secondary source
can also support a calculation when it publishes the required matched inputs.

- [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro_public) measures
  resolved repository tasks.
- [Terminal-Bench](https://www.tbench.ai/benchmarks) tests terminal work.
- [Next.js evals](https://nextjs.org/evals) cover framework-specific tasks.
- [Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend)
  provides human preference on finished interfaces. Inspect its Reference-Based
  Design, Brand & Marketing, and Consumer Product categories for task fit
  ([category methodology](https://arena.ai/blog/new-categories-code-arena)).
  Use [Image-to-WebDev](https://arena.ai/leaderboard/code/image-to-webdev)
  for following screenshots or an existing visual direction. Category views
  share WebDev evidence, so do not count them as independent sources.
  Arena Text informs writing taste.
- [Design Arena](https://www.designarena.ai/leaderboard/website)
  is a separate human-preference source ([methodology](https://www.designarena.ai/about));
  match its single-turn website or agentic web-app category to the work.
- [OpenDesign](https://open-design.ai/llm-arena-for-design/) adds designer-rated
  prototype quality and per-artifact cost/time; check effort and harness disclosure
  before using it to choose an effort. Treat its recommendation weights as that
  site's preferences, not ours.

Practitioner reports can clarify workloads and failure modes; anecdotes do
not establish quality, cost, and time at different effort settings.

### Check each source

Inspect the methodology and results used in the comparison. Record:

- URL, observation date, and exact model and effort.
- Benchmark version, task set, metric meaning, grading, and harness.
- Overlap with other sources, and matched cost and time where available.

Identify binary success, partial-credit, preference, and composite scores.
Distinguish test-verified, human, model-judged, and blended grading. Record
whether runs use only the named model or can fall back to another.
A page update alone does not make its candidate results current.

Check the population behind each metric. A source may omit a failure from a
quality average while retaining its cost or counting it as an attempted task.
Use matching populations for each calculation; otherwise report the mismatch
and leave the calculation unresolved.

Keep component quality paired with that component's costs; a weighted index
cost describes the whole benchmark mix. Distinguish billed spend from
API-equivalent cost estimates, and measured task runtime from estimated
token-generation time, noting excluded work. Mark missing or inaccessible
data. Do not fill gaps with unrelated runs or infer task cost from token
prices alone.
For design sources, distinguish blind human preference from rubric scores and
single-author examples, and single-turn generation from agentic or iterative
work. Undisclosed effort can inform model choice, not an effort comparison.

Use independent audits such as [Epoch's reviews](https://epoch.ai/data/benchmark-reviews-documentation/included-benchmarks)
to flag issues. Investigate linked data, defects, and maintainer fixes when
they could change the decision. Match findings to the evaluated version and
harness rather than inheriting an older verdict. Audits inform source
suitability, not extra ranking votes or a requirement for admission.
