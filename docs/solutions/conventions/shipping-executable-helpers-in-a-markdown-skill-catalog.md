---
title: "Shipping executable helpers in a markdown skill catalog"
date: 2026-07-31
last_updated: 2026-11-14
category: conventions
module: "skills"
problem_type: convention
component: tooling
severity: medium
applies_when:
  - "Adding the first (or any) scripts/ directory to a skill in this catalog"
  - "Running the Install Probe for a skill that bundles executable files"
  - "Deciding what a listing-level description check does and does not prove"
tags: [skills, bundled-scripts, install-probe, skills-ref, executable-bits]
---

# Shipping executable helpers in a markdown skill catalog

The readiness skills and their dedicated tests were retired on 2026-10-13, and
`creating-portable-skills` (with `signal-scan.sh`) was retired on 2026-11-18.
Their examples and source-path citations below describe the historical workflow.
Current shipping follows [WORKFLOWS.md](../../../WORKFLOWS.md#ship), current
skill evaluation follows [SKILLS.md](../../../SKILLS.md#skill-evals), and
post-merge activation verification uses the maintainer's
[Install Probe](../../../GLOSSARY.md#install-probe); the general lessons here
still apply to surviving skills and checks.

## Context

Until `checking-pr-readiness`, every published skill in this catalog was
markdown-only. Bundling three bash helpers surfaced packaging facts that had
never been exercised here, and that the authoring conventions did not yet
record. This work shipped in #23. The readiness helpers
`skills/checking-pr-readiness/scripts/surface-report.sh` and
`skills/checking-merge-readiness/scripts/fetch-pr-history.sh` are retired.
`skills/creating-portable-skills/scripts/signal-scan.sh` was retired with its
skill on 2026-11-18. The current helper is
`skills/managing-issues/scripts/config_check.py`.

## Guidance

- **Validate the scripts-bearing skill with `skills-ref` before writing helper
  logic.** The validator accepted a `scripts/` directory containing
  non-markdown files on first contact (version 0.1.5 printed
  `Valid skill`), but that was unknown until tried — treat the first
  non-markdown addition to any skill as a stop-condition check, run
  immediately after creating the directory with a stub file.
- **Check the executable bits in the installed copy at release time.** The
  original probe with `npx skills add <repo-path> --skill <name> --copy` into
  a disposable project delivered all files with executable bits intact
  (`-rwxr-xr-x`). A symlinked or copied install can differ in whether
  permission bits and file identity survive, and an installed copy is the only
  place that would show it. Agents no longer install candidates locally; the
  maintainer checks the bits after installing from `main`, as
  [RELEASING.md](../../../RELEASING.md) lists. Record the skills CLI version
  with the check — it is a fast-moving tool resolved fresh via `npx`.
- **A listing-level description check is a proxy, never activation proof.**
  Judging queries against a skill's name and description shows the description
  works as an activation API; only a per-harness in-session
  [Install Probe](../../../GLOSSARY.md#install-probe) — install, fire one test
  request, and confirm from the trace which copy loaded — shows the harness
  actually loads and runs the skill. That probe is a maintainer step after
  merge, never an agent install before merge. Record the probe per harness, or
  record an unavailable harness as Unmeasured per
  [RELEASING.md](../../../RELEASING.md); never fold a skipped harness into a
  probe's pass line.

## Why This Matters

The first skill to carry executable files walks packaging paths nothing else
in the catalog has exercised. Each fact above was cheap to confirm and
expensive to discover late: a validator rejection after the helpers were
written would have forced a repackaging; lost executable bits would surface as
a broken helper on an installer's machine; and a listing-level description check
mistaken for activation coverage conflates metadata review with a real harness
load.

## When to Apply

Whenever a skill in this catalog gains its first non-markdown file, and
whenever an [Install Probe](../../../GLOSSARY.md#install-probe) is run for a
scripts-bearing skill. The Install Probe activation rule applies to every skill,
scripts or not.
