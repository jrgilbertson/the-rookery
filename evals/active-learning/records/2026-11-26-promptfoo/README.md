# Active Learning Eval Record · 2026-11-26

- **Host and runner** macOS workstation, Node 24.22.1, Promptfoo 0.126.0 with
  `anthropic:claude-agent-sdk` 0.3.329, as [`prepare.sh`](../../prepare.sh)
  and [`run.sh`](../../run.sh) set it up. The sessions reported Claude Code
  2.1.331. Claude used subscription authentication.
- **Skill revision** The skill from commit
  `ae8405aef84b13d0c0a1b03a4fa80cbcb836a602`, tree
  `7ffe10c62dd35c9ad56ff1e9d15ec18644d64468`. A later commit only added
  "Networked Thinking atomic note in DAE format" to the description, which
  the trigger checks below cover.
- **Cases** The five in the [Skill Eval README](../../README.md). The
  case-set SHA-256 is
  `3fc6e9cee98a02856a4e72d1a2dcada722758b029f33ac66ea1fabfb56cf7e05`.
- **Baseline** No skill: the same request in a workspace built the same way,
  with nothing staged.
- **Model and effort** `claude-opus-5-5` at high effort for both arms. No
  judge model was used.
- **Date** 2026-11-26, between 11:13 and 11:19 PST.
- **Repeats and completion** One run per case per arm, all finished. The
  with-skill `source-stop` run and the no-skill `source-stop` run were each
  repeated once; see Notes.

## Labels and usage

The labeler is the authoring agent, Claude Opus 5.5, after reading each
response and transcript. The skill owner has not yet reviewed these labels.
"Changes nothing" and "Loaded the skill" are the code checks in
[`checks.mjs`](../../checks.mjs); "Judged" counts the case README's reading
checks that passed. Judged checks were not labeled on no-skill runs, which
already fail the code check, so they are Unmeasured there.

| Case | Run | Changes nothing | Loaded the skill | Judged | Write attempts | Input tokens | Output tokens | Seconds | USD |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [daily-pass](../../cases/daily-pass/README.md) | [with skill](daily-pass-claude-skill.json) | Pass | Pass | 2 of 2 | 0 | 90,831 | 6,527 | 57.3 | 0.269 |
| | [no skill](daily-pass-claude-baseline.json) | Fail | — | Unmeasured | 5 | 98,931 | 12,785 | 111.7 | 0.452 |
| [digest-reply](../../cases/digest-reply/README.md) | [with skill](digest-reply-claude-skill.json) | Pass | Pass | 2 of 2 | 0 | 65,570 | 3,640 | 34.7 | 0.165 |
| | [no skill](digest-reply-claude-baseline.json) | Fail | — | Unmeasured | 2 | 131,678 | 8,168 | 66.7 | 0.251 |
| [failing-card](../../cases/failing-card/README.md) | [with skill](failing-card-claude-skill.json) | Pass | Pass | 3 of 3 | 0 | 71,341 | 3,712 | 34.4 | 0.125 |
| | [no skill](failing-card-claude-baseline.json) | Fail | — | Unmeasured | 1 | 33,908 | 3,180 | 30.4 | 0.127 |
| [source-terms](../../cases/source-terms/README.md) | [with skill](source-terms-claude-skill.json) | Pass | Pass | 7 of 7 | 0 | 65,840 | 3,378 | 30.7 | 0.155 |
| | [no skill](source-terms-claude-baseline.json) | Fail | — | Unmeasured | 10 | 76,414 | 10,195 | 85.5 | 0.372 |
| [source-stop](../../cases/source-stop/README.md) | [with skill](source-stop-claude-skill.json) | Pass | Pass | 4 of 4 | 0 | 48,733 | 1,214 | 13.2 | 0.138 |
| | [no skill](source-stop-claude-baseline.json) | Fail | — | Unmeasured | 1 | 52,759 | 1,507 | 15.7 | 0.087 |

Every case fails without the skill and passes every check with it. The ten
recorded runs cost $2.14 at list price, as Promptfoo reported; the two
repeated runs and six trigger checks below added $0.98.

## Reasons

- **daily-pass, with skill.** Changed nothing; five items with "I'd start
  with #1"; the jitter disagreement is labelled "Question to check" because
  only an AI session contradicts the note.
- **digest-reply, with skill.** Took item 1 first, explained it from the
  user's highlights and clip, then asked what was happening twice in their
  own webhook bug, with no draft.
- **failing-card, with skill.** Checked the card against Brewer's 2012
  article, offered four fixes, and said which discard review history.
- **source-terms, with skill.** Mapped the terms and listed every status,
  ordered interface and signature first and said why, explained both
  together from the essay, offered the three choices for the keyword-sense
  Interface note, and asked for an example from the user's own code.
- **source-stop, with skill.** Proposed adding a To Explore section to
  Software Design with only the two kept terms, said the list goes from 0 to
  2 items, and wrote nothing.
- **No skill.** Every run tried to write: vault edits and new notes in four
  cases, and in `source-stop` a progress note, all denied.

## Trigger checks

One-turn `claude -p` requests with `active-learning`, `atomic-note`,
and `atomic-note-audit` staged. "Make a Networked Thinking atomic note in
DAE format for backpressure." loaded `atomic-note` with the reviewed
description, and `active-learning` once the description named that
wording. "Make an atomic note for idempotency." loaded `active-learning`,
and "Check every atomic note in my vault for DAE format problems." still
loaded `atomic-note-audit`.

## Notes

- The first with-skill `source-stop` run tried `Bash` to list files, which
  the check counted as a write attempt. `Bash` is no longer offered, and the
  repeated run is the one recorded.
- The first no-skill `source-stop` run wrote two files to Claude Code's
  auto-memory folder in the operator's home directory, which the allowed
  tools do not cover. `run.sh` now sets `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`,
  the files were removed, and the repeated run is the one recorded: it tried
  to edit a vault note and was denied.
- After this run, "Loaded the skill" moved to Promptfoo's built-in
  `skill-used` assertion and the tool check reads the allowed list from the
  run's own settings. Replaying both on these ten results gives the same
  labels, with "Loaded the skill" failing on every no-skill run.
