# Creating Portable Skills evaluation

Five frozen cases measure activation and one bounded read-only audit:

- [CPS-ACT-001](cases/activation-near-miss.md): generic grader request, no activation.
- [CPS-ACT-002](cases/activation-authoring.md): implicit authoring, activation.
- [CPS-ACT-003](cases/activation-explicit-review.md): named review, activation.
- [CPS-ACT-004](cases/activation-writing-near-miss.md): meeting instructions, no activation.
- [CPS-AUD-001](cases/vendor-guidance-audit.md): compare the supplied synthetic
  guide and skill while preserving portability and their files.

The maintained execution interface is Promptfoo **0.123.1**, using the built-in
`openai:codex-app-server` and `anthropic:claude-agent-sdk` subscription providers.
There is no custom model transport, recorder, controller or dashboard. Grok is
outside scope. Case INPUTs, audit fixtures and criterion prompts remain canonical.
Draft quality, updating and migration are not measured by the activation cases.

## Prepare outside the repository

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow) for authorization and
limits before live runs. All dependencies, configs, workspaces, native homes,
SQLite, logs, traces and exports must live in an approved private directory.
Set the shell variables below to absolute private paths. `eval_root` must be a
new directory; preparation fails if it exists. Keep the source worktree intact
while its absolute config references are in use.

```sh
npm install --prefix "$eval_tools" promptfoo@0.123.1
# Claude SDK is an optional dependency; if absent, install it privately:
npm install --prefix "$eval_tools" @anthropic-ai/claude-agent-sdk@0.3.263

python3 tests/creating-portable-skills/promptfoo_suite.py prepare codex "$eval_root" \
  --native-config "$approved_native_toml" --codex-bin "$native_codex" \
  --auth-store "$approved_auth_json"
# Prepare Claude in a different new private directory:
python3 tests/creating-portable-skills/promptfoo_suite.py prepare claude "$claude_eval_root"
```

`native_codex` names the inspected Codex **0.160.0** executable. The approved
non-secret native TOML supplies normal model/effort defaults and native skill
configuration; do not put credentials in it. Preparation copies that TOML into a
private native home and symlinks the existing approved auth store without copying
or logging secrets. Keep skill object arrays in valid TOML: the pinned provider's
CLI serializer cannot encode them correctly. Native SQLite and instrumentation
output stay private. Existing native auth and state are not modified.

Preparation copies the entire unchanged repository skill under ordinary
`.agents/skills/` or `.claude/skills/` discovery, and supplies AUD's frozen fixtures
at their named relative paths. It extracts exactly each INPUT paragraph into a
separate case config. No hints, criteria, isolation prose or native skill
attachment are added to creator input. Host settings are recorded separately.
The native Codex home can provision native system skills; admission records their
reads separately and does not claim creator exclusivity.

Codex runs use read-only, network disabled, approvals never, ephemeral threads,
no server reuse and native tool metadata. Each case has its own native trace
root. `executed_tool_call_metadata` can enrich inference history; disclose runs
as instrumented native CodeMode, retaining native default model/effort. Auth is
forced to the ChatGPT subscription. Claude uses project discovery, subscription
auth, no API fallback, no persistent session, and only Read/Glob/Grep/Skill tools
with `dontAsk`. This restricts tools; it does not prove every read's provenance.
No live Claude run should be attempted while quota is exhausted.

## Run and export each case

Use one config per invocation, sequentially, once, with no retries. The native
Codex turn limit is 570 seconds; the supervising caller must impose a 600-second
process limit. Do not combine configs: Promptfoo applies extensions across the
combined suite. Disable paid/API environment credentials and alternate cloud
auth before execution. Set Promptfoo state to a private directory as well.

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

The same commands apply to Claude's case directories. Built-in JSON exports
preserve provider output, available usage and latency. Subscription cost is
unknown; an API price estimate is not actual billed cost. The lifecycle hook
captures AUD input snapshots immediately before and after execution, using the
unchanged [C3 comparator](evaluate_read_only.py). C3 is a file observation,
reported separately from capture admission and semantic grades.

The capture assertion is deterministic and invokes no model. It checks frozen
package/body identity, canonical native input, ordinary discovery without body
preload, native thread/turn completion, closed item/call/result inventories and
actual command cwd/status. Supported reads are single `cat` operations, optionally
inside one native shell wrapper, within the workspace or native system-skill
root. Native CodeMode evidence comes from the native trace bundle, not interpreted
JavaScript: completed exec children must match invocation, runtime and terminal
output payloads and provider command items. Runtime argv must match the single
literal read in both the invocation and provider command; started/completed
command and cwd fields stay fixed. Shell operators are unsupported. Item/call
starts precede results, and cells and their children close before turn completion.
Every inference response payload is loaded, and ordered assistant answers and
facade calls must agree with raw notifications, display items and exported output.
The pinned provider can redact raw assistant content as exactly `['[...]']`;
that marker requires matching identity/phase and a full native response answer
that agrees with display and raw projected text. Other missing text is Unmeasured.
Every inference request retains the first request's user/developer context while
allowing accumulated assistant/tool history. Pinned `response.create` deltas may
inherit context only through a matching earlier response ID in the same turn;
added user/developer context is unsupported.
Trace schema support is pinned to
Codex 0.160.0. Native hooks, yielded cells, other tools, scripts,
unresolved/opaque commands, missing/altered/foreign records and unsupported discovery are **Unmeasured**.
Claude automated admission is currently Unmeasured pending native evidence review.

Only admitted complete captures grade behavior: a successful exact frozen body
read activates; complete supported absence passes the two near-misses and fails
positive activation cases. A failed body load remains an attempt, Unmeasured.
Listings, mentions, failed reads and Promptfoo's `skill-used` path heuristic do
not establish activation. Missing capture never passes, including near-misses.
Read-only blocks writes, not all reads. These checks inspect observed native
provenance; they do not certify every incidental OS read or authenticate evidence
against a malicious producer. Preserve traces for independent review.

Promptfoo's binary assertion UI displays Unmeasured as a non-pass diagnostic.
Use the exported capture and behavior fields to distinguish it from behavioral
Fail. Startup, timeout and quota failures are Unmeasured without retry.

## Provisional subscription judges

C1/C2/C4 use the frozen [criterion prompts](judges/) and synthetic challenges;
C3 remains deterministic. Prepare challenge configs from an existing private
creator config, using the same native subscription provider/defaults in empty
judge workspaces. Neither labels nor other judge prompts enter the judge input.

```sh
python3 tests/creating-portable-skills/promptfoo_suite.py prepare-judges \
  "$eval_root/CPS-AUD-001/promptfooconfig.json" "$judge_root"
# Run C1.json, C2.json and C4.json individually with the eval command above.
python3 tests/creating-portable-skills/promptfoo_suite.py extract-judge \
  "$judge_root/C1-results.json" > "$judge_root/C1-verdicts.json"
python3 tests/creating-portable-skills/judges/validate_results.py \
  CPS-AUD-001.C1 "$judge_root/C1-verdicts.json"
```

For the actual audit, prepare a separate new judge directory with
`--candidate-results "$eval_root/CPS-AUD-001/results.json"`, run its three configs,
and extract their arrays. Extraction checks native completion, candidate identity,
binary verdict and nonempty critique. Actual decisions remain provisional and
separate from synthetic challenge agreement. Do not admit subjective grades from
an inadmissible creator capture. Independent human calibration remains
**Unmeasured**; synthetic agreement cannot establish alignment or success rates.

## Offline checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/creating-portable-skills/fixtures/run-eval-checks.py
bash tests/creating-portable-skills/fixtures/run-signal-scan-checks.sh
```

The fixture runner exercises production admission with positive/negative
activation, capture removal, altered package/body, wrong cwd/status, unsupported
commands, outside-root reads, foreign identity and input/discovery contamination,
closed CodeMode child and zero-child captures, missing responses/children,
later context/model drift, delta references, raw answer contradictions, reordered
lifecycles and truncated outputs. It also exercises the production CJS hooks
through export for a modified-fixture C3 Fail, plus judge schema/challenges. Live results and
calibration evidence are private artifacts, not repository dependencies.
