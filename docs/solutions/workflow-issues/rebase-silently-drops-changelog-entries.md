---
title: "Union accumulating files during a rebase instead of taking one side"
date: 2026-07-29
category: workflow-issues
module: "git workflow for long-lived documentation branches"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Rebasing a long-lived branch onto a base that changed the same files"
  - "Resolving a conflict in a file whose contents accumulate rather than evolve"
  - "Any branch that adds a CHANGELOG entry and outlives one base rewrite"
symptoms:
  - "A conflict resolution looks clean, the tree builds, and nothing downstream fails"
  - "The branch's own changelog entry is missing from the pull request that ships it"
  - "The loss is invisible in review because the remaining entries read as complete"
tags: [git, rebase, conflict-resolution, changelog, silent-data-loss, verification-gates, documentation]
related_components:
  - documentation
  - tooling
---

# Union accumulating files during a rebase instead of taking one side

## Context

A documentation branch ran for about ten days and fifty-one commits while `main` moved underneath it. The rebase conflicted in five files. Four of them had been genuinely rewritten on `main`, so taking the upstream version was correct: keeping the branch's edits would have deleted new content to preserve older phrasing.

`CHANGELOG.md` conflicted the same way and got the same resolution. That one was wrong. The branch's two `Unreleased` entries, describing the very work the branch existed to do, were discarded. Nothing failed. The file parsed, the remaining entries read as a complete list, and the pull request was ready to open with its headline change unannounced.

It surfaced only because a pre-PR verification step asked a question no build system asks: does the changelog actually record this branch's work? A grep for the feature name in `CHANGELOG.md` returned only an unrelated older entry.

## Guidance

Sort conflicted files by how their contents change over time before resolving any of them.

**Files that evolve** hold one current statement of something. A concept definition, a README section, a configuration value. When both sides edited one, the newer and more complete side usually wins wholesale, and taking it is a real decision with a visible cost.

**Files that accumulate** hold a growing list where each entry is independent. Changelogs, release notes, contributor lists, migration indexes, `docs/` tables of contents. Both sides almost always *added* to the same region, so the conflict is positional rather than semantic. Neither side is more correct, and taking either one deletes the other's entries.

For an accumulating file, union the two sides. Keep every entry from both, ordered sensibly, and resolve only genuine duplicates.

Then verify the union held, because this is the class of mistake that leaves no trace:

```bash
# after any rebase or merge that touched CHANGELOG.md
git diff ORIG_HEAD -- CHANGELOG.md | grep '^-' | grep -v '^---'
```

Removed lines in a changelog after a rebase are almost always a mistake. A genuine deletion (a retracted entry) is rare enough to be worth confirming by hand.

The durable version of the check belongs in whatever gate runs before a pull request opens: confirm the branch's own work appears in the changelog. That question survives the specific mechanism, so it catches the same loss from a bad merge, a squash, or a hand edit. That gate now exists here as sweep class 3 in `skills/checking-pr-readiness/references/sweep-classes.md`, backed by `skills/checking-pr-readiness/scripts/changelog-union.sh`. It asks whether the branch's work appears at all, which complements the `ORIG_HEAD` diff above rather than replacing it.

## Why This Matters

Most conflict resolutions are self-correcting. Take the wrong side of a code conflict and a test fails, a type check breaks, or the feature stops working. The mistake announces itself.

An accumulating file has no such feedback. Every entry is independent, so removing one leaves the rest syntactically and semantically intact. The file looks finished because it *is* finished, just shorter than it should be. There is nothing to notice unless someone asks the specific question.

That makes it worse than a loud failure in one way that matters: the loss is discovered later by a reader who wanted to know what changed and could not find out, long after the context needed to reconstruct the entry is gone.

The asymmetry also explains why the wrong resolution felt right at the time. Four files in the same conflict genuinely called for taking the upstream side. Applying the fifth the same way was consistent, fast, and wrong, because consistency across files is the wrong axis. How the file accumulates is the right one.

## When to Apply

Sort by file behavior on any rebase or merge where the base has moved substantially. The risk rises with branch age, since a long-lived branch is likelier to span a base rewrite, and with the number of conflicts, since a large conflict set encourages resolving them as a batch under one rule.

The check is worth running unconditionally after a rebase that touched a changelog. It costs one command.

Skip the sorting exercise entirely for a short branch rebased onto a base that has barely moved; there, a conflict in an accumulating file is rare and obvious when it happens.

## Examples

Both sides add under the same heading, which is what makes the conflict positional rather than semantic:

```markdown
## [Unreleased]

### Changed

<<<<<<< HEAD
- `creating-portable-skills` now grounds guidance in real project evidence.
=======
- WORKFLOWS.md grew from an index into a full playbook.
- The README gained the guiding principles and the rookery framing.
>>>>>>> feature-branch
```

Taking either side alone produces a valid file and loses real information. The correct resolution keeps all three:

```markdown
## [Unreleased]

### Changed

- `creating-portable-skills` now grounds guidance in real project evidence.
- WORKFLOWS.md grew from an index into a full playbook.
- The README gained the guiding principles and the rookery framing.
```

One wrinkle worth expecting: entries restored after a rebase may need rewriting rather than restoring verbatim. In this case the original entry credited the branch with a vocabulary change that `main` had independently made in the meantime, so replaying the old text would have claimed work the branch no longer did. Recover the entry, then check that it still describes the diff you are actually shipping.

Both the loss and the repair are visible in [#17](https://github.com/jrgilbertson/the-rookery/pull/17).
