# Sessions audit

Review recent AI sessions with the installed `retro` skill.

| Orca job | Cadence | Timezone |
|---|---|---|
| Sessions audit (local) | Daily at 03:00 | America/Los_Angeles |
| Sessions audit (remote) | Daily at 01:00 | America/Los_Angeles |

- **Requires:** Matt Pocock's [`retro`](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) and [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) skills installed for the selected agent, this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, access to that machine's AI session histories, and access to the repository's current guidance. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Before scheduling, follow the
[upstream installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup)
for the agent selected in Orca, or run `npx skills@latest add mattpocock/skills`
and select `retro` and `writing-for-agents` for that agent. Repeat the
installation on each host where a session audit will run.

Create each job on the Orca host whose sessions it should review; a job on one
host does not establish coverage of the other. Both jobs share the prompt
below, and each adds its own closing paragraph from
[Consolidation](#consolidation). Replace The Rookery with the repository whose
skills, workflows, guidance, and configuration you want reviewed.

The prompt reviews the previous 24 hours on every run. Widen the review window
after missed runs to cover sessions from when the host was unavailable.

## Prompt

The prompt starts with the `/retro` slash command because `retro` sets
`disable-model-invocation`, so Claude Code loads it only from a slash command.
On another agent, invoke `retro` the way that agent loads user-invoked skills.

```text
/retro this host's AI sessions from the past 24 hours alongside The Rookery's skills, workflows, guidance, and configuration.

Read actual transcripts across configured agents and account homes. Select by modification time, follow symlinks, deduplicate real paths, and cross-check Orca's session journal; it does not cover all terminal or external-app sessions. Describe personal threads by category only.

Recommend environment and workflow improvements supported by session evidence. Assessment only: issue creation, implementation, and PR publication require separate approval.

Confirm each finding's cause in the transcript lines it cites, not in a reader's summary. Then run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `sessions-audit` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```

## Consolidation

When the same work spans both hosts, two separate reports ask the owner the
same question twice, and neither job sees the other's evidence. The remote job
therefore runs two hours before the local one, saves its report, and asks the
owner nothing. The local job reads that report, becomes the remote workspace's
parent in Orca, and brings the owner one prioritized list. The owner answers in
one place, and each host's evidence can support or contradict the other's.

Add this paragraph to the end of the remote job's prompt:

```text
Consolidation: end the saved report with this session's Orca session ID and workspace, then stop without asking the owner. The local Sessions audit reads the report, becomes this workspace's parent in Orca, and brings the owner one combined list. Answer its messages and carry out what it relays.
```

Add this paragraph to the end of the local job's prompt:

```text
Consolidation: when the remote host's audit saved a report in the past 24 hours, read it and make this workspace the parent of its workspace in Orca. Merge both hosts' revised recommendations into one prioritized list before `ce-pov` judges it: combine matching findings, say where the two hosts' evidence conflicts, and mark each item's host. The owner answers here; relay each answer for the remote host to its session through Orca. With no remote report, say so and report this host only.
```

A job that runs on one host only uses the shared prompt without either
paragraph.
