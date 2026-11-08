# Design system audit

Review every page of the interface against its design system, find drift and repeated patterns, and recommend fixes, shared components, and design-contract upgrades for approval.

- **Cadence:** Wednesday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The [`impeccable`](https://github.com/pbakaus/impeccable) skill, this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, a browser tool the agent can drive, and a local development stack that can start unattended with Docker and seed a fictional signed-in account. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Use a repository-specific slug in the prompt. Keep the automation paused while validating its first manual run. The run needs the strongest model you have, because judging taste is the job. Replace each bracketed placeholder with your own project's value. This is the prompt I run, with only project names, paths, and commands swapped out.

## Prompt

```text
Assess [product]'s interface against its design system and recommend fixes for approval, using the `impeccable` skill. Run impeccable only in its read-only modes: never run `document`, `extract` past its planning steps, `polish` or any other command that applies changes, `doctor --fix`, ignore-list changes, `live`, or `npx impeccable update`. This run is unattended: put every question impeccable would ask the user, including critique's closing questions, in the report's "Questions for you" section and continue.

[design contract] is the contract for drift findings, and [sidecar file] is its sidecar. Run impeccable `context` once from the repository root, then read the design contract in full.

Review every page, public and signed-in. A page family is a set of pages that share a route group and the same page shell or layout. Start from the previous report's family map and include the current one in the report.

1. Mechanical sweep, every page: run [token and layout validators]; impeccable `detect --json` over [UI source paths] only, because it ignores .gitignore (exit code 2 means findings, not failure); impeccable `doctor --json`; and [sidecar tests].
2. Rendered review: start the local stack with [local stack start command] in the background and wait until the app responds. Seed a throwaway review account with [review-account seed command], using a fictional email, a fresh UUID, and a random password generated for this run, then sign in through [development sign-in code endpoint]. Capture every page the account can reach, building URLs for parameterized routes from the seeded data. Review token-bound or one-time routes, and pages the account cannot reach, from code, and list them by name. If the stack or sign-in fails, review signed-in pages from code, say so, and finish everything else. Always end with [local stack teardown command that removes the database volumes], including after a failure.
3. Critique each page family once with impeccable `critique`, and apply the `audit` rubric. Add per-page notes only where a page departs from its family.

For each finding, name its kind: token drift (a hard-coded value where a token belongs), pattern drift (the same element built differently in different places), rule drift (a design-contract rule applied unevenly), or a complexity or hierarchy problem. Give the evidence (page, file and line, capture), the rule or token it breaks, and a fix that uses existing shared components and tokens.

- Extraction: recommend a shared component or page template only for a pattern used three or more times with the same intent and the same reason to change. Use `extract` through its planning steps only. Name the proposed piece, its variants, and the call sites it would replace.
- Sidecar: compare the sidecar with the design contract and with the source components it describes, including any part no test guards. Report an exact proposed patch; do not write it.
- Premium bar: separately from drift, propose design-contract revisions that raise the interface toward the craft of [reference products]. They set the quality bar, not the look; the contract's own identity and Do's and Don'ts take precedence. Give evidence and tradeoffs for each.
- Ratchet: when a finding recurs, meaning the same title or cause appeared in two or more earlier reports or it matches a kind the owner already accepted, propose an automated check, such as a lint rule or validator, that would catch it permanently, following the project's existing design checks.

Report in this order: the top five issues by impact; a table comparing this run's numbers with the last run's (validator and detector counts, duplicate-pattern clusters, extraction candidates, sidecar mismatches, pages rendered versus reviewed from code, findings by priority); the remaining findings grouped by cause; the sidecar patch; premium-bar proposals; proposed checks; questions for you; and what was not assessed or was blocked. Keep screenshots only as evidence for the top issues and premium-bar proposals.

Assessment only: do not modify tracked files, create or update issues, or publish PRs; implementation and issue creation require separate approval. The local stack and its seeded account are the only allowed side effects.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `design-system-audit-<repository name>` runs and owner decisions before assessing, and save the final report afterward, with its screenshots under that slug's `evidence/<UTC run stamp>/` folder. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence, such as the pattern reaching more pages or getting worse.
```
