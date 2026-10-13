# Maintaining the routing model table

On a maintainer's update request, recommend model slots for Planner, Executor,
and Design/taste. Retain Reviewer as the selection rule, not a separate ranking.
Update only the requested profiles. Each ranked row may contain at most one
model per provider; leave a slot empty when no suitable alternative is
justified. Adding a profile is a separate maintainer decision. Choices are qualitative judgments informed by quantitative inputs,
not an automatic ranking. This procedure maintains the recommendations in
[ROUTING.md](../ROUTING.md); it does not choose or start a workflow.

## Gather

Start with affected roles, current selections, candidates, and explicit
maintainer constraints. All supported efforts, including max, are eligible
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
Seek independent corroboration without requiring a fixed number of boards,
every effort level, or a waiting period. A partial sweep informs the steps it
measures; max-only evidence establishes neither a lower effort's quality nor
the best effort.

**Sources by role.** Start here, follow current evidence, and replace stale
or saturated rankers. This is a shortlist, not a required catalog. Where direct
role evaluations are missing, use the closest relevant evidence and explain
the transfer. No single source needs to cover every dimension of a role.

- Executor: repository repair, debugging, and terminal correctness. Start with
  [FrontierCode](https://cognition.com/frontiercode),
  [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro_public),
  [Terminal-Bench](https://www.tbench.ai/benchmarks),
  [Next.js evals](https://nextjs.org/evals), and
  [AA Coding Agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex).
  Inspect AA's components and matched agent cost/time, distinct from its
  general intelligence index.
- Design/taste: human preference on finished interfaces. Start with
  [Arena WebDev Frontend](https://arena.ai/leaderboard/code/webdev/frontend),
  inspecting its Reference-Based Design, Brand & Marketing, and Consumer
  Product categories for task fit ([category methodology](https://arena.ai/blog/new-categories-code-arena)).
  Use [Image-to-WebDev](https://arena.ai/leaderboard/code/image-to-webdev)
  for following screenshots or an existing visual direction. Category views
  share WebDev evidence, so do not count them as independent sources.
  Cross-check [Design Arena](https://www.designarena.ai/leaderboard/website),
  a separate human-preference source ([methodology](https://www.designarena.ai/about));
  match its single-turn website or agentic web-app category to the work.
  [OpenDesign](https://open-design.ai/llm-arena-for-design/) adds designer-rated
  prototype quality and per-artifact cost/time; check effort and harness disclosure
  before using it to choose an effort. Treat its recommendation weights as that
  site's preferences, not ours.
  Keep visual preference separate from implementation correctness. Arena Text
  informs writing taste. Image-generation rankings inform image-model selection,
  not the coding LLM's design ability.
- Planner: reasoning, decomposition, and repository comprehension. Label
  general reasoning and coding evidence as indirect evidence of plan quality.

[AA's general intelligence index](https://artificialanalysis.ai/leaderboards/models)
and [VulcanBench](https://vulcanbench.com/leaderboard.html) add quality/cost and
effort context; identify their relevance to the role. Prefer test-verified
correctness and human preference for taste. Practitioner reports can clarify
workloads and failure modes; anecdotes do not establish an effort curve.

**Source check.** Inspect the methodology and results used in the comparison.
Record URL, observation date, exact model/effort,
benchmark version, metric meaning, grading, harness, overlap with other sources,
and matched cost/time where available. Distinguish human, model-judged, and
blended scores, and pure-model from fallback-enabled runs. A page update alone
does not make its candidate results current. Mark missing or inaccessible data;
do not estimate it from unrelated runs or infer task cost from token rates.
For design sources, distinguish blind human preference from rubric scores and
single-author examples, and single-turn generation from agentic or iterative
work. Undisclosed effort can inform model choice, not an effort comparison.

Use independent audits such as [Epoch's reviews](https://epoch.ai/data/benchmark-reviews-documentation/included-benchmarks)
to flag issues. Investigate linked data, defects, and maintainer fixes when
they could change the decision. Match findings to the evaluated version and
harness rather than inheriting an older verdict. Audits inform source
suitability, not extra ranking votes or a requirement for admission.

## Compare

Use the same benchmark version, scoring rule, and comparable harness conditions
for each comparison. Keep quality, cost, and available latency visible together.
Give each independent, role-relevant source equal qualitative weight; compare
conclusions rather than averaging incompatible scores or assigning custom weights.
Count overlapping aggregates, components, and republished results once.

**Cost per pass.** Pass rate is the fraction of attempts or tasks meeting the
benchmark's binary success criterion. For matched cost and success units:

    cost per pass = average cost per attempt ÷ pass rate as a fraction

At $0.60 per attempt and 60% passing, cost per pass is $1.00; zero observed
passes gives no finite estimate. Pass@4 requires the matching attempt-budget
cost, not one attempt's cost. Indices, preference scores, and partial-credit
percentages are not pass rates. This measures spend across evaluated work,
not a guarantee that retries solve a hard task. Retain raw success alongside
cost/pass; neither automatically takes priority.
See [Cost-of-Pass](https://arxiv.org/abs/2504.13359).

**Frontier.** Remove dominated settings: another has at least as much quality,
no greater cost or latency, and is strictly better on one measure. Missing
latency leaves that dimension unresolved; note unique capabilities separately.
Compare the remaining settings within and across models for the role's work.

**Marginal gains.** For successive remaining effort settings, skipping dominated
levels, show quality gain, absolute and percentage cost/time increases, and
additional dollars and minutes per point. For a positive gain:

    cost per additional point = (higher-effort cost − lower-effort cost)
                                ÷ (higher-effort score − lower-effort score)

Moving from 48 points at $0.21 to 50 at $0.32 costs $0.055 per additional point.
Name the metric and distinguish percentage points from relative percentages;
compare increments only within that metric. Added cost without better quality
is no observed gain, not a negative-cost bargain. Missing cost prevents the
calculation, not use of the quality observation.

**Balance.** Prefer the curve's bend: a role-suitable setting before cost and
time rise disproportionately to useful quality gains. Keep measured costs
unchanged; the role determines which gains warrant paying more. Neither the
highest score nor maximum score/dollar establishes suitability. A choice beyond
the bend needs an evidence-backed reason for both premiums. Without a matched
curve, use the Design/taste rule below for that profile; otherwise make a
provisional effort judgment from the available evidence and the role's needs
rather than defaulting to the highest effort or leaving the choice unresolved.

**Design/taste without an effort curve.** Choose using relevant human visual
preference and compare measured task cost/time where available. Retain the
configuration supporting the selection, including its effort. If effort is
undisclosed, choose it provisionally without attributing it to that result.
Depart from the observed configuration
only for an explicit workload, budget, or latency reason; label unmeasured
quality and savings assumptions. An observed max result proves neither that
max is necessary nor that a lower effort preserves its quality. Missing economics
remain unknown, not evidence of an optimum.

Explain conflicting boards rather than automatically taking higher effort.
Use no fixed point gap, quality floor, statistical gate, or marginal-cost
threshold.

## Recommend

Propose Primary, Secondary, and Tertiary provider/model/effort slots for each
affected role. Show before-to-after choices and a short reason for each change
or retention, comparing alternatives in the row. Where measured, state why
the next upgrade's quality gain is or is not worth its cost and time.

- **Fallback fit:** choose credible substitutes for the role and disclose their
  main weakness. Apply the same balanced-setting rule as for the primary,
  including the Design/taste exception. Covering a fallback's weakest task
  category alone does not justify higher effort. Before paying that premium,
  compare the upgrade with other models' role-relevant quality, cost, and time.
  They need not be proven equivalent to the primary. Keep
  specialists that require a narrower task separate from unconditional slots.
  An already-paid subscription may retain a usable fallback despite weaker API
  economics: benchmark dollars are not subscription marginal prices or quotas.
- **Provisional choices:** use incomplete or indirect evidence to make the best
  justified choice, separating observations from model/effort judgment. Name
  the evidence date, material gap, and revisit trigger. Missing coverage limits
  confidence, not eligibility. Leave a slot empty when no candidate seems
  suitable for the role, not merely because evaluations are incomplete.

**Deliver:** a compact evidence comparison followed by the proposed table and
rationale. Show source coverage, exact-release and effort gaps, agreement and
disagreement, measured upgrade tradeoffs, and revisit triggers alongside the
choices they inform.

Repeated runs may confirm existing choices; change them only when evidence or
constraints justify it. Apply only when authorized: update the root table,
review date, and affected rationale together. Keep provider diversity,
subscription-billing preferences, and evidence gaps explicit.
