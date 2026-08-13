# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and status concepts with project-specific meaning. It starts with the core terms
and grows through `ce-compound`, `ce-compound-refresh`, and direct edits. This is
a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day intention recorded during wind-down. It visibly connects the current authoritative evidence or labeled user premise, the user-owned desired outcome, and the future observable evidence that will show completion, with a concise rationale for why it matters. These meanings may read as natural prose rather than labeled fields. Exact user wording that omits one remains visible as nonconforming input and is not certified as a complete commitment. When the live daily-journal template includes a configured Meaningful Commitments section, that journal carries three to five of them as next-day intent; without the section, ordinary next-day planning continues. They express intent without replacing canonical task state or calendar capacity, and they do not require a separate morning reaffirm step.

### Source Access Audit

A required, conversation-only account of the relevant source roles considered for one visible personal-chief-of-staff response. For each role, it records the bounded current-response access attempt and result (`Accessed — evidence found`, `Accessed — no relevant evidence`, or `Attempted — unavailable or failed`), or an explicit no-attempt classification (`Not configured`, `Declined`, or `Not needed`), plus the effect on that response's findings. It is reconciled from those attempts and classifications, rendered after the answer-first synthesis, and discarded after the response. It is not a source registry, claim-provenance ledger, approval, freshness record, or new source of truth.

### Daily CRM Scan

Required wind-down pass over configured relationship interaction sources for the active scan window, run before the initial reconstruction whether or not a candidate person already surfaced. Default window: closing local day. After a short miss of one or two immediately prior local days (missing prior journals), expand over those days plus the closing day as a catch-up breath. Attribute messages by sender; evaluate substantive direct contact for each bindable person; leave unknown handles unresolved. Covers contact-date outcomes and selective durable meaning. Separate from prepare-tomorrow’s overdue / useful-tomorrow exception check. Excludes CRM catch-up mode, exhaustive history, and indiscriminate Person-note creation.

## Workflow processes

### Delivery Sequence

The five-job path from Research through Plan, Design, Build, and Ship. Each job
transforms a named input into an artifact the next job can use. Design is
conditional for interface work and continues through later delivery rather
than existing only as an isolated stop.

### Repository Memory Current

The Maintain feedback path that observes recurring signals across the Delivery
Sequence and encodes each lesson at the strongest durable layer that can hold it,
preferring enforceable layers when available. It improves future work
throughout the system rather than beginning only after Ship.

### Personal Learning Current

The Learn feedback path that turns experience into linked personal knowledge,
names the gap that remains, and returns a better question to Research. It is
distinct from the Repository Memory Current because it improves the operator's
understanding rather than the repository's safeguards and procedures.

### Grilling Session

A targeted, stateless interview for resolving one coherent decision tree whose
answers depend on one another. The agent recommends answers and looks up
discoverable facts. The user makes each decision.

### Shared Understanding Gate

A user-confirmed state in which the material decision branches have been
resolved. Reaching it ends the Grilling Session and allows the clarified intent
to return to planning.

## Shipping and verification

### Published Catalog

The skills available for individual installation from this repository.
Installers read the default branch, so anything merged there becomes available
immediately. That branch stays install-clean. A skill is published once it
appears in the catalog and installs on its own.

### Install Probe

The per-harness smoke check proving that an exact skill revision installs
through the repository's documented path and activates on one trigger query.
A passing probe establishes installability and activation for that harness
only; it is not behavioral evidence. Runs before merge from the local source
and again after merge against the published state.

### Same-Door Rule

The maintainer installs from this repository exactly the way a visitor does.
Nothing in the published catalog may depend on context that exists only on the
maintainer's machine, including absolute paths, private names, or
personal-environment assumptions. A verification sweep enforces the rule
across shipped files. The rule binds from the moment the repository declares
itself public-bound, regardless of its current hosting visibility.

## Readiness checkpoints

### Evidence Pack

The structured record a readiness checkpoint composes when the owner approves:
plan-vs-delivered status, checks run with results, the explicit not-verified and
attested list, sweep findings, UI critique scores when present, and the durable
learning signal. The checkpoint only composes the pack into its readout;
durability begins when the finishing path renders it into the pull request
description, which is its durable home — the pre-merge checkpoint reads it back
from there. Nothing is written to the tracked tree or any local state store.

### Falsifiability Contract

The requirement that a bundled helper's output can prove failure as readily as
success, so a gap can never be laundered into a green result. How a helper
meets it depends on what it produces. A helper that emits gate verdicts gives
every documented state a distinct verdict line and every state class its own
exit code, where verdicts exit 0 with the verdict line distinguishing negative
from positive, absent input exits 2, deferral to a repository-owned gate exits
3, and environment failure exits 4. A transport helper carries a payload
rather than grading one, so it proves failure with its exit code and an empty
stdout, which keeps a partial payload from being mistaken for a complete one.

The contract is executable, not prose: a committed, rerunnable fixture runner
asserts the exact verdict-and-exit pair for every documented state, including
adversarial states, and the runner ships in the same change as the helper it
pins — a helper that merges ahead of its fixtures is unfalsifiable for exactly
that window. A helper whose contract exists only in its header comment
is itself a prose-only invariant — the defect class it exists to catch.

### Merge Digest

The pre-merge readout `checking-merge-readiness` composes before the owner
merges: a thin **Process Residual** and host merge-rule check, then the
load-bearing **Global Pass** over the change from PR open to tip — intent
drift, graded Risk Drivers, redesign pressure, and follow-up debt — rolling
into one recommendation of merge, debug, or do not merge. It lives in the
conversation and changes nothing, so the owner still does the merging.

### Global Pass

The merge-readiness skill's primary job: systems judgment on the full arc
from pre-review intent through the final tip. It catches local-opt failure
modes that babysitting and point comments miss — overengineering, YAGNI,
intent drift, redesign-worthy shape, and future work that should be captured
before main. Distinct from clearing individual review threads.

### Process Residual

The thin pre-merge process floor in the Merge Digest: whether the review loop
is quiet enough to grade (substantive items resolved or deferred, no new open
fire) and whether host merge rules such as required conversation resolution
pass. Residual is named honestly; it is not a second product of reviewer
identity, durable AI receipts, or tip-OID non-author theater.

### Risk Driver

A named, graded (low / medium / high) finding in the Merge Digest's risk
profile: one specific thing about the change or its review that an owner
would want to weigh before merging. Principle-tension classes cover
complexity accretion, knowledge duplication, and speculative generality.
Other classes cover unresolved review items, cross-round fix interaction,
material security concerns, and PR text that tries to steer the assessment.
Drivers roll up into one merge-risk grade; a word grade traceable to a named
driver is used instead of a numeric score.

### Targeted Sweep

The pre-PR gate's check of the evidence-backed finding classes that drive
automated-review rounds, run against the branch before any PR exists.
Mechanical classes run through bundled helpers that defer to repo-owned
equivalents; judgment classes run by model instruction. The class list comes
from PR forensics and is refreshable as review history accumulates.

## Repository gardening

### Repository Automation Loop

One repository-scoped `Sense -> Decide -> Act -> Verify -> Learn` pass. The
parent surveys nine lanes, may deepen current signals, and may supervise a
live-policy-bounded child through an unmerged pull request. The model owns
qualitative judgment; deterministic code checks only tracker-record closure.

### Gardening Tracker

The append-only run records and mutable morning projection for
repository-gardening facts. Exactly one `run-opened` and one consolidated
`run-closed` managed comment carry each run ID. It never owns source truth,
mutation authority, or authored-work state.

### Current Portfolio

A legacy report projection retained for history-chain compatibility during
early dogfooding. It is not a queue or ownership database. Native pull requests,
branches, heads, checks, and states are authoritative for authored work.

### Run History

The complete structurally hash-linked receipt history from genesis, with
unverified provenance. New gardening runs add only `run-opened` and
`run-closed` receipts. Legacy kinds remain readable. History supplies
visibility, not a lock, queue, authority grant, or planning-quality verdict.
The full readable kind inventory is `decision`, `effect`, `evidence`,
`manifest`, `release`, `run`, `run-opened`, `run-closed`, and `scout`.

### Scout Receipt

A legacy per-lane terminal record retained in older history. Current runs place
all nine lane results in the consolidated closing record instead of writing
nine separate managed comments.

### Register Revision

A monotonic body version used to detect stale preparation and bad readback. It
is not an atomic provider precondition, compare-and-swap, or distributed lock.

### Effect Receipt

The intended-effect and terminal-outcome evidence for one stable,
repository-qualified logical report operation. Its identity is the pair
`(repository_id, operation_id)`, not the operation ID alone. The intended
receipt is read back before invoke; the terminal receipt is read back after the
authoritative post-read. Ambiguity blocks blind retry.

### Attention State

The report projection `Action required`, `Merge-ready`, `Watching`, or
`Routine`. Attention communicates current handling; it is not a persisted work
state or authority grant.

### Completion Partition

The disjoint, exhaustive pair `affected_work` and
`remaining_unblocked_work`. Every named item appears exactly once, and every
unblocked remainder is continued, durably delegated, or gated by its own named
prerequisite.

## Research synthesis

### Storm Research

Deep, source-backed investigation that establishes a baseline, dispatches
independent research lenses, preserves their disagreements, and synthesizes the
result for the requested purpose. It may inform a decision, but unlike
`ce-pov`'s compact, project-grounded verdict it preserves a multi-perspective
research record as the primary result.

### Research Depth Questions

Questions used throughout Storm Research to clarify the facts, assumptions,
constraints, and mechanisms beneath material claims and to examine relevant
system relationships, patterns over time, and downstream effects. They shape
research and synthesis without requiring separate sections in the briefing.
Formal system-dynamics models remain separate, user-requested deliverables.

### Storm Fidelity Review

An independent check that compares a Storm Research briefing with its baseline,
source audit, raw lens returns, and internal run record for lost or invented
disagreement and untraced analytical claims. Every finding is binding; each
revision goes to a new clean reviewer until the check is clean or the run records
reduced verification.

## Skill quality gates

### Baseline Test

A Baseline Test checks whether a skill changes agent behavior in the intended
direction. New skills run realistic prompts with and without the skill;
revisions compare the frozen prior and revised versions, each in a fresh
context with the intended variant confirmed loaded. Cases are binary
pass/fail, and a substantive revision ships only when the discriminating
cases show the intended improvement with no regression. The repository's
testing convention owns the protocol.

### Independent Review Context

An Independent Review Context is a fresh session in which the reviewing agent
neither saw the artifact's authoring discussion nor produced the artifact.

One context may grade a matched case, while another performs the final holistic
review. Deterministic scripts remain appropriate for mechanical checks. If an
independent context is unavailable, the affected result stays unverified and
moves to a separate session through a self-contained handoff.

The run's log line names the fresh-context mechanism used (a fresh session,
CLI execution, or subagent); recorded context identifiers are not kept in
test artifacts. The named mechanism does not replace artifact or trace
evidence for the judgment made in that run.

### Degradation Path

A skill's defined behavior when something it prefers is absent, such as a
validator that cannot run, a companion skill that is not installed, or a tool
without a clean-context mechanism. The skill uses the best available substitute
and states what was skipped.

### Disposition List

A Disposition List is the per-item record a prune or restructure leaves in its
commit message: each removed item marked kept, folded into a named survivor,
or dropped with a reason. It is a checkable contract, not a narrative — a
folded claim must point to the surviving line that carries the contract, a
dropped claim must hold against its rationale, and a retired claim must
survive a search for live references. Verified dispositions are what make
git-as-archive recovery trustworthy.

### Delete Test

The instruction-economy check asks one question for every line: would the agent
get this wrong without it? A line that restates default model behavior fails and
is cut whole. The test decides only whether to keep the line. The separate
operationalize-the-qualifier check handles words that survive but still steer
unpredictably.

### System-Owned Invariant

A hard constraint that stays explicit because the user or surrounding system
owns it. Examples include portable formats, user authority, deterministic
validation, exact output requirements, and fragile operation order. Generic
reminders to think, narrate, or recheck may be removed when they no longer help.

### Trigger Contract

A Trigger Contract treats a skill's description as a tested activation API,
not documentation. At the fire-or-skip decision, the agent sees only the
skill's name and description. Test this metadata with should-trigger phrasings
that must activate and near-misses that must not, judged in fresh contexts
under the repository's testing convention.
