<!-- banner artwork lands here and doubles as the social preview image -->

# The Rookery

An opinionated, always-current home for how I build with AI. It holds the workflows I run every day and the skills that power them. A skill is a portable set of instructions an agent loads when a task calls for it. Every skill here installs individually as a standard Agent Skills package for Claude Code, Codex, and other compatible tools.

A rookery is where corvids gather to nest. This one is named for the two most famous, Odin's ravens Huginn and Muninn. Huginn is thought, Muninn is memory. Each morning they fly out to see the world, and each evening they return with what they've learned.

This repo is the return trip.

## Guiding principles

1. **Cross-agent and cross-harness.** Flexible, generalizable approaches that avoid vendor lock-in.
2. **Minimize skill volume.** Too many skills create conflicting guidance, fill up the context window, and lead to unintended behavior as models get smarter.
3. **Continuous improvement.** Every addition should make the whole system better.

## Install

Install skills one at a time or all at once.

```bash
# list available skills
npx skills add jrgilbertson/the-rookery --list

# install one skill
npx skills add jrgilbertson/the-rookery --skill <name>

# or take everything
npx skills add jrgilbertson/the-rookery --all
```

This works in any harness that reads `SKILL.md`, including Claude Code, Codex, Cursor, and Gemini CLI. See the [Agent Skills](https://agentskills.io) ecosystem for the full list. Add `-g` to install once for your whole machine instead of per project.

<details>
<summary>Prefer a clone?</summary>

Clone the repo and symlink any <code>skills/&lt;name&gt;</code> folder into your agent's skills directory, such as <code>~/.claude/skills/</code> or your harness's equivalent. The npx route does exactly this for you.
</details>

## The workflows

Everything here fits into seven jobs. The walkthroughs live in [WORKFLOWS.md](WORKFLOWS.md).

- [**Research**](WORKFLOWS.md#research). Gather real signal before deciding. last30days for what people actually use, multi-perspective deep research for the hard questions.
- [**Plan**](WORKFLOWS.md#plan). Compound Engineering turns intent into a clear objective; targeted grilling is an optional pressure test for a consequential, interdependent decision cluster.
- [**Design**](WORKFLOWS.md#design). Impeccable drives every interface decision, from first layout to final polish.
- [**Build**](WORKFLOWS.md#build). Implement in Orca with parallel worktrees and delegated agents.
- [**Ship**](WORKFLOWS.md#ship). Review gates, the pre-PR readiness checkpoint, and changelogs and releases with Compound Engineering.
- [**Maintain**](WORKFLOWS.md#maintain). Keep repos healthy. Hygiene passes, architecture reviews, evals, and data quality checks.
- [**Learn**](WORKFLOWS.md#learn). Turn what you read and build into durable knowledge. Networked Thinking, atomic notes, and learnings that compound back into the system.

## The skills

- [creating-portable-skills](skills/creating-portable-skills/SKILL.md). Create a new agent skill, or review, update, and migrate an existing one. One loop from intent interview through baseline testing to a packaged skill that works across models and harnesses.
- [personal-chief-of-staff](skills/personal-chief-of-staff/SKILL.md). Run a daily wind-down and journal, weekly review, or quarterly review from your existing sources. Every durable change stays reviewable before it lands.
- [managing-personal-crm](skills/managing-personal-crm/SKILL.md). Keep relationship context in canonical Person notes and tasks. Capture interactions, prepare for a conversation, find who could help with current work, and clean up notes in stages, with no separate CRM database.
- [reviewing-meetings](skills/reviewing-meetings/SKILL.md). Turn completed meetings from a configured source into grounded notes and follow-up actions. Duplicate work is prevented, each outcome gets one canonical owner, and scheduled runs stay read-only.
- [checking-pr-readiness](skills/checking-pr-readiness/SKILL.md). Gate a branch before the pull request opens: the full working surface reported, upstream steps verified from receipts, the plan compared against what was delivered, and a sweep of the finding classes that drive repeated review rounds. It ends in one owner decision plus an evidence pack for the PR body.
- [checking-merge-readiness](skills/checking-merge-readiness/SKILL.md). Digest a fully reviewed pull request before you merge it. You get plain-language themes of what review did, an intent-drift check against the earliest available description baseline, and a graded risk profile that rolls up into one recommendation of merge, pause, or do not merge.

## My other projects

- [Networked Thinking](https://networkedthinking.ai). My note system for durable learning: the book, the site, and the [skills](https://github.com/jrgilbertson/networked-thinking-skills) that run the Learn step here.

## Standing on

This system builds on work by people who share theirs. Use them directly.

- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) by Trevin Chow ([@trevin](https://x.com/trevin)) and Kieran Klaassen ([@kieranklaassen](https://x.com/kieranklaassen)). The development spine.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) by Matt Pocock. The targeted grilling pattern used to pressure-test dependent decisions.
- [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus ([@pbakaus](https://x.com/pbakaus)). The design language that makes agents better at design.
- [last30days](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn ([@mvanhorn](https://x.com/mvanhorn)). Recent-signal research across Reddit, X, YouTube, HN, and the web.
- [Orca](https://github.com/stablyai/orca) by Jinjing Liang ([@JinjingLiang](https://x.com/JinjingLiang)). The agentic IDE all of this runs in.

## Contributing

Fixes and portability PRs are welcome. New skills start as an issue. See [CONTRIBUTING](CONTRIBUTING.md) for how this repo stays healthy.

## License

[MIT](LICENSE).
