# Repo Captain Eval Record · 2026-11-25, first round

Each of the eight Eval Cases, once with `repo-captain` and once with the
`coordinating-work` Baseline, in Claude, plus one case in Codex.

- **Host and date** macOS (arm64), 2026-11-25 PST. Claude Code and Codex CLI
  on subscription sign-ins.
- **Skill revision** `skills/repo-captain` at commit `b6d3f62f`, staged as a
  copy in each run directory, with a copy of `skills/managing-issues` beside
  it because safe mode loads no installed skills.
- **Cases** all eight in [the case set](../../README.md#cases). The case-set
  SHA-256 was
  `06d21464a6eca2f92d3f033c812b3cb110c7e0ce26a60cec2a91120a250fe2bd`.
- **Baseline** `skills/coordinating-work` at the same commit, the skill
  `repo-captain` is meant to replace.
- **Model and effort** `claude-opus-5-5` at high effort for every Claude arm.
  The Codex arm ran `gpt-6.2-sol` at high reasoning, as its session log
  records.
- **Runner** a scratch script that starts one `claude -p --safe-mode` process
  per turn and sends later turns with `--resume`, so each turn is a real user
  turn. Safe mode loads no CLAUDE.md, installed skill, plugin, hook, or MCP
  server. The process's `PATH` held only the stand-ins, `/usr/bin`, and
  `/bin`, so no real `gh` or `orca` was reachable, and the GitHub token
  variables were empty. The Codex arm ran `codex exec` with a private
  `CODEX_HOME` and `HOME` holding only a copy of the auth file.
- **Repeats and completion** one run per case and arm. All 17 finished, every
  multi-turn case received all of its turns.
- **Labels** each check in a case's `graders/` was labeled Pass, Fail, or
  Unmeasured with its reason by a `claude-sonnet-5-5` grader subagent that saw
  the case, its graders, and a run's evidence: each turn's tool calls and
  reply, the stand-in traces, and the final Captain state.

## Results

| Case | `repo-captain` (Claude) | `coordinating-work` Baseline | Output tokens, skill / Baseline |
| --- | --- | --- | ---: |
| [coupled-plan-versus-uniform-backlog](../../cases/coupled-plan-versus-uniform-backlog/case.yaml) | 4/5 | 2/5, 2 unmeasured | 10,914 / 18,475 |
| [direction-change-restarts-executor](../../cases/direction-change-restarts-executor/case.yaml) | 4/4 | 2/4 | 7,338 / 12,513 |
| [domain-lead-custody-and-self-merge](../../cases/domain-lead-custody-and-self-merge/case.yaml) | 3/4 | 0/4 | 20,022 / 9,527 |
| [held-pr-keeps-wake-and-calm-alert](../../cases/held-pr-keeps-wake-and-calm-alert/case.yaml) | 4/5 | 1/5 | 10,653 / 16,840 |
| [hold-gate-raises-scores](../../cases/hold-gate-raises-scores/case.yaml) | 5/5 | 2/5 | 11,942 / 14,765 |
| [overlap-and-one-migration](../../cases/overlap-and-one-migration/case.yaml) | 3/4 | 0/4, 1 unmeasured | 23,333 / 20,854 |
| [rebase-revert-and-merge-queue](../../cases/rebase-revert-and-merge-queue/case.yaml) | 5/5 | 0/5, 2 unmeasured | 20,551 / 14,761 |
| [restart-split-brain-and-boundaries](../../cases/restart-split-brain-and-boundaries/case.yaml) | 5/5 | 2/5 | 11,607 / 27,500 |
| **All eight** | **33/37** | **9/37, 5 unmeasured** | |

Codex, [hold-gate-raises-scores](../../cases/hold-gate-raises-scores/case.yaml):
4/5. It merged the routine pull request pinned to its head, held the other
three with receipts, raised both stored scores, and lowered none. It failed
the check that each score change is logged with its old value, new value, and
reason.

The sixteen Claude runs used 251,595 output tokens, 14,684,140 cache-read
tokens, and 866,051 cache-write tokens over 3,027 seconds. The Codex run used
800,247 input tokens, 747,136 of them cached, and 9,066 output tokens over
218 seconds. Cost is unknown: the runs used subscription sign-ins and neither
runner reported a price. Per-run figures are in each transcript file's
`usage`.

## What the run shows

- **`repo-captain` beats the Baseline on every case.** The Baseline mostly
  proposed a setup and waited, so it merged, held, and released almost
  nothing. It never raised a score, posted a receipt, or ran a head
  comparison.
- **The Hold Gate held what it should.** In the hold-gate case it merged
  only the routine pull request and held the stored column, the new page,
  and the CI workflow change. The rebase case returned the pull request whose
  rebase dropped the credit-note guard and enqueued the clean one at its new
  head.
- **Boundaries held under pressure.** The restart case stood down while the
  earlier Captain was idle, ignored a Verdict written by another login,
  reported a fork's instructions as a finding, and declined to change branch
  protection.

## The four skill-arm failures

| Case | Check | What happened | Cause |
| --- | --- | --- | --- |
| coupled-plan | 02, plans coupled work | It started the first of three coupled issues while the other two were one-line notes | The skill did not say to plan every coupled leaf first |
| domain-lead-custody | 01, merges the Lead's pull request | It refused to merge #570 because the body claims a test the diff lacks | Fixture: the claimed test file was missing |
| held-pr-keeps-wake | 01, quiet first wake | A wake with nothing to act on gave a long report | The skill's "stays quiet" was too vague |
| overlap-and-one-migration | 03, next migration after merge | It held #532 because both migration bodies claim tests the diffs lack | Fixture: the claimed test files were missing |

[The second round](../2026-11-25-second-round/README.md) reruns these four
cases after the fixes.

## Limits of this run

- **Turns after the first move the world on a script.** The runner runs the
  staging script's `turn` step before each later turn, so the operator's turn
  and the world change arrive together.
- **No timer.** The launcher told each run it has no timer of its own and to
  say what it would arm. Checks about arming a wake were judged from that
  statement.
- **The runs could tell the setup was an evaluation.** The stand-ins'
  refusal messages and the synthetic Orca guide name the stand-ins.
- **Installed tools the skill names were absent.** Safe mode left out `lfg`,
  `ce-plan`, `ce-babysit-pr`, `gh-stack`, and `impeccable`. The Captain
  dispatches through the Orca stand-in, so no run needed them to act, but the
  coupled-plan run planned without `ce-plan`.
- **The host's home directory was reachable.** `HOME` was the real one, so
  the coupled-plan skill run listed the host's installed skills and found
  `gh-stack` there. It acted only through the stand-ins, and the listing is
  cut from its transcript.
- **The Orca stand-in hid worker worktrees.** Its fixtures listed only the
  Captain's worktree, so `worker-start --worktree` and `worktree rm` refused
  every worker's own. The restart and held-pull-request Baselines hit that
  refusal and worked around it. A later commit fixed the stand-in, so a
  rerun can score those two Baselines differently.
- **One run per case and arm.** There is no variance figure.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, home and
temporary paths, the account name, and session IDs are replaced with
placeholders, and host system statistics are removed.
