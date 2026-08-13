---
title: The repo's declared contract governs artifact placement, not its current visibility
date: 2026-08-13
category: workflow-issues
module: repository-conventions
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "Deciding where to store an artifact that references sensitive or private material"
  - "A repository's instruction files declare it public or open-source-bound"
  - "Sensitive content was committed and the branch has not been pushed"
tags:
  [artifact-placement, same-door-rule, git-history, disclosure, public-bound]
---

# The repo's declared contract governs artifact placement, not its current visibility

## Context

During review of the repo-gardener sensing-floors change, a recall-reference
file listing roughly forty unpatched security findings of another private
repository was committed to `tests/` after checking only GitHub visibility
(the repo is private today). A standards review then caught what the
visibility check missed: `AGENTS.md` opens with "This is a public open-source
repository" and routes user-generated artifacts to per-run temporary
directories and approved private destinations, and `CONTRIBUTING.md`'s
same-door rule forbids private repo names and personal-environment
assumptions in the tree. The file violated the repo's own contract even while
the repo was private, and open-sourcing later would have disclosed it from
git history no matter when it was deleted.

## Guidance

Check the repository's declared contract before placing an artifact, not its
current visibility. A repo whose instruction files declare it public-bound is
public for placement decisions from that moment, because visibility is one
settings change away while git history is forever.

For an artifact that fails the contract: relocate the sensitive content to a
machine-local private destination outside every repository tree, keep only a
generic protocol or pointer document in-tree (one that carries no sensitive
rows, no private repo names, and no absolute paths), and — when the sensitive
file was already committed on an unpushed branch — amend or rewrite that
unpushed history so the file never exists in any commit. A follow-up removal
commit is not a fix: the content remains in history and ships with the first
push.

## Why This Matters

Visibility checks answer "who can read this today"; the contract answers "who
is this tree written for". Only the second survives an open-sourcing
decision. In this instance the gap was caught by review before the first
push, which is the last moment the clean fix (history amendment) is
available; after a push, removal requires history rewriting on a shared
remote plus treating the content as disclosed.

## When to Apply

- Before committing any artifact derived from private material into a repo
  whose instruction files declare it public, open-source, or install-from-main
- When a review flags sensitive content on a branch that has not been pushed:
  amend, do not add a removal commit
- When tempted to justify placement with "the repo is private" — verify the
  declared contract instead

## Examples

Wrong: commit a recall-reference file into the tests directory carrying rows
like "the fictional widget service trusts a client-supplied admin flag" (a
wholly invented stand-in — real rows named real weaknesses) into a repo
declared public-bound, because `gh repo view` says PRIVATE. (That file was
removed from all history by the fix; it exists in no commit.)

Right: store the findings table in machine-local automation state, commit
only `tests/repo-gardener/recall-protocol.md` (generic scoring rules, no
findings, location resolved from operator session context), and
`git commit --amend` the unpushed branch so the findings file never entered
history.

## Related

- `docs/solutions/architecture-patterns/separate-scout-measurement-stages-from-authoring-capacity.md`
  — sibling placement rule for repo-gardener run summaries (tracker or
  caller-approved destination, never public repository source); this doc adds
  the contract-over-visibility rule and the history-amendment remedy.
