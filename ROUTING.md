# Routing work

Use `route-work` when you want help choosing where to start a task. It recommends
one workflow, who will do the work, models and effort, and a kickoff you can
copy into the receiving session. It returns **Resume** when the requested phase
already has a proven owner, or **Questions** when a routing fact is missing.

## How it works

Ask explicitly to route or kick off the work. Other planning, debugging,
design, implementation, and issue requests use their normal workflows.

The coordinator is the session receiving the kickoff. It owns the conversation
and completion, and usually does the work itself. With workers, it delegates
assigned units and implements only work it owns. An Executor implements assigned
work; a Reviewer judges it. Planner is a model/effort profile, not another agent.
The coordinator plans scope and dependencies and coordinates owners as needed.
A parent issue alone does not make it coordination-only; preserve supplied
implementation boundaries.

Routing uses your request, one explicitly named primary artifact, directly
cited repository instructions, and authoritative metadata already supplied in
context. For an issue, it reads the named node and supplied or visible
relationship summary. It does not search the repository broadly, walk the
issue graph, or probe external state. Mentioning facts about an artifact does
not supply the artifact or its relationships.

The router recommends a route and exits without changing state or storing
routing state outside the conversation. Pasting the kickoff approves starting
the work. Your stated grants, limits, and conditions go into Setup and the
kickoff once, unchanged; the router adds no authority. Withheld or unsupplied
authority remains a limit. Predicting later implementation grants nothing;
the selected workflow controls its own gates.

## Choose the starting workflow

Choose the first question to answer or change to make. Apply the
[existing-work rules](#existing-work-and-issue-families) before this table.
Choose from the work itself, not the host, model, or predicted later steps.

<a id="choose-what-needs-to-happen-first"></a>

| What you need first | Workflow |
|---|---|
| Decide what to build or settle its scope | `ce-brainstorm` |
| Pressure-test a supplied decision document in dependency order | `grill-with-docs` |
| Plan execution when the outcome and acceptance criteria are settled | `ce-plan` |
| Find the cause of broken or unexpected behavior | `ce-debug` |
| Implement concrete work, including a fix whose cause is known | `ce-work` |
| Inspect or change issues, relationships, coverage, or readiness | `managing-issues` |
| Decide visual direction, interaction, or design quality | `impeccable` |

Let `impeccable` choose its workflow unless one exact command is already obvious.
For work outside these seven workflows, return Questions with no owner and point
to this table. Ask only questions that would change the route, using supplied
evidence and defaults first. A routing attempt may span multiple turns.

## Choose who does the work

Start with **Single owner**, even for implementation. Add Executors only when
supplied evidence establishes independent units, such as separate modules with
separate write paths, or a plan that states its units are independent.

| Pattern | Who does what | When to use it |
|---|---|---|
| Single owner | The coordinator does the work on the starting workflow's profile. | Default. Later stages of the same owner's work do not require extra workers. |
| Executor + Reviewer | The coordinator writes and revises; the Reviewer judges without editing. | You request a separate Reviewer, or explicit acceptance criteria exist for work that will not implement through `ce-work`, which runs its own review. |
| Coordinator + Executors | The coordinator runs the workflow; Executors implement independent units. | Implementation is expected or predicted and independent units are established. |

For Executor + Reviewer, use one review round: give the Reviewer the criteria
and stop when they pass or fail. If both multi-worker patterns apply, use
Coordinator + Executors and add the Reviewer.

Count workers, not steps. Use one Executor per named or counted unit, or up to
three when independent units are established without a count. The kickoff
assigns their model and effort; the executing workflow decides how many run
and when. The coordinator is the receiving session, not an added worker.

Size the roster for the expected end of the work. Assume it reaches implementation
unless you limit it to planning or withhold implementation, or the starting
workflow is `managing-issues` or `grill-with-docs`. Do not ask whether
implementation follows. An advisor gathers bounded evidence on its coordinator's
profile; it has no ownership and does not count as a worker.

## Choose models and effort

**Last reviewed: 2026-10-13**

| Profile | Used for | Primary or selection rule | Secondary | Tertiary |
|---|---|---|---|---|
| Planner | Coordinator on `ce-brainstorm`, `grill-with-docs`, `ce-plan`, or `managing-issues` | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6.1-sol` / high | Google / `gemini-4-argon` / high |
| Executor | Coordinator on `ce-work` or `ce-debug`, and Executor workers | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / medium | — |
| Reviewer | Reviews, including adversarial reviews and verification gates | [Different-provider Executor](#reviewer-selection) | — | — |
| Design/taste | Coordinator on `impeccable`, and reviews judged on taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | Google / `gemini-4-argon` / high |

Design/taste recommendations follow available evals and list tested efforts;
in practice, the maintainer typically chooses the model's Executor or Planner effort.

Each ranked row contains at most one model per provider. Empty slots are allowed.
Argon's Planner and Design/taste choices are provisional; see
[current rationale](#current-rationale).

Each coordinator and worker uses its assigned profile. Resolve your model
choices and supplied availability before selecting a Reviewer. Use listed
order to skip unavailable models without changing the starting workflow.
When availability is unknown, keep the default and omit availability commentary.

Use the listed effort unless you choose another setting. The router may suggest
a higher effort but selects it only with your approval. The Design/taste
footnote describes maintainer practice, not an automatic effort override.

Every Route kickoff requires the assigned providers' official CLIs with
subscription authentication. Do not use API-key billing or switch to it as a
fallback. Report a blocker if subscription access cannot be established or
its usage limit is reached.

## Use the routing response

The response is a portable card: a Route, Resume, or Questions. A Route names
one starting workflow, explains the choice, lists the setup, and gives you a
standalone kickoff. The receiving workflow executes the work.

Use the [response rules](#response-rules) for the exact templates and required
wording. The card contains no narration of phases, checkpoints, stopping
points, or plan storage.

## Reference

### Existing work and issue families

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

### Missing information and unavailable models

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

### Delegation and handoffs

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

### Response rules

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

### Maintaining the recommendations

On a maintainer's request, recheck the affected profiles against independent,
exact-release evaluations. Compare quality, measured task cost, and time for
the role; prefer a useful balance over the highest score. Select one model per
provider in each ranked row. Keep Reviewer as a selection rule.

The detailed [evaluation procedure](https://github.com/jrgilbertson/the-rookery/blob/main/skills/route-work/references/model-evaluations.md)
covers sources, methodology checks, effort comparisons, and provisional choices.
It applies to maintenance, not routing a task. Update the table, review date,
and affected rationale together, then synchronize the bundled copy.

### Current rationale

Reviewed 2026-10-13. These are qualitative recommendations, with the following
limits and revisit triggers.

- **Planner:** Opus 5.5 high and Sol 6.1 high retain a useful reasoning/cost
  balance in [AA's index](https://artificialanalysis.ai/leaderboards/models).
  Argon high adds a third provider. These are indirect planning judgments;
  direct planning evidence and matched Argon latency remain incomplete.
  Revisit on stronger planning or repository-comprehension results.
- **Executor:** Opus 5.5 medium and Sol 6.1 medium balance repository quality,
  cost, and time on [FrontierCode 1.1](https://cognition.com/frontiercode) and
  [AA's agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex).
  FrontierCode's Argon medium costs about $6.74/task versus Opus $0.80 and
  Sol $0.36, with a lower mergeability score. Its Chisel harness differs from
  [AA's Antigravity CLI high run](https://artificialanalysis.ai/agents/coding-agents/comparisons/antigravity-cli-vs-claude-code).
  Leave tertiary empty; revisit if a different-provider substitute justifies
  its quality, cost, and time. Opus fallback-enabled results, including
  [VulcanBench](https://vulcanbench.com/benchmarks/swe-v4-opus55-v315.html),
  do not establish pure-model effort performance.
- **Design/taste:** Opus max and Sol max retain configurations measured by
  [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend).
  Argon high has preliminary frontend preference evidence; it lacks
  [screenshot-following coverage](https://arena.ai/leaderboard/code/image-to-webdev).
  Astra remains a screenshot-focused specialist outside the ranked row.
  [OpenDesign](https://open-design.ai/llm-arena-for-design/) supports Sol's
  general prototype fit but does not disclose effort. Max is not proven
  necessary or economically optimal. Revisit on matched visual quality,
  task cost, and time across efforts and accessible independent
  [Design Arena](https://www.designarena.ai/leaderboard/website) results.

Benchmark dollars do not predict subscription quotas. Missing exact-release
results are unevaluated, not evidence of poor performance. New
[Muse Wonder results](https://artificialanalysis.ai/articles/muse-wonder/) and
[AA-3D](https://artificialanalysis.ai/articles/aa-3d) warrant tracking;
the latter is specialist 3D evidence and lacks Argon coverage. AA's
[FrontierCode publication](https://artificialanalysis.ai/articles/frontiercode)
reuses Cognition's evidence and is not independent corroboration.
