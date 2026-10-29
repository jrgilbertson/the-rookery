# Test audit

Review the repository's tests, find gaps in what they protect, and recommend improvements.

- **Cadence:** Thursday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-simplify-code` skill and access to the target repository.

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
```
