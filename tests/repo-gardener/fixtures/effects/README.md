# Synthetic report-effect matrix

These fixtures grade Release A's report-register effect protocol. The checker
passes complete synthetic GitHub snapshots through the shipped `effect-v1` v2
prepare/verify and `completion-v1` subprocess interfaces, then compares their
results with the separate expectation file. It mutates every load-bearing
readback, identity, compatibility, completion, and precondition field. Caller
authority and verdict fields are rejected rather than trusted. All identities
and outcomes are synthetic; snapshot provenance remains unverified.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/effects/check_effects.py
```
