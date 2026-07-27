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
The verification gate proving a skill installs through the repository's documented install path and loads in at least one real harness. A probe passes only when its success is discriminating: output that cannot distinguish a working mechanism from a silent fallback proves nothing. Runs before merge from the local source and again after merge against the published state.

### Same-Door Rule
The maintainer installs from this repository exactly the way a visitor does.
Nothing in the published catalog may depend on context that exists only on the
maintainer's machine, including absolute paths, private names, or
personal-environment assumptions. A verification sweep enforces the rule
across shipped files.

## Skill quality gates

### Baseline Test
A Baseline Test checks whether a skill changes agent behavior in the intended
direction. New skills run realistic prompts with and without the skill.
Revisions compare frozen prior and revised versions in fresh contexts after
establishing each version's Loaded Skill Identity. A substantive revision ships
only when the required comparison supports it. A waiver can permit shipment
when a required check is unavailable, but it cannot replace missing evidence,
support an otherwise unsupported change, or raise the evidence label.

### Loaded Skill Identity
Loaded Skill Identity proves that the declared skill package supplied the
instructions observed in a model-harness run. A matching name is not enough
because project, user, shared, and system copies may collide.

Fresh context does not establish Loaded Skill Identity. A native run needs
source-to-install identity and observable load evidence. A bounded policy probe
may embed the exact authoritative policy, but that does not prove native
discovery or loading. Exclude any run that cannot establish the intended
identity.

### Degradation Path
A skill's defined behavior when something it prefers is absent, such as a
validator that cannot run, a companion skill that is not installed, or a tool
without a clean-context mechanism. The skill uses the best available substitute
and states what was skipped.

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

### Claim Ceiling
A Claim Ceiling limits conclusions to the evidence collected. One successful
execution is a smoke test. A small matched baseline supports a directional
observation. Reliability or causal-improvement claims require repeated,
controlled evidence that accounts for normal run variation.

### Trigger Contract
The stance that a skill's description is a tested activation API, not documentation: only the name and description are loaded when the fire-or-skip decision happens, so the description alone decides whether the skill ever runs. Tested with should-trigger phrasings that must activate and near-misses that must not, judged in fresh contexts.
