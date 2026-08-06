# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and status concepts with project-specific meaning. It starts with the core terms
and grows through `ce-compound`, `ce-compound-refresh`, and direct edits. This is
a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day outcome recorded during wind-down with an observable finish line and a concise rationale for why it matters. When the live daily-journal template includes a configured Meaningful Commitments section, that journal carries three to five of them as next-day intent; without the section, ordinary next-day planning continues. They express intent without replacing canonical task state or calendar capacity, and they do not require a separate morning reaffirm step.

### Daily CRM Scan

Required wind-down pass over configured relationship interaction sources for the active scan window, run before the initial reconstruction whether or not a candidate person already surfaced. Default window: closing local day. After a short miss of one or two immediately prior local days (missing prior journals), expand over those days plus the closing day as a catch-up breath. Attribute messages by sender; evaluate substantive direct contact for each bindable person; leave unknown handles unresolved. Covers contact-date outcomes and selective durable meaning. Separate from prepare-tomorrow’s overdue / useful-tomorrow exception check. Excludes CRM catch-up mode, exhaustive history, and indiscriminate Person-note creation.

## Workflow processes

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
across shipped files.

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
success: every documented state produces a distinct verdict line, and every
state class carries its own exit code — verdicts exit 0 with the verdict line
distinguishing negative from positive, absent input exits 2, deferral to a
repository-owned gate exits 3, environment failure exits 4 — so a gap can
never be laundered into a green result.

The contract is executable, not prose: a committed, rerunnable fixture runner
asserts the exact verdict-and-exit pair for every documented state, including
adversarial states. A helper whose contract exists only in its header comment
is itself a prose-only invariant — the defect class it exists to catch.

### Merge Digest

The pre-merge readout `checking-merge-readiness` composes from a PR's
description, diff, and review history: plain-language themes of what review
did, an intent-drift check, and graded Risk Drivers rolling into a three-light
recommendation of merge, debug, or do not merge. It lives in the conversation
and changes nothing, so the owner still does the merging.

### Risk Driver

A named, graded (low / medium / high) finding in the Merge Digest's risk
profile: one specific thing about the change or its review that an owner
would want to weigh before merging. Seven classes are graded. Three cover
tension the accumulated fixes put on an engineering first principle such as
DRY, single source of truth, or YAGNI: complexity accretion, knowledge
duplication, and speculative generality. The other four need no such tension
to fire: review items left unresolved, cross-round fix interaction, material
security concerns, and PR text that tries to steer the assessment. Drivers
roll up into one merge-risk grade; a word grade traceable to a named driver
is used instead of a numeric score.

### Targeted Sweep

The pre-PR gate's check of the evidence-backed finding classes that drive
automated-review rounds, run against the branch before any PR exists.
Mechanical classes run through bundled helpers that defer to repo-owned
equivalents; judgment classes run by model instruction. The class list comes
from PR forensics and is refreshable as review history accumulates.

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
