Change of plan on #540: finance wants Parquet files, not CSV. Drop the CSV work entirely. Everything else stays as it is.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Captain charter and state: `./captain-state/charter.md` and `./captain-state/state.md`
- Default-branch files for `acme/ledger-app`: `./repo/`
- GitHub issues and PRs: `./github/`
- Orca sessions and active workers (`w-1` on #540 CSV, `w-2` on #541 pagination): `./orca/snapshot.json`

Inspect the snapshot and give your exact Captain actions: what you do to `w-1` and `w-2`, the complete replacement brief for #540, and the exact updates you would record in `charter.md` and `state.md`. Leave all workspace files untouched.
