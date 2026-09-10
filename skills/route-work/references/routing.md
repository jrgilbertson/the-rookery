# Routing work

`route-work` turns one explicit routing request and its supplied evidence into
one recommended way to start the work: a first workflow, a lead, a pattern, a
roster of roles with models and effort, and a copy/paste kickoff. When work
already has a proven owner it says where to resume. When it lacks a routing
fact it asks. It leaves execution to the selected workflow.

Workflow names in its cards are portable capability labels. Using this router
does not require those workflow packages to be installed.

## Activation boundary

Route only when the operator explicitly asks to route or kick off work. A
planning, debugging, design, implementation, or issue request without that
intent proceeds through its normal workflow and does not produce a card.

One routing attempt may span multiple conversational turns. Ask only questions
that change the owner, pattern, profile, structured orchestration, ownership
handoff, or placement. Use supplied evidence and contract defaults before
asking. Continue until the setup is clear.

Put product discovery, diagnosis, planning, and design on those owners' route
cards. Each response returns one Route, Resume, or Questions card and persists
no routing state outside the visible conversation.

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
changing state.

Copy only authority the operator supplied. Artifact approval is task state,
not an authority grant. An implementation kickoff never
infers permission to commit, push, open a pull request, publish, merge, or
change external state. Authorized document writes use repository-defined
locations. Supplied authority is the only thing that bounds how far the lead
carries the work; the card never narrates phases, checkpoints, or stopping points beyond it, and never says where plans are
stored. When the operator supplied a grant or an explicit limit, state it on
the card in one sentence; an operator saying some authority is withheld or
not supplied is an explicit limit, and it is never dropped. When the operator
said nothing about authority, say nothing about it. Never list
unsupplied permissions on a card, even to say they are not inferred.

## Handle parent, child, and existing work

Use only supplied issue-family and plan state. This table can replace the owner
or switch the card to Resume; apply it before the owner table.

| Supplied state | Result |
|---|---|
| Family coverage, descendants, blockers, readiness, or structure is incomplete or uncertain | Route to `managing-issues`. Do not pick a child or call the family ready. |
| A complete current family is supplied, but parent integration, sequencing, or shared-surface planning is missing | Route the parent to `ce-plan` |
| An approved parent plan and implementation authorization are supplied | Route to `ce-work` |
| An approved parent plan is supplied, but implementation authorization is absent | Return Questions to establish implementation authority |
| A child is named directly | Route from what needs to happen first for that child while preserving supplied parent constraints |
| The requested phase already has a proven active owner | Return a Resume card and no duplicate kickoff unless replacement or restart is explicit |

A proven active owner of the requested phase takes precedence. A directly named
child uses the owner table unless supplied evidence says unresolved family
state blocks it.

Active ownership is proven only by an operator statement or supplied artifact
that names a specific in-flight owner for the requested phase. A stated
worktree, branch, pull request, worker, or parallel effort without that phase
owner adds `Active ownership unverified` to the normal kickoff: ownership is
unknown, not vacant. The router does not discover or monitor ownership.

## Choose what needs to happen first

Choose exactly one starting workflow based on what needs to happen first: the
earliest question to answer or durable change to make before useful work can
continue. Choose it from this table, not from the host, model, or later steps.
The lead runs it, and the lead carries the work forward from there within
supplied authority.

| What needs to happen first | Owner | Discriminator |
|---|---|---|
| Product outcome, behavior, or scope boundary is unsettled | `ce-brainstorm` | Clarify what should be built before planning how |
| A supplied decision document needs a focused, dependency-ordered pressure test | `grill-with-docs` | Run a focused grill |
| Outcome and acceptance boundary are settled, but the execution plan is missing | `ce-plan` | Plan without reopening settled product choices |
| Broken or unexpected behavior still has an unresolved causal chain | `ce-debug` | Diagnose first; an established cause and fix route to `ce-work` |
| Concrete implementation is ready and authorized, including an already-diagnosed fix | `ce-work` | Execute within the supplied authority |
| Canonical issue content, relationship graph, coverage, or readiness state must be inspected or changed | `managing-issues` | The first need is to inspect or edit issues, links, coverage, or ready-or-not state |
| Visual direction, interaction design, or design quality is unresolved | `impeccable` | Let Impeccable select its internal workflow unless one exact command is already obvious |

Work that needs a starting owner outside these seven gets a Questions card
that names no owner and points to the supported starting owners in the table at
https://github.com/jrgilbertson/the-rookery/blob/main/ROUTING.md#choose-what-needs-to-happen-first.

## Ambiguity and missing input

- If one request could be two different owners, ask the discriminator.
- For two separate workstreams that could both start and neither blocks the
  other, ask which starts first. A recommended order is allowed; the operator
  still chooses. The Route card names exactly one starting workflow.
- When the remaining uncertainty belongs to the downstream work, route to its
  workflow instead of continuing to ask.
- If the request already names the work, route it. Do not require a plan file,
  issue, or other artifact first. When issue-family state is supplied, use
  Handle parent, child, and existing work first.
- If a named or required primary artifact cannot be read, the operator says
  they cannot answer a required routing question, the selected workflow is
  confirmed unavailable, or all three profiles for a role are stated
  unavailable, return a Questions card asking for what would let routing
  proceed. Name no workflow in it, not even as an example.

## Estimate the pattern and roster

Every route has a lead. Name the role for each worker, and count workers, not
steps.

When implementation is expected, start with Lead + Executors. Use Single
owner only when supplied evidence establishes one bounded piece or sequential
work for one owner. Unnamed units are not evidence of a bounded piece.

| Pattern | Roles | Use when | Guardrail |
|---|---|---|---|
| Single owner | The lead alone, in the selected owner's role. | The run ends with the starting workflow, the work is one bounded piece, or it is sequential phases of one owner | One worker covers later stages of the same owner. |
| Executor + Reviewer | Two workers: the lead writes and revises; the Reviewer only judges. | Explicit acceptance criteria exist or the operator asks for review | One round. Stop when the Reviewer's stated criteria pass or fail. Hand the Reviewer the criteria. The Reviewer does not write the artifact. This is not advisor consultation. |
| Lead + Executors | Lead plans and dispatches; Executor workers implement units. Scout or Researcher workers only for search slices. | Implementation is expected, from supplied authority or an operator statement that implementation follows, and the work has or will yield independent units, whichever workflow starts | Give each worker a separate write path before parallel writes. |

Size the roster for where the run ends, not where it starts, including a
brainstorm, grill, debug, or plan that implementation will follow. The lead's
profile still comes from the starting workflow. Do not ask whether
implementation follows; when nothing says so, size for the starting workflow
and invite the override in Why. Add a Reviewer when the input carries explicit
acceptance criteria or the operator asks.

Budget five concurrent workers total, including the lead and Reviewer. Use
one Executor per named unit, or up to three when units are unnamed, capped by
the remaining slots. Queue units that do not fit; keep all requested work.

Use Critic in the Reviewer role only when the judgment is adversarial. Use
Design/taste as the judge only when the finish line is taste.

An advisor only gathers bounded evidence. Do not count it as a worker and do
not give it ownership. If the operator asked for an advisor, mention it in
Setup. Subagents, forks, teams, and background sessions are how work runs, not
which pattern to recommend. The lead may change the pattern when new evidence
justifies it.

## Keep orchestration and placement separate

Workflow ownership, structured orchestration, ownership handoff, and worktree
placement are independent decisions.

| Axis | Choice | Meaning |
|---|---|---|
| Structured orchestration | None | Continue without structured orchestration |
| Structured orchestration | Supervised through Orca | The current coordinator remains the sole human-facing owner and integrator; acting on this recommendation requires Orca's installed version-matched orchestration contract |
| Ownership | Current owner or full handoff | Full handoff transfers human-facing ownership to the receiving worktree or agent; the sender gains no monitoring duty |
| Placement | Current worktree or isolated worktree | Use isolation for concurrent mutation; disjoint write scopes are still required before parallel writes |

The selected starting workflow remains the owner. Structured orchestration is
optional and currently depends on Orca; ordinary worktree placement does not.
When supervised orchestration is selected, say so in Setup and the kickoff,
tell the operator to follow Orca's installed contract, and add to Setup: once
orchestration is running, continue with the lead in its terminal and close
this session. Do not copy Orca commands into the card. Read-only scouts and
fresh-context reviewers can work in the current worktree.

## Select the role profile

Pick each role's profile from the pattern:

- The lead uses Lead, except that a `ce-work` lead uses Executor unless it
  coordinates separate Executor workers, a `ce-debug` lead uses Researcher, and
  an `impeccable` lead uses Design/taste.
- Executor workers use Executor. Reviewer workers use Reviewer.

| Role | Responsibilities |
|---|---|
| Lead | Runs the starting workflow, plans, dispatches workers, and revises the plan from their results |
| Executor | Implements the assigned change and revises it |
| Reviewer | Independent evaluators and named review or verification gates |
| Critic | Independent adversarial pressure-test advisors or evaluators; not the owning `grill-with-docs` route |
| Researcher | Causal investigation inside `ce-debug` and evidence-backed synthesis |
| Scout | Bounded evidence gathering and advisor research |
| Design/taste | `impeccable` and design-quality evaluation |

### Availability fallback

Use operator-stated or already-supplied availability to filter unavailable
profiles in primary, secondary, then tertiary order. Keep the selected owner
unchanged. When availability is unknown, keep the default selection and omit
availability from the response. Mention availability only when it changes a
selected profile.

### Subscription billing

Every Route kickoff includes this execution constraint: use the assigned providers’ official CLIs with subscription authentication.
Do not use API-key billing or switch to it as a fallback. If subscription access cannot be established or its usage limit is reached, report the blocker.
The executing workflow verifies authentication; the router does not probe credentials.

### Effort escalation

Use the table's listed effort by default. The router may suggest a higher
effort, but selects one only when the operator approves it.

## Model and effort recommendations

**Last reviewed: 2026-09-09**

| Role | Primary | Secondary | Tertiary |
|---|---|---|---|
| Lead | Anthropic / `claude-fable-5-1` / medium | OpenAI / `gpt-6-astra` / low | xAI / `grok-4.6` / high |
| Executor | xAI / `grok-4.6` / high | Anthropic / `claude-opus-5` / medium | OpenAI / `gpt-5.6-sol` / medium |
| Reviewer | OpenAI / `gpt-5.6-sol` / high | Anthropic / `claude-opus-5` / medium | xAI / `grok-4.6` / high |
| Critic | OpenAI / `gpt-5.6-sol` / xhigh | Anthropic / `claude-opus-5` / medium | xAI / `grok-4.6` / high |
| Researcher | OpenAI / `gpt-5.6-sol` / high | xAI / `grok-4.6` / high | Anthropic / `claude-opus-5` / medium |
| Scout | xAI / `grok-4.6` / high | OpenAI / `gpt-5.6-terra` / high | Anthropic / `claude-opus-5` / medium |
| Design/taste | Anthropic / `claude-fable-5-1` / medium | OpenAI / `gpt-5.6-sol` / high | xAI / `grok-4.6` / high |

## Return one portable response

The card is the entire final answer, with no preamble, narration, or closing remark
around it. Its first line is exactly `**Route**`, `**Resume**`, or
`**Questions**`. Bold marks that line and the section labels, with a blank
line after each; use no `#` headings, and never fence the kickoff. Write every
section as natural prose, not a string of stock sentences, and render model
IDs as ordinary names, such as "Fable 5.1 at medium".

### Route

    **Route**

    Start with [starting workflow] on [lead model] at [effort].

    **Why**

    [One or two sentences on what needs to happen first and why this pattern fits. Name where the run is expected to end, which the roster was sized for, and when implementation is authorized say that the lead carries the work into it. Name any pattern or roster default the route relied on instead of supplied evidence, so the operator can override it in one reply; availability stays out of the card when it is unknown.]

    **Setup**

    [The roster: every role in the pattern with its model and effort, stated even when it repeats the decision line. The Executor count. The pattern, named in a sentence, when it is not Single owner. Orchestration and placement only when they differ from the default. Authority only when the operator supplied it. An advisor, Active ownership unverified, or a profile fallback only when it applies.]

    **Copy/paste kickoff**

    Start [starting workflow] from [stable artifact locator or concise supplied request]. You are the lead on [model] at [effort]. [Each other role with its model, effort, and count.] [Subscription billing constraint.] [Orchestration and placement sentences only when they differ from the default.] Treat [the supplied artifact or request] as the source of truth. [Supplied authority in one sentence, only when the operator supplied it.]

The decision line never names a role; roles live in Setup. A single-owner
Setup omits placement and orchestration when they are the default. The
kickoff must stand alone when pasted, so it repeats the roster, supplied
authority, and any `Active ownership unverified` marker.

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
orchestration and placement. Batch only independent questions; a dependent
question waits for its prerequisite. Every question carries a recommendation
on its own line: one concrete answer, the way a grill recommends, never a test
for the operator to apply. Use the contract default where one exists; where
the operator holds the fact, recommend the answer that lets routing proceed
under the defaults. Never write "no default". A Questions card
names no workflow, model, role profile, or kickoff. When the starting owner falls outside the
seven, recommend choosing from the supported-owner table linked above; that
pointer is the concrete answer there, since the card may name no workflow.

<!-- route-work-contract-end -->

> Maintainer note: root `ROUTING.md` is the human-edited source. Copy it
> byte-for-byte to `skills/route-work/references/routing.md` in the same change.

Maintainers update the model table manually from external evidence. Benchmark
scores, cost, quota, confidence, automatic rankings, and staleness state stay
outside the contract.
