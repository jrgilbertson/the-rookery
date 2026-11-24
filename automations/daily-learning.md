# Daily learning

Run `daily-learning` read-only overnight across recent vault activity, local and paired remote AI sessions, and Anki status, then turn chosen items into linked notes, reference-note tags, flashcards, and strategy or learnings updates interactively when you reply.

- **Cadence:** Daily at 05:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The installed `daily-learning` skill (plus `atomic-note`, `obsidian-cli`, and `obsidian-markdown` on the local workstation hosting Obsidian and Anki), access to your vault or bare Git backup mirror, local AI session histories, optional paired remote Orca hosts, optional AnkiConnect, and a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Create this job once on the local workstation hosting Obsidian and Anki. Select Chat mode, set the schedule, and save an explicit model and effort using [ROUTING.md](../ROUTING.md).

The automation prompt owns host-specific discovery and private run history; the installed `daily-learning` skill supplies the learning judgment and Phase 2 interactive authoring. Replace the placeholders below with your vault identity, optional read-only Git backup mirror (so overnight runs work while Obsidian desktop is closed), reference-note folder and tags, focus/strategy paths, optional paired remote Orca host and timeout budget, and private shared run-state repository. Remove any optional bullet you do not use.

When including a paired remote Orca host, point it at a dedicated existing remote folder workspace (`folder:<id>` or existing path selector) rather than `current` or a new Git worktree.

## Prompt

```text
Before assessing, confirm the required skills (`daily-learning`, `atomic-note`, `obsidian-cli`, and `obsidian-markdown`) are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

Run a scheduled overnight `daily-learning` pass (read-only) using these host sources, then stop and wait for my reply to enter Phase 2 interactive authoring:

- Vault: `<your Obsidian vault name>`
- Vault backup mirror (optional, for closed-Obsidian overnight reads): remote `<your SSH/HTTPS vault backup Git URL>`, bare `0700` mirror cache at `<cache path outside all repos and live vault>`
- Reference notes (optional): `<vault-relative folder, e.g. Reference Notes/>` (in-progress `#reading`, completed `#reviewed`, untagged = unprocessed)
- Strategy and learning focus notes (optional): `<vault-relative paths, e.g. Strategy/Personal Strategy.md, Structure Notes/Personal Learnings.md>`
- Paired remote Orca host (optional): `--on <host>`, `--worktree <existing remote folder workspace>`, `--agent <agent>`, scan timeout `<10>` minutes
- AnkiConnect (optional): loopback `http://127.0.0.1:8765`
- Shared run-state repository: `<your private automation-state repository>` at `~/.local/state/automation-runs` (slug `daily-learning`)

1. Sync run history first (`git -C ~/.local/state/automation-runs pull --rebase --autostash`). Read `daily-learning/decisions.md` and the last 14 daily runs under `daily-learning/runs/` for prior watermarks, recurrence, engineering skew, and self-edited note paths. Cap missed-run catch-up at 7 days. Re-enter explicitly `deferred` items from the most recent daily run once (labeled `carried from <date>`, competing inside the 5-item cap); keep `declined` items suppressed unless materially new evidence appears.

2. Gather read-only inputs:
   - **Vault (primary):** Update the bare Git backup mirror (`git clone --mirror` on first run, `git fetch --prune` thereafter, with hooks disabled) and diff since the last run's mirror commit, reading blobs via `git show` (ignoring symlinks and skipping notes edited by this automation since the last run unless a newer human edit changed them). Fall back to live `obsidian` CLI only when no mirror is configured or the mirror is stale/unreachable; never touch the live vault directory directly on disk. Read the configured strategy and learning notes from the same source.
   - **Local AI sessions (secondary):** Scan recent non-audit local transcripts across configured harnesses and account homes (counting child transcripts with their parent, excluding this automation's own threads and other scheduled audits, and describing personal threads by coarse category only).
   - **Paired remote Orca host (optional):** If configured, dispatch one strictly read-only worker (`orca orchestration worker-start --on <host> --worktree <workspace> --agent <agent>`) bounded by the configured minute timeout (no fixed session-count cap—grouping child/subagent transcripts with their parent work session, prioritizing human-initiated sessions plus breadth across the window, and wrapping up before the timeout). Wait via `orca orchestration check --wait --types "worker_done,escalation" --timeout-ms <minutes * 60000>` (tracking per-host deadlines if multiple hosts are configured). Require `read_count`, `eligible_count`, and abstracted concepts only (zero credentials or verbatim sensitive excerpts); mark `sampled` when `read_count < eligible_count` and fence timeouts or offline hosts as partial coverage gaps.
   - **Anki pulse (optional):** If AnkiConnect responds on loopback, run bounded read-only queries for due/overdue counts, recent lapses, and suspended cards (distinguishing `leech` from manual suspensions, capping card detail reads at 25). If Anki is closed, mark Anki unchecked for Phase 2 and continue cleanly.

3. Invoke `daily-learning` Phase 1 on those gathered inputs to rank up to 5 labeled items (no Leverage scores), highlight one deepen-today pick, and draft the morning digest with one plain-prose coverage paragraph.

4. Save the run file under `daily-learning/runs/YYYY-MM-DD-HHMMSS-<host>.md` inside `~/.local/state/automation-runs` (UTC timestamp, compact YAML frontmatter with run window, mirror commit, per-host coverage counts, Anki status, and self-edited note paths, followed by the full digest for fresh-thread recovery). Before committing or pushing, run a secret check (`gitleaks` when installed plus credential-pattern check) on staged files and fail closed on any match without committing. Commit only owned `daily-learning/` files, `git pull --rebase --autostash`, and push. Present the digest and stop read-only.

5. When I reply in this thread (or resume in a fresh thread from the latest saved run), follow `daily-learning` Phase 2 interactively with live Obsidian CLI and AnkiConnect, and append abstracted decisions (date, run file, item title, disposition, and short note/action summary—never verbatim sensitive quotes or secrets) plus edited note paths to `daily-learning/decisions.md` and the run file, secret-scanned and pushed.
```

## Verify setup

Before enabling the daily schedule, run the configured Orca job manually once on the local workstation and verify:

1. All required skills load without installing or updating any skill or plugin.
2. Vault changes read cleanly from the bare read-only Git backup mirror (or live `obsidian` CLI fallback) with zero writes to the live vault or Anki.
3. Any configured paired remote Orca worker finishes within its configured minute budget with zero leaked worktrees and returns abstracted concepts only.
4. The morning digest passes secret scanning, saves cleanly under `daily-learning/runs/` inside `~/.local/state/automation-runs`, stays capped at five labeled items without Leverage scores, and discloses any sampled or unavailable sources honestly.
5. Replying with one selected item runs the expected pretest, skeleton, or triage prompt and waits for explicit approval before making any Obsidian or Anki write.
