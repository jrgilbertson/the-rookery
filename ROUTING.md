# Routing work

`route-work` turns one explicit routing request and its supplied evidence into
one recommended way to start the work: a first workflow, a coordinator, a
pattern, a roster of roles with models and effort, and a copy/paste kickoff.
When work already has a proven owner it says where to resume. When it lacks a
routing fact it asks. It leaves execution to the selected workflow.

The coordinator is not an added worker. It is the session the operator pastes
the kickoff into, and it runs on the profile the model table names for its
starting workflow. It owns the human-facing conversation. In Single owner, the
default, it does all the work itself. When a route adds workers, it also
dispatches them and integrates their results. It judges completion within
supplied authority.

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
summary. Without an explicitly supplied artifact or locator, use the request
itself as the kickoff's source of truth.

## Preserve authority

The router assesses supplied evidence, renders one card, and exits without
changing state or persisting routing state outside the visible conversation.

Never add authority the operator did not supply. An operator request to
implement the work, including a request to route the kickoff to implement it,
is implementation authorization. Artifact approval is task state, not an
authority grant.

Never list permissions the operator did not mention, even to say they are not
inferred. The card never narrates phases, checkpoints, or stopping points, and
never says where plans are stored.

Leave supplied grants off the card. When the operator states a limit, including
saying some authority is withheld or not supplied, such as a grill without
document-write authority, or attaches a condition or scope to a grant, state it
on the card in one sentence and never drop it. Unless the operator granted
merge, every kickoff whose run may reach implementation, including `impeccable`
design and front-end work, ends its authority text with "Don't merge without
human approval." When the operator withheld merge, that line is the limit's one
sentence. Otherwise say nothing about authority.

## Handle parent, child, and existing work

Use only supplied issue-family and plan state. This table can replace the owner
or switch the card to Resume; apply it before the owner table.

| Supplied state | Result |
|---|---|
| Family coverage, descendants, blockers, readiness, or structure is incomplete or uncertain | Route to `managing-issues`. Do not pick a child or call the family ready. |
| A complete current family is supplied, but parent integration, sequencing, or shared-surface planning is missing | Route the parent to `ce-plan` |
| An approved parent plan and implementation authorization are supplied | Route to `ce-work` |
| An approved parent plan is supplied, but implementation authorization is absent | Return Questions to establish implementation authority |
| A child is named directly | Route from what needs to happen first for that child while preserving supplied parent constraints, unless supplied evidence says unresolved family state blocks it |
| The requested phase already has a proven active owner | Return a Resume card and no duplicate kickoff unless replacement or restart is explicit |

A named in-flight owner is proven only by an operator statement or supplied
artifact that names a specific owner for the requested phase. A stated
worktree, branch, pull request, worker, or parallel effort without that phase
owner still uses the normal Route. Setup and the kickoff then each end with the
occupancy sentence, exactly "No named owner was proven for this phase; this
start is still allowed." Treat occupancy as unknown, not vacant.

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
| Concrete implementation is ready and authorized, including an already-diagnosed fix | `ce-work` | Execute within the supplied authority |
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
independent. A stated worktree, branch, pull request, worker, or parallel
effort is occupancy evidence, not evidence of independent units.

| Pattern | Roles | Use when | Guardrail |
|---|---|---|---|
| Single owner | The coordinator alone, on the selected owner's profile. It writes the work itself. | The default when neither other pattern applies | One worker covers later stages of the same owner. |
| Executor + Reviewer | Two workers: the coordinator writes and revises; the Reviewer only judges. | Explicit acceptance criteria exist or the operator asks for review | One round. Stop when the Reviewer's stated criteria pass or fail. Hand the Reviewer the criteria. The Reviewer does not write the artifact. |
| Coordinator + Executors | The coordinator runs the starting workflow, which dispatches Executor workers to implement the units. Scout or Researcher workers only for search slices. | Implementation is expected and supplied evidence establishes independent units, whichever workflow starts | The kickoff names the Executors' model and effort; the workflow decides how many run and when. |

Size the roster for where the run ends, not where it starts, including a
brainstorm, grill, debug, or plan that implementation will follow. Do not ask
whether implementation follows; when nothing says so, size for the starting
workflow and invite the override in Why.

Use one Executor per named or counted unit, or up to three when evidence
establishes independent units without naming or counting them.

An advisor only gathers bounded evidence. Do not count it as a worker and do
not give it ownership.

## Keep orchestration and ownership separate

Workflow ownership, structured orchestration, and ownership handoff are
independent decisions.

Supervised orchestration through Orca keeps the current coordinator as the sole
human-facing owner and integrator, and acting on it requires Orca's installed
version-matched orchestration contract. A full handoff transfers human-facing
ownership to the receiving worktree or agent and leaves the sender no
monitoring duty.

When supervised orchestration is selected, say so in Setup and the kickoff,
tell the operator to follow Orca's installed contract, and add to Setup: once
orchestration is running, continue with the coordinator in its terminal and
close this session. The kickoff's orchestration sentence says "Orca
orchestration" in those words and tells the coordinator to use Orca's
`orchestration` skill when it is installed, because the receiving session
matches that phrase to the skill. Do not copy Orca commands into the card.

## Select profiles

Each seat and worker uses the profile whose row in the model table names it.

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

**Last reviewed: 2026-09-22**

| Profile | Seat or worker | Primary | Secondary | Tertiary |
|---|---|---|---|---|
| Planner | The coordinator on `ce-brainstorm`, `grill-with-docs`, `ce-plan`, or `managing-issues` | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6-astra` / high | — |
| Executor | The coordinator on `ce-work`, and Executor workers | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6-sol` / high | xAI / `grok-4.7` / high |
| Reviewer | Reviewer workers and named review or verification gates | OpenAI / `gpt-6-sol` / high | Anthropic / `claude-opus-5-5` / high | xAI / `grok-4.7` / high |
| Critic | The Reviewer or an advisor only when the judgment is adversarial; never the coordinator on `grill-with-docs` | OpenAI / `gpt-6-sol` / max | Anthropic / `claude-opus-5-5` / high | xAI / `grok-4.7` / high |
| Researcher | The coordinator on `ce-debug`, and Researcher workers for evidence-backed synthesis | OpenAI / `gpt-6-sol` / high | Anthropic / `claude-opus-5-5` / high | xAI / `grok-4.7` / high |
| Scout | Scout workers and advisors that gather bounded evidence | xAI / `grok-4.7` / high | OpenAI / `gpt-6-sol` / high | — |
| Design/taste | The coordinator on `impeccable`, and the Reviewer when the finish line is taste | Anthropic / `claude-fable-5-1` / medium | OpenAI / `gpt-6-astra` / medium | — |

## Return one portable response

The card is the entire final answer, with no preamble, narration, or closing
remark around it. Its first line is exactly `**Route**`, `**Resume**`, or
`**Questions**`. Bold marks that line and the section labels, with a blank line
after each; use no `#` headings, and never fence the kickoff. Write every
section as natural prose, not a string of stock sentences, except the occupancy
sentence, which is emitted exactly when it applies. Render model IDs as
ordinary names, such as "Fable 5.1 at medium".

### Route

    **Route**

    Start with [starting workflow] on [coordinator model] at [effort].

    **Why**

    [One or two sentences on what needs to happen first and why this pattern fits. Name where the run is expected to end, which the roster was sized for; when the run reaches implementation, say that the coordinator carries the work into it. When the route relies on a pattern or roster default instead of supplied evidence, name the default and invite the override in one reply, such as naming independent units to add Executors.]

    **Setup**

    [The roster: every role in the pattern with its model and effort, stated even when it repeats the decision line. The Executor count. The pattern, named in a sentence, when it is not Single owner. Orchestration only when it differs from the default. Authority only as the authority rules require. An advisor, the occupancy sentence, or a profile fallback only when it applies.]

    **Copy/paste kickoff**

    Start [starting workflow] from [stable artifact locator or concise supplied request]. You are the coordinator on [model] at [effort]. [Each Reviewer, advisor, Scout, or Researcher worker with its model and effort. In Executor + Reviewer: hand the Reviewer the criteria and stop after one round, when they pass or fail.] [Subscription billing constraint.] [In Coordinator + Executors: When the work reaches implementation, run implementation workers on [Executor model] at [effort]; [the implementing workflow] decides how many and how to schedule them.] [Orchestration sentence only when it differs from the default.] Treat [the supplied artifact or request] as the source of truth. [Authority as the authority rules require, ending with the no-merge line when the run may reach implementation.] [Occupancy sentence last, only when it applies.]

The decision line never names a role; roles live in Setup. The kickoff states
each worker's model and effort as settings to apply and leaves how workers are
started to the workflow and harness. The implementation-workers sentence keeps
its template wording exactly; the Executor count and units stay in Setup. The
kickoff must stand alone when pasted, so it repeats every role's model and
effort, authority, and any occupancy sentence.

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

Order questions by routing impact: owner, then pattern, then profile, then
orchestration and ownership handoff. Batch only independent questions; a
dependent question waits for its prerequisite. Every question carries one
concrete recommendation, never a test for the operator to apply, and its reason
cites only supplied facts or contract defaults. Use the contract default where
one exists; where the operator holds the fact, recommend the answer that lets
routing proceed under the defaults. A Questions card names no workflow, model,
profile, or kickoff. When the starting owner falls outside the seven, the
recommendation is the supported-owner table link.

<!-- route-work-contract-end -->

> Maintainer note: root `ROUTING.md` is the human-edited source. Copy it
> byte-for-byte to `skills/route-work/references/routing.md` in the same change.

## Maintaining the model table

Maintainers update the table manually from external evidence. Benchmark scores,
cost, quota, confidence, automatic rankings, and staleness state stay outside
the contract.

### Order models by cost of pass

- Order each row by cost of pass: cost per attempt divided by pass rate,
  measured on work like that role's.
- A row lists only models that earn a place, so some rows have fewer than
  three.
- A model may rank by a capability the others lack, as xAI does for Scout
  with X search.
- A subscription already paid for may keep an otherwise dominated model in a
  last slot where it still does the role's work well.

### Pick effort where the curve bends

- Choose the cheapest effort whose pass rate on the role's work is close to
  that model's ceiling. That is where its cost per extra point bends upward.
- A composite index across effort levels shows the curve's shape, but its
  average is not a pass rate. It hides how low effort fails on hard tasks, so
  low effort always looks cheapest.
- Confirm each effort choice on at least two independent boards that report
  every effort level, such as the Artificial Analysis Intelligence Index,
  Zapier's AutomationBench, and VulcanBench.

### Use evidence that matches the role

- Executor: coding-agent boards such as FrontierCode, CursorBench,
  Terminal-Bench, or a coding-agent index. Cognition's FrontierCode
  leaderboard publishes a pass rate and a cost per rollout for every effort
  level in each model's native harness, usually on launch day, in
  https://cognition.com/data/frontiercode-leaderboard/data.json.
- Design/taste: human-preference boards.
- Planner: no public benchmark scores planning or coordination work, so this
  row is a judgment call. It follows vendor practice of giving planning more
  reasoning effort than execution; revisit it when a planning benchmark
  reports every effort level.
