---
title: "Prove which skill loaded in cross-harness dogfood runs"
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

# Prove which skill loaded in cross-harness dogfood runs

## Context

The original `creating-portable-skills` acceptance work, merged in PR
jrgilbertson/the-rookery#4, ran the skill end to end in Codex CLI, Grok CLI,
and a Claude Code visitor session in a clean repository. Those runs exposed
degradation paths the author did not anticipate. Sandbox policies, missing
tools, and bare environments triggered the fallbacks naturally.

The frontier-model retune in issue jrgilbertson/the-rookery#13 exposed another
risk. A fresh conversation and a bare repository do not prove which same-named
skill the harness loaded. Two Opus 5 policy probes quoted rules absent from the
project files, so both were discarded. A bounded, tool-less rerun with the
authoritative policy embedded produced usable evidence for that policy case
(`tests/creating-portable-skills/results.md`, "FR-P4 new-skill
unavailable-target policy").

A valid run needs two checks. Fresh context prevents conversational carry-over.
An identity check catches discovery precedence, stale installs, and same-name
collisions. One cannot replace the other.

## Guidance

Before treating a cross-harness skill run as evidence:

1. Declare the exact package revision, model, harness version, and material
   configuration before the run. Do not silently substitute an alias, a nearby
   model, or another package copy.
2. Run the skill end to end from a clean local-source install in each target
   harness. Reviewing documentation alone does not count as a native run.
   Compare the installed files with the declared source before using the result
   as evidence.
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

These runs often surface small fixes. A destination ambiguity may need one
clause in the skill. An identity failure needs better isolation and evidence.
Polished output from the wrong skill remains contaminated.

## Why This Matters

Scripted failures confirm only the path the author already imagined. A
differently constrained harness produces a real failure and can expose paths
the author missed.

Realistic environments also make silent fallback more dangerous. A same-name
collision can load the wrong copy. In this run, polished output quoted absent
clauses and was consistent with, but did not prove, an older user-level policy.
Without identity proof, the run could have produced a false pass. A useful
check must fail when the wrong skill copy loads.

## When to Apply

- A skill is being installed or evaluated in more than one named harness.
- A skill has explicit fallback or degradation instructions (validator unavailable, tool missing, network denied) that have only ever been tested by the author simulating the failure.
- A skill was authored and tested entirely inside the author's own configured environment.
- A project skill shares its name with a user-level, global, or system-provided skill.
- A model response mentions an instruction, section, state, or clause absent from the authoritative package.
- An adversarial reviewer demands proof that a fallback path fires in a native
  run.

## Examples

The first three cases come from the historical run log in
`tests/creating-portable-skills/results.md`:

1. **Codex CLI, network-denied sandbox.** `npx skills-ref` failed with
   `ENOTFOUND` mid-run. The agent followed the skill's manual fallback checks
   and reported that the validator was skipped. This was the degradation path
   the reviewer wanted to test, produced without a scripted network failure.
2. **Claude Code visitor run, clean repo.** Surfaced three destination ambiguities the author's own runs never hit: where the new skill directory goes, where filled test templates go, and what "install" means when the user-level home is unreachable. The author's environment had answered all three implicitly. Each became a one-clause fix, applied and re-validated same-day.
3. **Grok CLI run.** Its fresh-context baseline found a real double-bucketing
   defect in the generated skill. The subtract pass fixed a bug that the
   author's own context had missed.
4. **Opus 5 same-name collision.** Two policy-probe attempts quoted rules absent
   from the exact project files. They were excluded rather than averaged into
   the result. A fresh safe-mode, tool-less run with the exact policy embedded
   supplied bounded policy evidence only. The later native rerun separately
   installed from local source, compared all six installed files with that
   source, recorded the project-local load path, and checked a distinctive body
   sentence (`tests/creating-portable-skills/results.md`, "Final-source U4
   rerun").

## Related

- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` covers
  the same shipping evidence from a different angle. In the recorded skills
  CLI 1.5.19 behavior, `@ref` targeting cloned the repository but scanned the
  default branch instead of checking out the requested ref.
- `tests/creating-portable-skills/baseline-cases.md` contains the matched cases
  and contamination records for the frontier retune.
- `tests/creating-portable-skills/results.md` contains the final package
  identity and native model-harness evidence.
- Issue jrgilbertson/the-rookery#13 is the frontier-model retune that surfaced
  the same-name collision.
