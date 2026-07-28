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

The package-harness verification gate proving that an exact skill revision
installs through the repository's documented path and that the installed
content matches its source. A passing probe establishes installability and
content identity only for the checked package-harness cell. Native discovery,
load, and trigger are separate model-harness states; a native load pass also
requires [Loaded Skill Identity](#loaded-skill-identity), including
deterministic runtime provenance. Runs before merge from the local source and
again after merge against the published state.

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

Fresh context does not establish Loaded Skill Identity. A native load pass
needs deterministic runtime provenance tied to the installed source: a native
trace naming the exact installed path or base directory, or equivalent runtime
evidence linked to the installed content hash. Distinctive output may
corroborate that provenance, but cannot independently prove which copy loaded.
If deterministic runtime provenance is unavailable, keep native load unverified
rather than failed. A bounded policy probe may embed the exact authoritative
policy, but that does not prove native discovery or loading. Keep
source-to-install identity, native discovery, native load, native trigger, and
behavioral evidence separate, and exclude identity-dependent claims from runs
that cannot establish the intended loaded copy.

### Independent Review Context

An Independent Review Context is a fresh session in which the reviewing agent
neither saw the artifact's authoring discussion nor produced the artifact.

One context may grade a matched case, while another performs the final holistic
review. Deterministic scripts remain appropriate for mechanical checks. If an
independent context is unavailable, the affected result stays unverified and
moves to a separate session through a self-contained handoff.

A recorded context ID identifies the run. It does not replace artifact or
trace evidence for the judgment made in that run.

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
execution is only a smoke probe and earns no baseline label. A small matched
baseline supports a directional observation. Reliability or
causal-improvement claims require repeated, controlled evidence that accounts
for normal run variation.

### Verification Mode

Verification Mode records whether listing-query checks use the ordinary
personal tier or the public or unusually load-bearing tier.

The selected tier determines query count, repetition, and tier-specific
judgment rules. Matched behavioral comparisons, structural validation, native
and installation checks, and declared model-harness targets remain separate
requirements.

### Trigger Contract

A Trigger Contract treats a skill's description as a tested activation API,
not documentation. At the fire-or-skip decision, the agent sees only the
skill's name and description. Test this metadata with should-trigger phrasings
that must activate and near-misses that must not. Record each judgment in a
fresh context with a context or transcript reference.
