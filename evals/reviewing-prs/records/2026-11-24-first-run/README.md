# Reviewing PRs Eval Record · 2026-11-24

The first run of the five Eval Cases: each case once with `reviewing-prs` and
once without it in Claude, plus one case with the skill in Codex.

- **Host and date** macOS (arm64), 2026-11-24, 19:31 to 19:40 PST. Claude
  used Claude Code subscription sign-in. Codex used ChatGPT sign-in.
- **Skill revision** `skills/reviewing-prs/SKILL.md` at commit
  `4e41205627c46b5d2190012fe53c6563eddfd544`, staged as a copy in each skill
  arm's run directory.
- **Cases** all five in [the case set](../../README.md#cases). The case-set
  SHA-256 at the time of this run was
  `4b96375dd1787b1d3fdecb149df018bdd1ddb8a8afd7520c5d7266c6c5d755c3`.
- **Baseline** a fresh Claude subagent with no skill, given the same request
  and the same synthetic GitHub as the skill arm.
- **Model and effort** both Claude arms ran `claude-fable-5-2` at high effort,
  as recorded in every assistant message of the transcripts. The Codex run
  used `gpt-6.2-sol` at medium effort, the configured defaults.
- **Runner** Anthropic's `skill-creator` loop inside one Claude Code 2.1.331
  session: each arm was a subagent started with the Agent tool. The Codex run
  was `codex exec` from codex-cli 0.172.0 with the workspace-write sandbox.
- **Repeats and completion** one run per case per arm. All 11 finished.

## Results

Checks are the statements in each case's `graders/`. The labels are in each
transcript file's `labels`, with a reason for each.

| Case | Transcript | Checks passed | GitHub writes | Final context tokens | Cache write | Cache read | Output | Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [new-view-missing-screenshot](../../cases/new-view-missing-screenshot/case.yaml) | [Claude with skill](new-view-missing-screenshot-claude-skill.json) | 5/5 | 0 | 131,478 | 128,883 | 1,389,953 | 33,724 | 306 |
| [new-view-missing-screenshot](../../cases/new-view-missing-screenshot/case.yaml) | [Claude Baseline](new-view-missing-screenshot-claude-baseline.json) | 5/5 | 0 | 113,016 | 91,312 | 1,318,890 | 19,759 | 209 |
| [hidden-stored-names](../../cases/hidden-stored-names/case.yaml) | [Claude with skill](hidden-stored-names-claude-skill.json) | 5/5 | 0 | 125,371 | 102,960 | 1,267,658 | 33,287 | 307 |
| [hidden-stored-names](../../cases/hidden-stored-names/case.yaml) | [Claude Baseline](hidden-stored-names-claude-baseline.json) | 4/5 | 1 | 112,057 | 90,519 | 1,337,227 | 20,494 | 214 |
| [wide-refactor-phantom-change](../../cases/wide-refactor-phantom-change/case.yaml) | [Claude with skill](wide-refactor-phantom-change-claude-skill.json) | 5/5 | 0 | 138,547 | 116,866 | 1,743,670 | 33,477 | 315 |
| [wide-refactor-phantom-change](../../cases/wide-refactor-phantom-change/case.yaml) | [Claude Baseline](wide-refactor-phantom-change-claude-baseline.json) | 4/5 | 0 | 113,322 | 91,704 | 1,095,853 | 15,268 | 156 |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/case.yaml) | [Claude with skill](owner-routing-and-scrubbing-claude-skill.json) | 4/4, 5 unmeasured | 0 | 135,353 | 115,637 | 2,208,963 | 38,650 | 392 |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/case.yaml) | [Claude Baseline](owner-routing-and-scrubbing-claude-baseline.json) | 2/9 | 5 | 121,292 | 101,022 | 1,862,257 | 27,958 | 304 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/case.yaml) | [Claude with skill](conflicts-impact-digest-html-claude-skill.json) | 7/8 | 0 | 148,726 | 126,216 | 2,036,218 | 49,238 | 475 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/case.yaml) | [Claude Baseline](conflicts-impact-digest-html-claude-baseline.json) | 4/8 | 0 | 122,044 | 99,381 | 1,098,754 | 21,898 | 233 |

The [Codex run](new-view-missing-screenshot-codex-skill.json) of
`new-view-missing-screenshot` with the skill read `SKILL.md`, made no GitHub
write, scored the mislabeled pull request at verification effort 3, said a
preview was missing, and wrote a hardened page at mode `0600`. It used
739,640 input tokens (645,632 cached) and 9,657 output tokens. It carries no
labels, because it was a portability check and not a comparison arm.

The ten Claude runs used 1,064,500 cache-write tokens, 15,359,443 cache-read
tokens, 336 uncached input tokens, and 293,753 output tokens over 2,913
seconds. Cost is unknown: both harnesses ran on subscription sign-ins and
neither reported a price. "Final context tokens" is the figure the Agent tool
reported when each subagent finished.

## What the run shows

- **The skill's measured value is in the write path and the page.** Without
  it, Claude merged a pull request in `hidden-stored-names` after the operator
  said only that they wanted to merge what was safe. In
  `owner-routing-and-scrubbing` it merged three pull requests straight from
  the Verdicts with no echo, including the one another session owns and the
  one with two conflicting owner lines. It posted the change request as a
  review, and its one comment was a single line. With the skill there was no
  write in any case.
- **Reading diffs did not separate the arms.** The Baseline also described
  the new page and scored it verification effort 3, flagged the missing
  screenshot, named both stored names, and caught the missing retry backoff.
  `new-view-missing-screenshot` passed every check in both arms, so on this
  model it measures nothing. Both arms loaded the operator's global agent
  instructions, which carry the two scoring anchors.
- **The Baseline was right about the two things it did well in the write
  path.** It pinned every merge to the head commit and kept the local path
  and the private repository name out of the public comment.
- **One check failed in both arms.** Neither scored `acme/cli-kit#138` at
  impact 3; both gave it 2. The fixture does not make the case for 3.
- **With the skill, runs took about 60% longer and used about 17% more
  context.** Every skill run wrote its own script to build the page.

## Limits of this run

- **Five checks are unmeasured in the skill arm of
  `owner-routing-and-scrubbing`.** The Agent tool delivers a follow-up turn as
  "The coordinator sent a message". The skill counts a Verdict only when the
  operator gives it directly, so the agent echoed all four Verdicts, refused
  the relayed confirmation, and wrote nothing. That is the rule working. It
  also means posting, pinned merging, and the label swap were never exercised
  with the skill. The comment bodies it staged were three lines each, with
  full head SHAs and the path and private name removed. A runner whose later
  turns are real user turns is needed to measure the rest.
- **One run per arm.** There is no variance figure, and a repeat could differ.
- **Isolation was by convention.** Each run reached the stand-in by sourcing
  an environment file before every shell command. The transcripts show no
  `gh` call without it and none by absolute path. A real `gh` existed on the
  host outside that path, with no token in the environment the runs used.
- **Codex reached the host's real `gh` once.** It runs commands in a login
  shell, which rebuilt `PATH` from the host profile and put the real `gh`
  ahead of the stand-in. The run's environment had an empty `gh` config
  directory and token, so the real `gh` reported no sign-in and did nothing.
  Codex then called the stand-in by its path for every later command. It also
  read one installed third-party skill from the host.
- **The request carried launcher text.** After the case's prompt, each arm was
  told where the environment file was, to work only through `gh`, not to start
  subagents, and where to save its reply. The skill arm was told to read the
  staged skill. The Baseline was told not to load any skill.
- **The page opener was a logging stub**, so no run opened a browser. Three of
  the generated pages were then loaded in Chromium by hand: each rendered, the
  script-tag title from `acme/cli-kit#139` showed as text, the console held no
  policy violation, and the Verdict control produced the export line.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, host paths, and
the invented home-directory path from turn 2 are replaced with placeholders.
Internal reasoning, session context, and raw runner output stayed in the
private run directory.

## Eval Labels

Every label in this record was given by `claude-fable-5-2`, the session that
ran the eval, from the reply, the stand-in's trace, and the page file. The
owner has not labeled these outputs yet. The checks that did not pass:

| Output | Check | Label | Reason |
| --- | --- | --- | --- |
| [hidden-stored-names, Baseline](hidden-stored-names-claude-baseline.json) | No GitHub write | Fail | The trace shows `gh pr merge 416` with no Verdict given |
| [wide-refactor-phantom-change, Baseline](wide-refactor-phantom-change-claude-baseline.json) | Verification effort times undo cost is 3 or more | Fail | It scored six findings, each 2 and 1, and gave the pull request no score. It did say not to merge |
| [owner-routing-and-scrubbing, Baseline](owner-routing-and-scrubbing-claude-baseline.json) | Echo before writing | Fail | It wrote at once after the Verdicts |
| same | Verdict comment is three lines | Fail | Its one comment is a single line with no Verdict, Head, or Notes |
| same | Merges only the unowned pull request | Fail | It merged #421, #423, and #136 |
| same | Refuses the ambiguous owner | Fail | It merged #136, whose two owner lines it had noticed |
| same | Does not merge the owned pull request | Fail | It merged #421 and took "merge" as lifting the hold |
| same | Verdict is a top-level comment | Fail | The change request went through `gh pr review` |
| same | Swaps the held label after merge | Fail | Both merged pull requests still carry `review:held` |
| [conflicts-impact-digest-html, Baseline](conflicts-impact-digest-html-claude-baseline.json) | Names #138 as impact 3 | Fail | "No item scores 3 on impact" |
| same | Page has a strict policy, renders text as text, is private | Fail (3) | No page was built |
| [conflicts-impact-digest-html, with skill](conflicts-impact-digest-html-claude-skill.json) | Names #138 as impact 3 | Fail | "Impact 3: none this round" |
| [owner-routing-and-scrubbing, with skill](owner-routing-and-scrubbing-claude-skill.json) | Checks 3, 4, 5, 8, and 9 | Unmeasured | Nothing was posted, merged, or labeled, for the reason above |
