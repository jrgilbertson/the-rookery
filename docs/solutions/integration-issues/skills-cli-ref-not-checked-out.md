---
title: "skills CLI @ref targeting silently scans the default branch"
date: 2026-07-16
category: integration-issues
module: "skills CLI install check (creating-portable-skills)"
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
tags: [skills-cli, vercel-labs, git-ref, default-branch, false-positive, install-check, ref-resolution]
---

# skills CLI `@ref` targeting silently scans the default branch

## Problem

`npx skills add owner/repo@<name>` looks like ref syntax and is not. The CLI
parses the `@` suffix as a skill-**name** filter, then clones and scans the
default branch. Passing a branch name there quietly scans the wrong tree and
usually reports `No skills found`, while the echoed `Source: ...@<name>` and
`Repository cloned` lines suggest the ref was honored. Any pre-merge install
check built on `@<branch>` or `@<sha>` is testing the default branch.

Ref targeting does exist, under a different form: `owner/repo#<ref>` is passed
through to `git clone --branch`. That form genuinely checks out the ref and
fails loudly on a bad one, so it is usable for a pre-merge install check
against a pushed branch. A 40-character commit SHA still fails, since `git clone --branch`
cannot take one, but it fails loudly (`Remote branch <sha> not found in
upstream origin`) rather than falling back.

This surfaced while running the install-check gate for `skills/creating-portable-skills` on branch `jrgilbertson/Initial-setup` of `jrgilbertson/the-rookery`. PR #4 merged on 2026-07-17. The original gate evidence lived in `tests/creating-portable-skills/results.md`, which the lightweight-tests restructure removed; it is in git history at commit `cc66ee8`.

## Symptoms

- `npx skills add jrgilbertson/the-rookery@jrgilbertson/Initial-setup` echoed `Source: ...@jrgilbertson/Initial-setup` and `Repository cloned`, then reported `No skills found`, while `gh api` confirmed that ref contained `skills/creating-portable-skills/SKILL.md` with valid frontmatter.
- The same result with a full 40-character commit SHA as the ref, ruling out slashed-branch-name parsing as the cause.
- A local-path scan of the identical tree discovered the skill correctly (session-verified with `npx skills add . --list`; the recorded gate evidence uses the install form shown under Solution), isolating the failure to remote ref handling.

## What Didn't Work

- **The `@` form** (`owner/repo@branch-name`): not a ref at all. It filters by skill name, so the scan runs against the default branch and the branch name matches nothing.
- **Commit SHAs** (`owner/repo#<full-40-char-sha>`): unsupported in either form, because `git clone --branch` cannot take a SHA. On 1.5.21 this errors rather than falling back.
- **The earlier "confirmation" that the branch-ref form worked.** At the time of that verification, the target branch also had zero skills, so `No skills found` was indistinguishable between correct-ref-with-no-skills and silent-fallback-to-default. The verification was structurally incapable of failing, which makes it a false positive generator rather than a check.

## Solution

Split the install check by merge state:

**Pre-merge**: install from the local source, then verify files actually land in the agent homes:

```console
$ npx skills add . --skill creating-portable-skills --agent claude-code --agent codex -g -y --copy
# verify: files present in ~/.claude/skills/ and ~/.agents/skills/,
# skill registered live in the running harness
```

**Post-merge**: re-run the plain remote install check against the default branch, which is the tree the CLI actually scans:

```console
$ npx skills add owner/repo --list
```

Record the CLI version alongside every install check, and which syntax form you used (`@` or `#`). The original observation was on `skills` 1.5.19; the mechanism above was re-checked on 1.5.21 (2026-08-01), where the `@`-as-name-filter behavior and the working `#<ref>` form were both confirmed directly. The tool is resolved fresh via `npx`, so its surface can change silently between runs.

Where the branch is pushed, `npx skills add owner/repo#<branch> --list` is now a genuine remote pre-merge option: it checks out the ref and fails loudly on a bad one. Checking against the local source stays the default for unpushed work. The gate row recording the original local install check as the pre-merge pass is in git history at commit `cc66ee8`; `tests/creating-portable-skills/log.md` is the current run log. The deferred publication check completed after merge on 2026-07-27: `npx skills@1.5.20 add jrgilbertson/the-rookery --list` reported four skills from the default branch and included `creating-portable-skills`. This confirms default-branch publication. The catalog has since grown past four skills, so treat that count as a fact about 2026-07-27 rather than a current one.

## Why This Works

The local-path scan reads the working tree directly, so it exercises the same discovery logic (frontmatter parsing, skill layout) without the broken remote ref resolution. Verifying installed files in the agent homes confirms the full install path, not just discovery. The post-merge remote install check then tests the only remote configuration the CLI actually supports (the default branch) at the moment it becomes the true state of the repo. Together the two install checks cover everything the `@ref` form pretended to cover, with each check's success observable only when its mechanism genuinely works.

## Prevention

- Never trust a CLI's echo of your arguments as evidence they were honored. `Source: ...@<ref>` plus `Repository cloned` proved nothing about which tree was scanned.
- The meta-lesson: **a verification that cannot distinguish success from fallback is a false positive generator.** Design probes whose success state is observable only when the mechanism works. Here, that means probing against a ref that DOES contain the artifact. If the ref has skills and the default branch doesn't (or they differ detectably), the output discriminates; if both are empty, "No skills found" confirms nothing. Before accepting a green result, ask: what would this check print if the mechanism silently fell back?
- When a remote tool misbehaves, bisect with a local equivalent over the same tree (`npx skills add . --list` here). If local discovery passes and remote fails, the defect is in remote handling, not your artifact.
- Pin the observation to the tool version. For 0.x tools resolved fresh via `npx`, re-verify the failure mode before relying on this workaround; the ref handling may be fixed (or changed) in a later release.

## Related Issues

- PR jrgilbertson/the-rookery#4 (merged 2026-07-17; the branch whose install-check gate surfaced this)
- `tests/creating-portable-skills/log.md` — the current run log; the original gate evidence and caveat are in git history at `cc66ee8`
