Review round please: everything open, plus whatever merged without me since November 13.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Viewer, organizations, and snapshot timestamp (`2026-11-20T17:00:00Z`): `./github/viewer.json`
- Repositories, default-branch guidance, open and merged pull request lists, PR metadata, comments, and raw diffs (`acme/ledger-app`, `acme/cli-kit`, `acme/handbook`): `./github/repos/`

Inspect the snapshot and produce three clearly separated sections without modifying any files:
1. **Review-page data:** The structured round data covering the open pull requests and everything merged since November 13, 2026.
2. **Local review-page build:** How you would render and handle the local review page (location, permissions, escaping, and security checks) if writing it to disk.
3. **Operator summary:** The short summary for the operator covering the round order, risk drivers, and what, if anything, would be written to GitHub.
