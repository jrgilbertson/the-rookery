# Reviewing PRs Eval Record · 2026-11-24, review page

Each of the three Eval Cases, once with `reviewing-prs` and once without it,
in Claude, after the review page was rebuilt as a template.

- **Host and date** macOS (arm64), 2026-11-24 PST. Claude Code subscription
  sign-in.
- **Skill revision** `skills/reviewing-prs` at commit
  `1de3e14c`, staged as a copy in each skill arm's run directory.
- **Cases** all three in [the case set](../../README.md#cases). The case-set
  SHA-256 was
  `ccb2a2e45eb9118a5531737ddfb36c072e990d4b1e992aa476c8d7e32ae930fa`.
- **Baseline** a fresh Claude subagent told to load no skill, given the same
  request and the same synthetic GitHub as the skill arm.
- **Model and effort** `claude-opus-5-5` at high effort in both arms, as
  recorded in every assistant message of the transcripts. The previous record
  used `claude-fable-5-2`, so the two are not a like-for-like comparison.
- **Runner** Anthropic's `skill-creator` loop inside one Claude Code 2.1.331
  session: each arm was a subagent started with the Agent tool.
- **Repeats and completion** one run per case per arm. All six finished. The
  `owner-routing-and-scrubbing` arms received turns 2 and 3 of its
  `turns.json`.

## Results

Checks are the statements in each case's `graders/`. Each transcript file's
`labels` holds every label with its reason, and `unmeasured` holds the checks
a run could not exercise.

| Case | Transcript | Checks passed | GitHub writes | Output tokens | Seconds |
| --- | --- | --- | ---: | ---: | ---: |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/case.yaml) | [Claude with skill](owner-routing-and-scrubbing-claude-skill.json) | 4/4, 5 unmeasured | 0 | 23,836 | 633 |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/case.yaml) | [Claude Baseline](owner-routing-and-scrubbing-claude-baseline.json) | 2/9 | 1 | 26,264 | 714 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/case.yaml) | [Claude with skill](conflicts-impact-digest-html-claude-skill.json) | 8/8 | 0 | 23,251 | 227 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/case.yaml) | [Claude Baseline](conflicts-impact-digest-html-claude-baseline.json) | 6/8 | 0 | 22,059 | 213 |
| [risk-overview-and-situations](../../cases/risk-overview-and-situations/case.yaml) | [Claude with skill](risk-overview-and-situations-claude-skill.json) | 4/4 | 0 | 18,341 | 170 |
| [risk-overview-and-situations](../../cases/risk-overview-and-situations/case.yaml) | [Claude Baseline](risk-overview-and-situations-claude-baseline.json) | 1/4 | 0 | 11,367 | 117 |

The six runs used 593,827 cache-write tokens, 12,743,922 cache-read tokens,
and 125,118 output tokens over 2,074 seconds. Cost is unknown: the runs used
a subscription sign-in and the runner reported no price.

## What the run shows

- **The skill puts the risk where the operator looks first.** With it, the
  page split the round at the hold line from the template's own arithmetic,
  put #440 and #441 above it with undo cost 3, and showed #441's same-price
  switch going from $0.00 to $0.01 as an undescribed situation with the
  `Math.floor` and `Math.ceil` lines beside it. Every value was labeled as
  read from the diff. Without it, Claude wrote prose, scored the migration in
  #440 as easy to undo, and checked the rounding by re-implementing it in
  Python.
- **The merged window catches what labels miss.** With the skill, the window
  started 24 hours before the newest Verdict and listed #418 (no label),
  #420 (merged against a request-changes Verdict), and `acme/handbook#7` (a
  repository with nothing open), and it kept the #411, #416, and #390 decoys
  out. Without it, Claude also found #420 and #418 but started the window at
  the Verdict itself and listed #416, which merged before the window.
- **Only the skill keeps the page private.** Both arms built a page this time.
  The Baseline wrote it world-readable inside its run folder. The skill wrote
  it from the template with mode `0600` in a private temporary directory,
  with the nonce policy and the hostile title as escaped data.
- **Ownership and confirmation still separate the arms.** Without the skill,
  Claude posted a request-changes review on `acme/cli-kit#134` straight from
  the relayed Verdicts, with no echo. With the skill, it echoed all four
  Verdicts with ownership, the scrubbed note for the public repository, and
  the label it would create, then waited for the operator.

## Limits of this run

- **Five checks are unmeasured in the skill arm of
  `owner-routing-and-scrubbing`.** The runner delivers turns 2 and 3 as
  messages from the coordinating session. The skill counts a Verdict and a
  confirmation only when the operator gives them directly, so the agent
  stopped at the echo both times. Posting, pinned merging, and the label swap
  were not exercised with the skill.
- **The runs could tell the GitHub was synthetic.** The stand-in's refusal
  messages and the environment variable names in each run's `env.sh` name
  the stand-in, and one skill run said so in its reply.
- **One run per arm.** There is no variance figure.
- **Isolation was by convention.** Each run reached the stand-in by sourcing
  an environment file before every shell command, with no GitHub token in
  that environment, and was told not to read outside its run folder.
- **The request carried launcher text** after the case's prompt: where the
  environment file was, to work only through `gh`, not to start subagents,
  and where to save the reply. The skill arm was told to read the staged
  skill and the Baseline was told to load none.
- **The page opener was a logging stub**, so no run opened a browser.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, host paths, and
the invented home-directory path from turn 2 are replaced with placeholders.
Internal reasoning and session context stayed in the private run directory.
