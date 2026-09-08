# Trigger contract: checking-merge-readiness

The description is a tested activation API. Judges see only a realistic skill
listing (both siblings plus PR-management one-liners: ce-babysit-pr,
ce-code-review, ce-commit-push-pr) and one user query, blind to the expected
direction. Expected outcome is the skill name a correct judge picks, or `none`.

## PR-management one-liners in the judged listing

These three skills live outside this repository and stand in for the
PR-management neighbors a real listing would carry; a judge sees only the
descriptions below, exactly as written here.

- ce-babysit-pr: "Watches an already-open pull request through its review and CI cycle, resolving feedback until it is merge-ready."
- ce-code-review: "Performs a code review of changes and reports the findings."
- ce-commit-push-pr: "Commits, pushes, writes the pull request description, and opens the pull request."

## Should trigger (expected: checking-merge-readiness)

- S1. "Is this PR safe to merge?"
- S2. "The bots left like 50 comments on my PR. Digest what happened before I merge it."
- S3. "What did all those review rounds actually do to this PR?"
- S4. "Should I merge #42?"
- S5. "After all those review fixes, is this still the change I set out to make?"
- S6. "Give me a pre-merge readout of this pull request."
- S7. "Merge this PR."

## Near miss (expected: the named other skill, or none)

- N1. "Is this branch ready for a PR?" Expected: checking-pr-readiness (pre-PR gate owns branch readiness).
- N2. "Watch this PR and handle the review feedback as it comes in." Expected: ce-babysit-pr (PR management, excluded).
- N3. "Review this code before I put up a PR." Expected: ce-code-review (performing review, excluded).
- N4. "Write a good PR description for this branch." Expected: ce-commit-push-pr (finishing path, excluded).
