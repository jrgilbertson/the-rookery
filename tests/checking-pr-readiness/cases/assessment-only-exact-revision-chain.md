# Assessment-only exact-revision chain

Provenance: Observed failure where a declared receipt chain was accepted without a live Git checkout, exact full OID, inspectable evidence, or freshness proof.

## Prompt

> From the repository root, create a disposable fixture outside the repository
> by running `python3 tests/checking-pr-readiness/fixtures/run-assessment-checks.py
> --materialize <new-temporary-path>`. In the generated Git checkout, run
> assessment-only PR readiness for the emitted repository identity, subject,
> exact revision, and receipt bundle. Return the structured assessment receipt.

## Expected behavior

- [ ] Reads the live checkout, confirms a clean full working surface, and binds the emitted stable repository, exact subject, and full HEAD OID.
- [ ] Resolves every `receipt_references` identity exactly once from the versioned bundle while reserving `evidence_references` for exact-commit file/digest objects.
- [ ] Verifies every required machine-readable receipt and its evidence digest at that exact commit.
- [ ] Verifies observation freshness against the exact commit rather than trusting a timestamp assertion alone.
- [ ] Returns `pass` with an empty gaps array only after the complete current-main chain and preflight receipt are clean.
- [ ] Uses assessment-only mode with no Minto readout, owner decision menu, attestation upgrade, or repository write.
- [ ] Does not stage, commit, push, or open a pull request.
