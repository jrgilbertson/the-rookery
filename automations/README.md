# Automations

These recurring Orca reviews are part of how I build with AI. Each file
contains a prompt, schedule, and prerequisites you can adapt to your own
repository.

| Automation | Purpose | Cadence | Timezone |
|---|---|---|---|
| [Sessions audit (local)](sessions-audit.md) | Review recent AI sessions on the local host | Daily at 03:00 | America/Los_Angeles |
| [Sessions audit (remote)](sessions-audit.md) | Review recent AI sessions on the remote host | Daily at 01:00 | America/Los_Angeles |
| [Analytics gap audit](analytics-gap-audit.md) | Find shipped user actions without analytics and events that never arrive, and file issues | Monday at 04:00 | America/Los_Angeles |
| [Test audit](test-audit.md) | Review tests, find protection gaps, and recommend improvements | Thursday at 21:00 | America/Los_Angeles |
| [Optimize CI](optimize-ci.md) | Review continuous integration | Saturday at 09:00 | America/Los_Angeles |
| [Weekly codebase design](weekly-codebase-design.md) | Review codebase design | Saturday at 04:00 | America/Los_Angeles |
| [Coding standards audit](coding-standards-audit.md) | Keep adopted coding guidance current and useful | Saturday at 07:00 | America/Los_Angeles |

All schedules use America/Los_Angeles. Choose a cadence and timezone that suit
your work.

## Set up a scheduled review

Create an automation in Orca and select the target repository and agent. Set
the schedule and paste the prompt from its file. Install any named skills and
give the agent access to the sources the review requires. For Sessions audit,
replace the reference to The Rookery with your own repository.

Sessions audit invokes `retro` on each host separately. Install its required
skills on both hosts before scheduling both jobs.

Some prompts invoke an existing skill; others describe the review directly.
Orca runs the prompt on a schedule; an invoked skill tells the agent how to do
the work. Copy the definitions into Orca manually. To change an existing job,
edit it in Orca too.

Keep local paths, repository selections, account identifiers, and enabled
status in Orca. Run findings and the owner's decisions go in the shared run
state below. Review findings before deciding which changes to pursue. Session
excerpts and other private review evidence stay outside this public repository.

## Shared run state

Orca starts each run in a fresh worktree, and the same kind of project work
runs on more than one machine; Sessions audit, for example, runs on a laptop
and on a dev server. Local files would leave each run blind to what earlier
runs found and what the owner already decided. The 2026-11-02 retro's declined
items were applied anyway for exactly this reason. Every automation therefore
reads and writes one private Git repository, cloned to
`~/.local/state/automation-runs` on each host.

- **Shared across machines.** Every host's runs read from and add to one
  store, so a run on the dev server knows what the laptop's run found and what
  the owner already declined. Git keeps the history.
- **Separate from the work repositories.** Run findings, session excerpts, and
  decisions about the automations are not project source. They stay out of the
  repositories where the work happens, so they never land in a project's
  history or a public repository such as this one.
- **Works for teams too.** A team would create one private repository for its
  own workers' automations and keep it out of its monorepo, for the same
  reason.

Large caches, such as Optimize CI's GitHub API cache, stay on each host.

Each prompt ends with a paragraph that points the run at this contract. Copy
the template below into your private repository's README; this is the
canonical public version.

```markdown
# Automation runs

## Layout

One folder per automation slug:

- `<slug>/runs/YYYY-MM-DD-<host>.md`: one file per run, with the window
  reviewed, the findings as presented (with numbers and short stable titles),
  and what the run changed. `<host>` is `hostname -s`.
- `<slug>/decisions.md`: append-only, one entry per answered finding, with the
  date, run file, finding title, decision (`accepted`, `declined`, `deferred`,
  or `already-fixed`), the owner's words, and the issue or PR that carries it.

## Run contract

1. Start with `git -C ~/.local/state/automation-runs pull --rebase`, cloning
   the repository first if it is missing. Read `<slug>/decisions.md` and the
   three newest runs from any host.
2. Report a declined finding only with materially new evidence, labeled as
   previously declined. Mark repeats and say whether the fix held.
3. At the end, write the run file, commit, `git pull --rebase`, and push. On a
   push race, rebase and push again.
4. When the owner answers, append the answers to `decisions.md`, then commit
   and push before acting on them.
```
