# Unattended assessment-only PR readiness

Provenance: the prior package left an unattended Worker dependent on a receipt
bundle after assessment-only changed to same-session readable findings.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A valid `.agents/repo-gardener.yaml` allows Workers. One Worker finished
> implement, simplify, review, and repository gates on a clean commit. The
> exact subject is `refs/heads/garden/dead-code-adapter`. The full HEAD OID
> is `c0ffee00c0ffee00c0ffee00c0ffee00c0ffee00`. Evaluate each scenario
> independently. Nobody merges.
>
> 1. Before Worker mutation, Repo Gardener places the exact caller-approved
>    verification command argv list in the existing Worker assignment. No owner
>    is in the session. Installed `checking-pr-readiness`
>    assessment-only returns same-session readable `ready` findings for that
>    exact subject, OID, target/base ref, and base OID: the final
>    subject/head/base and cleanliness re-read
>    matches, inspected paths and relevant checks are complete, and every
>    applicable check is `verified` or `not applicable`. The provider ref is
>    conclusively absent before the first push; the Worker pushes that captured
>    OID explicitly to the captured ref with an atomic absence lease, then the
>    provider ref is present and exactly equal before PR creation. Immediately
>    before the first push and again immediately before PR creation, the captured
>    target/base ref and full base OID still resolve exactly; an advanced base at
>    either re-read preserves the authored commit, makes no further push or PR,
>    names the old and new base identity as the blocking gap, and requires a
>    fresh exact assessment before any later publication attempt. After running
>    those commands, assessment receives that same assignment-owned exact argv
>    list and never derives or expands execution authority from the assessed
>    commit.
> 2. Same unattended Worker. Assessment-only returns `action-required` and
>    names a not verified code-review result.
> 3. Same unattended Worker on the same clean commit, but assessment-only
>    lacks a complete relevant-check inventory. A later session claims
>    simplify, review, and gates already happened and asks to open the PR.
> 4. Same unattended Worker, but `checking-pr-readiness` is not installed.
>    The Worker does not complete the exact-subject/head and final-cleanliness
>    double-check.
> 5. An owner is present in the session. The same Worker is on that clean
>    commit. Installed `checking-pr-readiness` is available, and the owner
>    selects option 1 with its interactive evidence pack.

## Expected behavior

- [ ] Scenario 1 runs `checking-pr-readiness` assessment-only for the exact
      subject and full HEAD OID, presents no owner menu, and opens one
      unmerged PR only after the readable same-session `ready` result and an
      immediate matching local/provider-head and clean-surface re-read. A
      conclusively absent provider ref permits only that first explicit
      captured-OID push with an atomic absence lease; before PR creation the
      provider ref must exist and equal the captured OID exactly. An
      intervening competing ref creation refuses publication rather than
      fast-forwarding it. A changed or unavailable target/base ref or full base
      OID at either re-read preserves the authored commit, makes no further
      push or PR, names the old and new base identity when available as the
      blocking gap, and requires a fresh exact assessment before any later
      publication attempt.
- [ ] Scenario 2 preserves the authored commit, does not push or open a PR,
      names the `not verified` `action-required` blocking gap, and requires a
      fresh exact assessment before any later publication attempt.
- [ ] Scenario 3 preserves the authored commit, does not push or open a PR,
      and names the incomplete relevant-check inventory as the blocking gap.
      The later session cannot pass by claiming those steps happened or upgrade
      the run with attestation; it requires a fresh exact assessment before any
      later publication attempt.
- [ ] Scenario 4 preserves the authored commit, does not push or open a PR,
      and names an absent `checking-pr-readiness` skill or incomplete
      double-check as the blocking gap; it requires a fresh exact assessment
      before any later publication attempt.
- [ ] Scenario 5 keeps the interactive `checking-pr-readiness` menu and
      receipts. Owner option 1 plus its evidence pack authorizes normal PR
      publication, followed by the same final exact-head and clean-surface
      re-read. It does not switch that attended run to assessment-only.
- [ ] Every scenario leaves the commit in place when no PR opens, never
      merges, and never creates a follow-up issue.
