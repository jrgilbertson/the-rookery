# Daily learning

Review recent Obsidian vault activity, local and paired remote AI sessions, and Anki status overnight, then turn chosen items into linked notes, structure-note updates, reference-note tags, Anki cards, and strategy or learnings updates after you reply.

- **Cadence:** Daily at 05:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The installed `daily-learning` skill plus `atomic-note`, `obsidian-cli`, and `obsidian-markdown` on the local workstation hosting Obsidian and Anki. Runs need your private host `daily-learning` configuration file, access to your configured vault backup mirror or Obsidian CLI, local AI session histories, optional paired remote Orca environments, optional AnkiConnect, and a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Create this job once on the local workstation hosting Obsidian and Anki. Select Chat mode, set the schedule, and save an explicit model and effort using [ROUTING.md](../ROUTING.md).

Run `daily-learning` interactively on demand once first so guided setup creates and previews your private host configuration file before enabling the overnight schedule. If the private configuration file is missing or invalid when the schedule fires, the run stops cleanly without writing any files.

When configuring paired remote Orca environments, point each server at a dedicated existing remote folder workspace and an installed remote agent ID rather than creating daily Git worktrees. When a remote harness does not expose a runtime-enforced read-only sandbox, note that remote read-only isolation is instruction-enforced plus local payload validation and confirm you accept that risk before including that server.

Replace the placeholders in the prompt below with your private configuration path and your private shared automation-state repository. Unlike the code-review automations in this folder, `daily-learning` intentionally ranks items by qualitative learning value and strategic fit without Rookery Leverage scores, uses a 14-run lookback for recurrence and skew checks, stores abstracted `decisions.md` entries without verbatim sensitive owner quotes, and transitions into approval-gated interactive authoring when you reply in the same thread while keeping the scheduled overnight pass strictly read-only.

## Prompt

```text
Before assessing, confirm the required skills (`daily-learning`, `atomic-note`, `obsidian-cli`, and `obsidian-markdown`) are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

Run the installed `daily-learning` skill in scheduled overnight read-only mode.

- Private configuration: `<your private daily-learning config path>`
- Shared run-state repository: `<your private automation-state repository>` at `~/.local/state/automation-runs` (slug `daily-learning`)

Follow the installed `daily-learning` skill's Phase 1 assessment, trust boundaries, redaction rules, secret-scanned run-state persistence, and stopping contract without mutating Obsidian, Anki, or private configuration overnight. When I reply in this thread (or resume from the saved run file), continue into the skill's approval-gated interactive authoring phase.
```

## Verify setup

Before enabling the daily schedule, run the configured Orca job manually once on the local workstation and verify:

1. All required skills load without installing or updating any skill or plugin.
2. Recent vault changes read cleanly from your configured bare read-only Git backup mirror (or Obsidian CLI fallback) with zero writes to the live Obsidian vault, Anki collection, or private configuration.
3. Any configured paired remote Orca worker runs in its existing remote folder workspace, finishes or times out cleanly with zero leaked remote worktrees, and returns abstracted concepts only.
4. The morning report passes secret scanning, saves cleanly under `daily-learning/runs/` inside `~/.local/state/automation-runs`, stays capped at five labeled items without Leverage scores, and discloses any source or Anki gaps accurately.
5. Replying with one selected item triggers the expected pretest or skeleton prompt and waits for explicit approval before making any Obsidian or Anki write.
