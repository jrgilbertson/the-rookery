# Daily learning

Run a `daily-learning` review each morning across the last day's vault changes, local and paired remote AI sessions, and Anki status. The run changes nothing. When you reply in its chat, it helps you turn the items you pick into notes and cards.

- **Cadence:** Daily at 05:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The installed `daily-learning` skill, plus `atomic-note`, `obsidian-cli`, and `obsidian-markdown` on the workstation that hosts Obsidian and Anki. Read access to your vault or a Git backup mirror of it, and to local AI session histories. Optionally, a paired remote Orca host and AnkiConnect.

## Setup

Create this job once on the workstation that hosts Obsidian and Anki. Select Chat mode, set the schedule, and save an explicit model and effort using [ROUTING.md](../ROUTING.md).

The prompt owns where to look; the skill owns what to recommend and how to coach. Replace the placeholders below and remove any optional line you do not use. A Git backup mirror lets the run read the vault while Obsidian is closed. For a paired remote Orca host, point it at a dedicated existing remote folder workspace (`folder:<id>` or an existing path selector), not `current` or a new Git worktree.

This job keeps no run history. Each run covers the last 24 hours, and its digest lives in that run's Orca chat, which is where you reply. A missed day is not caught up, and an item you declined can come back if it shows up again in a later day's changes.

## Prompt

```text
Before starting, confirm the `daily-learning`, `atomic-note`, `obsidian-cli`, and `obsidian-markdown` skills are available. If one is missing, report it and stop. Do not install or update skills or plugins.

Run a `daily-learning` review of the last 24 hours using these sources, then stop and wait for my reply in this chat:

- Vault: `<your Obsidian vault name>`
- Vault backup mirror (optional): remote `<your vault backup Git URL>`, bare mirror cache at `<a path outside every repository and the live vault>`
- Reference notes (optional): `<vault-relative folder>`; `#reading` means in progress, `#reviewed` means done, untagged means unprocessed
- Strategy and learning notes (optional): `<vault-relative paths>`
- Paired remote Orca host (optional): `--on <host>`, `--worktree <existing remote folder workspace>`, `--agent <agent>`, scan timeout `<10>` minutes
- AnkiConnect (optional): `http://127.0.0.1:8765`

1. Vault: update the mirror (`git clone --mirror` the first time, `git fetch --prune` after that, with hooks disabled) and read the notes changed in the last 24 hours with `git log` and `git show`. Without a mirror, or if it is unreachable, use the `obsidian` CLI. Never read or write the live vault folder directly.
2. Local AI sessions: read the last 24 hours of transcripts across this machine's harnesses, leaving out this job's own runs and other scheduled audits. Describe personal threads by topic only.
3. Remote AI sessions (optional): start one read-only worker with `orca orchestration worker-start --on <host> --worktree <workspace> --agent <agent>`, and tell it to read the last 24 hours of sessions and return concepts only, with no credentials or verbatim personal text, before the timeout. Wait with `orca orchestration check --wait --types "worker_done,escalation" --timeout-ms <minutes * 60000>`. If the host is offline or the worker times out, say so in the digest and continue.
4. Anki (optional): if AnkiConnect answers, read due and overdue counts, recent lapses, and suspended cards, noting which were suspended as leeches and which by hand. If Anki is closed, say so and continue.
5. Follow `daily-learning` to write the digest. End it with one sentence on what you read and anything you could not read. Then stop.

When I reply, follow `daily-learning` to work the items I pick, using the `obsidian` CLI and AnkiConnect for approved changes.
```

## Verify setup

Before enabling the schedule, run the job once manually on the workstation and check that:

1. The required skills load without installing or updating anything.
2. The digest lists at most five items, names one to start with, and says what it read and could not read.
3. The vault and Anki are unchanged after the run.
4. A configured remote worker finishes within its timeout and leaves no worktree behind.
5. Replying with one item gets a question before any draft, and nothing is written until you approve the exact change.
