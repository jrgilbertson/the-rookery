# Managing Issues Eval Record · 2026-11-19

- **Host** dev-machine, Linux x86-64, Node 24.22.1. Claude used Claude Code
  subscription authentication and Codex used ChatGPT authentication.
- **Skill revision** `e8bc36c5335461d5457159bec3d0711d5843bbf2`.
  The staged `skills/managing-issues` tree is
  `a8351c839150cf7356e2672768be455963e614fb`.
- **Case** [password-reset-plus](../../cases/password-reset-plus/prompt.md).
  The case-set SHA-256 is
  `470541e9a113b28a7330e531207be1d9c2de55d8b0085f1a2b4b7f7b4e254088`.
  From the Skill Eval directory, reproduce it with
  `sha256sum cases/password-reset-plus/{prompt.md,checks.mjs,audit-shell.py} | sha256sum`.
- **Baseline** A fresh Claude session without the `managing-issues` package.
- **Models** `claude-opus-5-5` with medium effort and `gpt-6.2-sol` with high
  effort. Native session metadata confirmed both settings. No model saw the
  six draft responses for judging.
- **Runners** Promptfoo 0.126.0, `anthropic:claude-agent-sdk` 0.3.329 and
  `openai:codex-sdk` 0.169.1. The comparison used Claude Code `plugin eval`
  2.1.329 and `codex exec` 0.170.0.
- **Repeats** One per arm. All six arms finished on 2026-11-19 PST.

## Usage and observations

| Runner and arm | Staged skill invoked | Three sections | Four scores | Tool calls | Input tokens (cached) | Output (reasoning) | Seconds | List-price USD |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| [Promptfoo Claude with skill](promptfoo-claude-with-skill.json) | Yes | Present | Present | 4 reads or skill calls | 40,180 (0) | 1,628 (428) | 17.637 | 0.193280 |
| [Promptfoo Claude Baseline](promptfoo-claude-baseline.json) | Absent | Absent | Absent | 1 read | 17,047 (0) | 1,055 (84) | 12.137 | 0.089288 |
| [Promptfoo Codex with skill](promptfoo-codex-with-skill.json) | Yes | Present | Absent | 3 shell items, read-only | 51,565 (38,784) | 489 (88) | 16.039 | 0.034330 |
| [Native Claude with skill](native-claude-with-skill.json) | Yes | Present | Present | 4 reads or skill calls | 42,637 (0) | 2,155 (964) | 24 | 0.213648 |
| [Native Claude Baseline](native-claude-baseline.json) | Absent | Absent | Absent | 1 read | 18,358 (0) | 1,081 (58) | 13 | 0.095052 |
| [Native Codex with skill](native-codex-with-skill.json) | Yes | Present | Absent | 3 shell items, read-only | 74,745 (58,240) | 505 (154) | 28.739 | 0.043884 |

The runs account for **$0.669482 at list price**. The harnesses reported cost
except for `codex exec`, which reports usage only. Its price estimate uses
$2 per million uncached input tokens, $0.10 per million cached input tokens,
and $10 per million output tokens. These figures compare usage under existing
logins. Promptfoo times are per-evaluation latency, native Claude times are
reported per-run durations, and native Codex time is shell wall clock. Its
startup logged a model-catalog refresh timeout before completing the turn.
[GPT-6.2 Sol pricing](https://developers.openai.com/api/docs/models/gpt-6.2-sol)

The Claude treatment transcripts show the resolved skill call and reads from
the staged package. The Baselines had no `managing-issues` skill in their
catalogs. Both Codex rollouts list the staged skill and record successful reads
of its `SKILL.md`. Each disposable workspace lacked tracker configuration.
The tool inventory shows zero tracker writes. Claude had no tracker MCP server
and no shell access. Both Codex rollouts report read-only filesystem access
and restricted command network access.

The initial Promptfoo Codex audit flagged a command item that batched several
reads. The committed audit recognizes those read-only commands individually.
Replaying the captured items offline accepted all six inventories. The
section and score observations are from the original responses. The shell
`codex exec` arm read the prompt from stdin with a trailing newline.

Promptfoo disk caching, sharing, and telemetry were off. Claude prompt
caching was off in both runners. The native runners made fresh sessions.
Codex reported cached model input tokens in both runners. Claude `plugin eval`
used `--no-publish` and a $1.50 suite cap. Promptfoo capped each Claude arm at
$0.95.

## Eval Labels

The repository owner labeled all six outputs on 2026-11-19 PST in a local
review page that showed each transcript beside the harness's code checks. No
model judge was used.

| Output | Label | Reason |
| --- | --- | --- |
| [Promptfoo Claude with skill](promptfoo-claude-with-skill.json) | Pass | Has Problem, Scope and Verification with observable checks, shows all four leverage scores, and wrote nothing to a tracker. (wording proposed by the Coordinator and approved by the owner) |
| [Promptfoo Claude Baseline](promptfoo-claude-baseline.json) | Fail | It failed because it doesn't have a problem scope verification sections along with the leverage scores. Nor does it appear to have been invoked. |
| [Promptfoo Codex with skill](promptfoo-codex-with-skill.json) | Fail | It doesn't show the leverage scores and other metadata that's expected for the managing issues. |
| [Native Claude with skill](native-claude-with-skill.json) | Pass | Has Problem, Scope and Verification with observable checks, shows all four leverage scores, and wrote nothing to a tracker. (wording proposed by the Coordinator and approved by the owner) |
| [Native Claude Baseline](native-claude-baseline.json) | Fail | It failed because it doesn't have a problem scope verification sections along with the leverage scores. Nor does it appear to have been invoked. (the owner's reason for the Promptfoo run of this arm, applied with the owner's approval) |
| [Native Codex with skill](native-codex-with-skill.json) | Fail | It doesn't show the leverage scores and other metadata that's expected for the managing issues. (the owner's reason for the Promptfoo run of this arm, applied with the owner's approval) |

Both Claude runs with the skill pass, and both Baselines fail, so the skill
changes the result on Claude. Both Codex runs invoked the skill and wrote the
three sections but left out the four leverage scores, so they fail. The
runner made no difference to any label.

The linked transcripts have the user requests, assistant messages, tool
arguments and results, and relevant session context. Temporary paths and one
account email were redacted. Internal reasoning, replay metadata, vendor
boilerplate, and raw runner output were excluded from the public record.
