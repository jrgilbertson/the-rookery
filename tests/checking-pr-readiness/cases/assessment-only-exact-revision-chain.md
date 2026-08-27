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
- [ ] Returns the same pass when the documented top-level bundle shape contains
  only `schema`, `assessment`, and `receipts`, while its caller-selected
  same-session inline references carry complete, digest-matched evidence and
  result documents outside the commit.
- [ ] Requires each inline document pair to bind the same repository, subject,
  exact revision, bundle ID, and receipt ID inside its digest-covered identity,
  so an older revision or concurrent Worker bundle cannot be relabeled into a
  valid current assessment.
- [ ] Derives one shared bundle ID from the documented inline references and
  rejects any disagreement between those references.
- [ ] Verifies observation freshness against the exact commit rather than trusting a timestamp assertion alone.
- [ ] Returns `checking-pr-readiness-assessment/v2`; `pass` has an empty gaps
  array, and every material gap is exactly a producer-owned nonempty `key` plus
  a human-readable `message`.
- [ ] Keeps a material obligation's key stable across different exact heads,
  receipt order, timestamps, and real producer message presentations without
  parsing the key or treating it as a status. Two independent receipt or
  evidence obligations have distinct keys; split or combined details of one
  obligation retain its key without suppressing another.
- [ ] Uses assessment-only mode with no Minto readout, owner decision menu, attestation upgrade, or repository write.
- [ ] Does not stage, commit, push, or open a pull request.
