# Reviewing PRs Eval Record · 2026-11-25, post only

Each of the three Eval Cases, once with `reviewing-prs`, in Claude, after the
skill stopped merging and the PR review feedback was addressed. The skill now
posts the operator's Verdict and leaves acting on it to the session that owns
the pull request. It also covers collaborator repositories and review
requests, adds a `not applicable` Verdict, uses a merged window the operator
names or else the last 7 days, and leaves drafts out. The Baseline is the
previous version of the skill.

- **Host and date** macOS (arm64), 2026-11-25 PST. Claude Code subscription
  sign-in.
- **Skill revision** `skills/reviewing-prs` at commit `4f0a8a92`, staged as a
  copy in each run directory.
- **Cases** all three in [the case set](../../README.md#cases). The case-set
  SHA-256 was
  `3d813afffd2be671f444c767f36768e00afec24a772a13c4a123e59067bd1ff9`.
- **Baseline** the [2026-11-25 simplify-pass record](../2026-11-25-simplify-pass/README.md),
  which ran `reviewing-prs` at `dc81d24e`. The
  [2026-11-24 record](../2026-11-24-review-page/README.md) holds the last
  no-skill Baseline.
- **Model and effort** `claude-opus-5-5` at high effort, as recorded in every
  assistant message of the transcripts, the same as the Baseline.
- **Runner** Anthropic's `skill-creator` loop inside one Claude Code 2.1.331
  session: each run was a subagent started with the Agent tool.
- **Repeats and completion** one run per case. All three finished. The
  `owner-routing-and-scrubbing` run received turns 2 and 3 of its
  `turns.json`.

## What changed in the cases

The case set changed with the skill, so the Baseline's counts are not a
like-for-like comparison.

- `owner-routing-and-scrubbing` no longer expects a merge. Four graders were
  rewritten: nothing merges and no label changes, `#421` goes to its owner
  session, `#136` goes to the operator because its owner lines conflict, and
  `#423` and `#134` go to the operator. The label-swap grader and the fourth
  turn, which only asked about a direct merge, were removed. Grader 03 now
  requires a Verdict comment on each decided pull request.
- `conflicts-impact-digest-html` names its merged window's start in the prompt,
  November 13, so the case does not depend on today's date. `#416`, which
  merged inside that window with no label and no Verdict, moved from decoy to
  merged without the operator.

## Results

Checks are the statements in each case's `graders/`. Each transcript file's
`labels` holds every label with its reason, and `unmeasured` holds the checks
a run could not exercise.

| Case | Transcript | Checks passed | Baseline (`dc81d24e`) | GitHub writes | Output tokens | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/README.md) | [Claude with skill](owner-routing-and-scrubbing-claude-skill.json) | 6/6, 3 unmeasured | 4/4, 5 unmeasured | 0 | 22,223 | 234 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/README.md) | [Claude with skill](conflicts-impact-digest-html-claude-skill.json) | 8/8 | 8/8 | 0 | 20,464 | 198 |
| [risk-overview-and-situations](../../cases/risk-overview-and-situations/README.md) | [Claude with skill](risk-overview-and-situations-claude-skill.json) | 4/4 | 4/4 | 0 | 14,765 | 142 |

The three runs used 315,333 cache-write tokens, 6,137,354 cache-read tokens,
and 57,452 output tokens over 574 seconds. Seconds and the reported totals
are each run's last turn, because the runner's figures are cumulative across
turns. Cost is unknown: the runs used a subscription sign-in and the runner
reported no price.

## What the run shows

- **Nothing regressed.** Every check that passed with the previous version
  passed again.
- **The skill says who acts next instead of merging.** In
  `owner-routing-and-scrubbing` it named repo-captain for `acme/ledger-app#421`
  and the operator for `#423`, `#134`, and `#136`, and planned no merge or
  label change.
- **Discovery reports its new reach.** Each run searched collaborator
  repositories and review requests, found none in these fixtures, and said
  so. The digest run stated the operator's window, "Since 2026-11-13, as you
  asked", listed `#416` with `#417`, `#418`, `#420`, and `acme/handbook#7` as
  merged without the operator, and kept out `#411` and `#390`.
- **The write path is prepared but still not exercised.** The owner-routing
  run wrote four Verdict comments to its private round directory, each three
  lines with the reviewed 40-character head, and scrubbed the #136 note. It
  posted none of them, for the reason below.

## Limits of this run

- **Three checks are unmeasured in `owner-routing-and-scrubbing`.** The runner
  delivers turns 2 and 3 as messages from the coordinating session. The skill
  counts a Verdict and a confirmation only when the operator gives them
  directly, so the agent stopped at the echo both times. Posting and the
  review-versus-comment form were not exercised.
- **The runs could tell the setup was an evaluation.** The stand-in's refusal
  messages and environment variable names name the stand-in, and the
  session's agent list still named earlier runs `eval-r1` to `eval-r3`.
- **One run per case, and no new no-skill arm.** There is no variance
  figure.
- **Isolation was by convention.** Each run reached the stand-in by sourcing
  an environment file before every shell command, with no GitHub token in
  that environment, and was told not to read outside its run folder.
- **The request carried the Baseline's launcher text** after the case's
  prompt: where the environment file was, to work only through `gh`, not to
  start subagents, to read the staged skill, and where to save the reply.
- **The page opener was a logging stub**, so no run opened a browser.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, host paths, and
the invented home-directory path from turn 2 are replaced with placeholders.
Internal reasoning and session context stayed in the private run directory.
