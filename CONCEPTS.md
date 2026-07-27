# Concepts

Shared domain vocabulary for this project — entities, named processes, and status concepts with project-specific meaning. Seeded with core domain vocabulary, then accretes as ce-compound and ce-compound-refresh process learnings; direct edits are fine. Glossary only, not a spec or catch-all.

## Shipping and verification

### The Shelf
The public catalog of skills this repository stocks. Whatever lands on the default branch is immediately what installers receive, so the default branch stays install-clean at all times. A skill is on the shelf once it appears in the catalog and installs individually — visitors never need to adopt the whole collection.

### Install Probe
The verification gate proving a skill installs through the repository's documented install path and loads in at least one real harness. A probe passes only when its success is discriminating: output that cannot distinguish a working mechanism from a silent fallback proves nothing. Runs before merge from the local source and again after merge against the published state.

### Same-Door Rule
The maintainer installs from this repository exactly the way a visitor does, so nothing on the shelf may depend on context that exists only on the maintainer's machine — no absolute paths, no private names, no personal-environment assumptions. Enforced as a verification sweep over the shipped files, not as a convention.

## Skill quality gates

### Baseline Test
The comparison gate for observing whether a skill changes agent behavior in the intended direction: a new skill runs realistic prompts with and without it, while a revision runs the prior version against the revised one in fresh contexts with each variant's Loaded Skill Identity established. A substantive revision ships only when the required comparison supports it; a waiver may authorize shipment when a required check is unavailable, but cannot satisfy absent or inconclusive evidence, authorize an unsupported change, or raise the evidence label.

### Loaded Skill Identity
The evidence property that the exact declared skill package, rather than a same-named project, user, shared, or system copy, supplied the instructions observed in a model-harness run.

Fresh context does not establish Loaded Skill Identity. A native run needs source-to-install identity plus observable load evidence; a bounded policy-only probe may instead embed the exact authoritative policy, but it does not become native discovery or load evidence. A run that cannot establish the intended identity is excluded from the comparison.

### Degradation Path
A skill's defined behavior when something it prefers is absent — a validator that cannot run, a companion skill not installed, a harness without a clean-context mechanism. A degradation path degrades loudly: the skill does the best available substitute and names what was skipped, never failing or skipping silently.

### Delete Test
The instruction-economy check applied line by line to agent instructions: would the agent get this wrong without this line? A line that restates default model behavior fails and is cut whole. The test decides cut-or-keep only — a word can pass it and still steer unpredictably, which is the separate operationalize-the-qualifier check's job.

### System-Owned Invariant
A hard constraint that must remain explicit because the user or surrounding system, rather than model judgment, owns it. Portable formats, user authority, deterministic validation, exact output requirements, and fragile operation order are system-owned; generic reminders to think, narrate, or recheck are model-owned cognition and may be removed when they no longer help.

### Claim Ceiling
The strongest conclusion an evidence record is allowed to state. A smoke test proves only that one execution worked, a small matched baseline supports a directional observation, and reliability or causal-improvement language requires repeated controlled evidence that accounts for ordinary run variation.

### Trigger Contract
The stance that a skill's description is a tested activation API, not documentation: only the name and description are loaded when the fire-or-skip decision happens, so the description alone decides whether the skill ever runs. Tested with should-trigger phrasings that must activate and near-misses that must not, judged in fresh contexts.
