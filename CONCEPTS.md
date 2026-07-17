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
The comparison gate proving a skill changes agent behavior in the intended direction: a new skill runs realistic prompts with and without it, a revision runs the prior version against the revised one, always in fresh contexts so carried-over conversation cannot contaminate the result. A substantive change ships only with this comparison or an explicit recorded waiver.

### Degradation Path
A skill's defined behavior when something it prefers is absent — a validator that cannot run, a companion skill not installed, a harness without a clean-context mechanism. A degradation path degrades loudly: the skill does the best available substitute and names what was skipped, never failing or skipping silently.

### Delete Test
The instruction-economy check applied line by line to agent instructions: would the agent get this wrong without this line? A line that restates default model behavior fails and is cut whole. The test decides cut-or-keep only — a word can pass it and still steer unpredictably, which is the separate operationalize-the-qualifier check's job.

### Trigger Contract
The stance that a skill's description is a tested activation API, not documentation: only the name and description are loaded when the fire-or-skip decision happens, so the description alone decides whether the skill ever runs. Tested with should-trigger phrasings that must activate and near-misses that must not, judged in fresh contexts.
