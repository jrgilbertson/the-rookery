# Subscription eval harness

A standalone runner with `harness.py` and `usage.py` installed together. Skills contain their evals and fixtures,
not this runner. A POSIX host (macOS or Linux), Python 3.12+, and standard library tests suffice. Runtime pricing
also requires the configured `ccusage` command. CLI binaries resolve through PATH.

Copy `example-round.json` to a private directory outside the public source repo
and outside the runner directory. Replace paths, models, and the commit SHA.
The archive and workspace roots must be separate, outside the repository, and
must not contain the repository. Workspace ancestors must have no agent rules or
configuration. The example is a template, not an executable eval configuration.

`--targets a,b` selects Executors and `--evals 1,2` selects cases. Targets with a
`grader` are Executors; targets without one are available only as graders. The
grader must name a different model from its Executor. Multiple Executors run
sequentially. Each gets one execution per selected eval by default; `runs` can
explicitly request repeats. `run_arms` defaults to just `changed_arm`.

Grade packets shuffle anonymous letters and scrub revision and workspace paths.
They include full tool names and inputs, project artifacts, and available child
readouts from saved sessions. Raw tool outputs remain in the private archive. Encrypted dispatch text is explicitly unavailable; neither the
parser nor grader should infer the exact prompt. This is evidence-based grading,
not proof that every internal model action was observable.

Inspect every failure, including invalid grading, isolation failures, missing
outputs, and failed assertions. Compare the old skill only on failing cases using
a separate config with a new `iteration`, the old commit in `arms`, and those
`evals`. Reports preserve the benchmark's `metadata`, `run_summary`, `runs`, and
`notes` shape, add raw assertion/cost evidence, and use null for ungraded results.
There are no aggregate deltas, thresholds, automatic ship verdicts, baseline
reuse, carry-forward, trigger screens, regrading workflow, or forced iteration
limit. The operator attributes failures and decides whether to ship. Incomplete reports stay under `incomplete/`; only fully graded rounds produce
benchmark files. Inspect their public-safe contents before committing evidence.

A `run` invocation preserves each slot, including failures, without automatically
retrying it. Use a new round for another execution. Explicitly invoking `grade`
again retries only ungraded valid executions in a new attempt directory; previous
grader attempts remain. Successful grades are retained. Config, eval content, runner source,
and package identities are frozen within a round. Actual CLI versions are recorded. Prefer immutable commit SHAs.

## Commands

Install [ccusage](https://github.com/ccusage/ccusage) on PATH, or set
`ccusage_command` to its argv in the private config. Version 20.0.24 was used
for the archived accounting checks. All providers use its calculate mode;
pricing stays with ccusage’s upstream sources.

```sh
python3 tools/eval-harness/harness.py isolation-check --round /private/path/round.json
python3 tools/eval-harness/harness.py run --round /private/path/round.json
python3 tools/eval-harness/harness.py grade --round /private/path/round.json
python3 tools/eval-harness/harness.py report --round /private/path/round.json
```

Authorize the round’s targets and budget before `run`. Inspect failures before
starting another round; creating a new config does not authorize more spend.
A missing ccusage command blocks inference before the first call. A model whose
price or usage cannot be resolved after a call leaves an unknown cost and blocks
the next call. `report` remains available for that incomplete round.

## Subscription access and isolation

Codex requires ChatGPT auth (`auth_mode: chatgpt` with tokens), forces that login
method, and ignores user config. Grok requires supported browser-session auth
in the official CLI’s issuer/client OIDC record. Access tokens must not be expired
or within one minute of expiry. Unrecognized login-file formats fail closed. Subscription
entitlement itself is checked by the provider when the CLI runs; auth-file
presence cannot prove remaining quota. Parent API-key environments, API-key auth
files, and API billing configuration are rejected. Child environments are built
from scratch; there is no API fallback. Login/quota failures stop the command.
The runner currently supports Codex and Grok subscription execution. Claude
parsing and cost normalization are retained for archived evidence; new Claude
invocation is disabled.

Each call copies only login material to a throwaway HOME and saves its sessions
before deleting that HOME. Refreshed auth is never copied back to the user's
setup or into the archive. Graders also retain session stores. An interrupted
persistence step leaves its HOME/workspace for recovery rather than destroying
unarchived evidence. These private scratch directories can contain credentials;
remove them after recovery. Archives contain prompts and session evidence and
must remain private.

`isolation-check` is static and makes no inference calls. Runtime traces are
checked for forbidden tool surfaces, missing reads of the installed skill,
foreign packages/user skills, and nested agent CLIs. This retains the original
trace-based isolation approach; it is not an OS security boundary. CLI flags and
session formats still need integration validation against the installed versions.

## Cost and stopping

Every execution and grader attempt, including a failed launch or invalid grade,
gets `cost.json` and a current-round ledger entry. The runner calls
`usage.estimate(adapter, transcript, sessions_or_none, output, command,
scratch_root, model=recorded_model)`. `ccusage_command` defaults to `["ccusage"]`.
`cli_cost_usd` is kept separately from the ccusage estimate.

One `budget_usd` covers all providers, Executors, graders, and failed attempts in
that round. Previous rounds are excluded. Calls are sequential and reserve
`call_allowance_usd` before launch. This allowance is **not a guaranteed dollar
hard cap**: Codex/Grok may overrun it in flight. The next call stops if insufficient
budget remains. Cost figures are API-equivalent estimates, not exact subscription
bills. The harness has no hardcoded rates or account-wide usage deltas.

A pending, missing, invalid, or unknown cost blocks further inference, including
a restart. Do not substitute zero. The operator must recover pricing from the
preserved call evidence and update both that call's `cost.json` and corresponding
`_ledger.jsonl` entry with the verified estimate and resolution evidence before
continuing. `report` remains available with unknown costs. No automatic cost
fallback or resolution command is provided. The ledger and its linked ccusage
report must agree before another call can begin.

## Zero-inference verification

```sh
python3 -m unittest discover -s /path/to/tools/eval-harness -p test_harness.py -v
```

`detector-check --round /private/path/round.json` runs the same suite. All launches
and usage estimation in these tests are fake. Coverage includes unknown-cost
stops, subscription-only guards, all-provider accounting including grader
failures, current-round budgets, retained sessions/attempts, blind packets,
full-length observations, private config paths, and foreign-access detection.
No real CLI, credentials, or eval is needed for the tests. `test_usage.py` covers isolated ccusage inputs, completed aggregate usage,
and rejection of partial pricing. The archived integration check used ccusage
20.0.24. Run both test files with `-p 'test_*.py'`.

`usage.py` calls ccusage in calculate mode with an empty local configuration,
to avoid loading ambient user pricing overrides. Codex saved sessions
include child sessions; tool-free ephemeral traces require their recorded model.
Claude and Grok completed per-model summaries include delegated usage and are
normalized to ccusage input records. Streaming partial usage is not a total.
Grok cache reads are added to its native input-token field exactly once.
The report retains ccusage’s version, output, warnings, and estimate limitations.
Aggregate summaries cannot recover per-request context tiers or Claude cache-write
TTLs; these remain estimates. No provider billing credentials go to ccusage.

The runner accepts one `with_skill` or `old_skill` arm per round. No-skill
diagnostics need a host that supports them. Complete reports use the canonical
benchmark filename; incomplete or identity-mismatched reports remain under
`incomplete/` with their original assertions. Text artifacts are retained in full;
raw tool outputs and installed skill text stay out of blind grading packets.
