# Managing Issues Eval Record · 2026-11-19

- **Host and date** dev-machine, Linux x86-64, Node 24.22.1, 2026-11-19 PST.
  Claude used Claude Code subscription authentication. Codex used ChatGPT authentication.
- **Skill revision** `797baa11d1c0e8d03c437997f989a5d616642110` from main.
  The staged `skills/managing-issues` tree was
  `a8351c839150cf7356e2672768be455963e614fb`.
- **Cases** `password-reset-plus`, `file-both-single`, `follow-up-later`,
  `recurring-gap`, and `mention-link`. The case-set SHA-256 at the time of this
  run was `34629dcd49cf33cb11e7cd5475643cf03d305087de37fc9e3c165fd6834c4377`.
  After this run, `file-both-single` and `recurring-gap` were removed because
  they cannot be tested without a connected tracker; the updated three-case set
  SHA-256 for future runs is
  `314fba0c05c1a6d6638f4fa9b68a41e7684d559ed956f54ccdf8cb59a268c914`. From the
  Skill Eval directory, reproduce it with
  `{ find cases fixtures -type f -print0; printf '%s\0' promptfooconfig.cjs; } | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum`.
- **Baseline** Fresh Claude sessions without the `managing-issues` package,
  with the same requests and tracker fixtures as the treatment arms.
- **Model and effort** Both Claude arms used `claude-opus-5-5` at medium
  effort. The Codex arm used `gpt-6.2-sol` at high effort. The session
  metadata confirmed both settings. The owner supplied the final labels below.
  An LLM judge (`claude-opus-5-5`) also labeled the outputs, and the owner and
  the judge agree on all nine kept outputs.
- **Runner** Promptfoo 0.126.0 with `anthropic:claude-agent-sdk` 0.3.329
  and `openai:codex-sdk` 0.169.1. The provider sessions reported Claude
  Code 2.1.329 and Codex CLI 0.169.1.
- **Repeats and completion** One recorded invocation per case per arm.
  All 15 finished sequentially. The excluded pilot attempts are listed below.

## Code checks and usage

| Case | Transcript | Sections | Scores | Tool audit | One Problem | STORE-412 | Input (cached) | Output (reasoning) | Seconds | List-price USD | Note |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| [password-reset-plus](../../cases/password-reset-plus/README.md) | [Claude with skill](password-reset-plus-claude-skill.json) | Pass | Pass | Pass | — | — | 59,260 (0) | 2,169 (595) | 23.632 | 0.280420 | |
| [password-reset-plus](../../cases/password-reset-plus/README.md) | [Claude Baseline](password-reset-plus-claude-baseline.json) | Fail | Fail | Pass | — | — | 26,355 (0) | 1,210 (218) | 15.332 | 0.129620 | |
| [password-reset-plus](../../cases/password-reset-plus/README.md) | [Codex with skill](password-reset-plus-codex-skill.json) | Pass | Fail | Fail | — | — | 78,962 (53,120) | 706 (196) | 31.111 | 0.064056 | |
| file-both-single | [Claude with skill](file-both-single-claude-skill.json) | Pass | Pass | Pass | Pass | — | 61,268 (0) | 2,571 (857) | 27.673 | 0.296492 | case removed after this run: cannot be tested without a connected tracker |
| file-both-single | [Claude Baseline](file-both-single-claude-baseline.json) | Fail | Fail | Pass | Fail | — | 26,579 (0) | 894 (105) | 10.828 | 0.124196 | case removed after this run: cannot be tested without a connected tracker |
| file-both-single | [Codex with skill](file-both-single-codex-skill.json) | Fail | Fail | Fail | Pass | — | 176,745 (143,232) | 1,528 (379) | 60.921 | 0.096629 | case removed after this run: cannot be tested without a connected tracker |
| [follow-up-later](../../cases/follow-up-later/README.md) | [Claude with skill](follow-up-later-claude-skill.json) | Pass | Pass | Pass | — | — | 67,547 (0) | 2,168 (599) | 23.328 | 0.313548 | |
| [follow-up-later](../../cases/follow-up-later/README.md) | [Claude Baseline](follow-up-later-claude-baseline.json) | Fail | Fail | Pass | — | — | 8,477 (0) | 406 (82) | 5.564 | 0.042028 | |
| [follow-up-later](../../cases/follow-up-later/README.md) | [Codex with skill](follow-up-later-codex-skill.json) | Pass | Fail | Fail | — | — | 175,494 (131,840) | 1,243 (134) | 43.056 | 0.112922 | |
| recurring-gap | [Claude with skill](recurring-gap-claude-skill.json) | Pass | Pass | Pass | — | — | 80,779 (0) | 2,619 (884) | 30.160 | 0.375496 | case removed after this run: cannot be tested without a connected tracker |
| recurring-gap | [Claude Baseline](recurring-gap-claude-baseline.json) | Fail | Fail | Pass | — | — | 26,449 (0) | 1,210 (253) | 14.344 | 0.129996 | case removed after this run: cannot be tested without a connected tracker |
| recurring-gap | [Codex with skill](recurring-gap-codex-skill.json) | Pass | Fail | Fail | — | — | 127,981 (110,848) | 1,385 (510) | 52.116 | 0.059201 | case removed after this run: cannot be tested without a connected tracker |
| [mention-link](../../cases/mention-link/README.md) | [Claude with skill](mention-link-claude-skill.json) | Pass | Pass | Pass | — | Pass | 60,007 (0) | 2,667 (656) | 27.043 | 0.293368 | |
| [mention-link](../../cases/mention-link/README.md) | [Claude Baseline](mention-link-claude-baseline.json) | Fail | Fail | Pass | — | Pass | 17,141 (0) | 962 (106) | 11.006 | 0.087804 | |
| [mention-link](../../cases/mention-link/README.md) | [Codex with skill](mention-link-codex-skill.json) | Pass | Fail | Fail | — | Pass | 81,170 (65,536) | 1,126 (285) | 47.838 | 0.049082 | |

The 15 recorded runs used **$2.454858** at list price and took 423.952 provider seconds. Seconds are Promptfoo's per-output latency. Claude's
provider reported the cost. Codex cost uses the recorded per-request tokens
and published list prices of $2 per million uncached input tokens, $0.10 per
million cached input tokens, and $10 per million output tokens. No Codex
request in the matrix crossed the long-context threshold.
[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing).
[GPT-6.2 Sol pricing](https://developers.openai.com/api/docs/models/gpt-6.2-sol).

## Reading the checks

- **Formatting can affect the section and score checks.** For example, the
  password-reset, export, and mention Codex responses give all four scores in a sentence the
  score check misses. In the export case, replaying the one-section check
  with inline bold headings allowed recognized one Problem section in the
  Codex output. The shared section check still requires separate headings.
- **The tool check now verifies Codex sandbox enforcement instead of parsing
  shell text.** During this run, the original narrow shell allowlist flagged
  Codex for tool discovery, chained reads, and Python probes even though the
  transcripts show no tracker writes. After this run, the shell parser was
  removed; the Codex check now asserts the run's recorded sandbox settings
  (`sandbox_mode` read-only or restricted read/deny filesystem permissions,
  command networking disabled, and `approval_policy` `never`) alongside the
  recorded Bubblewrap sandbox probe. The export run's in-memory CSV example is
  visible in its transcript for the operator to assess.
- **The mention check finds the identifier.** The operator can check whether
  the preview explicitly says Linear will add a related link. The create
  cases likewise need human review of approval, coverage, and any reasons
  given for unresolved preview fields.

The workspaces had synthetic GitHub or Linear configuration, including the
password-reset case that lacked a fixture in the first bake-off. No tracker
connector was enabled. Claude could read local files and invoke the skill.
Codex could read the active workspace, with command networking blocked. The
local preparer validated both fixture configs, and a sandbox probe verified
that Codex could read its skill and fixture while the model login, other
workspaces, writes, and outbound sockets were unavailable to shell commands.
No arm could complete live authentication or matchback. Promptfoo disk caching,
sharing, and telemetry were off. Claude's prompt caching was off. Claude had a
$0.95 cap per invocation. Codex had a five-minute per-invocation timeout.

Four Codex pilot attempts were excluded from the matrix. The first
profile exposed the installed Orca CLI. Its runtime probes failed before
contacting a tracker, and the next in-flight attempt was stopped. Two pilots
under a separate mount namespace then failed to start the nested shell
sandbox. The recorded Codex runs used the narrower native read-only profile.
The excluded attempts cost $0.322564 at list price for the reported tokens. The stopped attempt
may have unreported tokens from its last request. The run allowed $0.52 for
excluded usage in the budget check and remained below the $6 cap.

The saved transcripts preserve user and assistant messages, call arguments
and results, and run-specific session context. Temporary paths, host account
identifiers, and email addresses were replaced with placeholders. Internal reasoning, duplicate
vendor boilerplate, and runner logs stayed in the private run directory.

## Eval Labels

The run had no Linear or GitHub connection, so sign-in and target checks were
expected to be unresolved.

The owner asked for an LLM judge pass before labeling, to check that the cases
made sense. The judge (`claude-opus-5-5`, the Team lead) read each final output
and its tool calls against the case README. The owner labeled without seeing
the judge's verdicts. The owner and the judge agree on all nine.

| Output | Label | Labeler | Reason |
| --- | --- | --- | --- |
| [password-reset-plus-claude-skill](password-reset-plus-claude-skill.json) | Pass | owner | All right, this is good because it also proactively says that it wasn't able to check against the live repository, so that's clear. |
| [password-reset-plus-claude-baseline](password-reset-plus-claude-baseline.json) | Fail | owner | A clear failure for not using the sections or the scores. |
| [password-reset-plus-codex-skill](password-reset-plus-codex-skill.json) | Pass | owner | It uses the proper sections. The scores themselves do come through the suggested metadata, so we may need to slightly tweak it so it comes back through like on Opus 5.5, because the LLM as judge said scores failed here. But I do see the scores. It also seems like it was read-only, so I'm curious why the LLM judge thought it was a read-only fail. |
| [follow-up-later-claude-skill](follow-up-later-claude-skill.json) | Pass | owner | Yep, proper, proper response, plus it clarified that it needed access to Linear so it could actually do the next step. |
| [follow-up-later-claude-baseline](follow-up-later-claude-baseline.json) | Fail | owner | It was good about calling out not having a Linear connection, but it did fail on the Sections and the Scores. |
| [follow-up-later-codex-skill](follow-up-later-codex-skill.json) | Fail | owner | The sections are here, but it failed on the scores, and it seems like it was read-only as well. So I'm curious why the LLM as judge thought it was a fail for read-only tools. |
| [mention-link-claude-skill](mention-link-claude-skill.json) | Pass | owner | All right, looks good. Captured the sections, the scores appears to be read-only, and the STORE-412 is named. |
| [mention-link-claude-baseline](mention-link-claude-baseline.json) | Fail | owner | It did not capture the sections or the scores, but it did reference the store. |
| [mention-link-codex-skill](mention-link-codex-skill.json) | Pass | owner | This passed because it has the sections, it has the scores, although the scores aren't in a format that seems like are readable for you. It does mention the STORE-412, and it does appear to be read-only, so I'm curious why LLM as judge thought it would think it's a failure there. |

Where a reason mentions the "LLM judge" finding a score or read-only failure,
it refers to the code-check results shown on the review page, not to the
judge. The fixed checks now pass those outputs.
