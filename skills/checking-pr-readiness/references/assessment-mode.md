# Exact-head identity and caller argv

Every run of this skill binds one native subject in the same assessment session.
There is no separate assessment-only form. SKILL.md owns the brief, numbered live
options, and the wait for a numbered reply.

## Bind the native subject, full head, and base

At the start, resolve the selected native subject through its authoritative
read-only boundary and capture its full head, target/base ref, and full base
OID once. For a checked-out branch, read the live branch ref and run:

```sh
git rev-parse --verify HEAD^{commit}
```

For a pull-request subject, read the provider's current head OID through the
caller's read-only boundary and require the checkout to match it. If the
subject is unavailable, ambiguous, or does not match the checkout, name that
gap, omit Approve, and wait for a numbered reply. Never infer the subject
from a display name or an earlier report. Resolve the selected target/base
ref and its full commit OID through that same boundary; an unavailable or
ambiguous base is the same omit-Approve gap.

Staged, unstaged, or untracked paths are part of the working surface, not
covered by the full head. Name every affected category and path in the
gather. They ship if option 1 is taken.

## Helper base binding

Before each helper whose result depends on the base, require its base
selector to resolve exactly to the captured full base OID. The existing
surface helper accepts a branch selector rather than a raw OID, so derive the
selector from the captured target/base ref and first prove that its
branch-namespace resolution still yields the captured full base OID, then
run:

```sh
surface-report.sh --base "$captured_base_selector" --full
```

Capture helper stdout into the owner-only temp directory from SKILL.md step
1. Do not echo it. If that exact selector binding is unavailable, mismatched,
or cannot be re-resolved, record the helper as `not verified` and omit
Approve; do not fall back to its implicit default base. Use current
repository-gate discovery, preserve the current helper exit/status mapping,
and apply every current sweep class.

The captured gather must include every inspected path and every relevant check.
Incomplete gather cannot offer Approve.

## Caller-owned commands

A repository-authored check may be rerun only from a caller-authorized exact
argv list, through the existing constrained direct-argv safety boundary
without a shell, production credentials, unrelated-file access, or network
unless separately authorized. Assessment never derives or expands authority
from assessed content. Otherwise record the check as `not verified` and omit
Approve.

## Deferred sweep classes

A sweep-class `--defer` outcome may normalize from `skipped` to `verified`
evidence only when its exact named equivalent repository gate is present and
`verified` in the same complete assessment session. A bare, missing,
unrelated, mismatched, unavailable, or not verified gate leaves the skipped
class as a named gap; do not accept skipped classes generally.

An unresolved finding is named as next work attached to an allowed status,
for example `code review: not verified`. Check-result spelling is canonical:
`not verified` and `not run`.

## Re-read before option 1

Immediately before accepting Approve, re-resolve the same native subject,
full head, target/base ref, and full base OID through the same boundary and
re-read staged, unstaged, and untracked content. If the subject, head, base
ref, or base OID differs from the captured state, reject the prior findings,
name the old and new subjects when the subject changed, the old and new full
OIDs when the head changed, and the old and new base identity when the base
changed, then require a fresh run. If any required state is unavailable, name
every exact gap and omit Approve. Do not reuse findings across moved heads or
bases. A matching re-read is silent.

This skill remains read-only except for dispatching a present companion skill
from the live menu. It does not write to the repository, stage, commit, push,
or open a pull request.
