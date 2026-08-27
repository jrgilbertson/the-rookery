# Routing work

`route-work` turns one explicit routing request and its supplied evidence into
one supported first workflow owner, a continuation of proven in-flight work, or
a named stop. It returns a portable kickoff and leaves execution to the selected
workflow.

> Maintainer note: The human-edited source for this mirrored contract is root
> `ROUTING.md`. Copy it byte-for-byte to
> `skills/route-work/references/routing.md` in the same change so an installed
> skill remains standalone.

## Activation boundary

Route only when the operator explicitly asks to route or kick off work. A
planning, debugging, design, implementation, or issue request without that
intent proceeds through its normal workflow and does not produce a route card.

One invocation performs one read-only assessment and returns one route card,
continuation, clarification question, or stop, then exits. If a clarification
is necessary, the operator's answer joins the original evidence for the same
bounded conversational attempt. The next assessment returns a route,
continuation, or named stop. Use `Insufficient input` when the answer still
does not resolve an owner. Ask no second question and persist no routing state.

## Choose the first owner

Choose exactly one owner from the **first unresolved effect**: the earliest
uncertainty to resolve or durable change to produce before useful work can
continue. The request's carrier, model, harness, and eventual workflow sequence
do not determine the owner.

| First unresolved effect | Owner | Discriminator |
|---|---|---|
| Product outcome, behavior, or scope boundary is unsettled | `ce-brainstorm` | Clarify what should be built before planning how |
| One consequential dependency-ordered decision tree needs pressure-testing against supplied documents | `grill-with-docs` | Run a focused grill; durable document updates require authority and repository-defined locations |
| Outcome and acceptance boundary are settled, but the execution plan is missing | `ce-plan` | Plan without reopening settled product choices |
| Broken or unexpected behavior still has an unresolved causal chain | `ce-debug` | Diagnose first; an established cause and fix route to `ce-work` |
| Concrete implementation is ready and authorized, including an already-diagnosed fix | `ce-work` | Execute within the supplied authority |
| Canonical issue content, relationship graph, coverage, or readiness state must be inspected or changed | `managing-issues` | Keep tracker truth and complete graph claims with the issue workflow |
| Visual direction, interaction design, or design quality is the first unresolved effect | `impeccable` | Let Impeccable select its internal workflow unless one exact command is already obvious |

An effect outside these seven owners returns `Unsupported in v1` and points to
the [public workflow catalog](https://github.com/jrgilbertson/the-rookery/blob/main/WORKFLOWS.md).
That stop contains no executable kickoff and links only to the public catalog.

### Ambiguity and missing input

- For coequal workstreams with no dependency order, ask which one starts first.
- For any other ambiguity, ask the one question that most narrows the possible
  owner set.
- Route a self-contained request without demanding an artifact. If a named or
  required primary artifact is missing or unreadable, return
  `Insufficient input`.
- Never split, rank, or order coequal workstreams on the operator's behalf.

## Recommend a starting topology

Recommend one topology for the selected owner.

| Pattern | Use when | Guardrail |
|---|---|---|
| Single owner | Bounded work, dependent reasoning, ambiguity, taste-led iteration, or no proven coordination benefit | Default to one accountable owner |
| Staged delivery | Settled phases have distinct outputs, permissions, or fresh-context gates | Sequential phases do not imply parallel workers |
| Evaluator loop | An independent evaluator has explicit criteria or reliable external feedback | Default to one produce-evaluate-revise round with a named stop condition |
| Lead + bounded workers | Packages are independent, scopes are named, and one lead can integrate them | Bound fan-out and establish conflict-safe writes before concurrent mutation |

Advisor consultation can modify any topology without transferring ownership.
An advisor supplies bounded evidence. The selected owner may revise the
starting topology when new evidence justifies it. Subagents, forks, teams, and
background sessions are execution mechanisms.

## Keep Orca and placement separate

Workflow ownership, Orca involvement, and worktree placement are independent
decisions.

| Axis | Choice | Meaning |
|---|---|---|
| Orca involvement | None | Proceed without Orca coordination |
| Orca involvement | Supervised `/orchestration` | The current coordinator remains the sole human-facing owner and integrator and loads Orca's installed version-matched contract |
| Orca involvement | Full ownership handoff | Human-facing ownership transfers to the receiving worktree or agent; the sender gains no monitoring duty |
| Placement | Current worktree or isolated worktree | Use isolation for concurrent mutation; disjoint write scopes are still required before parallel writes |

The selected startup workflow remains the owner; Orca only coordinates windows
and worktrees. Load Orca's version-matched contract instead of hardcoding its
command grammar. Read-only scouts and fresh-context reviewers can work in the
current worktree.

## Handle parent, child, and existing work

Use only supplied issue-family and plan state.

| Supplied state | Result |
|---|---|
| Family coverage, descendants, blockers, readiness, or topology is incomplete or uncertain | Route to `managing-issues`; do not declare a Ready Frontier or choose a leaf |
| A complete current family is supplied, but parent integration, sequencing, or shared-surface planning is missing | Route the parent to `ce-plan` |
| An approved parent plan is supplied | Route to `ce-work`; use Lead + bounded workers only when independent units, one integrator, and safe write boundaries are proven |
| A child is named directly | Route from the child's unresolved effect while preserving supplied parent constraints |
| The requested phase already has a proven active owner | Return continuation context and no duplicate kickoff unless replacement or restart is explicit |

When rows overlap, a proven active owner of the requested phase takes
precedence. Otherwise, a directly named child routes from its own unresolved
effect unless supplied evidence says unresolved family state blocks that
child. All other incomplete or uncertain family-state starts route to
`managing-issues`.

Active ownership is proven only by an operator statement or supplied artifact
that names a specific in-flight owner for the requested phase. A stated
worktree, branch, pull request, worker, or parallel effort without that phase
owner adds `Active ownership unverified` to the normal kickoff. The router does
not discover or monitor ownership.

## Select the role profile

Map the selected owner and any conditional handoff to its current
responsibility.

| Role | Responsibilities |
|---|---|
| Orchestrator/planner | `ce-brainstorm`, the owning `grill-with-docs` workflow, `ce-plan`, `managing-issues`, and a `ce-work` lead coordinating bounded workers |
| Executor | Direct `ce-work`, implementation workers, and execution of a diagnosed fix |
| Reviewer | Independent evaluators and named review or verification gates |
| Critic | Independent adversarial pressure-test advisors or evaluators; not the owning `grill-with-docs` route |
| Researcher | Causal investigation inside `ce-debug` and evidence-backed synthesis |
| Scout | Bounded evidence gathering and advisor research |
| Design/taste | `impeccable` and design-quality evaluation |

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

For Lead + bounded workers, use the orchestrator/planner profile for the lead
and the executor profile for workers.

### Availability fallback

Use operator-stated or already-supplied authoritative capability metadata to
filter unavailable profiles in primary, secondary, then tertiary order. Keep
the selected owner unchanged. If all three profiles are unavailable, return
`Profiles exhausted`. If the workflow itself is confirmed unavailable, return
`Owner unavailable`. When availability is unknown, mark it `unverified`, keep
the default selection, and return the portable kickoff. Never probe a host,
provider quota, model catalog, tracker, pull request, worktree, or dispatch
system.

### Effort escalation

Effort escalation is exceptional and operator-controlled. Use the table's
listed effort by default; it is a deliberate recommendation, not a complexity
estimate. Large, ambiguous, important, or technically complex work does not by
itself justify more effort. Prefer narrowing the request, clarifying
constraints, supplying references, or decomposing the work.

A higher effort may be used only when the operator explicitly requests it, a
governing workflow requires it, or supplied evidence shows that the default
previously failed because of insufficient reasoning depth. The router may
suggest escalation but never selects it without operator approval.

Maintainers update this table manually from external evidence. It carries only
ordered recommendations and the review date; benchmark scores, cost, quota,
confidence, automatic rankings, and staleness state stay outside the contract.

## Inspect only supplied evidence

The assessment may read:

- the request;
- one explicitly named primary artifact, when present;
- directly cited repository instructions; and
- authoritative metadata already supplied in the current context.

For an issue, use only the named node and an already-supplied or visible
relationship summary. Do not conduct a broad repository search, recursively
walk an issue graph, or probe external state.

## Preserve authority and stop cleanly

The router assesses supplied evidence, renders one card, and exits without
changing state. It performs no downstream workflow invocation, agent dispatch,
diagnosis, planning, research, implementation, issue or worktree mutation,
orchestration, scheduling, monitoring, quota or cost calculation, version-control
or pull-request operation, merge, or publication.

Copy only authority the operator supplied. An implementation kickoff never
infers permission to commit, push, open a pull request, publish, merge, or
change external state. A grilling kickoff may pressure-test supplied documents,
but it withholds domain-model or ADR writes unless the operator authorizes them
in repository-defined locations.

The named stops are:

| Stop | Use when | Next prerequisite |
|---|---|---|
| `Insufficient input` | The single clarification did not resolve an owner, or a named or required primary artifact is unavailable | Supply the missing discriminating fact or readable artifact |
| `Unsupported in v1` | The first unresolved effect falls outside the seven startup owners | Choose from the public workflow catalog or request a supported startup route |
| `Owner unavailable` | The selected workflow is confirmed unavailable | Make that workflow available or choose how to proceed outside the router |
| `Profiles exhausted` | All three profiles for the selected role are stated unavailable | Supply an available profile or updated availability |

Each stop contains its reason and next prerequisite, with no owner, profile, or
executable kickoff.

## Return one portable card

### Ready route

```markdown
## Route

**Owner:** <one startup owner>

**Pattern:** <topology> — <why it fits>; <role>: <provider> / <model> / <effort>

### Kickoff

- **Objective:** <the next job owned by this workflow>
- **Verifiable end state:** <observable completion condition>
- **Start here:** <stable artifact locator and first action>
- **Decisive facts:** <supplied facts that determined the route>
- **Constraints:** <scope, safety, and supplied authority>
- **Evidence gaps:** <material unknowns that do not block kickoff, or none>
- **Authority gates:** <external or durable actions still requiring approval>
```

For Lead + bounded workers, `Pattern` names both lead and worker profiles. Add
advisor use, Orca involvement, placement, conditional handoff, availability,
or `Active ownership unverified` only when material. A conditional handoff is a
preview controlled by the active owner; owner-changing evidence requires a new
explicit routing request, while topology-only evidence stays with the current
owner. Summarize supplied artifacts rather than copying them.

### Continuation

```markdown
## Continuation

**Owner:** <proven active owner>

**Resume with:** <stable locator, current phase, decisive context, and next action>
```

A continuation contains no duplicate kickoff.

### Clarification

```markdown
## Clarification

<the single question that most narrows the owner set>
```

### Stop

```markdown
## Stop

**Stop:** <named stop>

**Reason:** <why routing cannot proceed>

**Next prerequisite:** <what would permit a new assessment>
```

For `Unsupported in v1`, include the absolute public workflow-catalog URL in
the reason or prerequisite.

## Representative examples

| Supplied request and evidence | Result |
|---|---|
| “Route this feature idea; the intended user behavior is still disputed.” | `ce-brainstorm`, Single owner, orchestrator/planner profile |
| “Kick off a pressure test of this supplied decision document.” | `grill-with-docs`; durable document writes remain gated by supplied authority |
| “The approved requirements are attached, but there is no execution plan.” | `ce-plan`, Single owner, orchestrator/planner profile |
| “This command fails and the cause is unknown.” | `ce-debug`, Researcher profile; a supplied established cause and authorized fix instead routes to `ce-work` |
| “Route work for this issue family; descendant coverage and blockers are uncertain.” | `managing-issues`; do not select a child or certify readiness |
| “This approved parent plan has independent packages, one integrator, and disjoint writes.” | `ce-work`, Lead + bounded workers, with orchestrator/planner lead and executor worker profiles |
| “Route this named child issue under the supplied parent constraints.” | Select from the child's first unresolved effect |
| “The interaction direction is unresolved.” | `impeccable`, Single owner, design/taste profile |
| “Resume the implementation phase already owned by this named worker.” | Continuation with the proven owner; no duplicate kickoff |
| “Use a hands-off delivery workflow to run this end to end.” | `Unsupported in v1` with the public workflow-catalog URL and no kickoff |
| “Route this plan; the primary orchestrator profile is unavailable.” | Keep the selected owner and use the secondary orchestrator/planner profile |

<!-- route-work-contract-end -->
