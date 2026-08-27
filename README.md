<!-- markdownlint-disable-file MD041 -->

![The Rookery banner showing Huginn returning with a field dispatch to a blueprint workspace](docs/assets/the-rookery-readme-banner.webp)

# The Rookery

An always-current field guide to how I build with AI. It connects a practical workflow for research, planning, design, implementation, shipping, maintenance, and learning with the skills I use to run it. A skill is a portable set of instructions an agent loads when a task calls for it.

A rookery is where corvids gather to nest. This one is named for Odin's ravens, Huginn and Muninn. Huginn is thought, Muninn is memory. Each morning they fly out to see the world, and each evening they return with what they've learned.

## Guiding principles

1. **Works across tools.** Skills should not depend on one agent or harness.
2. **Add skills sparingly.** Create one only when existing tools leave a repeated gap.
3. **Improve from use.** Turn recurring failures into tests, rules, or clearer instructions.

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

These packages use the [Agent Skills](https://agentskills.io) format supported
by tools including Claude Code, Codex, Cursor, and Gemini CLI. Installation and
runtime behavior remain harness-specific. Add `-g` to install once for your
whole machine instead of per project.

`main` is the rolling catalog and the normal install source. Semantic-version
[Release Snapshots](CONCEPTS.md#release-snapshot) are immutable historical
checkpoints with release notes; they are not install pins.

## The workflows

Everything here fits into five core jobs, Research through Ship, plus two feedback loops: Maintain and Learn. The walkthroughs in [WORKFLOWS.md](WORKFLOWS.md) are how I run that loop. The skills in this catalog plug into it and work in other editors and harnesses too.

- [**Research**](WORKFLOWS.md#research). Gather current evidence, test it against opposing views, and curate enough context to plan.
- [**Plan**](WORKFLOWS.md#plan). Define what to build, the guardrails execution has to honor, and how success will be verified.
- [**Design**](WORKFLOWS.md#design). Set the visual direction and written design system for interface work.
- [**Build**](WORKFLOWS.md#build). Implement the plan in bounded, independently verified slices.
- [**Ship**](WORKFLOWS.md#ship). Review and verify the finished change before merging and documenting it.
- [**Maintain**](WORKFLOWS.md#maintain). Keep repositories healthy by turning recurring problems into durable safeguards.
- [**Learn**](WORKFLOWS.md#learn). Turn experience into linked knowledge and new questions for Research.

## The skills

- [checking-merge-readiness](skills/checking-merge-readiness/SKILL.md). Review a pull request after its review cycle for intent drift, unnecessary complexity, failed merge rules, and unresolved risks. Run it immediately before merging to decide whether the finished change belongs on `main`.
- [checking-pr-readiness](skills/checking-pr-readiness/SKILL.md). Check a finished branch before opening a pull request. Use it to confirm the change matches the plan, required checks pass, and major risks are resolved.
- [checking-simplicity](skills/checking-simplicity/SKILL.md). Challenge a completed requirements or approach draft before implementation planning, and a finished implementation plan before execution. Use it again before an in-build design choice to find the smallest safe scope or approach without inventing implementation details.
- [creating-portable-skills](skills/creating-portable-skills/SKILL.md). Create, revise, migrate, or audit a skill, then verify its structure, triggers, behavior, and installation. Use it when you need a portable skill package with separate evidence for behavior and installation.
- [managing-issues](skills/managing-issues/SKILL.md). Manage GitHub or Linear issues and their native parent and blocker relationships through the repository's canonical tracker. Use it to read, draft, create, or update a single issue or multi-issue graph, and to assess readiness, dependencies, or completion.
- [managing-personal-crm](skills/managing-personal-crm/SKILL.md). Keep relationship context in one note per person while messages and other raw interactions stay in their original apps. Use it to prepare for someone, capture an interaction, reconnect an overdue relationship, or find who could help with current work.
- [personal-chief-of-staff](skills/personal-chief-of-staff/SKILL.md). Turn information from your configured sources into a daily, weekly, or quarterly review. Run it when you need to orient, reflect, and decide what to do next across several parts of your life and work.
- [repo-gardener](skills/repo-gardener/SKILL.md). Check a repository across nine maintenance areas and, when warranted, assign parallel workers that each leave one unmerged pull request. Run it on a schedule or by hand; a human still merges.
- [reviewing-meetings](skills/reviewing-meetings/SKILL.md). Turn completed meetings into draft notes and follow-up actions grounded in the meeting source. Run it after a meeting or during a catch-up when you want to capture outcomes and approve each follow-up before anything is written.
- [storm-research](skills/storm-research/SKILL.md). Research a hard question through independent perspectives and produce a source-backed briefing that preserves disagreements and blind spots. Reach for it when a decision, investment, or long-form deliverable needs evidence from several perspectives.

## My other projects

- [Networked Thinking](https://networkedthinking.ai). My system for turning what I learn into durable, linked notes, explained through a book and website. Use it when something I learn should become knowledge I can connect and reuse.
- [Networked Thinking Skills](https://github.com/jrgilbertson/networked-thinking-skills). A collection of skills and deterministic helpers for Networked Thinking notes and tasks in Obsidian. Use it when you want an agent to create or audit atomic notes or manage Obsidian tasks.

## Standing on

This system builds on work by people who share theirs. Use them directly.

- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) by Trevin Chow ([@trevin](https://x.com/trevin)) and Kieran Klaassen ([@kieranklaassen](https://x.com/kieranklaassen)). Plans, implements, reviews, and documents the development work.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) by Matt Pocock. The targeted grilling and issue-planning patterns that shaped `managing-issues`.
- [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus ([@pbakaus](https://x.com/pbakaus)). Shapes design direction, critiques interfaces, and keeps design systems coherent.
- [last30days](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn ([@mvanhorn](https://x.com/mvanhorn)). Recent-signal research across Reddit, X, YouTube, HN, and the web.
- [Orca](https://github.com/stablyai/orca) by Jinjing Liang ([@JinjingLiang](https://x.com/JinjingLiang)). The agentic IDE I use to run this workflow across several harnesses. The skills also work in VS Code, Claude Cowork, Codex, and other compatible tools.

## Contributing

Fixes and portability PRs are welcome. New skills start as an issue. See [CONTRIBUTING](CONTRIBUTING.md) for how this repo stays healthy.

This is a solo-maintained project with no support SLA. Please report security
issues privately through the process in [SECURITY.md](SECURITY.md), and use the
[Code of Conduct](CODE_OF_CONDUCT.md) for community participation.

## License

[MIT](LICENSE).
