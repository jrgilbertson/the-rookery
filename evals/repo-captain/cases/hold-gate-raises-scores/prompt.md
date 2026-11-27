Wake check.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Captain charter and state: `./captain-state/charter.md` and `./captain-state/state.md`
- Default-branch files for `acme/ledger-app`: `./repo/`
- GitHub issues (with stored scores) and four open green PRs (#550, #551, #552, #553) with raw diffs: `./github/`
- Orca sessions and workers: `./orca/snapshot.json`

Inspect the snapshot and give your exact Captain actions for this wake: your diff-based scoring and merge/hold decision for each of #550–#553 (with exact `--match-head-commit` SHAs, receipts, and label changes), every tracker score edit you would make (showing old value, new value, and reason), any scores you leave unchanged, and your state/wake updates. Leave all workspace files untouched.
