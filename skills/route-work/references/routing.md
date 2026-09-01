# Routing work

`route-work` turns one explicit routing request and its supplied evidence into
one supported first workflow owner, a continuation of proven in-flight work, or
a named stop. It returns a portable kickoff and leaves execution to the selected
workflow.

Workflow names in its cards are portable capability labels. Using this router
does not require those workflow packages to be installed.

## Activation boundary

Route only when the operator explicitly asks to route or kick off work. A
planning, debugging, design, implementation, or issue request without that
intent proceeds through its normal workflow and does not produce a route card.

One routing attempt may span multiple conversational turns. Ask only questions
that change the owner, topology, profile, structured orchestration, ownership
handoff, or placement. Ask independent questions together. Wait to ask a
question whose answer depends on another unanswered question. Use supplied
evidence and contract defaults before asking. Continue until the setup is
clear, a required artifact is unavailable, or the operator cannot supply a
required routing fact.

Put product discovery, diagnosis, planning, and design on those owners' route
cards. Each response returns one route, continuation, clarification, or stop
and persists no routing state outside the visible conversation.

## Inspect only supplied evidence

The assessment may read:

- the request;
- one explicitly named primary artifact, when present;
- directly cited repository instructions; and
- authoritative metadata already supplied in the current context.

For an issue, use only the named node and an already-supplied or visible
relationship summary. Do not conduct a broad repository search, recursively
walk an issue graph, or probe external state.

## Preserve authority

The router assesses supplied evidence, renders one card, and exits without
changing state.

Copy only authority the operator supplied. An implementation kickoff never
infers permission to commit, push, open a pull request, publish, merge, or
change external state. A grilling kickoff may pressure-test supplied documents,
but it withholds domain-model or ADR writes unless the operator authorizes them
in repository-defined locations.

## Handle parent, child, and existing work

Use only supplied issue-family and plan state. This table can replace the owner
or switch the card to Continuation; apply it before the owner table.

| Supplied state | Result |
|---|---|
| Family coverage, descendants, blockers, readiness, or topology is incomplete or uncertain | Route to `managing-issues`. Do not pick a child or call the family ready. |
| A complete current family is supplied, but parent integration, sequencing, or shared-surface planning is missing | Route the parent to `ce-plan` |
| An approved parent plan is supplied | Route to `ce-work`; use Orchestrator/planner + Executors only when independent units, one integrator, and safe write boundaries are proven |
| A child is named directly | Route from what needs to happen first for that child while preserving supplied parent constraints |
| The requested phase already has a proven active owner | Return continuation context and no duplicate kickoff unless replacement or restart is explicit |

A proven active owner of the requested phase takes precedence. A directly named
child uses the owner table unless supplied evidence says unresolved family
state blocks it.

Active ownership is proven only by an operator statement or supplied artifact
that names a specific in-flight owner for the requested phase. A stated
worktree, branch, pull request, worker, or parallel effort without that phase
owner adds `Active ownership unverified` to the normal kickoff. The router does
not discover or monitor ownership.

## Choose what needs to happen first

Choose exactly one owner based on what needs to happen first: the earliest
question to answer or durable change to make before useful work can continue.
Choose the owner from this table, not from the host, model, or later steps.

| What needs to happen first | Owner | Discriminator |
|---|---|---|
| Product outcome, behavior, or scope boundary is unsettled | `ce-brainstorm` | Clarify what should be built before planning how |
| A supplied decision document needs a focused, dependency-ordered pressure test | `grill-with-docs` | Run a focused grill |
| Outcome and acceptance boundary are settled, but the execution plan is missing | `ce-plan` | Plan without reopening settled product choices |
| Broken or unexpected behavior still has an unresolved causal chain | `ce-debug` | Diagnose first; an established cause and fix route to `ce-work` |
| Concrete implementation is ready and authorized, including an already-diagnosed fix | `ce-work` | Execute within the supplied authority |
| Canonical issue content, relationship graph, coverage, or readiness state must be inspected or changed | `managing-issues` | The first need is to inspect or edit issues, links, coverage, or ready-or-not state |
| Visual direction, interaction design, or design quality is unresolved | `impeccable` | Let Impeccable select its internal workflow unless one exact command is already obvious |

Work that needs a starting owner outside these seven returns
`Unsupported in the current version`. Sequential phases of the same owner
still use that owner.

## Ambiguity and missing input

- If one request could be two different owners, ask the discriminator, then
  stop.
- For two separate workstreams that could both start and neither blocks the
  other, return a Clarification card: ask which starts first. A recommended
  order is allowed; the operator still chooses. The Route card names exactly
  one owner.
- When the remaining uncertainty belongs to the downstream work, route to its
  workflow instead of continuing the clarification.
- If the request already names the work, route it. Do not require a plan file,
  issue, or other artifact first. When issue-family state is supplied, use
  Handle parent, child, and existing work first.
- If a named or required primary artifact cannot be read, or the operator
  cannot answer a required routing question, render the `Insufficient input`
  stop.

## Recommend a starting topology

Recommend one topology for the selected owner. Name the role for each worker.
Count workers, not steps.

| Pattern | Roles | Use when | Guardrail |
|---|---|---|---|
| Single owner | The selected owner's role. One worker. | Bounded work, dependent reasoning, ambiguity, taste-led iteration, sequential phases of the same owner, or no proven coordination benefit | Default. One worker covers later stages of the same owner. |
| Executor + Reviewer | Executor writes and revises. Reviewer only judges. Two workers cycling. | Independent evaluation with explicit criteria or reliable external feedback | Two workers. One round. Stop when the Reviewer's stated criteria pass or fail. The Reviewer does not write the artifact. This is not advisor consultation. |
| Orchestrator/planner + Executors | Orchestrator/planner lead; Executor workers. Scout or Researcher workers only for search slices. | Independent packages, named scopes, and one lead can integrate them | Limit how many workers run at once. Give each worker a separate write path before they write in parallel. |

Use Critic in the Reviewer role only when the judgment is adversarial. Use
Design/taste as the judge only when the finish line is taste.

An advisor only gathers bounded evidence. Do not count it as a topology worker
and do not give it ownership. If the operator asked for an advisor, mention it
in Setup. Subagents, forks, teams, and background sessions are how work runs,
not which topology to recommend. The selected owner may change the starting
topology when new evidence justifies it.

## Keep orchestration and placement separate

Workflow ownership, structured orchestration, ownership handoff, and worktree
placement are independent decisions.

| Axis | Choice | Meaning |
|---|---|---|
| Structured orchestration | None | Continue without structured orchestration |
| Structured orchestration | Supervised through Orca | The current coordinator remains the sole human-facing owner and integrator; acting on this recommendation requires Orca's installed version-matched orchestration contract |
| Ownership | Current owner or full handoff | Full handoff transfers human-facing ownership to the receiving worktree or agent; the sender gains no monitoring duty |
| Placement | Current worktree or isolated worktree | Use isolation for concurrent mutation; disjoint write scopes are still required before parallel writes |

The selected startup workflow remains the owner. Structured orchestration is
optional and currently depends on Orca; ordinary worktree placement does not.
If the operator asked for supervised orchestration, say so in Setup and the
kickoff, and tell the operator to follow Orca's installed contract. Do not copy
Orca commands into the card. Read-only scouts and fresh-context reviewers can
work in the current worktree.

## Select the role profile

Pick one profile from the selected owner and topology:

- Single-owner `ce-work` uses Executor.
- Orchestrator/planner + Executors uses Orchestrator/planner for the lead and
  Executor for workers.
- `ce-debug` uses Researcher.
- `impeccable` uses Design/taste.
- The other startup owners use Orchestrator/planner.

Leave later workflows out of the current owner line.

| Role | Responsibilities |
|---|---|
| Orchestrator/planner | `ce-brainstorm`, the owning `grill-with-docs` workflow, `ce-plan`, `managing-issues`, and a `ce-work` lead coordinating bounded workers |
| Executor | Direct `ce-work`, implementation workers, and execution of a diagnosed fix |
| Reviewer | Independent evaluators and named review or verification gates |
| Critic | Independent adversarial pressure-test advisors or evaluators; not the owning `grill-with-docs` route |
| Researcher | Causal investigation inside `ce-debug` and evidence-backed synthesis |
| Scout | Bounded evidence gathering and advisor research |
| Design/taste | `impeccable` and design-quality evaluation |

### Availability fallback

Use operator-stated or already-supplied availability to filter unavailable
profiles in primary, secondary, then tertiary order. Keep the selected owner
unchanged. If all three profiles are unavailable, return `Profiles exhausted`.
If the workflow itself is confirmed unavailable, return `Owner unavailable`.
When availability is unknown, keep the default selection and omit availability
from the response. Mention availability only when it changes the selected
profile or stops routing.

### Effort escalation

Use the table's listed effort by default. A higher effort may be used only when
the operator explicitly requests it, a governing workflow requires it, or
supplied evidence shows that the default previously failed because of
insufficient reasoning depth. The router may suggest escalation but never
selects it without operator approval.

## Model and effort recommendations

**Last reviewed: 2026-08-26**

| Role | Primary | Secondary | Tertiary |
|---|---|---|---|
| Orchestrator/planner | Anthropic / `claude-fable-5` / medium | OpenAI / `gpt-5.6-sol` / high | xAI / `grok-4.6` / high |
| Executor | xAI / `grok-4.6` / high | Anthropic / `claude-opus-5` / medium | OpenAI / `gpt-5.6-terra` / high |
| Reviewer | OpenAI / `gpt-5.6-sol` / high | Anthropic / `claude-opus-5` / medium | xAI / `grok-4.6` / high |
| Critic | OpenAI / `gpt-5.6-sol` / xhigh | Anthropic / `claude-opus-5` / medium | xAI / `grok-4.6` / high |
| Researcher | OpenAI / `gpt-5.6-sol` / high | xAI / `grok-4.6` / high | Anthropic / `claude-opus-5` / medium |
| Scout | xAI / `grok-4.6` / high | OpenAI / `gpt-5.6-terra` / high | Anthropic / `claude-opus-5` / medium |
| Design/taste | Anthropic / `claude-fable-5` / medium | OpenAI / `gpt-5.6-sol` / high | xAI / `grok-4.6` / high |

The table carries only ordered recommendations and the review date.

## Return one portable response

### Ready route

````markdown
## Route
Workflow: <one startup workflow>
Setup: <natural sentences naming the topology, relevant model and effort, worktree placement, and whether structured orchestration is used>

## Copy/paste kickoff
```text
Start <startup workflow> from <stable artifact locator or concise supplied request>. Use <model> at <effort> for <role>. <Plain-language topology, placement, orchestration, and handoff sentences when material.> Treat <the supplied artifact or request> as the source of truth. <One supplied constraint or authority sentence when material.>
```
````

Write the setup and kickoff as concise, natural prose with concrete names.

- Use "Continue in the current worktree without structured orchestration" for
  the default.
- Render model IDs as ordinary names, such as "Fable 5 at medium" or
  "Grok 4.6 at high."
- For Single owner, state the role once instead of adding a separate topology
  sentence.
- For Executor + Reviewer, name two cycling workers, one round, and stop when
  the Reviewer's stated criteria pass or fail.
- For Orchestrator/planner + Executors, name both profiles and use isolated
  worktrees.
- Name Orca only when supervised orchestration is selected.
- State a profile fallback only when supplied availability changed the
  selection.
- Mention an advisor, conditional handoff, `Active ownership unverified`, or
  supplied authority only when it applies.
- Point to a supplied artifact instead of restating it; when none exists, use a
  concise statement of the supplied request.
- The fenced kickoff is an inert portable prompt written without Markdown
  delimiters; the operator, not the router, uses it.
- A conditional handoff remains controlled by the active workflow;
  owner-changing evidence requires a new explicit route.
- When a lead will coordinate multiple PRs, add: "Prefer small, coherent PRs
  and merge them as they become ready. Run fresh `checking-pr-readiness`
  before opening or updating each PR and `checking-merge-readiness` against
  its current head immediately before each merge. After each merge, continue
  from the updated default branch. Merge only within supplied authority."

### Continuation

```markdown
## Continuation
Owner: <proven active owner>
Resume with: <stable locator, current phase, decisive context, and next action>
```

### Clarification

```markdown
## Clarification
<one unnumbered focused routing question, or a numbered list of related independent routing questions>
```

### Stop

```markdown
## Stop
Stop: <named stop>
Reason: <why routing cannot proceed>
Next prerequisite: <what would permit a new assessment>
```

| Stop | Use when | Next prerequisite |
|---|---|---|
| `Insufficient input` | A named or required primary artifact is unavailable, or the operator cannot supply a required routing fact | Supply the missing discriminating fact or readable artifact |
| `Unsupported in the current version` | The required starting work falls outside the seven startup owners | Choose from the public workflow catalog or request a supported startup route |
| `Owner unavailable` | The selected workflow is confirmed unavailable | Make that workflow available or choose how to proceed outside the router |
| `Profiles exhausted` | All three profiles for the selected role are stated unavailable | Supply an available profile or updated availability |

Each stop contains its reason and next prerequisite, with no owner, profile, or
executable kickoff. For `Unsupported in the current version`, include the
absolute public workflow-catalog URL
https://github.com/jrgilbertson/the-rookery/blob/main/WORKFLOWS.md
in the reason or prerequisite.

<!-- route-work-contract-end -->

> Maintainer note: The human-edited source for this mirrored contract is root
> `ROUTING.md`. Copy it byte-for-byte to
> `skills/route-work/references/routing.md` in the same change so an installed
> skill remains standalone.

Maintainers update the model table manually from external evidence. Benchmark
scores, cost, quota, confidence, automatic rankings, and staleness state stay
outside the contract.
