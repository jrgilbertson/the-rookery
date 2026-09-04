# Synthetic tracker-effect matrix

These fixtures grade two-comment preparation and verification. The checker
passes complete synthetic GitHub snapshots through the shipped `effect`
prepare/verify interface, then compares results with the separate expectation
file. It mutates load-bearing readback and identity fields and proves mention
and image rejection. Caller authority and verdict fields are rejected rather
than trusted. Hash fields and Current Portfolio JSON are not required.

Run from the repository root:

```bash
python3 tests/repo-gardener/fixtures/effects/check_effects.py
```
