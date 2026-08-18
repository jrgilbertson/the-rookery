---
title: Keep repository issue configuration semantic at transport boundaries
date: 2026-08-17
category: architecture-patterns
module: skills/managing-issues provider configuration
problem_type: architecture_pattern
component: development_workflow
severity: medium
applies_when:
  - A repository-level workflow supports more than one provider or client transport
  - Provider metadata has different runtime representations across transports
  - First-use setup must capture durable repository choices without freezing session mechanics
tags:
  - agent-skills
  - issue-management
  - repository-configuration
  - provider-boundaries
  - linear
  - interactive-setup
---

# Keep repository issue configuration semantic at transport boundaries

## Context

Issue-management configuration and provider access solve different problems.
Repository configuration should preserve the durable choices collaborators must
share: the canonical provider, its exact target, optional synchronization
identity, and the team's semantic mappings. The active command path is an
execution detail of one session. Persisting it would make repository state
depend on whichever client happened to be available when setup ran.

Managing Issues applies that separation directly. Its validator accepts only
`version`, `provider`, `target`, optional `synchronization`, and four metadata
mapping families. There is no transport field
(`skills/managing-issues/scripts/config_check.py:21-32`,
`skills/managing-issues/scripts/config_check.py:273-320`). The Linear starter
config records a workspace, team, canonical priority names, estimates, labels,
and readiness vocabulary without selecting MCP or Orca
(`skills/managing-issues/assets/config-template-linear.json:1-34`). The provider
reference selects a transport at runtime instead: an explicit operator choice
wins, otherwise authenticated Linear MCP is preferred and Orca is used when MCP
is unavailable (`skills/managing-issues/references/linear-and-sync.md:7-15`).

## Guidance

### Persist meaning, not mechanics

Store the operator's canonical provider and exact target, the metadata
vocabulary issue authors choose from, and optional synchronization identity.
Do not store an IDE, CLI binary, MCP server, skill name, or transport
preference. The validator normalizes version, provider, target, mappings, and
optional sync source as the complete durable configuration
(`skills/managing-issues/scripts/config_check.py:273-320`).

### Choose one transport per session

Honor an explicit request for MCP or Orca. Without one, select available
authenticated MCP; use Orca only when MCP is unavailable. If selected MCP lacks
a required operation, stop instead of falling through to Orca. Once selected,
do not switch after a failed, indeterminate, or partially applied effect. A
transport change starts a new proposal with a fresh read, preview, and approval
(`skills/managing-issues/references/linear-and-sync.md:7-21`).

### Translate canonical values at the command boundary

Keep values such as `high` semantic in repository configuration. When a runtime
schema requires a provider-specific type, translate immediately before
constructing the call. The current Linear MCP mapping is `none` to `0`,
`urgent` to `1`, `high` to `2`, `medium` to `3`, and `low` to `4`; if the
active schema does not document the conversion, stop rather than guess
(`skills/managing-issues/references/linear-and-sync.md:60-73`). The validator
reinforces this boundary by accepting canonical Linear priority names and
rejecting other representations
(`skills/managing-issues/scripts/config_check.py:217-230`).

### Gate setup on the first mutation

Missing or incompatible configuration does not block a read or draft. Before
the first tracker mutation, interactive setup resolves provider, exact target,
sync posture, and metadata mappings, then resumes the pending request after
setup completes (`skills/managing-issues/SKILL.md:74-120`).

Show starter recommendations beside discovered provider alternatives. For each
mapping family, let the operator accept the recommendations, map selected
existing values, or define custom representations. Existing tracker metadata
is evidence, not an automatic preference. Priority, estimate, and general-label
mappings may be empty, but readiness retains the three canonical choices
`needs-discovery`, `needs-planning`, and `ready` so issue state remains
intelligible across repositories
(`skills/managing-issues/SKILL.md:98-108`,
`skills/managing-issues/scripts/config_check.py:24-28`).

### Keep effect approvals separate

If chosen labels are missing, preview and approve their provider-side creation
as one metadata batch and verify them first. Preview the repository config and
optional sync map as a separate setup batch. Then reread current tracker state
and request separate approval for the original issue mutation
(`skills/managing-issues/SKILL.md:110-126`). Setup approval never doubles as
issue-write approval.

Synchronization remains identity-only. The configured provider stays
canonical; a sync map supplies exact cross-provider identity and readback
evidence, not a second write target
(`skills/managing-issues/SKILL.md:128-131`,
`skills/managing-issues/references/linear-and-sync.md:138-155`).

## Why This Matters

Transport-neutral configuration is simpler and more portable. The same
repository configuration works when one collaborator uses connected Linear MCP
and another uses Orca, without config churn or disagreement about which client
is canonical. Command details remain governed by the active runtime schema or
installed version-matched guide, where they can stay current
(`skills/managing-issues/SKILL.md:138-149`).

Canonical semantic values also prevent provider representations from leaking
into issue analysis. A person can reason about `high`; the adapter can turn it
into numeric `2` only when the selected MCP schema requires that representation.
Mutation-gated setup removes unnecessary ceremony from read-only work while
still establishing durable shared conventions before repository or tracker
state changes.

## When to Apply

- A repository supports more than one authenticated client for the same
  tracker.
- Provider APIs encode a shared concept with different runtime types.
- Collaborators need durable target and metadata conventions, but not a
  mandated IDE or command surface.
- First-use setup may create provider metadata or repository files before the
  requested mutation.
- Synchronized trackers need exact identity without dual writes.

Do not add repository configuration for ephemeral client availability,
authentication state, retry state, or orchestration. Keep durable state in the
canonical tracker and the small repository config; exclude approval ledgers,
retry queues, graph files, and agent-only state.

## Examples

### Linear priority through MCP

The repository config says provider `linear`, identifies workspace and team,
and maps semantic priority `high` to `high`
(`skills/managing-issues/assets/config-template-linear.json:1-14`). The operator
does not select a transport, authenticated MCP exposes every required
operation, and its update schema requires an integer. Select MCP for this
session, preview numeric priority `2`, and send `2`; do not persist `mcp` or `2`
in the repository config
(`skills/managing-issues/references/linear-and-sync.md:7-21`,
`skills/managing-issues/references/linear-and-sync.md:64-70`).

### Explicit Orca choice

The same repository configuration is present, but the operator explicitly asks
for Orca. Select Orca, load the installed version-matched `orca-linear` guide
before constructing commands, and use the priority representation documented
by that guide (`skills/managing-issues/references/linear-and-sync.md:27-52`,
`skills/managing-issues/references/linear-and-sync.md:71-73`). Do not rewrite the
config to record `orca`.

### First create in an unconfigured repository

Pause before the tracker mutation, ask the operator to choose provider, exact
target, synchronization off or on, and starter, existing, or custom metadata
mappings (`skills/managing-issues/SKILL.md:85-108`). If selected labels are
missing, approve and read back their creation first; next approve the exact
config and optional map files; finally reread the tracker and preview the issue
create for its own approval (`skills/managing-issues/SKILL.md:110-126`). A read
in that same repository skips setup because it creates no durable shared
choice.

### Failed MCP create with Orca available

If an approved MCP create returns no confirmable identity while Orca is
installed, report the create as indeterminate and stop later effects. Do not
fall through to Orca. Using Orca requires a fresh canonical read, complete
preview, and new approval because transport selection is part of the executable
proposal (`skills/managing-issues/references/linear-and-sync.md:13-21`,
`skills/managing-issues/references/linear-and-sync.md:116-123`).

## Related

- [Keep issue bodies centered on Problem, Scope, and Verification](../best-practices/keep-issue-bodies-centered-on-problem-scope-and-verification.md)
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md)
- [GitHub issue #66](https://github.com/jrgilbertson/the-rookery/issues/66)
