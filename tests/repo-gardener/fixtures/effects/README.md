# Synthetic report-effect matrix

These fixtures grade Release A's report-register effect protocol. The checker
passes scenario facts through the shipped `effect-v1` and `completion-v1`
subprocess interfaces, then compares their results with the separate
expectation file. It mutates every load-bearing authority, readback, identity,
compatibility, completion, ownership, and precondition field so an inert field
cannot leave the suite green. All identities and outcomes are synthetic.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/effects/check_effects.py
```
