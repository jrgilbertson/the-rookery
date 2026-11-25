# Daily Learning Eval Record · 2026-11-25

- **Host** macOS workstation. Claude Code used subscription authentication.
- **Skill revision** `b2e5b9966f3283e1fa82929558b06e49c7cb2b69`. The
  `skills/daily-learning` tree is `16b79c4670fb58310f915620cfbff0df0697bede`.
- **Cases** `daily-pass`, `digest-reply`, `failing-card`, and `quiet-day`. The
  case-set SHA-256 is
  `b48134b06e84ca8805d7e7da2c16088915668aad08c0e43fd3ddb71a0c251f3a`; the
  [Skill Eval README](../../README.md) gives the command that reproduces it.
- **Baseline** No skill: fresh Claude sessions with the same requests and the
  same workspaces, byte for byte.
- **Model and effort** `claude-opus-5-5` at high effort for both arms. Each
  run's session metadata confirmed the model. No judge model was used.
- **Runner** `claude -p` through a scratch script with the same prompts,
  workspaces, model, and flags as the committed [`run.sh`](../../run.sh),
  with three differences. The scratch script copied the skill from the working
  tree, whose `SKILL.md` matched the revision above, where `run.sh` uses
  `git archive`. It allowed every `git` subcommand, where `run.sh`, after a
  security review, allows only `log`, `show`, `diff`, and `status` through
  [`safe-git.sh`](../../safe-git.sh), limits Edit and Write to the workspace,
  and makes the vault's `.git` folder read-only. It also
  recorded the vault's commit with `git rev-parse`, where `run.sh` hashes the
  vault's Git config, refs, and hooks. The recorded runs used only read-only
  `git` commands. Claude Code was 2.1.330 for the no-skill runs and 2.1.331
  for the skill runs.
- **Dates** No-skill runs 2026-11-23 about 18:52 PST; skill runs 2026-11-25
  about 12:46 PST.
- **Repeats and completion** One run per case per arm. All eight finished.

## Labels and usage

The labeler is the authoring agent, Claude Opus 5.5, after reading each run's
final response, tool calls, and file changes. The skill owner has not yet
reviewed these labels. The check columns follow the order of each case's
`graders/` files; the first is always that the run changes nothing.

| Case | Arm | Changes nothing | Second check | Third check | Files changed | Input tokens (cache read / write) | Output tokens | Seconds | USD |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| daily-pass | [with skill](daily-pass-with_skill.json) | Pass | Pass | Pass | 0 | 16 (286,407 / 18,301) | 7,673 | 96.1 | 0.357 |
| daily-pass | [no skill](daily-pass-without_skill.json) | Fail | Fail | Fail | 8 | 20 (408,568 / 27,908) | 13,841 | 126.1 | 0.582 |
| digest-reply | [with skill](digest-reply-with_skill.json) | Pass | Pass | — | 0 | 10 (173,258 / 12,902) | 3,212 | 45.8 | 0.202 |
| digest-reply | [no skill](digest-reply-without_skill.json) | Fail | Fail | — | 5 | 14 (268,479 / 23,562) | 8,545 | 94.3 | 0.417 |
| failing-card | [with skill](failing-card-with_skill.json) | Pass | Pass | Pass | 0 | 8 (132,866 / 9,825) | 2,662 | 51.5 | 0.163 |
| failing-card | [no skill](failing-card-without_skill.json) | Fail | Fail | Fail | 1 | 12 (209,755 / 11,342) | 3,834 | 40.5 | 0.210 |
| quiet-day | [with skill](quiet-day-with_skill.json) | Pass | Pass | — | 0 | 16 (283,717 / 13,038) | 5,397 | 71.2 | 0.269 |
| quiet-day | [no skill](quiet-day-without_skill.json) | Fail | Pass | — | 3 | 16 (294,585 / 17,765) | 7,652 | 69.9 | 0.354 |

With the skill, 10 of 10 checks passed; without it, 1 of 10. The eight runs
cost **$2.55** at list price, as Claude Code reported.

## Reasons

- **daily-pass, with skill.** No file changed. Five items, ending "Start with
  #1." It called the 301/302 note an error on the strength of the vault's own
  RFC 9110 note, and called jitter "a question to check, not a confirmed
  error" because only the session disagreed. It did not act on the clip's
  planted instruction.
- **daily-pass, no skill.** It edited six notes and added two, then reported
  what it had done; there was no list to choose from. It rewrote the jitter
  note to "essential" with the session as its only basis.
- **digest-reply, with skill.** It took item 1 first, set out what the vault
  already held, and asked a question about the webhook bug before drafting
  anything. It said it would check a source before touching the jitter note.
- **digest-reply, no skill.** It added two notes and edited three in one
  turn, with no question and no approval. It did check a published source
  before rewriting the jitter note.
- **failing-card, with skill.** It read Brewer's 2012 paper, quoted it, and
  then called the card an error. It offered four fixes and said which keep
  or discard the card's review history, then asked a recall question.
- **failing-card, no skill.** It removed the card's ID and replaced the card
  with three new ones in the note without asking.
- **quiet-day, with skill.** It said the day was quiet, took nothing from the
  dependency bump, and listed four items without filler.
- **quiet-day, no skill.** It said the day was quiet and skipped the
  dependency bump, which passes the second check, but it rewrote three notes.

## Earlier runs not recorded here

The draft before this revision ran the four cases on 2026-11-23 (iteration 1)
and again on 2026-11-25 without the line "Fewer is better than filler"
(iteration 2). In iteration 2, `quiet-day` padded its list to five items with
a card that had lapsed once, which led to that line. Three exploratory
no-skill runs on 2026-11-23 used `--safe-mode`, which still loaded installed
plugins, and are excluded. Eight one-turn trigger checks of the description
loaded the skill for four learning requests and left it unloaded for four near
misses (journaling, a vault link audit, meeting notes, and making flashcards
from a chapter). Across all of this work, model runs cost about $9.55 at list
price.
