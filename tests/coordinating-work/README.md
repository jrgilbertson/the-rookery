# Coordinating Work verification

Run the existing deterministic package, catalog, repository, secrets, and helper
checks through the complete gate:

```sh
lefthook run pre-push --force
```

This prose package adds no executable helper or behavioral runner. Its one
fixture, `fixtures/run-boundary-checks.sh`, pins the sentences that carry the
merge guards: workers never merge, the merge approval comes only from the
approved proposal, nothing merges unless every checklist line is true,
held-change pull requests stay open unless pre-authorised, nothing produced
during a run widens the merge approval, and deploying, spending,
force-pushing, and destructive actions wait for the operator. It also pins one
sentence for each batch rule: branch currency left to a merge queue or an
enforced up-to-date rule, follow-ons started fresh, usage-limit prompts,
replies that keep the repository's gates whole, incidental work, closing an
issue only after its completion check, outside-service outages, short
merge-ready questions, held changes chosen at setup, and defaults reported with
every update. Two patterns are
forbidden anywhere in the skill: asking the watch to keep the branch current,
and a tracker's issue identifier. The fixture fails when a pinned sentence is
removed or a forbidden pattern appears, and proves both on a scratch copy each
run. It does not show that an agent obeys
them. The gate checks package validity and repository integration; it does not
establish successful team setup, unattended merging, conversation
continuation, or recovery. Name the
candidate, host, provider, and surface for any observed result; unavailable
evidence remains Unmeasured.

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow) for error analysis of real
usage. The package starts without a speculative case corpus. If an observed
failure persists after instruction fixes and warrants repeat measurement,
prepare a targeted case through the maintained evaluation workflow. Preserve
the source evidence privately, and use privacy-safe inputs for public fixtures.
Keep grader expectations outside the executor's access. Required input/grading
approval does not authorize model calls or live-team operations.
