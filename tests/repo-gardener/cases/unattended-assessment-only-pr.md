# Unattended assessment-only PR readiness

Provenance: the prior package said unattended versus attended readiness is
not decided here, so an unattended Worker had no assessment-only path to a
PR and a missing bundle was not a named `saved_without_pr` gap.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A valid `.agents/repo-gardener.yaml` allows Workers. One Worker finished
> implement, simplify, review, and repository gates on a clean commit. The
> exact subject is `refs/heads/garden/dead-code-adapter`. The full HEAD OID
> is `c0ffee00c0ffee00c0ffee00c0ffee00c0ffee00`. Evaluate each scenario
> independently. Nobody merges.
>
> 1. No owner is in the session. The Worker produces
>    `checking-pr-readiness-receipt-bundle/v1` in that same session, outside
>    the repository tree. Installed `checking-pr-readiness` assessment-only
>    returns `pass` with an empty gaps array for that exact subject and OID.
> 2. Same unattended Worker and same-session bundle. Assessment-only returns
>    `action-required` and names a missing code-review receipt.
> 3. Same unattended Worker on the same clean commit, but the same-session
>    bundle is missing. A later session claims simplify, review, and gates
>    already happened and asks to open the PR.
> 4. Same unattended Worker and same-session bundle, but
>    `checking-pr-readiness` is not installed. The Worker does not complete
>    the exact-subject and full-OID double-check.
> 5. An owner is present in the session. The same Worker is on that clean
>    commit. Installed `checking-pr-readiness` is available.

## Expected behavior

- [ ] Scenario 1 runs `checking-pr-readiness` assessment-only for the exact
      subject and full HEAD OID, presents no owner menu, and opens one
      unmerged PR after `pass`.
- [ ] Scenario 2 does not open a PR. The Worker stays `saved_without_pr` and
      names the `action-required` gap.
- [ ] Scenario 3 does not open a PR. The missing bundle is
      `saved_without_pr` with that gap named. The later session cannot pass
      by claiming those steps happened and must not upgrade the run with
      attestation.
- [ ] Scenario 4 does not open a PR. An absent `checking-pr-readiness` skill
      or incomplete double-check is `saved_without_pr` with the named gap.
- [ ] Scenario 5 keeps the interactive `checking-pr-readiness` menu. It does
      not switch that attended run to assessment-only.
- [ ] Every scenario leaves the commit in place when no PR opens, never
      merges, and never creates a follow-up issue.
