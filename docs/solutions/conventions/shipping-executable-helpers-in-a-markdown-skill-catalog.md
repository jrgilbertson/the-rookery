---
title: "Shipping executable helpers in a markdown skill catalog"
date: 2026-07-31
category: conventions
module: "skills"
problem_type: convention
component: tooling
severity: medium
applies_when:
  - "Adding the first (or any) scripts/ directory to a skill in this catalog"
  - "Running the install check for a skill that bundles executable files"
  - "Deciding what a trigger-suite pass does and does not prove"
tags: [agent-skills, bundled-scripts, install-check, skills-ref, executable-bits, smoke-test]
---

# Shipping executable helpers in a markdown skill catalog

## Context

Until `checking-pr-readiness`, every published skill in this catalog was
markdown-only. Bundling three bash helpers surfaced packaging facts that had
never been exercised here, and that the authoring conventions did not yet
record. This shipped in PR #23 (merged 2026-08-01); `checking-pr-readiness`
remains the catalog's only scripts-bearing skill.

## Guidance

- **Validate the scripts-bearing skill with `skills-ref` before writing helper
  logic.** The validator accepted a `scripts/` directory containing
  non-markdown files on first contact (version 0.1.5 printed
  `Valid skill`), but that was unknown until tried. Treat the first
  non-markdown addition to any skill as a stop-condition check, run
  immediately after creating the directory with a stub file.
- **Run the install check from local source with `--copy` and check the bits.**
  `npx skills add <repo-path> --skill <name> --copy` into a disposable project
  delivered all files with executable bits intact (`-rwxr-xr-x`). The `--copy`
  flag matters for scripts: a symlinked install can differ in whether
  permission bits and file identity survive, and the install check is the only
  place that would catch it. Record the skills CLI version with the install
  check, since it is a fast-moving tool resolved fresh via `npx`.
- **A trigger-suite pass is a proxy measure, never activation proof.** Judging
  queries against a skill's name and description shows the description works
  as an activation API; only a per-harness smoke test (install,
  fire one trigger query, confirm from the trace which copy activated) shows
  the harness actually loads and runs the skill. Log the smoke test per
  harness, or log an explicit not-run line that names its reason and date:
  `not run — harness unavailable`, or `not run — waived by owner decision
  (<date>)`; never fold a deferred smoke test into an install check's pass
  line.

## Why This Matters

The first skill to carry executable files walks packaging paths nothing else
in the catalog has exercised. Each fact above was cheap to confirm and
expensive to discover late: a validator rejection after the helpers were
written would have forced a repackaging; lost executable bits would surface as
a broken helper on an installer's machine; and a trigger-suite pass mistaken
for activation coverage is exactly the proxy-measure conflation the testing
convention forbids.

## When to Apply

Whenever a skill in this catalog gains its first non-markdown file, and
whenever an install check or run log is written for a scripts-bearing skill.
The smoke-test rule applies to every skill, scripts or not.

The packaging rules here govern files under `skills/`, the ones an installer
copies into a user's tree. Test-only executables never enter a skill package
and are out of scope for both the `skills-ref` validation and the
executable-bit check: `tests/checking-pr-readiness/fixtures/run-helper-checks.sh`
and `tests/checking-merge-readiness/fixtures/bin/gh` are run from the
repository, not shipped from it.
