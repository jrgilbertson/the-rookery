# Analytics gap audit

Find user actions that shipped without analytics tracking, and tracked events that never arrive in production, and recommend fixes for approval.

- **Cadence:** Monday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** PostHog's [`instrument-product-analytics`](https://github.com/PostHog/ai-plugin/blob/main/skills/instrument-product-analytics/SKILL.md) skill, loaded through the PostHog MCP with `learn posthog:instrument-product-analytics`, and this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, plus access to GitHub, the production PostHog project, the Vercel production aliases, Linear, and read-only access to the production Supabase database. This is a read-only assessment of the application and issue tracker. Review its recommendations before separately authorizing issue creation or implementation. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Replace each bracketed placeholder with your own project's value. This is the prompt I run, with only private names and paths swapped out.

## Prompt

```text
Audit [product] for analytics gaps and recommend fixes that follow PostHog's `instrument-product-analytics` skill. Load it through the PostHog MCP: `learn posthog:instrument-product-analytics`. If the skill does not load, report the run as failed and stop. Assess the application and issue tracker read-only; the audit report is the only persistent write.

Confirm access to GitHub, PostHog project [production analytics project], the Vercel production aliases, and Linear. If any is unreachable, report the run as failed and stop.

Look for:

- Missing: user actions added in PRs merged to `main` in the last 14 days that capture no event from [event schema] and are not covered by an existing production event. Use `gh pr list --state merged --base main --search "merged:>=<date>" --limit 1000`; the default limit truncates results. Report any remaining truncation.
- Silent: schema events live in production that have never arrived since release, despite consenting sessions reaching the triggering surface. Resolve the live SHA using [release runbook] and date releases with [release tags]. Exclude non-person events such as system jobs and webhooks. Recheck events awaiting exposure evidence on later runs.

If PostHog cannot establish surface usage, use read-only Supabase transactions. Label silent-gap evidence internal, real, or unclassified using the project's test-account filters.

Assign stable keys: `analytics-gap-key: missing:<file>#<handler, component, or route>` or `analytics-gap-key: silent:<event>`. Check Linear, including archived issues, for duplicates. Group new confirmed gaps by root cause or originating PR. Include keys, code locations, PR/release evidence, and fixes through the schema, [typed capture helpers], and [analytics data policy].

Report source availability, PRs in the window versus reviewed, proposed work, existing issues, and cases awaiting evidence. Do not create or update issues, implement fixes, or publish PRs without separate approval.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `analytics-gap-audit` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```
