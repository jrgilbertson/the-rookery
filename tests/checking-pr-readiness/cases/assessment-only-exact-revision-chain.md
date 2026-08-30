# Assessment-only same-session exact head

Provenance: Observed failure where an unattended decision accepted findings from
an older native head instead of inspecting the live checkout in one session.

## Prompt

> From the repository root, create a disposable fixture outside the repository
> by running `python3 tests/checking-pr-readiness/fixtures/run-assessment-checks.py
> --materialize <new-temporary-path>`. Use the emitted checkout for one
> assessment-only PR-readiness session. Capture its native full head and
> target/base ref plus full base OID, inspect
> the complete clean surface and current checks in that same session, establish
> a complete inspected-path inventory and a complete relevant-check inventory,
> prove the captured target/base ref still resolves to that captured full base
> OID, then run `surface-report.sh --base <captured-base-selector> --full`
> rather than allowing its implicit default-base selection,
> run its repository-owned `checks/fixture-quality.sh` command and record its
> actual `verified` result, and establish that every applicable required check
> is `verified` or proven `not applicable`. Re-read that unchanged native
> subject, head, and base immediately before deciding, then return readable
> findings and the resulting decision.

## Expected behavior

- [ ] Reads the emitted checkout path, confirms a clean full working surface,
      and captures the live native branch plus its full HEAD OID, target/base
      ref, and full base OID through the same read-only boundary.
- [ ] Runs steps 1 through 6 in one session, including a captured-base-bound
      `surface-report.sh --base <captured-base-selector> --full`, current
      gate discovery, helper status mapping, and current sweep classes; if the
      selector cannot be proven to resolve to the captured full base OID, it
      returns `action-required` instead of falling back to the implicit base.
- [ ] Executes the fixture repository's `checks/fixture-quality.sh` command
      and records its `verified` result; a workflow name alone is not a
      verified check.
- [ ] Returns readable findings that name the full head, every inspected path, and every relevant check with its result or gap.
- [ ] Re-reads the same native branch, full head, target/base ref, and full
      base OID immediately before deciding; returns `ready` for this stable
      complete case without external packaging or JSON.
- [ ] Uses assessment-only mode with no Minto readout, owner decision menu, attestation upgrade, or repository write.
- [ ] Does not stage, commit, push, or open a pull request.
