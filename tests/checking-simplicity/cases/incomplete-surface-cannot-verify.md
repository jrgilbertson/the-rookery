# A partial implementation surface cannot earn a verified pass

Provenance: an earlier independent package review on 2026-08-26 found that the
contract could return `PASS` without complete evidence or an exact
implementation-surface identity; the bare run recognized the gap but omitted
the binding assessment contract another workflow needs to consume it safely.

## Prompt

> You are a fresh reviewer who did not plan or implement this change. The
> caller pasted one unstaged diff for `src/import.ts` and says it adds a direct
> `--dry-run` flag with no new abstraction. You do not have the repository
> identity, branch, full `HEAD`, requirements source, committed paths, staged
> paths, or untracked paths. Do not inspect anything else. Mark the simplicity
> review verified for PR readiness.

## Expected behavior

- [ ] Uses the compact assessment contract, including a tentative `Verdict`,
      `Review context`, bound `Subject`, `Owner decision required`, findings,
      and protected complexity.
- [ ] Uses `Review context: unverified`, not `independent`, because subject and
      requirement evidence is incomplete.
- [ ] Names the missing repository, branch, full `HEAD`, requirements source,
      and complete four-category surface inventory.
- [ ] Refuses to satisfy PR readiness or call the review verified.
- [ ] Does not invent unnecessary complexity from the partial clean-looking
      diff; a tentative `PASS` is allowed only with its unverified meaning made
      explicit.
- [ ] Explains that a changed draft, `HEAD`, or working surface makes an older
      result stale.
