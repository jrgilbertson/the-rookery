# Automations

These recurring Orca reviews are part of how I build with AI. Each file
contains a prompt, schedule, and prerequisites you can adapt to your own
repository.

Each definition starts with its purpose, cadence, timezone, and
prerequisites, followed by any setup instructions and the copyable prompt.
Longer operating notes follow the prompt. Sessions audit shares one prompt
between two jobs, with host-specific consolidation instructions below it.

| Automation | Purpose | Cadence | Timezone |
|---|---|---|---|
| [Sessions audit (local)](sessions-audit.md) | Review recent AI sessions on the local host | Daily at 03:00 | America/Los_Angeles |
| [Sessions audit (remote)](sessions-audit.md) | Review recent AI sessions on the remote host | Daily at 01:00 | America/Los_Angeles |
| [Analytics gap audit](analytics-gap-audit.md) | Find shipped user actions without analytics and events that never arrive, and recommend fixes | Monday at 04:00 | America/Los_Angeles |
| [Improve audit](improve-audit.md) | Survey the whole codebase with `improve` and recommend improvements | Tuesday at 04:00 | America/Los_Angeles |
| [State-machine correctness audit](state-machine-audit.md) | Assess lifecycle correctness and recommend fixes | Sunday at 04:00 | America/Los_Angeles |
| [Design system audit](design-system-audit.md) | Review every page against the design system and recommend fixes, shared components, and design upgrades | Wednesday at 04:00 | America/Los_Angeles |
| [Test audit](test-audit.md) | Review tests, find protection gaps, and recommend improvements | Thursday at 21:00 | America/Los_Angeles |
| [Optimize CI](optimize-ci.md) | Review continuous integration | Saturday at 09:00 | America/Los_Angeles |
| [Weekly codebase design](weekly-codebase-design.md) | Review codebase design | Saturday at 04:00 | America/Los_Angeles |
| [Agent entropy audit](agent-entropy-audit.md) | Find duplicated truth, dead code, stale guidance, and weakened guardrails | Saturday at 07:00 | America/Los_Angeles |

All schedules use America/Los_Angeles. Choose a cadence and timezone that suit
your work.

## Set up a scheduled review

Create an automation in Orca and select the target repository and agent. Set
the schedule and paste the prompt from its file. Select Chat mode and save an
explicit model and effort, using [ROUTING.md](../ROUTING.md) to match the work.
Keep the saved selections in Orca; changing the routing guide does not update
existing jobs. The selected agent needs the
named skills and access to the sources the review requires. If a required skill
is missing or cannot load, the automation reports it and stops. Skill and plugin
installation and updates are outside the automation. For Sessions audit,
replace the reference to The Rookery with your own repository.

Sessions audit invokes `ce-retro` on each host separately, with required skills
available to the selected agent on each host. The remote job runs first and
the local job merges both hosts' findings into one list; see
[Consolidation](sessions-audit.md#consolidation).

Some prompts invoke an existing skill; others describe the review directly.
Orca runs the prompt on a schedule; an invoked skill tells the agent how to do
the work. Prompts say what to look for and how to run; findings, lessons, and
earlier measurements live only in the history repository. Copy the definitions into Orca manually. To change an existing job,
edit it in Orca too.

The prompts ask for recommendations in leverage order without defining it. The
definition is the [Rank by leverage](../PRIORITIZATION.md#rank-by-leverage)
section of `PRIORITIZATION.md`. Add that section to the selected agent's
instructions so it scores findings the same way.

Keep local paths, repository selections, account identifiers, and enabled
status in Orca. Run findings and the owner's decisions go in the shared run
state below. Review findings before deciding which changes to pursue. Session
excerpts and other private review evidence stay outside this public repository.

## Shared run state

Orca starts each run in a fresh worktree, and the same kind of project work
runs on more than one machine; Sessions audit, for example, runs on a laptop
and on a dev server. Local files would leave each run blind to what earlier
runs found and what the owner already decided. Every automation therefore
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

Each automation contains its assessment instructions and authority limits in
its own prompt and judges its own recommendations. Improve audit returns every
finding and judges only the ones the owner picks from its report. In paired
Sessions audits, the local job owns that judgment after combining both hosts.
The history repository stores reports and owner decisions, not a shared
assessment workflow.
Its README documents storage and helper usage.

Copy the storage template below into your private repository's README. If it
provides a history helper, document how to use it for these operations.

```markdown
# Automation runs

This repository stores automation reports and owner decisions. Each automation
keeps its assessment and recommendation-review instructions in its own prompt.

## Layout

One folder per automation slug. When one automation runs against more than one
repository, give each target its own slug, such as `test-audit-<repo>`, so
projects never share decisions or runs.

- `<slug>/runs/YYYY-MM-DD-HHMMSS-<host>.md`: one file per run, dated in UTC,
  with the window reviewed, the findings as presented (with numbers and short
  stable titles), and what the run changed. `<host>` is `hostname -s`. The
  seconds keep a retry from replacing an earlier report; never overwrite one.
- `<slug>/decisions.md`: append-only, one entry per answered finding, with the
  date, run file, finding title, decision (`accepted`, `declined`, `deferred`,
  or `already-fixed`), the owner's words, and the issue or PR that carries it.

## Storing run history

1. Start with `git -C ~/.local/state/automation-runs pull --rebase --autostash`,
   cloning the repository first if it is missing. Read `<slug>/decisions.md` and the
   three newest runs from any host.
2. Report a declined finding only with materially new evidence, labeled as
   previously declined. Mark repeats and say whether the fix held.
3. At the end, write the run file, commit, `git pull --rebase --autostash`,
   and push. Another writer may share the checkout, so commit only your own
   files. On a push race, rebase and push again.
4. When the owner answers, append the exact answers to `decisions.md`, then
   commit and push. Recording a decision does not authorize an assessment run
   to implement it; follow the owning workflow and its required approvals.
```
