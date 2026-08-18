<!-- markdownlint-disable-file MD041 -->

![The Rookery banner showing Huginn returning with a field dispatch to a blueprint workspace](docs/assets/the-rookery-readme-banner.webp)

# The Rookery

An always-current field guide to how I build with AI. It connects a practical
workflow for research, planning, design, implementation, shipping, maintenance,
and learning with the portable agent skills I use to run it.

A skill is a portable set of instructions an agent loads when a task calls for
it.

A rookery is where corvids gather to nest. This one is named for Odin's ravens, Huginn and Muninn. Huginn is thought, Muninn is memory. Each morning they fly out to see the world, and each evening they return with what they've learned.

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

These packages use the [Agent Skills](https://agentskills.io) format supported
by tools including Claude Code, Codex, Cursor, and Gemini CLI. Installation and
runtime behavior remain harness-specific. Add `-g` to install once for your
whole machine instead of per project.

`main` is the rolling catalog and the normal install source. Semantic-version
[Release Snapshots](CONCEPTS.md#release-snapshot) are immutable historical
checkpoints with release notes; they are not install pins. The first public
snapshot will be `v0.2.0`. The project remains in SemVer's initial-development
phase, so its public contract may continue to evolve before `1.0.0`.

## The workflows

Everything here fits into seven jobs. The walkthroughs live in [WORKFLOWS.md](WORKFLOWS.md).

- [**Research**](WORKFLOWS.md#research). Gather current evidence, test it against opposing views, and curate enough context to plan.
- [**Plan**](WORKFLOWS.md#plan). Define what to build, how to build it, and how success will be verified.
- [**Design**](WORKFLOWS.md#design). Set the visual direction and written design system for interface work.
- [**Build**](WORKFLOWS.md#build). Implement the plan in bounded, independently verified slices.
- [**Ship**](WORKFLOWS.md#ship). Review and verify the finished change before merging and documenting it.
- [**Maintain**](WORKFLOWS.md#maintain). Keep repositories healthy by turning recurring problems into durable safeguards.
- [**Learn**](WORKFLOWS.md#learn). Turn experience into linked knowledge and new questions for Research.

## The skills

- [storm-research](skills/storm-research/SKILL.md). Run deep, source-backed research through isolated practitioner, academic, skeptic, economist, and historian lenses. It tests foundations, mechanisms, system relationships, and downstream effects as part of the research, then preserves the evidence and disagreements in a reader-focused briefing. It can support a decision, but it does not replace `ce-pov`'s compact, decisive, project-grounded verdict.
- [creating-portable-skills](skills/creating-portable-skills/SKILL.md). Create a new agent skill, or review, update, and migrate an existing one. One loop from intent interview through a baseline comparison to a packaged skill that works across models and harnesses.
- [managing-issues](skills/managing-issues/SKILL.md). Manage one GitHub or Linear issue, or its native parent and blocker graph, through the repository's canonical tracker. It returns the current Ready Frontier for Build and marks completion only against Verification evidence. Release A applies approved GitHub effects; Linear stays read-only until the provider can prove the authenticated principal. Build owns execution orchestration, and the tracker remains the only durable work state.
- [personal-chief-of-staff](skills/personal-chief-of-staff/SKILL.md). Run a daily wind-down and journal, weekly review, or quarterly review from your existing sources. Every durable change stays reviewable before it lands.
- [managing-personal-crm](skills/managing-personal-crm/SKILL.md). Keep relationship context in canonical Person notes and tasks. Capture interactions, prepare for a conversation, find who could help with current work, and clean up notes in stages, with no separate CRM database.
- [reviewing-meetings](skills/reviewing-meetings/SKILL.md). Turn completed meetings from a configured source into grounded notes and follow-up actions. Duplicate work is prevented, each outcome gets one canonical owner, and scheduled runs stay read-only.
- [repo-gardener](skills/repo-gardener/SKILL.md). Run a nightly or manual nine-lane repository-health pass, deepen the strongest current signals, and, when live policy and evidence justify it, supervise bounded child work through an unmerged pull request. Native PRs own authored-work state; the tracker keeps two records per run for morning inspection.
- [checking-pr-readiness](skills/checking-pr-readiness/SKILL.md). Gate a branch before the pull request opens: the full working surface reported, upstream steps verified from receipts, the plan compared against what was delivered, and a sweep of the finding classes that drive repeated review rounds. Interactive runs end in one owner decision plus an evidence pack; assessment-only runs return an exact-subject/exact-revision receipt without a menu.
- [checking-merge-readiness](skills/checking-merge-readiness/SKILL.md). A whole-change pre-merge review of a pull request: birth-to-tip design health (intent drift, accretion, redesign pressure, follow-up debt), a thin review-completion check, host merge rules, and a graded risk profile that rolls up into merge, debug, or do not merge.

## My other projects

- [Networked Thinking](https://networkedthinking.ai). My note system for durable learning: the book, the site, and the [skills](https://github.com/jrgilbertson/networked-thinking-skills) that run the Learn step here.

## Standing on

This system builds on work by people who share theirs. Use them directly.

- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) by Trevin Chow ([@trevin](https://x.com/trevin)) and Kieran Klaassen ([@kieranklaassen](https://x.com/kieranklaassen)). The development spine.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) by Matt Pocock. The targeted grilling pattern, plus tracer-bullet issue leaves, blocker-first ordering, and frontier recomputation that informed `managing-issues`.
- [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus ([@pbakaus](https://x.com/pbakaus)). The design language that makes agents better at design.
- [last30days](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn ([@mvanhorn](https://x.com/mvanhorn)). Recent-signal research across Reddit, X, YouTube, HN, and the web.
- [Orca](https://github.com/stablyai/orca) by Jinjing Liang ([@JinjingLiang](https://x.com/JinjingLiang)). The agentic IDE all of this runs in.

## Contributing

Fixes and portability PRs are welcome. New skills start as an issue. See [CONTRIBUTING](CONTRIBUTING.md) for how this repo stays healthy.

This is a solo-maintained project with no support SLA. Please report security
issues privately through the process in [SECURITY.md](SECURITY.md), and use the
[Code of Conduct](CODE_OF_CONDUCT.md) for community participation.

## License

[MIT](LICENSE).
