# Analytics gap audit

Find user actions that shipped without analytics tracking, and tracked events that never arrive in production, and file each gap as an issue a coding agent can fix.

- **Cadence:** Monday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** PostHog's [`instrument-product-analytics`](https://github.com/PostHog/ai-plugin/blob/main/skills/instrument-product-analytics/SKILL.md) skill installed for the agent, plus access to GitHub, the production PostHog project, the Vercel production aliases, Linear, and read-only access to the production Supabase database. Issue creation reads the [`managing-issues`](../skills/managing-issues/SKILL.md) configuration file for the team, labels, and readiness, but skips that skill's per-batch approval: the job runs unattended and files issues on its own. Run it once read-only and review what it would file before enabling it. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Replace each bracketed placeholder with your own project's value. This is the prompt I run, with only private names and paths swapped out.

## Prompt

```text
Audit [product] for analytics gaps and file each new gap as a Linear issue that a coding agent can fix with the `instrument-product-analytics` skill. Creating Linear issues and writing this run to the shared state repository are your only writes.

First confirm you can reach GitHub, the PostHog project [production analytics project], the Vercel production aliases, and Linear. If any of them is unreachable, report the run as failed and stop.

A gap is one of two kinds:

- **Missing:** a client or server user action added in a PR merged to `main` in the last 14 days (`gh pr list --state merged --base main --search "merged:>=<date>" --limit 1000`; the default limit silently truncates) that captures no event from [event schema] and that no existing production event already covers.
- **Silent:** a schema event whose code is live in production and has never arrived in [production analytics project] since that release, even though consenting sessions reached the surface that fires it. Read the live SHA from the Vercel aliases as [release runbook] describes, and date releases with the [release tags]. Events sent only under non-person identities, such as system jobs and webhooks, are out of scope. When no sessions have reached the surface yet, list the event as awaiting evidence; every run checks it again.

When PostHog cannot show whether a surface was used, you may query the production Supabase database inside read-only transactions.

Label each silent gap's evidence internal or real using the project's test-account filters, or unclassified when none are set.

Give each gap a key taken from the code, so it stays the same across runs: `analytics-gap-key: missing:<file>#<handler, component, or route>` or `analytics-gap-key: silent:<event>`. A key already in Linear, in any state including archived, is already flagged.

File every new gap, grouping gaps that share a root cause or came from the same PR into one issue that lists each gap's key line. Create the issues directly with the Linear connector, using the team, labels, and readiness in `.agents/managing-issues.json`: `feature` for missing, `fix` for silent, readiness `ready`. Each issue carries its key lines, the file and line, the PR or release, the evidence, and a fix that goes through the schema, [typed capture helpers], and [analytics data policy].

End with a summary listing each source as reachable or failed, how many PRs the window held and how many you reviewed, the issues filed, gaps already flagged, and events awaiting evidence.

Shared state: before each run, clone or update <your private automation-state repository> at ~/.local/state/automation-runs, then read its README.md and follow the instructions for `analytics-gap-audit`.
```
