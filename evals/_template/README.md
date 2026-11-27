# Skill Eval Template

Canonical starter template for Skill Evals in The Rookery. Copy this directory
to `evals/<skill>/` when a skill gets its first synthetic Eval Case.

Every suite built from this template runs on Claude through Promptfoo's
`anthropic:claude-agent-sdk` provider with `apiKeyRequired: false`. It uses the
operator's signed-in Claude Code subscription on both macOS and Linux, with no
API key, no Bubblewrap, and no stored login files.

## Layout

- [`package.json`](package.json) and [`package-lock.json`](package-lock.json):
  pinned `promptfoo` and `@anthropic-ai/claude-agent-sdk` versions installed
  with `npm ci`.
- [`promptfooconfig.cjs`](promptfooconfig.cjs): Claude-only provider setup with
  `Claude with skill` and `Claude baseline` arms, `apiKeyRequired: false`,
  `permission_mode: 'dontAsk'`, `setting_sources: ['project']`,
  `strict_mcp_config: true`, `exclude_dynamic_sections: true`,
  `permissions.blockReadsOutsideWorkingDirectories: true`, auto-memory turned
  off in both `settings.autoMemoryEnabled` and
  `env.CLAUDE_CODE_DISABLE_AUTO_MEMORY`, and a bounded
  `evaluateOptions.timeoutMs`.
- [`checks.mjs`](checks.mjs): deterministic `file://` JavaScript assertion
  confirming every recorded tool call is in `custom_allowed_tools`.
- [`check-fixtures.mjs`](check-fixtures.mjs): offline check that exercises
  `checks.mjs` write-tool denial and asserts the `promptfooconfig.cjs`,
  lockfile, and launcher invariants. Runs automatically in the repository gate
  (`lefthook run pre-push --force`) with zero model calls.
- [`prepare.sh`](prepare.sh): stages the skill at a Git revision (default
  `HEAD`) into each with-skill workspace, builds plain synthetic workspaces
  (no Git repo, no `Bash` stand-ins), copies `package-lock.json`, and installs
  with `npm ci`.
- [`run.sh`](run.sh): runs one case on one arm with an isolated temporary
  `HOME` and `CLAUDE_CONFIG_DIR` inside the run directory while preserving
  signed-in Claude Code subscription auth, plus a per-run timeout.
- [`cases/example-case/`](cases/example-case/README.md): starter Eval Case
  holding `prompt.md` and human-read judgment statements in `README.md`.

## Tool boundaries

Offer `Write` and `Edit` in `tools`, allow only read-only tools in
`custom_allowed_tools`, and set `permission_mode: 'dontAsk'`. Every write
attempt is denied before touching disk and still recorded in
`providerResponse.metadata.toolCalls`, so `checks.mjs` catches it cleanly.

Do not offer `Bash`: distinguishing a read-only shell command from a writing
one requires parsing command strings. `Read`, `Glob`, and `Grep` cover file
inspection. Add `WebSearch` and `WebFetch` to `readTools` only when a suite's
cases require live web lookup.

## Multi-turn cases without a custom driver

Keep every Eval Case a single-turn Promptfoo run. When a case tests behavior
partway through a conversation, carry the earlier user and assistant turns
directly inside `cases/<id>/prompt.md` (see
[`cases/example-case/prompt.md`](cases/example-case/prompt.md)) and place any
prior state snapshots in plain files inside the case workspace.

## Grading assertions

Two deterministic assertions run on every case by default:

- **Changes nothing:** [`checks.mjs`](checks.mjs) (`file://./checks.mjs`)
  verifies that every tool call belongs to `custom_allowed_tools`.
- **Loaded the skill:** Promptfoo's built-in `skill-used` assertion verifies
  that the agent loaded `<skill-name>` (it is expected to fail on the no-skill
  baseline arm).

Judge reasoning, prioritization, and content quality by reading the response
and transcript against the statements in `cases/<id>/README.md`.

When automated semantic judging is wanted alongside human review, Promptfoo's
`llm-rubric` assertion is supported as an optional additive layer. Keep the
existing human-read statements in `cases/<id>/README.md`, and author and
calibrate any `llm-rubric` judge prompt with `write-judge-prompt` and
`validate-evaluator` before trusting its labels.

## Copy checklist

1. Copy `evals/_template/` to `evals/<skill>/`.
2. Update `package.json` (`name`), `prepare.sh` (`skill_name`), and
   `promptfooconfig.cjs` (`description` and the `skill-used` value).
3. Replace `cases/example-case/` with synthetic Eval Cases derived from
   observed failures, and add any case-specific workspace builder or fixture
   files.
4. Regenerate `package-lock.json` if `package.json` changed, then verify
   offline with `node evals/<skill>/check-fixtures.mjs` and
   `lefthook run pre-push --force`.

## Run

Each live run calls a paid model, so get the skill owner's approval first.
With Node.js 22.22 or later, npm, Git, and Claude Code signed in, run from the
repository root:

```sh
work=$(bash evals/<skill>/prepare.sh)
bash evals/<skill>/run.sh "$work" claude-skill <case-id>
bash evals/<skill>/run.sh "$work" claude-baseline <case-id>
```

Keep raw results, temporary run directories, and session logs outside the
repository. Commit only reviewed synthetic Eval Records under
`evals/<skill>/records/`.
