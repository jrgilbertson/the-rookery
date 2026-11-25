# Reviewing PRs Skill Eval

Each synthetic Eval Case runs against a fresh no-skill Baseline and against
the same revision of `reviewing-prs` in Claude and in Codex. Every arm talks
to the same synthetic GitHub: invented repositories (`acme/ledger-app`,
`acme/cli-kit`), an invented operator, and invented pull requests. No arm has
real GitHub credentials.

## Cases

Three no-skill Baseline runs against real repositories, made before the skill
was written, handled discovery, leverage ordering, and file conflicts. They
failed in six ways. Those runs read private repositories and are not
published. Each case rebuilds one or two of the failures with invented data.

| Case | Baseline failure it rebuilds | Fixture |
| --- | --- | --- |
| [new-view-missing-screenshot](cases/new-view-missing-screenshot/case.yaml) | 1. Scored a new customer-facing page at verification effort 2. 3. Did not say screenshots were missing | `fixtures/new-view-missing-screenshot` |
| [hidden-stored-names](cases/hidden-stored-names/case.yaml) | 2. Did not call out new stored and published names | `fixtures/hidden-stored-names` |
| [wide-refactor-phantom-change](cases/wide-refactor-phantom-change/case.yaml) | 4. Wrote the riskiest cards from descriptions without reading the diffs | `fixtures/wide-refactor-phantom-change` |
| [owner-routing-and-scrubbing](cases/owner-routing-and-scrubbing/case.yaml) | 5. Verdict lines in a different format each run. 6. Ignored who owned a pull request when merging | `fixtures/owner-routing-and-scrubbing` |
| [conflicts-impact-digest-html](cases/conflicts-impact-digest-html/case.yaml) | 6, second half: what merged without the operator. Also the review page's hardening | `fixtures/conflicts-impact-digest-html` |

Each case folder follows the `skill-creator` layout: `prompt.md` is the
operator's request, `case.yaml` describes a good result and names the failure
it came from, and each file in `graders/` is one statement to judge.
`owner-routing-and-scrubbing` has three operator turns, listed in its
`turns.json`. Its `prompt.md` is the first turn, so a single-turn runner only
reaches the review page.

The five-case set SHA-256 is
`11d05f1f0744bccbc4094df9f634bd9641ebec4de7b5fdd181aa46693a31a653`. From this
directory, reproduce it with:

```sh
find cases fixtures stand-ins -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

## The GitHub stand-in

The skill fetches its own data, so the cases substitute what it talks to
instead of handing it files.
[`stand-ins/gh`](stand-ins/gh) sits first on `PATH` and answers the GitHub CLI
commands a Review Round uses from one fixture's `world.json`. It never
contacts GitHub. It applies the round's few writes (comment, label, merge) to
a private state copy and appends every call to `trace.jsonl`. It refuses
anything else with exit 3, so a run that strays fails loudly. It enforces what
GitHub would: a merge with `--match-head-commit` fails when the SHA is not the
head, a label must exist before it is added, and nobody approves their own
pull request. No fixture has a merge queue.

[`tests/reviewing-prs`](../../tests/reviewing-prs/README.md) checks the
stand-in and every fixture in the repository gate, without a model.

## Stage a run

Live runs call a model. They need the operator's approval first and never run
in `lefthook run pre-push --force`.

```sh
run=$(mktemp -d)                                   # outside every repository
mkdir "$run/bin" "$run/state" "$run/workspace" "$run/gh-config"
cp evals/reviewing-prs/stand-ins/gh "$run/bin/gh"
cp evals/reviewing-prs/fixtures/<case>/world.json "$run/world.json"
export GH_STANDIN_WORLD="$run/world.json" GH_STANDIN_STATE="$run/state"
export GH_CONFIG_DIR="$run/gh-config" GH_TOKEN="" GITHUB_TOKEN=""
export PATH="$run/bin:<only what the harness itself needs>"
cd "$run/workspace"
```

Before grading a run, confirm three things:

1. **Only the synthetic GitHub was reachable.** `PATH` holds no real `gh` and
   no `orca`, the token variables are empty, and the harness exposes no GitHub
   connector or MCP server. A stand-in first on `PATH` shows intent, not
   isolation. If the launcher cannot show this, record the run as not run.
2. **The skill under test loaded.** For a skill arm, the transcript shows the
   candidate `skills/reviewing-prs/SKILL.md` being read, not a same-name copy
   installed on the host.
3. **The fixture is staged under a neutral name**, as above, so a path does
   not tell the agent what the case is looking for.

For `owner-routing-and-scrubbing`, replace `<<LOCAL_PATH>>` in turn 2 with an
invented home-directory path when you send it. Tracked files cannot hold one,
because the repository text check rejects them. Replace it with a placeholder
again in the saved transcript.

## Read the results

`trace.jsonl` in the state directory settles what ran: each line is one call
with its arguments and a kind of `read`, `write`, `refused`, or `error`. Code
can decide these from the trace and the page file:

- whether any write happened, and before or after the operator confirmed
- that a merge carried `--match-head-commit` with the full head SHA
- that a Verdict comment is exactly three lines and holds no scrubbed text
- that the page has the Content Security Policy, mode `0600`, and no
  `innerHTML`

Judge the rest by reading the response, the page, and the transcript against
the case's `graders/`. Add check scripts only after a recorded run shows the
shapes they must parse.

## Eval Records

No Eval Record is committed yet. The Baseline-against-skill runs and the Codex
run are paid model runs that wait for the operator's approval. When they run,
commit each record under `records/<date>-<slug>/` with the fields
[SKILLS.md](../../SKILLS.md#eval-records) lists, drop any case that passes on
the Baseline without the skill, and keep raw runner output, credentials, and
generated review pages outside the repository.
