# Automations

These recurring Orca reviews are part of how I build with AI. Each file
contains a prompt, schedule, and prerequisites you can adapt to your own
repository.

| Automation | Purpose | Cadence | Timezone |
|---|---|---|---|
| [Sessions audit (local)](sessions-audit.md) | Review recent AI sessions on the local host | Daily at 05:00 | America/Chicago |
| [Sessions audit (remote)](sessions-audit.md) | Review recent AI sessions on the remote host | Daily at 03:00 | America/Chicago |
| [Analytics gap audit](analytics-gap-audit.md) | Find shipped user actions without analytics and events that never arrive, and file issues | Monday at 06:00 | America/Chicago |
| [Test audit](test-audit.md) | Review tests, find protection gaps, and recommend improvements | Thursday at 23:00 | America/Chicago |
| [Optimize CI](optimize-ci.md) | Review continuous integration | Saturday at 09:00 | America/Los_Angeles |
| [Weekly codebase design](weekly-codebase-design.md) | Review codebase design | Saturday at 05:00 | America/Chicago |
| [Coding standards audit](coding-standards-audit.md) | Keep adopted coding guidance current and useful | Saturday at 07:00 | America/Los_Angeles |

Each schedule uses the timezone shown. Choose a cadence and timezone that suit
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

Keep local paths, repository selections, account identifiers, enabled status, and
run history in Orca. Review findings before deciding which changes to pursue.
Session excerpts and other private review evidence stay outside this public
repository.
