# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and status concepts with project-specific meaning. It starts with the core terms
and grows through `ce-compound`, `ce-compound-refresh`, and direct edits. This is
a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day outcome recorded during wind-down with an observable finish line and a concise rationale for why it matters. A Daily Journal carries three to five Meaningful Commitments into morning; they express intent without replacing canonical task state or calendar capacity.

## Workflow processes

### Grilling Session

A targeted, stateless interview for resolving one coherent decision tree whose
answers depend on one another. The agent recommends answers and looks up
discoverable facts. The user makes each decision.

The session ends when the user signs off, meaning the decisions that mattered
are settled and the clarified intent can go back to planning.

## Shipping and verification

### Union Merge

Git's name for resolving a conflict by keeping both sides rather than choosing
one. It is the right resolution for a file whose content accumulates, meaning
a growing list of independent entries such as a changelog, release notes, a
contributor list, or an index.

Accumulating files behave differently from files that evolve, which hold one
current statement of something and are meant to be replaced. Two sides of an
evolving file are competing statements, so one wins wholesale and the loss is
visible. Two sides of an accumulating file have almost always both appended,
so the conflict is positional rather than semantic, and taking either side
silently deletes the other's entries. Union the two, resolve only genuine
duplicates, then verify the union held. This is the class of mistake that
leaves no failing test behind.

### Published Catalog

The skills available for individual installation from this repository.
Installers read the default branch, so anything merged there becomes available
immediately. That branch stays install-clean. A skill is published once it
appears in the catalog and installs on its own.

### Install Check

Verification that an exact skill revision installs through the repository's
documented path and that every file arrives intact, with executable bits
preserved. It covers file mechanics only and says nothing about whether a
harness will load or activate the skill; a Smoke Test covers that. Runs before
merge from the local source and again after merge against the published state.

### Smoke Test

The per-harness check that a freshly installed skill actually activates. Ask
one trigger query in a real harness and confirm from the run's trace that the
copy which answered is the just-installed one, identified by its path or base
directory. When a same-name copy exists elsewhere and provenance cannot be
confirmed, the result is inconclusive rather than a pass.

### Dogfooding

The maintainer installs from this repository exactly the way a visitor does,
using the published path rather than a local shortcut. Nothing in the catalog
may depend on context that exists only on the maintainer's machine, including
absolute paths, private names, or personal-environment assumptions. A
verification sweep enforces this across shipped files.

## Readiness checkpoints

### Evidence Pack

The structured record a readiness checkpoint composes when the owner approves:
what was planned against what was delivered, the checks run and their results,
an explicit list of what went unverified or was taken on the owner's word,
sweep findings, and the learning signal.

The pull request description is the pack's home. The checkpoint only composes
it into a readout; it becomes durable when the finishing path writes it into
the description, and the pre-merge check reads it back from there. Nothing is
written to the tracked tree or a local state store.

### Fail-Closed Contract

The requirement that a bundled helper can report failure as readily as success.
Every documented state produces a distinct verdict line, and each class of
state carries its own exit code, so a check that could not run is never
mistaken for a check that passed. A helper that swallows an error and returns
empty fails closed in name only.

The contract is executable. A committed, rerunnable fixture runner asserts the
exact verdict-and-exit pair for every documented state, including adversarial
ones. A helper whose contract exists only in its header comment is itself the
unenforced-invariant defect it exists to catch.

### Merge Digest

The pre-merge readout `checking-merge-readiness` composes from a PR's
description, diff, and review history: plain-language themes of what review
did, an intent-drift check, and graded Risk Drivers rolling into a three-light
recommendation of merge, pause, or do not merge. It lives in the conversation
and changes nothing, so the owner still does the merging.

### Risk Driver

A named, graded (low / medium / high) finding in the Merge Digest's risk
profile: a specific place where accumulated review fixes put tension on an
engineering first principle such as DRY, single source of truth, YAGNI, or
defensive-complexity creep. Drivers roll up into one merge-risk grade; a word
grade traceable to a named driver is used instead of a numeric score.

### Sweep

The pre-PR gate's check of the evidence-backed finding classes that drive
automated-review rounds, run against the branch before any PR exists.
Mechanical classes run through bundled helpers that defer to repo-owned
equivalents; judgment classes run by model instruction. The class list comes
from PR forensics and is refreshable as review history accumulates.

## Skill quality gates

### A/B Test

The comparison that shows whether a skill changes agent behavior in the
intended direction. A new skill runs realistic prompts with and without it; a
revision compares the frozen prior version against the revised one. Each run
happens in a fresh context with the intended variant confirmed loaded, so the
pair differs only by the thing under test.

Cases are binary pass or fail. A substantive revision ships only when the
discriminating cases show the intended improvement with no regression. The
repository's testing convention owns the protocol.

### Blind Review

A review by an agent that neither produced the artifact nor saw the discussion
that produced it. The reviewer is blind to the authoring, which is what makes
its judgment evidence rather than an echo.

One session may grade a matched case while another performs the final holistic
review, and deterministic scripts remain appropriate for mechanical checks. If
no independent session is available, the affected result stays unverified and
moves to one through a self-contained handoff rather than being graded by its
own author.

### Graceful Degradation

A skill's defined behavior when something it prefers is absent, such as a
validator that cannot run, a companion skill that is not installed, or a tool
without a clean-context mechanism. The skill uses the best available substitute
and states what was skipped.

### Disposition List

A Disposition List is the per-item record a prune or restructure leaves in its
commit message: each removed item marked kept, folded into a named survivor,
or dropped with a reason. It is a checkable contract rather than a narrative.
A folded claim must point to the surviving line that carries the contract, a
dropped claim must hold against its rationale, and a retired claim must
survive a search for live references. Verified dispositions are what make
git-as-archive recovery trustworthy.

### Delete Test

The instruction-economy check asks one question for every line: would the agent
get this wrong without it? A line that restates default model behavior fails and
is cut whole. The test decides only whether to keep the line. The separate
operationalize-the-qualifier check handles words that survive but still steer
unpredictably.

### Hard Constraint

A rule that stays written down because something outside the model owns it:
the user, the file format, another system. Examples include portable formats,
user authority, deterministic validation, exact output requirements, and
fragile operation order. Generic reminders to think, narrate, or recheck are
not hard constraints and may be removed when they no longer help.

### Trigger Contract

A Trigger Contract treats a skill's description as a tested activation API,
not documentation. At the fire-or-skip decision, the agent sees only the
skill's name and description. Test this metadata with should-trigger phrasings
that must activate and near-misses that must not, judged in fresh contexts
under the repository's testing convention.

### Proxy Measure

What a passing Trigger Contract establishes: the description works as an
activation API when a judge is shown it directly. It stands in for the thing
you care about without being it, because no harness was involved and nothing
was installed, discovered, or loaded. Only a Smoke Test shows that the skill
activates in practice. Recording the proxy as activation evidence is the
substitution this entry exists to name.
