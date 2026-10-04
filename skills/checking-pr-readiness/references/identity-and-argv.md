# Exact-head identity and caller argv

Every run of this skill binds one native subject in the same assessment session.
SKILL.md owns the brief, numbered live options, and the wait for a numbered
reply.

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

## Simplicity identity

Record this identity at the end of step 1, in that step's temp directory, for
every gather, including when `checking-simplicity` is not dispatched. Do not
print it. Do not write it into the repository, the evidence pack, or the
readout. Approve and recompose compare this same record. The record is
the head OID, plus for staged, unstaged, and untracked paths only, each path,
mode, and content digest. That digest is the blob digest of the path's
contents, or of the link text when the path is a symlink. The committed
category is the head OID. Do not hash every committed blob. A new head,
including a message-only amend, restarts the simplicity check. A new commit
on the branch restarts the simplicity check.

For a staged path, record the mode and object from `git ls-files --stage` and
do not open the path. A staged deletion is the path with no blob. For an
unstaged or untracked path, test `[ -L "$path" ]` before any executable test,
because an executable test follows the link. Store a symlink as its link text
and never follow it: mode `120000`, and pipe that text to
`git hash-object --stdin` with no added newline. Do not run `git hash-object`
on the symlink path. For any other worktree file, record mode `100755` when
it is executable and `100644` otherwise.
Hash that file with `git hash-object --no-filters -- "$path"`.
An unstaged deletion is the path with no blob.

`surface-report.sh` lists paths and does not emit content digests. Do not
treat its path lists as this identity. An in-place edit of an already-listed
path does not change that listing, which is why the digest is required.

Compare the identity again when the simplicity result returns, so an in-place
edit during the check is caught. When the recorded head OID and the staged,
unstaged, and untracked path, mode, and content digest match, the clean result
counts, including a same-context result, and file bodies are not re-read to
prove it. The readout does not contain the digest or the commit hash. A
mismatch restarts the check. If the result returns after an in-place edit of
an already-listed path, that second compare restarts the check. Outside the
session the result stays not verified. The simplicity result does not replace
the whole-change grade.

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

Capture helper stdout into the owner-only `mktemp -d` directory outside the
target repository from SKILL.md step 1. Do not echo it. If that exact selector binding is unavailable, mismatched,
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
re-read the working-surface identity recorded at the end of step 1 rather
than the file bodies. That identity is the head OID and the staged, unstaged,
and untracked path, mode, and content digest. A missing record is unavailable
state. A same-name base OID change names the new base in one sentence and
keeps Approve. There is no GitHub mergeability object yet; do not invent a
conflict check. Do not stop pre-push or pre-PR publication solely for that
move.

A subject change, a head change, a base-ref rename, or a dirty surface that
differs from the recorded surface rejects the prior findings and requires a
fresh run. The recorded surface for that compare is the step-1 identity, so
a changed digest differs even when the path list does not. The compare runs
whether or not `checking-simplicity` was dispatched. A change to
staged, unstaged, or untracked files restarts the PR-readiness grade even
when the head commit is unchanged, and it restarts the simplicity check. A
changed digest on the dirty surface restarts the PR-readiness grade and the
simplicity check. A finished merge-readiness grade is about the pull-request
head, so this dirty-surface change does not restart it. Name the old and new
subjects when the subject changed, the old and new full OIDs when the head
changed, the old and new base identity when the base ref changed, and the old
and new paths and categories when working-tree content changed. Do not print
the blob digest. The already-typed 1 does not approve that rebuilt gather. If
any required state is unavailable, name every exact gap and omit Approve. Do
not reuse findings across a moved head, a renamed base ref, or a dirty
surface that differs from the recorded surface. Any other matching re-read is
silent. The one-sentence base naming is not a rebuild.

This skill remains read-only except for remaining-changes follow-up
picks and the option-1 finishing dispatch. A companion skill or repository
gate owns those writes. It does not itself stage, commit, push, open,
or merge a pull request.
