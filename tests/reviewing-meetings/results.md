# Acceptance results: reviewing-meetings

This file records only sanitized behavior and capability evidence. Private
meeting content, participant identities, account identifiers, source IDs,
source URLs, vault names, and local paths are intentionally omitted.

## U3: live meeting-contract alignment

Date: 2026-07-23

- Read-only discovery retrieved the configured Meeting Template and vault agent
  guidance through the official Obsidian CLI before any proposal or mutation.
- An adversarial review checked the proposed setup for privacy leakage, wrong
  destinations, duplicate state, unsupported claims, and unnecessary
  machinery. The accepted design retained the existing source-field convention
  and compact meeting structure.
- The user approved the exact two-target setup bundle before application.
- The Meeting Template kept empty automatic date fields and its five existing
  sections. Its instructions now distinguish source-derived and manual notes,
  require stable source identity for source-derived notes, define grounded
  refined synthesis, preserve approved-note authority, require verified links,
  and point follow-up work to one canonical owner.
- Vault guidance now requires CLI-only reads and mutations, exact target paths
  where supported, validated collection-search results, pre-write rereads,
  reviewed section-level revisions, and no direct vault edits or linting.
- Both approved changes were applied through the official CLI and immediately
  read back from the authoritative targets.
- No meeting note, task, issue, calendar event, transcript, or workflow state
  was created or changed during this unit.

Result: passed.

## U4: private live acceptance

Date: 2026-07-23

- A completed meeting from the configured source was retrieved with its native
  identity and matched to one existing imported note without creating a
  duplicate.
- The first review bundle correctly found an existing work item as the
  canonical owner for issue-owned work. It did not create a duplicate issue or
  a second task that merely pointed to it.
- A same-conversation rerun while the bundle was pending classified the meeting
  as already pending and did not repeat, renumber, recompute, or mutate it.
- User feedback revised the remaining actions before application. The accepted
  bundle contained one atomic meeting-note revision, one task, one durable
  context update, and one skipped communication draft.
- The meeting-note revision migrated the active note to generic source metadata
  and applied the refined body as one atomic Obsidian CLI operation. Readback
  verified the complete approved effect.
- The first task-create attempt failed without creating a partial task. After
  the user restarted Obsidian and explicitly approved one retry, the direct CLI
  created the task once and readback matched the approved task contract.
- The durable-context update applied once and preserved unrelated fields. No
  message was drafted or sent.
- A final read-only rerun classified the meeting as already approved, returned
  zero for every other disposition, and ended **Nothing new**.
- Historical provider-specific notes were neither migrated nor changed. Their
  legacy identity fields remain a read-only duplicate-prevention input.

Result: passed.

## U5: chat-attached schedule

Date: 2026-07-23

- Setup discovery found no existing matching automation, so one new job was
  created without replacing or duplicating another job.
- The active automation is a heartbeat attached to the dedicated ongoing
  meeting-review conversation rather than a detached cron task.
- The schedule runs four times daily at the approved local times. The host
  timezone was verified as Pacific at setup.
- The thin prompt invokes the source-neutral `reviewing-meetings` skill from the
  current checkout and preserves conversation-based pending and dismissal
  suppression.
- The prompt explicitly forbids applying any action because the schedule fired,
  including an older approved but unapplied action.
- Native readback verified the automation kind, display name, target
  conversation, schedule, active status, and prompt. Notifications remain
  enabled through the app's default policy.

Result: passed.

## U6: launch-readiness acceptance

Date: 2026-07-23

Harness: Codex desktop fresh-context agents and an isolated project-level Codex
installation. Model: session default.

- Three final fresh-context behavioral runs passed the new-meeting,
  append-only, and ambiguous-attribution cases. Compared with the characterized
  bare responses, the skill added exact dispositions, deterministic note
  naming, canonical routing, action boundaries, and explicit endings.
- Three fresh listing-level judges evaluated nine intended triggers and nine
  near misses using only the final name and description. All 54 judgments were
  correct, with no uncertain result.
- The official Agent Skills validator passed. The package contains portable
  frontmatter, 117 lines in the main skill, and four bundled resources one level
  deep.
- The portable-skill and `writing-great-skills` reviews passed after clarifying
  total disposition precedence, exact source-and-ID comparisons, filename and
  source-window boundaries, configured ownership, communication authority,
  progressive disclosure, and single-source-of-truth placement.
- The broader trigger wording remains a deliberate exception to strict synonym
  pruning because it passed every listing-level judgment and improves
  discoverability across model vocabularies.
- The final package and branch diff passed the private-data, absolute-path,
  retired-system, hidden-state, and unused-artifact sweep.
- A clean copied installation into an isolated Codex project discovered exactly
  `reviewing-meetings`; the installed package matched the source package.

Limitation: the automation configuration and same-conversation behavior are
verified, but the first naturally scheduled occurrence has not happened yet.
The dedicated conversation will make that delivery observable without adding a
cursor, ledger, or forced test run.

Result: passed with the stated natural-delivery limitation.
