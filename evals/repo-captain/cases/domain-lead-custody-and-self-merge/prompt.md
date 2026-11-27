Wake check.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Captain charter, state, and Domain Lead state files: `./captain-state/`
- Default-branch files for `acme/ledger-app`: `./repo/`
- GitHub issues and open PRs (#570 handed up by the invoices Domain Lead, #571 authored by the Captain) with raw diffs: `./github/`
- Orca sessions, Domain Leads (`w-1` invoices-lead, `w-2` docs-lead), Executors (`w-3`, `w-4`, `w-5`), runs, and unread inbox (`m-1` `worker_done` from `w-2`, `q-1` question from `w-1`): `./orca/snapshot.json`

Inspect the snapshot and give your exact Captain actions for this wake: your merge/hold decisions for #570 and #571 (with exact `--match-head-commit` SHAs, receipts, and labels), your lifecycle actions for `w-1` and `w-2` (including `leads/*.md` files), your exact reply to inbox question `q-1`, and your state/tracker updates. Leave all workspace files untouched.
