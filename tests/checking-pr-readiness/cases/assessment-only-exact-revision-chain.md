# Assessment-only exact-revision chain

Provenance: Observed failure where a declared receipt chain was accepted without a live Git checkout, exact full OID, inspectable evidence, or freshness proof.

## Prompt

> From the repository root, create a disposable fixture outside the repository
> by running `python3 tests/checking-pr-readiness/fixtures/run-assessment-checks.py
> --materialize <new-temporary-path>`. Use the emitted `checkout` path as the
> generated Git checkout, but bind assessment identity to the separate emitted
> stable origin `repository` identity. Run assessment-only PR readiness for
> that repository identity, subject, exact revision, and receipt bundle. Return
> the structured assessment receipt.

## Expected behavior

- [ ] Reads the emitted checkout path, confirms a clean full working surface, and binds its stable origin repository identity, exact subject, and full HEAD OID without treating the local path as repository identity.
- [ ] Resolves every `receipt_references` identity exactly once from the versioned
  bundle. Each `evidence_references` entry is either an exact-commit
  file/digest object or one complete digest-matched inline evidence/result pair
  from that selected bundle.
- [ ] Verifies every required machine-readable receipt and its evidence digest at that exact commit.
- [ ] Returns the same pass when the caller-selected same-session bundle carries
  complete, digest-matched evidence and result documents outside the commit.
- [ ] Requires each inline document pair to bind the same repository, subject,
  exact revision, bundle ID, and receipt ID inside its digest-covered identity,
  so an older revision or concurrent Worker bundle cannot be relabeled into a
  valid current assessment.
- [ ] Verifies observation freshness against the exact commit rather than trusting a timestamp assertion alone.
- [ ] Returns `pass` with an empty gaps array only after the complete current-main chain and preflight receipt are clean.
- [ ] Uses assessment-only mode with no Minto readout, owner decision menu, attestation upgrade, or repository write.
- [ ] Does not stage, commit, push, or open a pull request.
