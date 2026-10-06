# Creating Portable Skills evaluation

Promptfoo **0.123.1** is the maintained skill-evaluation harness. Codex uses the
stock `openai:codex-sdk` provider and existing ChatGPT login. Claude's separate
configuration uses `anthropic:claude-agent-sdk`. No upstream fork, custom model
transport, trace parser, or capture-admission gate is required.

Five unchanged cases cover:

- [CPS-ACT-001](cases/activation-near-miss.md): generic grader request, no skill use.
- [CPS-ACT-002](cases/activation-authoring.md): implicit authoring, skill use.
- [CPS-ACT-003](cases/activation-explicit-review.md): named review, skill use.
- [CPS-ACT-004](cases/activation-writing-near-miss.md): meeting instructions, no skill use.
- [CPS-AUD-001](cases/vendor-guidance-audit.md): portability audit of synthetic
  inputs, with deterministic file preservation and provisional semantic judges.

## Prepare privately

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow) and the user's current
execution allowance. Preparation does not call a model or authorize execution.
Use approved absolute paths outside the repository for tools, configurations,
workspaces, state, logs and exports. Each destination must be new.

```sh
# Install only if needed and separately authorized:
npm install --prefix "$eval_tools" promptfoo@0.123.1

python3 tests/creating-portable-skills/promptfoo_suite.py prepare codex "$eval_root" \
  --native-config "$approved_native_toml" --codex-bin "$native_codex" \
  --auth-store "$approved_auth_json"
# Optional separate host; do not run without its own allowance:
python3 tests/creating-portable-skills/promptfoo_suite.py prepare claude "$claude_eval_root"
```

`native_codex` is the inspected, unmodified stock Codex executable (verified with
0.160.0). The approved non-secret TOML supplies normal model/effort defaults.
Preparation copies it into a private home and links the approved auth store,
without copying or printing credentials. Skill configuration object arrays stay
in TOML because the pinned provider cannot serialize them correctly as CLI flags.

Each case gets an unchanged copy of the repository skill in ordinary
`.agents/skills/` or `.claude/skills/` discovery. The audit also gets the frozen
fixtures. Only the case's INPUT paragraph becomes the creator prompt; judge
criteria and expected labels are not included. Setup records the input and
package hashes. Those identify what was prepared, not everything the agent read.

Codex uses read-only filesystem permissions, approvals never, no network/search,
no thread reuse, no SDK retries, a minimal subprocess environment, and private
state/log directories. ChatGPT authentication is forced; unset API keys before
running so the SDK reuses the existing login. Claude uses project discovery,
Read/Glob/Grep/Skill tools and `dontAsk`; live availability must be checked
separately. Read-only constrains writes, not all reads.

## Run the approved cases

Run one config at a time, sequentially, once, with no retries. The caller must
impose a 600-second process limit. Do not combine configs: audit lifecycle hooks
must apply only to their case. Keep Promptfoo's own state private.

```sh
export PROMPTFOO_CONFIG_DIR="$eval_root/promptfoo-state"
export PROMPTFOO_DISABLE_TELEMETRY=1
export PROMPTFOO_MAX_RETRIES=0
# case_dir is, for example, "$eval_root/CPS-ACT-002".
env -u OPENAI_API_KEY -u CODEX_API_KEY -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN \
  -u CLAUDE_CODE_USE_BEDROCK -u CLAUDE_CODE_USE_VERTEX \
  "$eval_tools/node_modules/.bin/promptfoo" eval \
  -c "$case_dir/promptfooconfig.json" --no-cache --no-write --no-share \
  --max-concurrency 1 -o "$case_dir/results.json"
python3 tests/creating-portable-skills/promptfoo_suite.py export \
  "$case_dir/results.json" > "$case_dir/report.json"
```

Stock `skill-used` / `not-skill-used` assertions check the expected skill-use
observation. Every case also requires a nonempty final answer. Codex detects
skill paths in successful command text heuristically. This can miss legitimate
loads or match a command that only mentions the path. An observed match does
not establish exact instruction loading, complete tool capture or read confinement.
A negative observation means no matching skill use was reported, not proven absence.
Missing output and provider errors cannot pass the ordinary checks.

Audit C3 remains a real assertion using the existing file comparator. Hooks
snapshot the supplied audit inputs before and after execution; modified or
replaced inputs fail. Missing snapshots remain Unmeasured and do not pass.

Promptfoo owns execution, assertions and JSON exports. The report keeps ordinary
check results, skill-use observations, C3 and subjective grading separate. Strict
capture is not collected and remains Unmeasured. Historical incomplete captures
are not reclassified. Subscription cost is unknown; API price estimates are not
subscription charges. Human calibration is also Unmeasured.

## Explicit subscription judges

C1/C2/C4 retain their unchanged criterion prompts. Prepare each as an explicit
provider call using the same subscription runtime, in an empty judge workspace.
There is no implicit paid `llm-rubric` grader. Preparation with no candidate uses
the existing synthetic challenges; that requires a separate execution allowance.

```sh
python3 tests/creating-portable-skills/promptfoo_suite.py prepare-judges \
  "$eval_root/CPS-AUD-001/promptfooconfig.json" "$judge_root" \
  --candidate-results "$eval_root/CPS-AUD-001/results.json"
# Run C1.json, C2.json and C4.json separately with the same env-unset eval command.
python3 tests/creating-portable-skills/promptfoo_suite.py extract-judge \
  "$judge_root/C1-results.json" > "$judge_root/C1-verdicts.json"
```

A creator error or missing answer cannot become a judge candidate. Extraction
checks the SDK final answer, candidate inventory, binary verdicts and critiques.
Only execute actual audit judgments after its ordinary checks, including C3,
pass. Results remain provisional. Synthetic challenge agreement does not prove
human alignment.

The full behavioral suite is five creator turns and three audit criterion judge
turns, each once, if authorized. Passing means the activation observations match,
the audit files remain unchanged, and C1/C2/C4 each return Pass. The initial audit
config passing alone is not a complete audit grade. Repository checks prove the
configuration and evaluators work; they do not establish skill quality.

## Offline checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/creating-portable-skills/fixtures/run-eval-checks.py
bash tests/creating-portable-skills/fixtures/run-signal-scan-checks.sh
lefthook run pre-push --force
```

These exercise the production configuration generator, exact case inputs,
subscription judge configuration, SDK result extraction and C3 hooks against
synthetic files. They make no model calls.
