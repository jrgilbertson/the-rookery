# Agent entropy audit

Find duplicated truth, dead code, stale guidance, and weakened guardrails, and recommend cleanups, mechanical checks, and standards updates.

- **Cadence:** Saturday at 07:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Access to the target repository, its PR and review history, its installed linters and diagnostic tools, and current primary sources when a stack question needs one. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt (`agent-entropy-audit-<repository name>`) and replace each `<placeholder>`. Keep the automation paused while validating its first manual run. A run with no prior history performs a full-repository baseline sweep; later weekly runs focus on recent changes and remaining debt. If you are upgrading from the retired coding standards audit, copy any prior decisions from `coding-standards-audit-<repository name>/decisions.md` into `agent-entropy-audit-<repository name>/decisions.md` before the first run, and leave `runs/` empty so the first run still performs a baseline sweep.

## Prompt

```text
History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `agent-entropy-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Audit this repository for agent entropy: duplicated truth, dead code, stale guidance, and weakened guardrails that make the codebase harder to predict and change.

Scope: if no prior run exists for this repository, run a full baseline sweep. On later runs, focus on PRs and code touched since the last run, check whether prior fixes and ratchets (automated checks that cap existing violations at today's count so debt can shrink but never grow) held, and take one targeted pass at remaining baseline debt. Run already-installed project linters, typecheckers, and diagnostic tools in read-only, non-interactive mode (check wrapper scripts for hidden cache or build writes; no auto-fix, installs, or package downloads), and report unavailable tools or unassessed areas as coverage gaps. Skip ad-hoc repo-wide count tables; cite counts when an existing tool or ratchet already reports them.

Inspect four areas:
- Guardrail erosion: inline suppressions, config-level ignore lists, disabled rules, allowlists, and loosened thresholds across the repository's linters, typecheckers, static analyzers, and diagnostic tools. Every non-obvious exclusion (outside generated, vendored, or build output) needs a clear, still-valid reason; otherwise recommend fixing the code, tightening the check, or adding a ratchet.
- Comment and doc rot: tautologies, session narration, stale prose (including repo-local agent skills and learning logs), commented-out code, and excuse comments that rationalize hacks instead of fixing them or filing tracked issues. Keep only non-obvious constraints the code cannot show, public contracts types cannot express, and brief pointers to ADRs or issues. Prefer types, assertions, or tests over inline warnings.
- Dead code and duplicated truth: unused files, exports, dependencies, expired feature flags, leftover scaffolding, and business rules or recurring patterns implemented inconsistently across layers. Check dynamic entrypoints and public exports before calling code dead, and mark ambiguous cases uncertain. Favor one clear, idiomatic pattern per recurring concern, and leave mechanical formatting to tools.
- Standards alignment: for repositories with substantive source code, review root `CODING_STANDARDS.md` (and propose a lean, repository-specific first edition if missing); for documentation or skill repositories, review their existing convention docs instead. Check guidance against actual code, recent PRs and reviews, installed versions, and current primary sources where relevant. Keep `CODING_STANDARDS.md` as the home for code-level conventions, with `AGENTS.md` linking to it rather than repeating it. Flag duplicated rules across repository docs and any direct conflicts with loaded global instructions. Graduate recurring prose rules and unpromoted learnings into linters, type checks, tests, or ratchets and delete the prose; prune rules that are stale, ignored, or already default model behavior.

For each recommendation, give the concrete edit or check, current versus proposed enforcement, and dated primary-source links when an external claim supports it. Scope broader cleanups separately or put them on a ratchet, and apply new rules to new or materially changed code by default. "No changes warranted" is a valid outcome.

Assessment only: do not modify repository files, install tools, change configuration, create or update issues, or publish PRs without separate approval.

Judge each draft recommendation on its own against current evidence. Apply the same bar to recommendations to leave a confirmed finding unchanged, and check how recommendations interact. Put only the recommendations you support in the approval list, in leverage order, highest first, with each one's evidence, tradeoffs, and uncertainty. List each rejected recommendation in one line with its reason, outside the approval list.

Save the final report afterward.
```
