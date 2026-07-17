---
title: "skills CLI @ref targeting silently scans the default branch"
date: 2026-07-16
category: integration-issues
module: "skills CLI install probe (creating-portable-skills)"
problem_type: integration_issue
component: tooling
severity: high
symptoms:
  - "npx skills add owner/repo@<ref> reports \"No skills found\" for a branch that had just pushed a valid skill"
  - "Same \"No skills found\" result occurs against a full commit SHA ref, not only a branch name"
  - "CLI prints \"Source: owner/repo@<ref>\" but the clone step scans the default branch's tree instead of checking out that ref"
  - "An earlier \"verified working\" branch-ref workaround was actually a false positive, because the target branch also had zero skills at verification time"
root_cause: logic_error
resolution_type: workflow_improvement
related_components:
  - development_workflow
  - documentation
tags: [skills-cli, vercel-labs, git-ref, default-branch, false-positive, install-probe, ref-resolution]
---

# skills CLI `@ref` targeting silently scans the default branch

## Problem

The `skills` CLI (v1.5.19, resolved fresh via `npx`) accepts a ref suffix on remote installs — `npx skills add owner/repo@<ref>` — and its output claims the ref was honored. It was not. The CLI clones the repository but scans the default branch's tree, ignoring the requested ref entirely. Any pre-merge install probe that relies on `@<branch>` or `@<sha>` is testing the wrong tree.

This surfaced while running the install-probe gate for `skills/creating-portable-skills` on branch `jrgilbertson/Initial-setup` of `jrgilbertson/the-rookery` (PR #4, open as of this writing). Evidence recorded in `tests/creating-portable-skills/results.md`.

## Symptoms

- `npx skills add jrgilbertson/the-rookery@jrgilbertson/Initial-setup` echoed `Source: ...@jrgilbertson/Initial-setup` and `Repository cloned`, then reported `No skills found` — while `gh api` confirmed that ref contained `skills/creating-portable-skills/SKILL.md` with valid frontmatter.
- The same result with a full 40-character commit SHA as the ref, ruling out slashed-branch-name parsing as the cause.
- A local-path scan of the identical tree discovered the skill correctly (session-verified with `npx skills add . --list`; the recorded gate evidence uses the install form shown under Solution), isolating the failure to remote ref handling.

## What Didn't Work

- **Branch-ref form** (`owner/repo@branch-name`): output names the ref, but the scan runs against the default branch.
- **Commit-SHA form** (`owner/repo@<full-40-char-sha>`): same silent fallback, so both ref forms fail the same way.
- **The earlier "confirmation" that the branch-ref form worked.** At the time of that verification, the target branch also had zero skills, so `No skills found` was indistinguishable between correct-ref-with-no-skills and silent-fallback-to-default. The verification was structurally incapable of failing — a false positive generator, not a check.

## Solution

Split the probe by merge state:

**Pre-merge** — probe from the local source, then verify files actually land in the agent homes:

```console
$ npx skills add . --skill creating-portable-skills --agent claude-code --agent codex -g -y --copy
# verify: files present in ~/.claude/skills/ and ~/.agents/skills/,
# skill registered live in the running harness
```

**Post-merge** — re-run the plain remote probe against the default branch, which is the tree the CLI actually scans:

```console
$ npx skills add owner/repo --list
```

Record the CLI version alongside every probe (`skills` 1.5.19 this run). The tool is 0.x and resolved fresh via `npx`, so its surface can change silently between runs.

The gate row in `tests/creating-portable-skills/results.md` records the local probe as the pre-merge pass and defers the remote probe to post-merge under the "Remote install probe runs post-merge" caveat. That remote re-run is still pending: PR jrgilbertson/the-rookery#4 is open, not merged, as of this writing.

## Why This Works

The local-path scan reads the working tree directly, so it exercises the same discovery logic (frontmatter parsing, skill layout) without the broken remote ref resolution. Verifying installed files in the agent homes confirms the full install path, not just discovery. The post-merge remote probe then tests the only remote configuration the CLI actually supports — default branch — at the moment it becomes the true state of the repo. Together the two probes cover everything the `@ref` form pretended to cover, with each probe's success observable only when its mechanism genuinely works.

## Prevention

- Never trust a CLI's echo of your arguments as evidence they were honored. `Source: ...@<ref>` plus `Repository cloned` proved nothing about which tree was scanned.
- The meta-lesson: **a verification that cannot distinguish success from fallback is a false positive generator.** Design probes whose success state is observable only when the mechanism works. Here, that means probing against a ref that DOES contain the artifact — if the ref has skills and the default branch doesn't (or they differ detectably), the output discriminates; if both are empty, "No skills found" confirms nothing. Before accepting a green result, ask: what would this check print if the mechanism silently fell back?
- When a remote tool misbehaves, bisect with a local equivalent over the same tree (`npx skills add . --list` here). If local discovery passes and remote fails, the defect is in remote handling, not your artifact.
- Pin the observation to the tool version. For 0.x tools resolved fresh via `npx`, re-verify the failure mode before relying on this workaround; the ref handling may be fixed (or changed) in a later release.

## Related Issues

- PR jrgilbertson/the-rookery#4 (the branch whose install-probe gate surfaced this; the post-merge remote probe re-run is tracked in its Post-Deploy Monitoring section)
- `tests/creating-portable-skills/results.md` — the recorded gate evidence and caveat
