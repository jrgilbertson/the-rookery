# Synthetic reconciliation matrix

`scenarios.json` contains source facts only. The checker derives outcomes from
caller ownership, ordered gates, receipt coverage, capacity, and lifecycle
ordering before comparing them with `expectations.json`; the expectation file
is never used as an evaluator. Mutations pin each load-bearing decision input.
`lane-receipts.json` supplies terminal coverage for the ordered manifest.
`wrapper-readbacks.json` is a test-only narrow-wrapper stub. It supplies
completed persistence/readback facts to the executable contract without
adding a prompt-triggered fixture exception to the shipped skill.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/reconciliation/check_decisions.py
```
