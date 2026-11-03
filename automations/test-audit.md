# Test audit

Review the repository's tests, find gaps in what they protect, and recommend improvements.

- **Cadence:** Thursday at 21:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-simplify-code` skill and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
compound-engineering:ce-simplify-code do a test audit of this repo and provide recommendations for improvement.

Then look for what the tests fail to protect. List the repository's material high-risk behaviors and invariants, and map each one to the tests that protect it. Label the strongest evidence for each:

- declared: a test name or document claims coverage, but you did not read the test.
- inspected: you read the assertion and confirmed it exercises the real boundary.
- executed: you ran the test and observed the result.
- falsified: a safe, reverted break of the behavior made the test fail.

Report every risk without inspected evidence as a gap or unknown. Treat line coverage, test count, and pass rate as diagnostic signals, never as proof that a behavior is protected. For each gap, recommend the cheapest test layer that still exercises the real boundary.

Return a small, prioritized set of recommendations for approval, and state which surfaces you did not assess. Apart from a temporary break you revert to falsify a test, do not modify repository files, and do not publish issues or PRs without approval.

Shared state: follow the run contract in ~/.local/state/automation-runs/README.md for the `test-audit` folder; clone <your private automation-state repository> there first if it is missing. Before you start, read that folder's decisions.md and its three newest runs from any host. When you finish, write this run's file there and push it. When the owner answers your findings, record the answers in decisions.md and push before acting on them.
```
