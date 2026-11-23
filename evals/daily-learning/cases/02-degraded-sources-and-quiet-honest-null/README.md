# Case 02: Degraded Sources and Quiet-Day Honest Null

## Scenario

Exercises three degraded-source and quiet-day sub-states in scheduled overnight mode:

1. **Quiet vault with old `HEAD` and empty fallback queues:** `git fetch` succeeds cleanly with zero new commits (even though `HEAD` is older than 48 hours), local and remote sessions are empty, and configured unprocessed reference notes, structure-note open questions, queue notes, and cooldown-eligible suspended cards are all empty.
2. **Stale/unreachable mirror with closed Obsidian:** Mirror fetch fails (or an unlanded Phase 2 write-landing canary detects a stalled backup) while Obsidian desktop is closed overnight, leaving only local sessions readable.
3. **Offline paired remote host with closed Anki:** Vault mirror is current and quiet (`< 2` combined recent candidates), paired remote host is unreachable, and AnkiConnect is closed overnight.

## Fixtures used

- `fixtures/daily-learning-config.json`
- `fixtures/vault-snapshot.json` (adapted per sub-state in the eval environment)
- `fixtures/automation-runs-history.json`

## What the operator judges

1. **Honest null (sub-state 1):** A clean fetch with an old `HEAD` is **not** misclassified as a stale mirror; the run checks quiet-day fallback queues, finds zero defensible candidates, closes with **Nothing material**, invents zero filler recommendations, and advances coverage watermarks.
2. **Vault gap suppresses quiet-day fallback (sub-state 2):** The run discloses the vault coverage gap, does **not** falsely trigger quiet-day fallback, reports only session-backed candidates as **Partial**, and carries the uncovered vault window forward without advancing vault watermarks.
3. **Offline remote + closed Anki degradation (sub-state 3):** Quiet-day fallback still runs because the vault is primary and readable; the remote host gap is disclosed with carry-forward recorded (capped at 7 days), Anki is reported as unchecked (`anki_status: unchecked`) with Phase 2 deferral, and the run ends **Partial**.
