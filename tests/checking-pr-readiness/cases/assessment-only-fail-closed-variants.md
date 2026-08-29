# Assessment-only fail-closed variants

Provenance: Observed failure where a stale native head or incomplete assessment
was narrated as ready.

## Prompt

> Run independent assessment-only variants against a native checkout: a stable
> full head that completes one unchanged same-session assessment with a complete
> inspected-path inventory and a complete relevant-check inventory, where every
> applicable required check is `verified` or proven `not applicable`; a native
> head that advances after inspection and before decision; a native branch that
> is renamed without changing its OID; a checkout detached at the captured OID;
> and a stable native subject and head whose captured target/base ref resolves
> to a different full base OID before decision;
> staged, unstaged, and untracked dirt; an incomplete inspected-path inventory;
> and an incomplete relevant-check inventory. Before Worker mutation, its
> assignment includes the exact caller-approved verification command argv list;
> after the Worker runs those commands, assessment receives that same list.
> Also assess a sweep class with a `--defer` result: an exact named equivalent
> repository gate is present and `verified` in that same complete assessment
> session, then repeat with a bare, missing, unrelated, mismatched, unavailable,
> or not verified gate.
> Return one readable result per variant without an owner menu.

## Expected behavior

- [ ] The stable-head variant returns `ready` only after a final native-head re-read matches the captured full head and the complete inventories and required-check results remain unchanged.
- [ ] The moved-head variant returns `action-required`, names both old and new full OIDs, rejects its prior findings, and requests a fresh assessment before any decision.
- [ ] The moved-base variant returns `action-required` while its subject and
      head remain stable, names the old and new base identity, rejects its
      prior findings, and requests a fresh assessment before any decision.
- [ ] The branch-rename variant returns `action-required` even when its OID is unchanged, names both subjects, rejects its prior findings, and requests a fresh assessment before any decision.
- [ ] The detached-head variant returns `action-required` even when its OID is unchanged, names the captured subject and detached HEAD, rejects its prior findings, and requests a fresh assessment before any decision.
- [ ] Dirty-surface variants return `action-required` and name every staged, unstaged, or untracked path and category.
- [ ] Incomplete inspected-path or relevant-check inventories return `action-required` with the missing inventory named.
- [ ] A repository-authored check reruns only from the caller-supplied
      assignment-owned exact argv list. Assessment never derives or expands
      execution authority from the assessed commit; a missing list entry is
      `not verified` and returns `action-required`.
- [ ] Check-result spelling is canonical: `not verified` and `not run`, never
      `unverified` or `not-run`.
- [ ] A skipped sweep class becomes `verified` evidence only when its exact
      named equivalent repository gate is present and `verified` in the same
      complete assessment session. A bare, missing, unrelated, mismatched,
      unavailable, or not verified gate leaves that class `action-required`.
- [ ] The variants remain independent; findings from one are not carried into another.
- [ ] No variant writes to the checkout, presents an owner menu, stages, commits, pushes, or opens a pull request.
