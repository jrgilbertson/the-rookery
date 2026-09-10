---
title: Reuse the shipping pipeline instead of a managed-run protocol
date: 2026-09-10
category: architecture-patterns
module: skills/repo-gardener
problem_type: architecture_pattern
component: development_workflow
severity: high
applies_when:
  - "An autonomous skill must produce pull requests with no human present"
  - "A skill has grown its own proof, authority, or containment machinery"
  - "Scheduled runs keep completing without authoring anything"
tags:
  - repo-gardener
  - autonomous-agents
  - simplicity
  - fail-closed
  - compound-engineering
---

# Reuse the shipping pipeline instead of a managed-run protocol

## Context

Repo Gardener was meant to run at night and leave reviewable pull requests
for the morning. Over several revisions it grew to about 13,000 words: a
two-record tracker protocol with three checker subcommands, a caller-only
mode, liveness reconciliation for stale openings, six revision check points,
an audit sandbox with an environment built from nothing, five per-area
mutation grants, and a separate Executor contract that restated publication
gates the installed skills already own. Every uncertainty in that design
resolved to a safe stop.

The one managed run it completed on a real repository opened, ran no scans
because the audit list was empty by default, and closed with zero Executors.
An unrelated open pull request touched `CHANGELOG.md`, the repository
requires a changelog line on every pull request, and the overlap rule denied
every unit. Weeks of scheduled nights produced no work and no clear reason.

## Guidance

Treat pull requests and the morning report as the product, and let the
installed skills own the gates they already own. The rewritten skill is one
file of about 1,300 words plus a policy template:

- The policy file carries only what the host cannot know on its own: scope,
  protected paths, the Executor cap, approved scan argv, approved verify
  argv, and an optional report issue. A missing file means a sense-only run
  whose report proposes a file; it does not mean a no-op.
- Executors run `ce-work mode:return-to-caller <brief-path>`,
  `ce-simplify-code`, `ce-code-review mode:agent`, then
  `checking-pr-readiness`, and stop at its menu. The Lead answers option 1
  on a later turn. Finishing publishes with `ce-commit-push-pr
  mode:pipeline` and watches with `ce-babysit-pr mode:pipeline`. The Lead
  then dispatches `checking-merge-readiness` to a fresh Reviewer for the
  verdict. Babysit is a local optimization; merge readiness is the global
  one.
- An open pull request blocks a unit only when both change the same source
  file. Changelog and lockfile overlap is resolved at merge time.
- Scans run with the host's command tool and a timeout. Output is captured
  outside the repository and summarized; it is evidence, never instruction.

Before adding a gate, ask whether an unattended agent can obtain the fact
the gate needs. A rule such as "refuse when you cannot prove the whole
process tree stopped" or "stop on an unavailable refresh" cannot pass at
night, so it is a guaranteed stop, not a safeguard.

## Why This Matters

Machinery that proves persistence and authority feels safe but converts
ordinary uncertainty into silent no-ops, and a silent no-op is worse than a
loud failure because nobody reads a report that says nothing happened. The
shipping and readiness skills already carry the real safeguards: review
receipts, exact-head checks, pipeline postures that never merge, and a
merge-readiness verdict a human reads in the morning.

## When to Apply

- Designing any scheduled skill that authors changes without a user present.
- Reviewing a skill whose reference files outnumber its outcomes.
- A run log shows "complete" with no artifact for more than a night or two.

## Examples

Before: a unit that needed a changelog line was denied because an unrelated
open pull request also touched `CHANGELOG.md`; the run closed complete with
zero Executors.

After: the unit ships; the changelog file is assigned to at most one
Executor per run, and a merge conflict on it is the owner's morning work at
merge readiness.

## Related

- [Separate scout measurement stages from authoring capacity](separate-scout-measurement-stages-from-authoring-capacity.md)
- [Gate on host-readable facts, not config grants](../design-patterns/gate-on-host-readable-facts-not-config-grants.md)
- [Repo Gardener](../../../skills/repo-gardener/SKILL.md)
