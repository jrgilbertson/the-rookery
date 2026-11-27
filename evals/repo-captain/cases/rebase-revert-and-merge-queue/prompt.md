Prior conversation:
- User (Wake 1): "Wake check."
- Assistant (Wake 1): "Nothing new: #560 and #561 are still waiting for verdicts. Wake timer stays running."

Current turn (Wake 2):
Verdicts are in.

Workspace snapshot (read-only; do not modify any files or call external tools):
- Captain charter and state: `./captain-state/charter.md` and `./captain-state/state.md`
- Default-branch files for `acme/ledger-app` (includes merged PR #559): `./repo/`
- Current GitHub state (merge queue enabled, issues, PRs #559/#560/#561, verdicts, current diffs vs `main`, reviewed-head diffs, and reviewed-to-current range-diff comparisons): `./github/`
- Follow-up merge-queue wake events (Wake 3 ejection of #560 at unchanged head; Wake 4 confirmed merge of #560): `./github/follow-up-wakes.json`
- Orca sessions and workers: `./orca/snapshot.json`

Inspect the snapshot and produce three clearly separated sections without modifying any files:
1. **Wake 2 (now, "Verdicts are in"):** Compare each reviewed head against each PR's current head, then give your exact merge-queue/hold decisions, `--match-head-commit` SHAs, receipts, open decision/operator notice, and label status (note whether any rebase/push or label change happens while queued).
2. **Wake 3 (`wake3` in `./github/follow-up-wakes.json`):** Your exact action after the merge queue ejects #560 at its unchanged head.
3. **Wake 4 (`wake4` in `./github/follow-up-wakes.json`):** Your exact label, tracker, worktree, and state updates once GitHub confirms #560 is `MERGED`.
