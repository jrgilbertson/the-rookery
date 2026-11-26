---
title: Prove "changes nothing" by denying the write tools
date: 2026-11-26
category: best-practices
module: skill evaluation
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "A Skill Eval checks that the agent changes nothing, such as a review that must stay read-only"
  - "Moving a Claude Skill Eval to Promptfoo's Claude Agent SDK provider"
tags: [skill-evals, promptfoo, claude-agent-sdk, read-only, auto-memory, tool-permissions]
---

# Prove "changes nothing" by denying the write tools

## Context

The `active-learning` Skill Eval checks that the coach writes nothing until
the user approves. Its first harness let the model write inside a throwaway
workspace, then compared file hashes before and after. That missed a write:
one run created a draft outside the workspace, and the workspace-only hash
reported no change.

Moving the suite to Promptfoo, two more traps showed up:

- **A shell call is not a write.** Offering `Bash` but allowing only read
  tools made the check fail a run that only listed files with `ls`. Telling
  `ls` from `rm` means parsing command text, which a tool-name check cannot
  do.
- **Auto-memory writes get through the denial.** A no-skill run wrote two
  notes into Claude Code's auto-memory folder, in the operator's real home
  directory. The check caught both `Write` calls, but `dontAsk` did not deny
  them: Claude Code allows writes to its own memory folder, so the files
  landed.

## Guidance

- Offer `Write` and `Edit` but allow only read tools, with
  `permission_mode: 'dontAsk'`. Every write is then denied, and the attempt
  still appears in `providerResponse.metadata.toolCalls`, so a code check can
  fail any call outside the allowed list. Nothing is written anywhere.
- Read the allowed list from the run's own `custom_allowed_tools` in the
  check, so the config and the check cannot drift apart.
- Do not offer `Bash` when the check is about writes. Glob and Grep cover
  finding files.
- Turn auto-memory off for every eval run with
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- Use Promptfoo's built-in `skill-used` assertion to show the skill loaded,
  rather than a hand-written check.

## Why This Matters

A "changes nothing" check that passes while something was written is worse
than no check: it certifies the one behavior it exists to catch. A check
that fails harmless reads sends authors to loosen it, which removes it.

## When to Apply

Use this for any Skill Eval whose success depends on the agent leaving files
alone. A suite that needs real writes to judge a result needs a different
check, such as comparing a known set of files.

## Examples

`evals/active-learning/promptfooconfig.cjs` offers `[...readTools, 'Write',
'Edit']`, allows `readTools`, and runs in `dontAsk` mode. `checks.mjs` passes
a run only when every recorded tool call is in that allowed list. Replayed on
the ten recorded runs, it failed every no-skill run (each tried to write) and
passed every with-skill run.

## Related

- [Wait for background work before capturing eval results](wait-for-background-work-before-capturing-eval-results.md)
- [Trace native terminal failures before changing capture admission](trace-native-terminal-failures-before-changing-capture-admission.md)
- [Loosening a checklist during grading removes the check](../workflow-issues/loosening-a-checklist-during-grading-removes-the-check.md)
