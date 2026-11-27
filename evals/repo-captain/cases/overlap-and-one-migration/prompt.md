Captain for acme/ledger-app. Scope: #520, #521, #522, #525, #526, and #527. #520 already has a worker on it. Merge Approval: merge routine PRs yourself and hold the rest for me. My verdicts on #531 and #532 are in.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Default-branch files for `acme/ledger-app`: `./repo/`
- Current GitHub state (merge queue enabled, issues, open PRs #530/#531/#532 with diffs and verdicts): `./github/`
- Current Orca state (active worker `w-1` on #520): `./orca/snapshot.json`
- Follow-up wake state once whichever single migration PR you enqueue finishes merging: `./github/next-wake.json`

Inspect the snapshot and produce two clearly separated sections without modifying any files:
1. **Wake 1 (now):** Your exact dispatch and serialization decisions (naming each overlapping file), exact merge-queue enqueue action(s) with `--match-head-commit`, any label changes (or why labels wait), and charter/state updates.
2. **Wake 2 (after the follow-up state in `./github/next-wake.json`):** Your exact label updates, next merge-queue action with `--match-head-commit`, and whether #525 or #526 can dispatch yet.
