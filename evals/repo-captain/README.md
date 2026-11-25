# Repo Captain Skill Eval

Each synthetic Eval Case runs against the `coordinating-work` Baseline and
against the same revision of `repo-captain`, in Claude and in Codex. Every arm
talks to the same synthetic GitHub, Orca, and git: one invented repository
(`acme/ledger-app`), an invented operator (`dana-acme`), and invented issues,
pull requests, and workers. No arm has real GitHub or Orca access.

## Cases

One case covers each behavior group the skill must show. Add a case when a
failure returns after its fix, as
[SKILLS.md](../../SKILLS.md#improving-from-real-use) describes.

| Case | What it keeps | Turns |
| --- | --- | --- |
| [coupled-plan-versus-uniform-backlog](cases/coupled-plan-versus-uniform-backlog/case.yaml) | A lead spun up a worktree for an issue already fixed on main. Checks that coupled issues are planned together and independent ones go to `lfg` | 1 |
| [overlap-and-one-migration](cases/overlap-and-one-migration/case.yaml) | Two batches had to keep overlapping files and two migrations apart by hand. Checks overlap serialization and one migration in the merge queue at a time | 2 |
| [direction-change-restarts-executor](cases/direction-change-restarts-executor/case.yaml) | No observed failure yet. Checks that an Executor building a dropped direction is stopped and restarted | 1 |
| [hold-gate-raises-scores](cases/hold-gate-raises-scores/case.yaml) | The held list omitted CI workflows, and migration issues kept an undo cost of 1. Checks the hold tests and upward-only score edits | 1 |
| [rebase-revert-and-merge-queue](cases/rebase-revert-and-merge-queue/case.yaml) | No observed failure yet. Checks that a rebase quietly reverting main goes back to the operator, and that a queued merge waits for `MERGED` | 4 |
| [domain-lead-custody-and-self-merge](cases/domain-lead-custody-and-self-merge/case.yaml) | Two batches had to keep overlapping files apart by hand. Checks that the Captain merges what a Domain Lead hands up, holds its own pull request, and retires only a finished Lead | 1 |
| [held-pr-keeps-wake-and-calm-alert](cases/held-pr-keeps-wake-and-calm-alert/case.yaml) | Fixed-interval check-ins filled the chat with noise. Checks one contained alert after red default-branch CI and a wake check that stays on for held pull requests | 3 |
| [restart-split-brain-and-boundaries](cases/restart-split-brain-and-boundaries/case.yaml) | Reviving a lead risked two live sessions writing at once. Checks the stand-down, the takeover wake, a forged Verdict, and human-only actions | 3 |

Each case folder follows the `skill-creator` layout: `prompt.md` is the
operator's first message, `case.yaml` describes a good result and names the
failure it came from, and each file in `graders/` is one statement to judge.
A case with more than one turn lists every operator message in `turns.json`.
The world changes between some turns, as the fixture's `turns` entries say:
a head moves, a Verdict lands, CI finishes, a session ends.

Each fixture folder holds `world.json`, which both stand-ins read and which
also describes the git history to build, and, when the Captain is already
running, a `captain-state/` folder with its charter and state files. The
Baseline arm does not know that folder, so the cases that use it say what a
newcomer would have to rebuild. Fixture dates are fixed around 2026-11-20, so
no case depends on today's date.

The eight-case set SHA-256 is
`06d21464a6eca2f92d3f033c812b3cb110c7e0ce26a60cec2a91120a250fe2bd`. It
covers the shared GitHub stand-in too. From this directory, reproduce it
with:

```sh
find cases fixtures stand-ins ../reviewing-prs/stand-ins -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

[`trigger-queries.json`](trigger-queries.json) holds requests that should
load the skill and near misses that belong to another workflow, for tuning
the description. It is outside the case set and its hash.

## The stand-ins

The skill fetches its own data and dispatches its own workers, so the cases
substitute what it talks to instead of handing it files.

- **GitHub.** The [reviewing-prs `gh` stand-in](../reviewing-prs/README.md#the-github-stand-in)
  answers from the staged world. For these cases it also runs a merge queue
  (a queued pull request merges or is ejected at the next turn, as the world
  lists), serves check runs on merge commits, creates a pull request from a
  branch pushed to the staged remote, edits and closes issues, and reads and writes the
  four score fields the way `managing-issues` does on GitHub.
- **Orca.** [`stand-ins/orca`](stand-ins/orca) answers the Orca commands the
  skill names from the world's `orca` section: workers and their liveness,
  sessions, paired hosts, worktrees, and messages. Its command shapes are
  invented for the eval, and `orca skills get orchestration` serves a short
  guide that describes them. It refuses to release a worker that has not
  sent `worker_done`, refuses to retry a `circuit_broken` dispatch, and
  refuses anything outside its contract with exit 3 and a `refused` trace
  entry.
- **git.** Staging builds each case's history for real in a bare repository
  that plays GitHub's copy, so `git merge-base` and `git range-diff` run on
  real commits, and it writes their SHAs into the world so `gh` and git
  agree. GitHub serves any commit by SHA, so the remote does too. The remote
  accepts only new branches, such as a revert branch, because the world file
  says where an existing pull request's head is. A merge the `gh` stand-in
  performs is not written back to git.

[`tests/repo-captain`](../../tests/repo-captain/README.md) checks both
stand-ins, staging, and every fixture in the repository gate, without a model.

## Stage a run

Live runs call a model. They need the operator's approval first and never run
in `lefthook run pre-push --force`.

```sh
run=$(mktemp -d)/run                               # outside every repository
python3 evals/repo-captain/fixtures/stage.py <case> "$run"
cp -R skills/repo-captain "$run/skill"             # skill arms only
for name in $(env | sed -n 's/^\(ORCA_[A-Z_]*\)=.*/\1/p'); do unset "$name"; done
export GH_STANDIN_WORLD="$run/world.json" GH_STANDIN_STATE="$run/gh-state"
export ORCA_STANDIN_WORLD="$run/world.json" ORCA_STANDIN_STATE="$run/orca-state"
export ORCA_CLI_COMMAND="$run/bin/orca" XDG_STATE_HOME="$run/xdg-state"
mkdir "$run/gh-config"
export GH_CONFIG_DIR="$run/gh-config" GH_TOKEN="" GITHUB_TOKEN=""
export PATH="$run/bin:<python3, jq, git, and only what the harness itself needs>"
cd "$run/workspace"
```

Before sending turn N of a multi-turn case, move the world:

```sh
python3 evals/repo-captain/fixtures/stage.py turn "$run" N
```

That writes the turn for both stand-ins and moves the staged remote's branches
to the heads that turn lists. Send each turn as a real user turn in the same
session.

Give a skill arm the copy in `$run/skill`, never the repository checkout: the
checkout puts these cases and their graders within the agent's reach. Give the
Baseline arm `skills/coordinating-work` the same way.

Before grading a run, confirm four things:

1. **Only the synthetic GitHub and Orca were reachable.** `PATH` holds no real
   `gh` or `orca`, no other `ORCA_` variable survives, the token variables are
   empty, and the harness exposes no GitHub connector or MCP server. A
   stand-in first on `PATH` shows intent, not isolation. If the launcher
   cannot show this, record the run as not run.
2. **The skill under test loaded.** For a skill arm, the transcript shows the
   staged copy of `SKILL.md` being read, not a same-name copy installed on
   the host.
3. **Nothing the run can read holds the answers.** Keep the case's
   `case.yaml`, `graders/`, and any grading notes out of the run directory
   and out of the folder the agent saves its reply to.
4. **The fixture is staged under a neutral name**, as above, so a path does
   not tell the agent what the case is looking for.

## Read the results

`gh-state/trace.jsonl` and `orca-state/trace.jsonl` settle what ran: each
line is one call with its arguments and a kind of `read`, `write`, `refused`,
or `error`, or a `world` entry where the world moved to a later turn. The
Captain's charter and state files are in `xdg-state/ledger-app-captain/`.
Code can decide from the traces whether a merge was pinned to a given head,
what was enqueued in which turn, which workers were started, stopped, or
released, and whether any write was refused. Judge the rest by reading the
response and the transcript against the case's `graders/`.

## Eval Records

None yet. Commit each record under `records/<date>-<slug>/` with the fields
[SKILLS.md](../../SKILLS.md#eval-records) lists, and keep raw runner output,
credentials, and staged run directories outside the repository.
