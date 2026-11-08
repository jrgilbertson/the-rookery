# Design system audit

Review every page of the interface against its design system, find drift and repeated patterns, and recommend fixes, shared components, and design-contract upgrades for approval.

- **Cadence:** Wednesday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The [`impeccable`](https://github.com/pbakaus/impeccable) skill, this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, a browser tool the agent can drive, and a local development stack that can start unattended with Docker and seed a fictional signed-in account. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Use a repository-specific slug in the prompt. Keep the automation paused while validating its first manual run. The run needs the strongest model you have, because judging taste is the job. Replace each bracketed placeholder with your own project's value. This is the prompt I run, with only project names, paths, and commands swapped out.

## Prompt

```text
Audit [product]'s interface against its design system with the `impeccable` skill and recommend fixes for approval. [design contract] is the contract; [sidecar file] is its sidecar. Run impeccable `context` once from the repository root, then read the contract in full.

Review every page, public and signed-in, each run:

1. Run [token and layout validators], [sidecar tests], `impeccable doctor --json`, and `impeccable detect --json` over [UI source paths] only; detect ignores .gitignore, and exit code 2 means findings.
2. Start the local stack in the background and sign in as a throwaway fictional account, following [signed-in setup docs]. If the stack refuses its slot, claim another free slot whose leftover data it will clear on its own, and leave other worktrees' data in place. Capture every page that account can reach. Review token-bound routes, and pages it cannot reach, from code and name them. If the stack or sign-in fails, review signed-in pages from code and carry on. Always finish with [teardown command that removes the database volumes]; a kept database blocks next week's run.
3. Group pages into families that share a route group and page shell. Critique each family once with impeccable `critique` and the `audit` rubric, adding page notes only where a page departs from its family.

Report, in this order:

- The top five issues by impact.
- This run's counts beside the last run's: validator and detector findings, duplicate-pattern clusters, extraction candidates, sidecar mismatches, and pages rendered versus reviewed from code.
- The remaining drift, grouped by cause. Label each token, pattern, or rule drift, or a complexity problem, with its page, file and line, the contract rule it breaks, and a fix using existing components and tokens.
- Extractions: shared components or page templates for patterns used three or more times with the same intent, from `extract`'s planning steps.
- The exact sidecar patch.
- Premium bar: contract revisions that raise the craft toward [reference products], kept apart from drift. The contract's own identity wins over theirs.
- Ratchet: a lint rule or validator for any finding that appeared in two or more earlier reports.
- The questions impeccable would have asked, and what was not assessed.

Keep screenshots only for the top issues and premium-bar proposals. This is an assessment: impeccable stays in its read-only modes (`audit`, `critique`, `detect`, `doctor` without `--fix`, and `extract` through planning), and tracked files, issues, and PRs stay untouched.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `design-system-audit-<repository name>` runs and owner decisions before assessing, and save the final report afterward, with its screenshots under that slug's `evidence/<UTC run stamp>/` folder. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined or deferred findings only with new evidence, such as the pattern reaching more pages or getting worse.
```
