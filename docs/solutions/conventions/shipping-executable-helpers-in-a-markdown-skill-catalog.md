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
  - "Running the install probe for a skill that bundles executable files"
  - "Deciding what a trigger-suite pass does and does not prove"
tags: [skills, bundled-scripts, install-probe, skills-ref, executable-bits, activation-smoke]
---

# Shipping executable helpers in a markdown skill catalog

## Context

Until `checking-pr-readiness`, every published skill in this catalog was
markdown-only. Bundling three bash helpers surfaced packaging facts that had
never been exercised here, and that the authoring conventions did not yet
record. This work is pending on branch `jrgilbertson/checking-pr-readiness`.

## Guidance

- **Validate the scripts-bearing skill with `skills-ref` before writing helper
  logic.** The validator accepted a `scripts/` directory containing
  non-markdown files on first contact (version 0.1.5 printed
  `Valid skill`), but that was unknown until tried — treat the first
  non-markdown addition to any skill as a stop-condition check, run
  immediately after creating the directory with a stub file.
- **Run the install probe from local source with `--copy` and check the bits.**
  `npx skills add <repo-path> --skill <name> --copy` into a disposable project
  delivered all files with executable bits intact (`-rwxr-xr-x`). The `--copy`
  flag matters for scripts: a symlinked install can differ in whether
  permission bits and file identity survive, and the probe is the only place
  that would catch it. Record the skills CLI version with the probe — it is a
  fast-moving tool resolved fresh via `npx`.
- **A trigger-suite pass is a listing proxy, never activation proof.** Judging
  queries against a skill's name and description shows the description works
  as an activation API; only a per-harness in-session smoke run — install,
  fire one trigger query, confirm from the trace which copy activated — shows
  the harness actually loads and runs the skill. Log the smoke per harness, or
  log explicit `not run — harness unavailable` lines; never fold a deferred
  smoke into a probe's pass line.

## Why This Matters

The first skill to carry executable files walks packaging paths nothing else
in the catalog has exercised. Each fact above was cheap to confirm and
expensive to discover late: a validator rejection after the helpers were
written would have forced a repackaging; lost executable bits would surface as
a broken helper on an installer's machine; and a trigger-suite pass mistaken
for activation coverage is exactly the listing-proxy conflation the testing
convention forbids.

## When to Apply

Whenever a skill in this catalog gains its first non-markdown file, and
whenever an install probe or run log is written for a scripts-bearing skill.
The activation-smoke rule applies to every skill, scripts or not.
