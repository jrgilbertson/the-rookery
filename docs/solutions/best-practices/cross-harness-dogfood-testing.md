---
title: "Cross-harness dogfood is honest only when the loaded skill identity is proven"
date: 2026-07-16
last_updated: 2026-07-27
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Shipping an agent skill for more than one named harness"
  - "Before marking a degradation path done in a skill's verification plan"
  - "When a skill's authoring environment differs from its users' environments"
  - "When a project skill may share its name with a user-level or system-provided skill"
symptoms:
  - "Scripted tests only exercise the degradation paths the skill author already anticipated"
  - "Author-only runs never surface destination ambiguities because the author's own environment answers them implicitly"
  - "A model quotes rules that are absent from the exact project skill under evaluation"
tags: [cross-harness, dogfood-testing, agent-skills, portability, fresh-context, load-identity, skill-name-collision, false-evidence]
related_components:
  - development_workflow
  - documentation
---

# Cross-harness dogfood is honest only when the loaded skill identity is proven

## Context

The original `creating-portable-skills` acceptance work, merged in PR
jrgilbertson/the-rookery#4, ran the skill end to end in Codex CLI, Grok CLI,
and a Claude Code visitor session in a clean repository. Those runs showed that
differently constrained harnesses exercise degradation paths the author did not
anticipate, because sandbox policies, missing tools, and bare environments make
the fallbacks fire naturally.

The frontier-model retune in issue jrgilbertson/the-rookery#13 exposed a second
condition for honest dogfood evidence: a fresh conversation and a bare
repository do not prove which same-named skill the harness loaded. Two Opus 5
policy-probe attempts quoted rules absent from the exact project files and were
discarded as consistent with an older user-level installation. A bounded
tool-less rerun with the authoritative policy embedded then produced usable
evidence for that policy case (`tests/creating-portable-skills/results.md`,
"FR-P4 new-skill unavailable-target policy").

The durable pattern is therefore two-dimensional. A fresh context protects
against conversational carry-over; an explicit identity check protects against
discovery precedence, stale installs, and same-name collisions. Neither check
substitutes for the other.

## Guidance

Before treating a cross-harness skill run as evidence:

1. Declare the exact package revision, model, harness version, and material
   configuration before the run. Do not silently substitute an alias, a nearby
   model, or another package copy.
2. Run the skill end to end from a clean local-source install in each target
   harness. A documentation review is not a native run. Compare the installed
   files with the declared source before using the result as evidence.
3. Use a bare repository the author did not configure. The author's own
   environment answers questions implicitly, including where files go, what
   "install" means, and which companion tools exist.
4. Inventory project, user, shared-collection, and system skill locations for
   the same name. Temporarily move non-authoritative copies outside discovery
   scope, disable them, or use a harness mode that bypasses them. Do not delete
   a user's installation merely to simplify a test.
5. Capture proof of what loaded. Useful proof includes a native load trace that
   names the project-local path, installed-content hashes, or a distinctive
   expected sentence returned after the load. For a bounded tool-less policy
   probe, embed the exact authoritative policy and label the result policy-only;
   that does not prove native discovery or loading.
6. Treat each harness's constraint differences as free test fixtures. A
   network-denied sandbox tests the validator-unavailable fallback. A missing
   user-level home tests install-destination logic. A fresh-context baseline
   tests comparison discipline.
7. Record each evidence layer separately. Structural validation, listing
   judgment, installation, installed-content identity, native discovery, native
   load, and native trigger do not fill one another's states. If the output
   quotes a clause absent from the authoritative package, discard the run and
   rerun after isolating the collision.

Fixes surfaced this way are usually cheap. Destination ambiguities often need
one clause in the skill; identity failures need better isolation and evidence,
not reinterpretation of a polished but contaminated output.

## Why This Matters

Degradation paths are difficult to test honestly. If the author scripts the
failure, the test confirms only the path the author already imagined. A
differently constrained harness produces the failure for real and can expose
failures the author did not anticipate.

But a realistic environment also makes silent fallback more dangerous. A
same-name collision can load a non-authoritative copy. In this run, polished
output quoted absent clauses and was consistent with, but did not prove, an
older user-level policy. Without identity proof, such a run is a false-positive
generator. The governing principle is the same as for installer probes: a
verification that cannot distinguish success from silent fallback proves
nothing. The evidence must change when the wrong skill copy loads.

## When to Apply

- A skill is being installed or evaluated in more than one named harness.
- A skill has explicit fallback or degradation instructions (validator unavailable, tool missing, network denied) that have only ever been tested by the author simulating the failure.
- A skill was authored and tested entirely inside the author's own configured environment.
- A project skill shares its name with a user-level, global, or system-provided skill.
- A model response mentions an instruction, section, state, or clause absent from the authoritative package.
- An adversarial reviewer demands proof that a fallback path actually fires.

## Examples

The first three cases come from the historical run log in
`tests/creating-portable-skills/results.md`:

1. **Codex CLI, network-denied sandbox.** `npx skills-ref` failed with `ENOTFOUND` mid-run. The executing agent followed the skill's manual-fallback checks and declared the validator skipped — exactly the degradation path an adversarial reviewer had demanded, verified in the wild with no one scripting the network failure.
2. **Claude Code visitor run, clean repo.** Surfaced three destination ambiguities the author's own runs never hit: where the new skill directory goes, where filled test templates go, and what "install" means when the user-level home is unreachable. The author's environment had answered all three implicitly. Each became a one-clause fix, applied and re-validated same-day.
3. **Grok CLI run.** A real double-bucketing defect in the skill it produced was surfaced by its fresh-context baseline and resolved in the subtract pass — a bug the author's own context would have carried right past.
4. **Opus 5 same-name collision.** Two policy-probe attempts quoted rules absent
   from the exact project files. They were excluded rather than averaged into
   the result. A fresh safe-mode, tool-less run with the exact policy embedded
   supplied bounded policy evidence only. The later native rerun separately
   installed from local source, compared all six installed files with that
   source, recorded the project-local load path, and checked a distinctive body
   sentence (`tests/creating-portable-skills/results.md`, "Final-source U4
   rerun").

## Related

- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` — same
  shipping evidence, different lesson: in the recorded skills CLI 1.5.19
  behavior, `@ref` targeting cloned the repository but scanned the default
  branch instead of checking out the requested ref.
- `tests/creating-portable-skills/baseline-cases.md` — matched-case and
  contamination records for the frontier retune.
- `tests/creating-portable-skills/results.md` — final package-identity and native
  model-harness evidence.
- Issue jrgilbertson/the-rookery#13 — the open frontier-model retune that
  surfaced the same-name collision.
