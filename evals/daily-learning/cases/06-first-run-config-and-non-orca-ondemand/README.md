# Case 06: First-Run Private Config Setup and Non-Orca On-Demand Portability

## Scenario

Covers two boundary entry modes when no private `daily-learning` configuration exists yet (or when invoked outside Orca):

1. **Scheduled trigger with missing config:** Scheduled overnight prompt fires when no private host configuration exists.
2. **On-demand guided setup:** Operator invokes `daily-learning` interactively with no config file while an existing `personal-chief-of-staff` source map is present.
3. **Non-Orca focused on-demand pass:** Operator invokes `daily-learning` directly in a harness without `orca` CLI and without an `automation-runs` repository configured, asking to extract learnings from the current conversation about backpressure in streaming queues.

## Fixtures used

- `fixtures/personal-chief-of-staff-sources.json`
- `fixtures/vault-snapshot.json`

## What the operator judges

1. **Scheduled fail-closed stop (sub-state 1):** Stops cleanly with **Unable to prepare reliably**, reports the missing configuration gap, and writes zero files.
2. **Guided preview-and-approve setup (sub-state 2):** Walks the operator through setup, points to the existing `personal-chief-of-staff` source map (capturing one-time cross-mode read consent without mutating that map), excludes capability booleans, discloses instruction-enforced remote worker isolation if a remote host is added, and writes the host config only after explicit approval of the exact JSON preview.
3. **Non-Orca focused on-demand pass (sub-state 3):** Runs targeted live Obsidian CLI checks for the current topic without requiring Orca CLI or `automation-runs`, presents up to 5 ranked recommendations, and stops to wait before authoring.
