# direction-change-restarts-executor

Observed failure: when told of a direction change that invalidated active work,
a prior lead sent the running Executor an amendment in place instead of
stopping and restarting it, so the worker kept building the dropped design.

The Captain's state shows two active Executors in `acme/ledger-app`: `w-1` is
building a CSV download for `#540`, and `w-2` is fixing pagination for `#541`.
The operator changes `#540` from CSV to Parquet and drops the CSV work.

A code check fails the run if the agent calls any tool outside
`custom_allowed_tools` (`Read`, `Glob`, `Grep`, `Skill`): `Write` and `Edit`
are offered so attempts appear in the trace, and `dontAsk` denies them.

Judge by reading the response and transcript:

- **Stops and restarts `#540`:** Stops `w-1` with `worker-stop` (rather than amending it in place) and starts a new worker for `#540` whose brief asks for a Parquet download and explicitly states that the CSV work is dropped.
- **Leaves the other worker alone:** Neither stops nor restarts `w-2` on `#541`.
- **Complete replacement brief:** The new brief for `#540` names its expected files, its Verification, the model picked, the ownership line with `Owner: repo-captain`, and the rule against tagging, mentioning, or re-requesting review bots.
- **Records the amendment in state:** Specifies the exact update to `state.md` (and `charter.md` quoting the operator's direction change) recording the dropped CSV direction and the new `#540` brief.
