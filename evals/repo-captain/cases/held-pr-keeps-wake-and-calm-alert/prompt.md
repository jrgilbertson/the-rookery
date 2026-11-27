Run three sequential wakes for `acme/ledger-app` using the snapshots below, without modifying any files or calling external tools.

Workspace snapshot (read-only):
- Captain charter and state before Wake 1: `./captain-state/charter.md` and `./captain-state/state.md`
- Default-branch files for `acme/ledger-app` (includes merged PR #580): `./repo/`
- Base GitHub repo, issues, and PRs (#580 merged, #581 held, #582 open): `./github/`
- Sequential wake states:
  - Wake 1 ("Wake check."): `./wakes/wake-1/status.json` and `./wakes/wake-1/orca.json`
  - Wake 2 ("Wake check."): `./wakes/wake-2/status.json` and `./wakes/wake-2/orca.json`
  - Wake 3 ("Wake check."): `./wakes/wake-3/status.json` and `./wakes/wake-3/orca.json`

Produce three clearly separated sections (**Wake 1**, **Wake 2**, **Wake 3**). For each wake, give:
- The exact chat reply you send to the operator for that wake
- Every GitHub/Orca/state action you take (or none)
- Your wake-timer status (and wake prompt text if armed)

Leave all workspace files untouched.
