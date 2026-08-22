# Run record fixtures

`check_run_records.py` exercises the public `effect-v1` and `run-records-v1`
interfaces against synthetic GitHub issue snapshots. It proves that one run ID
owns exactly two managed comments, opened then closed, after exact readback.
Comments remain valid without hash fields. Current Portfolio JSON is not
required. A denied close is an interrupted run, not a fabricated closed record.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/run-records/check_run_records.py
```
