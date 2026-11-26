# Active Learning Eval Record · 2026-11-25

- **Host** macOS workstation. Claude Code 2.1.331 with subscription
  authentication, run through the `run.sh` harness, since replaced by Promptfoo, as committed at each
  skill revision below.
- **Skill revisions** Round 1 used `3684f0d2849758b2ca34d54f28af404e67eb909b`.
  Round 2 reran the four runs that failed with
  `ad48aca23550646ef106d137be5328b238d2910b`, which explains each idea
  before asking about it and names atomic-note requests in the description.
  Runs marked "+ atomic-note" also staged `atomic-note` from
  `jrgilbertson/networked-thinking-skills` at
  `ae25bc8176ef9ffcdc550f26a23ab57d963e4272`. Each with-skill run's
  `staged.txt` and transcript confirm which skills it loaded.
- **Cases** All eleven in the [Skill Eval README](../../README.md), which
  gives the case-set hash and the command that reproduces it. The hash
  changed during the work as graders were corrected; this record's labels use
  the graders in the final case set. Two more cases, `source-explain` and
  `topic-map`, were run without the skill and then dropped because they
  passed.
- **Baseline** No skill: fresh Claude sessions with the same requests and
  workspaces, byte for byte. The four original cases keep their no-skill
  runs from the [2026-11-25 daily-learning record](../2026-11-25-opus-5-5/README.md),
  since their workspaces are unchanged.
- **Model and effort** `claude-opus-5-5` at high effort for every run. No
  judge model was used.
- **Dates** 2026-11-25. No-skill runs finished about 17:25 PST, round 1
  about 17:31, round 2 about 17:34.
- **Repeats and completion** One run per case per arm per round. Every run
  finished.

## Labels and usage

The labeler is the authoring agent, Claude Opus 5.5, after reading each run's
final response, tool calls, and file changes. The skill owner has not yet
reviewed these labels. Labels follow the order of each case's `graders/`
files, P for pass and F for fail; the first is always that the run changes
nothing.

| Case | Run | Labels | Files changed | Input tokens (cache read / write) | Output tokens | Seconds | USD |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| daily-pass | [with skill, 3684f0d2](daily-pass-with_skill.json) | P P P | 0 | 12 (209,321 / 16,605) | 4,034 | 47.5 | 0.256 |
| digest-reply | [with skill, 3684f0d2](digest-reply-with_skill.json) | P P P | 0 | 14 (255,265 / 16,540) | 3,223 | 58.9 | 0.252 |
| failing-card | [with skill, 3684f0d2](failing-card-with_skill.json) | P P P P | 0 | 8 (134,041 / 11,940) | 3,509 | 56.6 | 0.198 |
| quiet-day | [with skill, 3684f0d2](quiet-day-with_skill.json) | P F | 0 | 18 (331,516 / 17,828) | 5,500 | 82.2 | 0.338 |
| source-terms | [no skill](source-terms-without_skill.json) | F F F F F P F F | 10 | 22 (399,367 / 56,739) | 12,989 | 142.6 | 0.794 |
| source-terms | [with skill, 3684f0d2](source-terms-with_skill-round1.json) | P P P P P F P P | 0 | 10 (178,393 / 13,901) | 2,617 | 30.8 | 0.200 |
| source-terms | [with skill, ad48aca2](source-terms-with_skill.json) | P P P P P P P P | 0 | 12 (221,409 / 15,251) | 4,042 | 41.6 | 0.247 |
| source-stop | [no skill](source-stop-without_skill.json) | F F F F F | 5 | 16 (271,628 / 46,074) | 6,111 | 69.8 | 0.545 |
| source-stop | [with skill, 3684f0d2](source-stop-with_skill.json) | P P P P P | 0 | 8 (137,524 / 11,680) | 1,262 | 19.8 | 0.146 |
| source-unreadable | [no skill](source-unreadable-without_skill.json) | F F | 4 | 14 (217,705 / 43,644) | 5,550 | 69.1 | 0.504 |
| source-unreadable | [with skill, 3684f0d2](source-unreadable-with_skill.json) | P P | 0 | 10 (176,437 / 11,924) | 1,314 | 23.6 | 0.157 |
| topic-frontier | [no skill](topic-frontier-without_skill.json) | P F F F | 0 | 8 (108,315 / 40,776) | 5,536 | 60.4 | 0.459 |
| topic-frontier | [with skill, 3684f0d2](topic-frontier-with_skill.json) | P P P P | 0 | 16 (313,672 / 25,585) | 6,126 | 81.9 | 0.463 |
| frontier-pick | [no skill](frontier-pick-without_skill.json) | P F F F | 0 | 8 (108,526 / 38,941) | 3,089 | 43.5 | 0.395 |
| frontier-pick | [with skill, 3684f0d2](frontier-pick-with_skill-round1.json) | P F P P | 0 | 12 (218,047 / 13,517) | 2,008 | 31.6 | 0.192 |
| frontier-pick | [with skill, ad48aca2](frontier-pick-with_skill.json) | P P P P | 0 | 12 (218,895 / 15,712) | 3,150 | 49.0 | 0.235 |
| free-time | [no skill](free-time-without_skill.json) | P F F F | 0 | 14 (231,681 / 42,777) | 2,988 | 43.8 | 0.449 |
| free-time | [with skill, 3684f0d2](free-time-with_skill.json) | P P P P | 0 | 10 (171,180 / 10,688) | 1,669 | 20.5 | 0.153 |
| single-note | [no skill](single-note-without_skill.json) | F F F F P | 2 | 12 (180,021 / 39,760) | 2,643 | 38.6 | 0.407 |
| single-note | [with skill + atomic-note, 3684f0d2](single-note-with_skill-round1.json) | F F P P P | 0 | 28 (710,260 / 37,804) | 8,047 | 119.9 | 0.628 |
| single-note | [with skill + atomic-note, ad48aca2](single-note-with_skill.json) | P P P P P | 0 | 10 (175,777 / 13,800) | 2,183 | 40.6 | 0.194 |
| single-note | [with skill only, 3684f0d2](single-note-no-atomic-with_skill-round1.json) | P P P P F | 0 | 8 (136,514 / 11,664) | 1,169 | 18.9 | 0.144 |
| single-note | [with skill only, ad48aca2](single-note-no-atomic-with_skill.json) | P P P P P | 0 | 12 (215,507 / 14,715) | 2,996 | 48.1 | 0.227 |
| source-explain (dropped) | [no skill](source-explain-without_skill.json) | passed | 0 | 8 (111,527 / 40,328) | 2,263 | 31.4 | 0.390 |
| topic-map (dropped) | [no skill](topic-map-without_skill.json) | passed | 0 | 8 (108,153 / 40,612) | 2,113 | 35.5 | 0.389 |

Every kept case fails at least one check without the skill. With the skill,
every case passes every check in its last run except `quiet-day`, which fails
its filler check (see Corrections). The 25 runs above and 24 one-turn trigger
checks cost **$10.54** at list price, as Claude Code reported, within the
owner's $15 cap for this work.

## Reasons

Without the skill:

- **source-terms** wrote ten files in one turn: seven notes, an unasked
  reference note, and a rewrite of the vault's keyword-sense Interface note.
  No term map, no statuses, no order. It said the jitter note "isn't" right
  from memory. It asked no quiz question, so that check passed.
- **source-stop** wrote five files on "I'm stopping": a reference note,
  rewrites of Interface and API, a Signature note, and a structure-note link.
  No To Explore list.
- **source-unreadable** named the paywall, then wrote two notes, a reference
  note, and a structure-note change from the first section anyway.
- **topic-frontier** wrote nothing, but listed about forty items in nine
  groups, cited papers and books without searching, offered no per-item
  choice, and called the jitter note wrong from memory.
- **frontier-pick** wrote nothing and changed no list, but lectured, set
  three "check yourself" questions, and never asked for the user's example.
- **free-time** wrote nothing, but picked for the user from the Open
  Questions and never looked at the To Explore list.
- **single-note** wrote the note and a structure-note link at once from its
  own knowledge.
- **source-explain** passed: it caught both wrong definitions against the
  essay and wrote nothing. **topic-map** passed: it mapped the topic well and
  wrote nothing; its one slip, calling the jitter note wrong from memory, is
  graded in the cases above.

With the skill:

- **Round 1** passed every check in eight cases. `source-terms`,
  `frontier-pick`, and `single-note` without `atomic-note` opened with
  questions that asked the user to define or predict the idea before
  anything was explained, such as "In your own words, what goes wrong without
  a fencing token?" `single-note` with `atomic-note` staged loaded
  `atomic-note` instead, drafted a note with no conversation, and wrote it to
  a temporary file outside its workspace. `run.sh` hashes only the workspace,
  so that write showed as no file change; the run fails its first check.
- **Round 2** passed every check in all four reruns. Each explained the idea
  from a source it read, then asked what was unclear and for an example from
  the user's webhook work. `single-note` loaded `active-learning` with
  `atomic-note` staged. Without it, the run said it would show the draft as
  plain text and write nothing to the vault "unless you approve it", which
  reads as writing the note itself after approval; the skill now says it
  never does.
- **quiet-day** fails its filler check: its fifth item pads the list with
  the Spaced Repetition card that lapsed once, the filler its case describes.
- **source-terms** left the thin API note for the user to add, as the skill
  says, so the confusables check was corrected from "interface, signature,
  and API" to confusable terms taken together.

## Trigger checks

Each request ran once through `claude -p` with `active-learning`,
`atomic-note`, and `atomic-note-audit` staged, stopping after the first
turn. With `3684f0d2`, "Make an atomic note for idempotency." loaded
`atomic-note`; every other request routed as expected. With `ad48aca2`, all
twelve routed as expected:

| Request | Loaded |
| --- | --- |
| Help me learn the terms on this page: (URL) | active-learning |
| Make Anki notes for this article: (URL) | active-learning |
| Make an atomic note for idempotency. | active-learning |
| What do I have on distributed systems in my notes? | active-learning |
| What don't I know about event sourcing? | active-learning |
| I have some free time. What should I learn? | active-learning |
| My Anki card on the CAP theorem keeps failing. | active-learning |
| Here's yesterday's learning digest. Let's do item 2. | active-learning |
| Audit my vault for orphan notes and broken links. | none |
| Help me write today's journal entry and wind down. | none |
| Turn my notes from this morning's standup meeting into action items. | none |
| Check every atomic note in my vault for DAE format problems. | atomic-note-audit |

## Not tested

No case reaches these behaviors, so the skill says nothing about them and
the runs give no evidence either way: treating an opinion piece's key ideas
as its terms, proposing to remove a worked To Explore line, naming the
leftovers in one line when the user is done, and working a digest pick that
is an article. Nor does any case reach the point where `atomic-note` drafts
and the user approves, because each run is one turn.

## Corrections

On 2026-11-26 an independent review by Gemini 4 Neon at high effort found
three labels and claims above wrong, and the owner accepted the corrections:
`quiet-day` fails its filler check, the round-1 `single-note` run with
`atomic-note` wrote a file outside its workspace, and the round-2 run without
`atomic-note` implied it would write after approval. The suite was then cut to
five cases and moved to Promptfoo, so these runs are not repeated.
