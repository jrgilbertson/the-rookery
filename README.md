<!-- banner artwork lands here and doubles as the social preview image -->

# The Rookery

An opinionated, always-current home for how I build with AI. It holds the workflows I use every day and the skills that power them. Each skill installs individually as a standard Agent Skills package in compatible harnesses such as Claude Code and Codex. One rule anchors it all. **I use this repo through the same front door you do.**

## Install

The front door is the [skills installer](https://github.com/vercel-labs/skills). No clone, no setup.

```bash
# browse the shelf
npx skills add jrgilbertson/the-rookery --list

# install one skill
npx skills add jrgilbertson/the-rookery --skill <name>

# or take everything
npx skills add jrgilbertson/the-rookery --all
```

The installer targets compatible harnesses that read `SKILL.md`, including Claude Code, Codex, Cursor, and Gemini CLI. See the [Agent Skills](https://agentskills.io) ecosystem for the full list. Add `-g` for a user-level install instead of per-project.

> **The first skill is on the shelf.** [creating-portable-skills](skills/creating-portable-skills/SKILL.md) installs with `npx skills add jrgilbertson/the-rookery --skill creating-portable-skills`. More are arriving. Watch [releases](../../releases) for arrivals.

<details>
<summary>Prefer a clone?</summary>

Clone the repo and symlink any <code>skills/&lt;name&gt;</code> folder into your agent's skills directory, such as <code>~/.claude/skills/</code> or your harness's equivalent. The npx route does exactly this for you.
</details>

## The workflows

Everything here fits into seven jobs. Each links to its walkthrough in [WORKFLOWS.md](WORKFLOWS.md).

- **[Research](WORKFLOWS.md#research)**. Gather real signal before deciding. last30days for what people actually use, multi-perspective deep research for the hard questions.
- **[Plan](WORKFLOWS.md#plan)**. Turn intent into work worth doing. Ideation, brainstorming, and planning with compound engineering.
- **[Design](WORKFLOWS.md#design)**. Impeccable drives every interface decision, from first layout to final polish.
- **[Build](WORKFLOWS.md#build)**. Implement in Orca with parallel worktrees and delegated agents.
- **[Ship](WORKFLOWS.md#ship)**. Review gates, pre-PR approval, and changelogs and releases that write themselves.
- **[Maintain](WORKFLOWS.md#maintain)**. Keep repos healthy. Hygiene passes, architecture reviews, evals, and data quality checks.
- **[Learn](WORKFLOWS.md#learn)**. Turn what you read and build into durable knowledge. Networked thinking, atomic notes, and learnings that compound back into the system.

## Standing on

This system builds on work by people who share theirs. Use them directly.

- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) by Kieran Klaassen and the team at Every. The development spine.
- [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus. The design language that makes agents better at design.
- [last30days](https://github.com/mvanhorn/last30days-skill) by mvanhorn. Recent-signal research across the platforms that matter.
- [Orca](https://github.com/stablyai/orca) by Stably. The agentic IDE all of this runs in.
- [skills](https://github.com/vercel-labs/skills) by Vercel Labs. The installer behind the npx front door above.

## Contributing

Fixes and portability PRs are welcome. New skills start as an issue. See [CONTRIBUTING](CONTRIBUTING.md) for how this repo stays healthy.
