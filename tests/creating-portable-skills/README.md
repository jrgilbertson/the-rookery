# Creating Portable Skills evaluation

Promptfoo **0.123.1** is the maintained skill-evaluation harness. Codex uses the
stock `openai:codex-sdk` provider and existing ChatGPT login. Claude's separate
configuration uses `anthropic:claude-agent-sdk`. No upstream fork, custom model
transport, trace parser, or capture-admission gate is required.

No cases are committed. Write a case only after error analysis of real use
finds a specific failure that persists after fixing the skill's instructions,
as [SKILLS.md](../../SKILLS.md#evaluation-workflow) describes. Prefer the code
checks below over a model judge.

A case is a Markdown file whose first line is `# <CASE-ID> — <title>` and which
contains a `## <CASE-ID>.INPUT` paragraph. Only that paragraph becomes the
executor prompt; keep expectations and notes in other sections. Commit a case
and its fixtures only when they are synthetic and safe to publish.

## Prepare privately

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow) and the user's current
execution allowance. Preparation does not call a model or authorize execution.
Use approved absolute paths outside the repository for tools, configurations,
workspaces, state, logs and exports. Each destination must be new.

```sh
# Install only if needed and separately authorized:
npm install --prefix "$eval_tools" promptfoo@0.123.1
# For Claude evaluations only, if needed and separately authorized:
npm install --prefix "$eval_tools" @anthropic-ai/claude-agent-sdk@0.3.263

python3 tests/creating-portable-skills/promptfoo_suite.py prepare codex "$case_file" "$eval_root" \
  --native-config "$approved_native_toml" --codex-bin "$native_codex" \
  --auth-store "$approved_auth_json"
# Optional: add --fixtures "$fixture_dir" to supply inputs checked unchanged,
# and --expect-no-skill-use for a near-miss case.
# Optional separate host; do not run without its own allowance:
python3 tests/creating-portable-skills/promptfoo_suite.py prepare claude "$case_file" "$claude_eval_root"
```

`native_codex` is the inspected, unmodified stock Codex executable (verified with
0.160.0). The approved non-secret TOML supplies normal model/effort defaults.
Preparation copies it into a private home and links the approved auth store,
without copying or printing credentials. Skill configuration object arrays stay
in TOML because the pinned provider cannot serialize them correctly as CLI flags.

The case gets an unchanged copy of the repository skill in ordinary
`.agents/skills/` or `.claude/skills/` discovery. `--fixtures` copies a directory
of synthetic inputs into the workspace. Setup records the input and package
hashes. Those identify what was prepared, not everything the agent read.

Codex uses read-only filesystem permissions, approvals never, no network/search,
no thread reuse, no SDK retries, a minimal subprocess environment, and private
state/log directories. ChatGPT authentication is forced; unset API keys before
running so the SDK reuses the existing login. Claude uses project discovery,
Read/Glob/Grep/Skill tools and `dontAsk`; live availability must be checked
separately. Read-only constrains writes, not all reads.

## Run an approved case

Run one config at a time, sequentially, once, with no retries. The caller must
impose a 600-second process limit. Do not combine configs: preservation hooks
must apply only to their case. Keep Promptfoo's own state private.

```sh
export PROMPTFOO_CONFIG_DIR="$eval_root/promptfoo-state"
export PROMPTFOO_DISABLE_TELEMETRY=1
export PROMPTFOO_MAX_RETRIES=0
# case_dir is the directory prepare printed, for example "$eval_root/CPS-ERR-001".
env -u OPENAI_API_KEY -u CODEX_API_KEY -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN \
  -u CLAUDE_CODE_USE_BEDROCK -u CLAUDE_CODE_USE_VERTEX \
  "$eval_tools/node_modules/.bin/promptfoo" eval \
  -c "$case_dir/promptfooconfig.json" --no-cache --no-write --no-share \
  --max-concurrency 1 -o "$case_dir/results.json"
python3 tests/creating-portable-skills/promptfoo_suite.py export \
  "$case_dir/results.json" > "$case_dir/report.json"
```

Stock `skill-used` assertions check the skill-use observation;
`--expect-no-skill-use` switches to `not-skill-used` for a near-miss. Every case also requires a nonempty final answer. Codex detects
skill paths in successful command text heuristically. This can miss legitimate
loads or match a command that only mentions the path. An observed match does
not establish exact instruction loading, complete tool capture or read confinement.
A negative observation means no matching skill use was reported, not proven absence.
Missing output and provider errors cannot pass the ordinary checks.

With `--fixtures`, a real assertion uses the file comparator in
`evaluate_read_only.py`. Hooks snapshot every supplied input before and after
execution; modified or replaced inputs fail. Missing snapshots remain Unmeasured
and do not pass.

Promptfoo owns execution, assertions and JSON exports. The report keeps ordinary
check results, skill-use observations and input preservation separate. Strict
capture is not collected and remains Unmeasured. Subscription cost is unknown;
API price estimates are not subscription charges. Human calibration is also
Unmeasured. Repository checks prove the configuration and evaluators work; they
do not establish skill quality.

## Offline checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/creating-portable-skills/fixtures/run-eval-checks.py
bash tests/creating-portable-skills/fixtures/run-signal-scan-checks.sh
lefthook run pre-push --force
```

These exercise the production configuration generator, case parsing, export
and preservation hooks against synthetic files. They make no model calls.
