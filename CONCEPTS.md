# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and status concepts with project-specific meaning. It starts with the core terms
and grows through `ce-compound`, `ce-compound-refresh`, and direct edits. This is
a glossary, not a specification or catch-all.

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

### Targeted Sweep

The pre-PR gate's check of the evidence-backed finding classes that drive
automated-review rounds, run against the branch before any PR exists.
Mechanical classes run through bundled helpers that defer to repo-owned
equivalents; judgment classes run by model instruction. The class list comes
from PR forensics and is refreshable as review history accumulates.

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
