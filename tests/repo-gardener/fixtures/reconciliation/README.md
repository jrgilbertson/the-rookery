# Synthetic reconciliation matrix

`scenarios.json` contains source facts only. The checker derives outcomes from
ordered gates, receipt coverage, capacity, and lifecycle
ordering before comparing them with `expectations.json`; the expectation file
is never used as an evaluator. Mutations pin each load-bearing decision input.
`lane-receipts.json` supplies terminal coverage for the ordered manifest.
`wrapper-readbacks.json` supplies synthetic complete pre/post GitHub snapshots
for deterministic effect preparation and verification.
The three immutable receipt collection envelopes are passed through the
production CLI and validated for every derivation; scenario derivations then
exercise the shipped `reconciliation-v2`,
`gates-v1`, and `capacity-v1` subprocess interfaces.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/reconciliation/check_decisions.py
```
