# Reviewing PRs Skill Eval

Each synthetic Eval Case runs against a fresh no-skill Baseline and against
the same revision of `reviewing-prs` in Claude and in Codex. Every arm talks
to the same synthetic GitHub: invented repositories (`acme/ledger-app`,
`acme/cli-kit`, `acme/handbook`), an invented operator, and invented pull requests. No arm has
real GitHub credentials.

## Cases

The set is three cases, kept small on purpose. Add a case when a failure
returns after its fix, as [SKILLS.md](../../SKILLS.md#improving-from-real-use)
describes.

| Case | What it keeps | Fixture |
| --- | --- | --- |
| [owner-routing-and-scrubbing](cases/owner-routing-and-scrubbing/case.yaml) | Without the skill, an agent merges pull requests straight from the Verdicts, including one another session owns and one with conflicting owner lines, and posts no three-line Verdict | `fixtures/owner-routing-and-scrubbing` |
| [conflicts-impact-digest-html](cases/conflicts-impact-digest-html/case.yaml) | Without the skill, an agent builds no review page, and nothing finds an unlabeled merge or one made against a request-changes Verdict | `fixtures/conflicts-impact-digest-html` |
| [risk-overview-and-situations](cases/risk-overview-and-situations/case.yaml) | No observed failure yet. Checks that the page splits the round at the hold line, shows an undescribed change as a situation with its code, and says where each value came from | `fixtures/risk-overview-and-situations` |

Three earlier cases were removed on 2026-11-24: a mislabeled new view, hidden
stored names, and a description claiming work the diff lacked. A no-skill
agent caught each of them, so they measured the model more than the skill. Git
history keeps them. `design-system-departures` was removed the same day because
both arms passed every check.

Each case folder follows the `skill-creator` layout: `prompt.md` is the
operator's request, `case.yaml` describes a good result and names the failure
it came from, and each file in `graders/` is one statement to judge.
`owner-routing-and-scrubbing` has three operator turns and one conditional
reply, listed in its `turns.json`. Its `prompt.md` is the first turn, so a single-turn runner only
reaches the review page. Fixture dates are fixed around 2026-11-20. The
digest case's merged window comes from the last Verdict comment in its
fixture, so no prompt names a date.

The three-case set SHA-256 is
`ccb2a2e45eb9118a5531737ddfb36c072e990d4b1e992aa476c8d7e32ae930fa`. From this
directory, reproduce it with:

```sh
find cases fixtures stand-ins -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

[`trigger-queries.json`](trigger-queries.json) holds requests that should
load the skill and near misses that belong to another workflow, for tuning
the description. It is outside the case set and its hash.

## The GitHub stand-in

The skill fetches its own data, so the cases substitute what it talks to
instead of handing it files.
[`stand-ins/gh`](stand-ins/gh) sits first on `PATH` and answers the GitHub CLI
commands a Review Round uses from one fixture's `world.json`. It never
contacts GitHub. It applies the round's few writes (comment, label, merge) to
a private state copy and appends every call to `trace.jsonl`. It refuses
anything else with exit 3, so a call outside it gets exit 3 and a `refused` entry in the trace. It enforces what
GitHub would: a merge with `--match-head-commit` fails when the SHA is not the
head, a label must exist before it is added, and nobody approves their own
pull request. No fixture has a merge queue. Calls may run in parallel. Its
answers look like GitHub's, but its refusals and its environment variable
names say it is a stand-in, so a run can tell it is not GitHub.

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
cp -R skills/reviewing-prs "$run/skill"            # skill arms only
export GH_STANDIN_WORLD="$run/world.json" GH_STANDIN_STATE="$run/state"
export GH_CONFIG_DIR="$run/gh-config" GH_TOKEN="" GITHUB_TOKEN=""
export PATH="$run/bin:<python3, jq, and only what the harness itself needs>"
cd "$run/workspace"
```

Give a skill arm the copy in `$run/skill`, never the repository checkout: the
checkout puts these cases and their graders within the agent's reach.

Before grading a run, confirm four things:

1. **Only the synthetic GitHub was reachable.** `PATH` holds no real `gh` and
   no `orca`, the token variables are empty, and the harness exposes no GitHub
   connector or MCP server. A stand-in first on `PATH` shows intent, not
   isolation. If the launcher cannot show this, record the run as not run.
2. **The skill under test loaded.** For a skill arm, the transcript shows the
   staged copy of `SKILL.md` being read, not a same-name copy installed on
   the host.
3. **Nothing the run can read holds the answers.** Keep the case's
   `case.yaml`, `graders/`, and any grading notes out of the run directory
   and out of the folder the agent saves its reply to.
4. **The fixture is staged under a neutral name**, as above, so a path does
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
- that the page has the Content Security Policy, mode `0600`, no
  `innerHTML`, and no literal `<` inside its data block

Judge the rest by reading the response, the page, and the transcript against
the case's `graders/`. Add check scripts only after a recorded run shows the
shapes they must parse.

## Eval Records

- [Review page, 2026-11-24](records/2026-11-24-review-page/README.md): each
  case once with the skill and once without, in Claude.

Commit each record under
`records/<date>-<slug>/` with the fields
[SKILLS.md](../../SKILLS.md#eval-records) lists, and keep raw runner output,
credentials, and generated review pages outside the repository.

A runner that sends later turns through another agent session cannot measure
the write phase of `owner-routing-and-scrubbing` with the skill: the skill
refuses a Verdict or confirmation the operator did not give directly. Use a
runner whose later turns are real user turns.
