# Identity fail-closed variants

Provenance: Observed failure where a stale native head or incomplete gather
was treated as ready to approve.

## Prompt

> Run independent checking-pr-readiness variants against a native checkout: a
> stable full head that completes one unchanged same-session gather with a
> complete inspected-path inventory and a complete relevant-check inventory,
> where every applicable required check is `verified` or proven `not
> applicable`; a native head that advances after inspection and before
> decision; a native branch that is renamed without changing its OID; a
> checkout detached at the captured OID; and a stable native subject and head
> whose captured target/base ref resolves to a different full base OID before
> decision; staged, unstaged, and untracked dirt; an incomplete
> inspected-path inventory; and an incomplete relevant-check inventory. Before
> Worker mutation, its assignment includes the exact caller-approved
> verification command argv list; after the Worker runs those commands,
> checking-pr-readiness receives that same list.
> Also assess a sweep class with a `--defer` result: an exact named equivalent
> repository gate is present and `verified` in that same complete assessment
> session, then repeat with a bare, missing, unrelated, mismatched, unavailable,
> or not verified gate.
> Brief each variant with numbered live options and wait for a numbered reply.

## Expected behavior

- [ ] The stable-head variant offers option 1 only after a final native-head re-read matches the captured full head and the complete inventories and required-check results remain unchanged.
- [ ] The moved-head variant omits Approve, names both old and new full OIDs, rejects its prior findings, and requires a fresh run before any Approve.
- [ ] The moved-base variant omits Approve while its subject and
      head remain stable, names the old and new base identity, rejects its
      prior findings, and requires a fresh run before any Approve.
- [ ] The branch-rename variant omits Approve even when its OID is unchanged, names both subjects, rejects its prior findings, and requires a fresh run before any Approve.
- [ ] The detached-head variant omits Approve even when its OID is unchanged, names the captured subject and detached HEAD, rejects its prior findings, and requires a fresh run before any Approve.
- [ ] Dirty-surface variants name every staged, unstaged, or untracked path and category as part of the working surface.
- [ ] Incomplete inspected-path or relevant-check inventories omit Approve with the missing inventory named.
- [ ] A repository-authored check reruns only from the caller-supplied
      assignment-owned exact argv list. Assessment never derives or expands
      execution authority from the assessed commit; a missing list entry is
      `not verified` and omits Approve.
- [ ] Check-result spelling is canonical: `not verified` and `not run`, never
      `unverified` or `not-run`.
- [ ] A skipped sweep class becomes `verified` evidence only when its exact
      named equivalent repository gate is present and `verified` in the same
      complete assessment session. A bare, missing, unrelated, mismatched,
      unavailable, or not verified gate leaves that class unable to support
      Approve.
- [ ] The variants remain independent; findings from one are not carried into another.
- [ ] No variant writes to the checkout, picks an option in the same turn, stages, commits, pushes, or opens a pull request.
