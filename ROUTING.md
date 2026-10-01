# Routing work

`route-work` uses an explicit routing request and supplied evidence to recommend
a starting workflow, coordinator, pattern, roster with models and effort, and
copy/paste kickoff. It returns Resume when work has a proven owner, or Questions
when a routing fact is missing. The selected workflow executes the work.

The coordinator is the session receiving the kickoff, not an added worker. It
owns the human-facing conversation and completion, using the model profile for
the starting workflow.

Planning defines scope, acceptance criteria, work breakdown, and dependencies.
Coordination assigns owners, tracks progress, unblocks dependencies, and
reconciles results. The same coordinator does both as needed; Planner is a
model/effort profile, not a separate agent.

In Single owner, the default, the coordinator does the work itself. With
workers, it delegates their units and implements only work it owns. A parent
issue does not by itself make the coordinator coordination-only; preserve any
supplied implementation boundaries in the kickoff, independently of profile.

## Activation boundary

Route only when the operator explicitly asks to route or kick off work. A
planning, debugging, design, implementation, or issue request without that
intent proceeds through its normal workflow and does not produce a card.

One routing attempt may span multiple conversational turns. Ask only questions
that would change the card, and use supplied evidence and contract defaults
first.

## Inspect only supplied evidence

The assessment may read:

- the request;
- one explicitly named primary artifact, when present;
- directly cited repository instructions; and
- authoritative metadata already supplied in the current context.

For an issue, use only the named node and an already-supplied or visible
relationship summary. Do not conduct a broad repository search, recursively
walk an issue graph, or probe external state.

Facts about an artifact do not mean the artifact was supplied. An issue
family's uncertain coverage supplies neither a named node nor a relationship
summary.

## Preserve authority

The router assesses supplied evidence, renders one card, and exits without
changing state or persisting routing state outside the visible conversation.
Pasting the kickoff is the operator's approval to start the work.

Carry each grant, limit, and condition the operator stated into Setup and the
kickoff once, without widening or dropping it, and add no other authority. A
statement that some authority is withheld or not supplied is a limit. A
predicted end grants nothing, so the starting workflow's own gates decide when
to move to the next phase. The card never narrates phases, checkpoints, or
stopping points, and never says where plans are stored.

## Handle parent, child, and existing work

Use only supplied issue-family and plan state. This table can replace the owner
or switch the card to Resume; apply it before the owner table.

| Supplied state | Result |
|---|---|
| Family coverage, descendants, blockers, readiness, or structure is incomplete or uncertain | Route to `managing-issues`. Do not pick a child or call the family ready. |
| A complete current family is supplied, but parent integration, sequencing, or shared-surface planning is missing | Route the parent to `ce-plan` |
| An approved parent plan is supplied | Route to `ce-work` |
| A child is named directly | Route from what needs to happen first for that child while preserving supplied parent constraints, unless supplied evidence says unresolved family state blocks it |
| The requested phase already has a proven active owner | Return a Resume card and no duplicate kickoff unless replacement or restart is explicit |

A named in-flight owner is proven only by an operator statement or supplied
artifact that names a specific owner for the requested phase. A stated
worktree, branch, pull request, worker, or parallel effort is occupancy
evidence: it establishes neither a phase owner nor independent implementation
units. Without a proven phase owner, use the normal Route.

## Choose what needs to happen first

Choose exactly one starting workflow based on what needs to happen first: the
earliest question to answer or durable change to make before useful work can
continue. Choose it from this table, not from the host, model, or later steps.

| What needs to happen first | Owner | Focus |
|---|---|---|
| Product outcome, behavior, or scope boundary is unsettled | `ce-brainstorm` | Clarify what should be built before planning how |
| A supplied decision document needs a focused, dependency-ordered pressure test | `grill-with-docs` | Run a focused grill |
| Outcome and acceptance boundary are settled, but the execution plan is missing | `ce-plan` | Plan without reopening settled product choices |
| Broken or unexpected behavior still has an unresolved causal chain | `ce-debug` | Diagnose first; an established cause and fix route to `ce-work` |
| Concrete implementation is ready, including an already-diagnosed fix | `ce-work` | Execute the ready work |
| Canonical issue content, relationship graph, coverage, or readiness state must be inspected or changed | `managing-issues` | The first need is to inspect or edit issues, links, coverage, or ready-or-not state |
| Visual direction, interaction design, or design quality is unresolved | `impeccable` | Let Impeccable select its internal workflow unless one exact command is already obvious |

Work that needs a starting owner outside these seven gets a Questions card that
names no owner and points to the supported starting owners in the table at
https://github.com/jrgilbertson/the-rookery/blob/main/ROUTING.md#choose-what-needs-to-happen-first.

## Ambiguity and missing input

- If one request could fit two owners, ask which owner's focus comes first.
- For two separate workstreams that could both start and neither blocks the
  other, ask which starts first. A recommended order is allowed; the operator
  still chooses. The Route card names exactly one starting workflow.
- If the request already names the work, route it. Do not require a plan file,
  issue, or other artifact first.
- If a named or required primary artifact cannot be read, the operator says
  they cannot answer a required routing question, the selected workflow is
  confirmed unavailable, or every listed model for a profile is stated
  unavailable, return a Questions card asking for what would let routing
  proceed.

## Estimate the pattern and roster

Name the role for each worker, and count workers, not steps.

Start with Single owner, including when implementation is expected. Supplied
evidence establishes independent units when it names units that need separate
write paths, such as named modules, or when a plan states its units are
independent.

| Pattern | Roles | Use when | Guardrail |
|---|---|---|---|
| Single owner | The coordinator alone, on the selected owner's profile. It writes the work itself. | The default when neither other pattern applies | One worker covers later stages of the same owner. |
| Executor + Reviewer | Two workers: the coordinator writes and revises; the Reviewer only judges. | The operator asks for a separate Reviewer, or explicit acceptance criteria exist for a run that does not implement through `ce-work`, which runs its own review | One round. Stop when the Reviewer's stated criteria pass or fail. Hand the Reviewer the criteria. The Reviewer does not write the artifact. |
| Coordinator + Executors | The coordinator runs the starting workflow, which dispatches Executor workers to implement the units. | Implementation is expected or predicted and supplied evidence establishes independent units, whichever workflow starts | The kickoff names the Executors' model and effort; the workflow decides how many run and when. |

When both Executor + Reviewer and Coordinator + Executors apply, use
Coordinator + Executors and add the Reviewer.

Size the roster for where the run ends, not where it starts, including a
brainstorm, grill, debug, or plan that implementation will follow. Do not ask
whether implementation follows. When nothing says so, predict that the run
reaches implementation and size for it. Skip the prediction when the operator
limits the run to planning or withholds implementation, or when the run starts
with `managing-issues` or `grill-with-docs`.

Use one Executor per named or counted unit, or up to three when evidence
establishes independent units without naming or counting them.

## Keep orchestration and ownership separate

Supervised orchestration through Orca keeps the current coordinator as the sole
human-facing owner and integrator. When acting on supervised orchestration,
follow Orca's installed, version-matched orchestration contract. A full handoff
transfers human-facing ownership to the
receiving worktree or agent; the sender has no monitoring duty.

When supervised orchestration is selected:

- Name it in Setup and the kickoff, and tell the operator to follow Orca's
  installed contract.
- In Setup, tell the operator to continue with the coordinator in its terminal
  and close this session once orchestration is running.
- In the kickoff, say "Orca orchestration" exactly and tell the coordinator to
  use Orca's `orchestration`
  skill when installed. The receiving session uses that phrase to find the skill.

Do not copy Orca commands into the card.

## Select profiles

Each seat and worker uses the profile whose row in the model table names it.
Resolve the operator's model choices and availability before assigning reviewers.
An advisor gathers bounded evidence using its coordinator's profile; it has no
ownership and does not count toward the worker roster.

### Reviewer selection

For the Reviewer profile, take the first available model in Executor order
whose provider differs from the selected worker producing the reviewed work.
When the coordinator writes directly, compare against the coordinator instead.
Retain the chosen model's Executor effort; reviewing adds no automatic increase.

If no different-provider option is available, use the first available Executor
model in a fresh review session and disclose the same-provider fallback in
Setup and the kickoff. Provider diversity does not guarantee independent errors.
Resolve the rule to a concrete model and effort in both places. Taste-led
review instead uses the first available Design/taste model at its listed
effort, without applying this provider-diversity rule.

### Availability fallback

Use operator-stated or already-supplied availability to filter unavailable
models in listed order. Keep the selected owner unchanged. When availability is
unknown, keep the default selection and omit availability from the response.

### Subscription billing

Every Route kickoff includes this execution constraint: use the assigned
providers’ official CLIs with subscription authentication. Do not use API-key
billing or switch to it as a fallback. If subscription access cannot be
established or its usage limit is reached, report the blocker.

### Effort escalation

Use the table's listed effort by default. The router may suggest a higher
effort, but selects one only when the operator approves it.

## Model and effort recommendations

**Last reviewed: 2026-09-30**

| Profile | Seat or worker | Primary or selection rule | Secondary | Tertiary |
|---|---|---|---|---|
| Planner | The coordinator on `ce-brainstorm`, `grill-with-docs`, `ce-plan`, or `managing-issues` | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6.1-sol` / high | — |
| Executor | The coordinator on `ce-work` or `ce-debug`, and Executor workers | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / medium | Anthropic / `claude-sonnet-5-5` / high |
| Reviewer | Reviewer workers, including adversarial reviews, and named review or verification gates | [Derive from Executor using the selected implementer's provider](#reviewer-selection) | — | — |
| Design/taste | The coordinator on `impeccable`, and the Reviewer when the finish line is taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | OpenAI / `gpt-6-astra` / max |

## Return one portable response

The card is the entire final answer, with no preamble, narration, or closing
remark around it. Its first line is exactly `**Route**`, `**Resume**`, or
`**Questions**`. Bold marks that line and the section labels, with a blank line
after each; use no `#` headings, and never fence the kickoff. Write every
section as natural prose, not a string of stock sentences. Render model IDs as
ordinary names, such as "Opus 5.5 at medium".

### Route

    **Route**

    Start with [starting workflow] on [coordinator model] at [effort].

    **Why**

    [One or two sentences on what needs to happen first and why this pattern fits. Name where the run is expected to end, which the roster was sized for; when the run reaches implementation, say that the coordinator remains accountable for completion, whether implementing or coordinating workers. When implementation is predicted, label it and say the coordinator can adjust the roster. When using a pattern or roster default, name it and invite an override, such as naming independent units to add Executors.]

    **Setup**

    [The roster: every role in the pattern with its model and effort, stated even when it repeats the decision line. The Executor count. The pattern, named in a sentence, when it is not Single owner. Orchestration only when supervised orchestration is selected. The operator's stated grants, limits, and conditions, when any. An advisor or a profile fallback only when it applies.]

    **Copy/paste kickoff**

    Start [starting workflow] from [stable artifact locator or concise supplied request]. You are the coordinator on [model] at [effort]. [Each Reviewer or advisor with its model and effort. In Executor + Reviewer: hand the Reviewer the criteria and stop after one round, when they pass or fail.] [Subscription billing constraint.] [In Coordinator + Executors: When the work reaches implementation, run implementation workers on [Executor model] at [effort]; [the implementing workflow] decides how many and how to schedule them.] [Orchestration sentence only when supervised orchestration is selected.] Treat [the supplied request, or the artifact whose contents or locator were supplied] as the source of truth. [The operator's stated grants, limits, and conditions, when any.]

If only facts about an artifact were supplied, name the request, not that
artifact, as the kickoff's source of truth.

The decision line never names a role; roles live in Setup. The kickoff states
each worker's model and effort as settings to apply and leaves how workers are
started to the workflow and harness. The implementation-workers sentence keeps
its template wording exactly; the Executor count and units stay in Setup. The
kickoff must stand alone when pasted, so it repeats every role's model and
effort and the operator's stated grants, limits, and conditions.

### Resume

    **Resume**

    [proven active owner] owns this work.
    Continue with [proven active owner] for [current phase]. [supplied locator, when present; decisive context and next action]

A Resume card carries no kickoff.

### Questions

    **Questions**

    1. [question]
    Recommended: [one concrete answer the operator can accept in a word]. [One-line reason.]
    2. [question]
    Recommended: [one concrete answer the operator can accept in a word]. [One-line reason.]

Order questions by routing impact: owner, pattern, profile, then orchestration
and ownership handoff. Batch independent questions; ask dependent questions
after their prerequisites are answered.

Give each question one concrete recommended answer, not a test for the operator
to apply. Use the contract default when one exists. When only the operator
knows the missing fact, recommend the answer that lets routing proceed under
the defaults.

The reason states what is unknown or ambiguous and what the answer decides,
using only supplied facts or contract defaults. Neither the question nor its
reason may treat an interpretation as the operator's statement, predict an
inspection's findings or the operator's answer, or name an unsupplied artifact.
For example: "Recommended: Fix. The
request could mean a bug fix or a redesign, and the answer decides where the
work starts."

A Questions card names no workflow, model, profile, or kickoff.
When the starting owner falls outside the seven, the recommendation is the
supported-owner table link.

<!-- route-work-contract-end -->

> Maintainer note: root `ROUTING.md` is the human-edited source. Copy it
> byte-for-byte to `skills/route-work/references/routing.md` in the same change.

## Maintaining the model table

On a maintainer's update request, recommend model slots for Planner, Executor,
and Design/taste. Retain Reviewer as the selection rule, not a separate ranking.
Update only the requested profiles. Adding a profile is a separate maintainer
decision. Choices are qualitative judgments informed by quantitative inputs,
not an automatic ranking. This procedure stays outside runtime: route-work
reads the table at kickoff.

### Gather

Start with affected roles, current selections, candidates, and explicit
maintainer constraints. All supported efforts, including max, are eligible
unless the maintainer excludes them. Use third-party evaluations rather than
provider launch claims or direct model trials. Product defaults, account access,
and CLI availability are outside this analysis; runtime handles availability.
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

### Compare

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

### Recommend

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
review date, and affected rationale, then copy the document byte-for-byte to
the bundled reference. Preserve runtime routing, subscription authentication,
availability fallback, and operator-approved effort escalation.

### Rationale retained from the current release update

Reviewed 2026-09-30. These are qualitative selections under the maintenance
procedure, with the following evidence gaps and maintainer constraints.

- **Planner:** Opus 5.5 high and Sol 6.1 high balance general reasoning quality
  against effort cost in [AA's index](https://artificialanalysis.ai/leaderboards/models).
  These are indirect plan-quality judgments, not measured planning optima.
  Planner tertiary remains empty: the maintainer excluded Gemini 4 Argon
  because it is not publicly available. Revisit on public availability and
  exact-release planning or repository-comprehension evidence.
- **Executor:** Opus 5.5 medium prioritizes repository quality; Sol 6.1 medium
  offers lower measured spend. [FrontierCode](https://cognition.com/frontiercode)
  and [AA agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex)
  inform the effort choices. Sonnet 5.5 high is a balanced fallback; its xhigh
  terminal gains do not justify the general cost/time premium against other
  models. Opus medium lacks matched AA terminal coverage, and
  [VulcanBench](https://vulcanbench.com/benchmarks/swe-v4-opus55-v315.html)
  includes fallback-model turns. Revisit on matched, fallback-free effort runs.
- **Design/taste:** Opus 5.5 max, Sol 6.1 max, and Astra max retain the
  configurations measured by [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend).
  Sol's consumer-product preference and [OpenDesign](https://open-design.ai/llm-arena-for-design/)
  prototype results support its secondary slot; Astra adds
  [screenshot-following evidence](https://arena.ai/leaderboard/code/image-to-webdev).
  OpenDesign does not disclose effort, so its costs are not attributed to max.
  These selections are not proven economic optima. Revisit on matched visual
  effort/cost/time data and accessible independent Design Arena results.
