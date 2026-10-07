# Review identity and caller argv

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

## Content-review identity

Record this identity at the end of step 1, in that step's temp directory, for
every gather, including when `checking-simplicity` is not dispatched. Do not
print it. Do not write it into the repository, the evidence pack, or the
readout. Keep the full head OID for publication binding separately from the
inputs a diff or simplicity review judges:

- Native subject and target/base ref.
- Committed tree OID from `git rev-parse --verify HEAD^{tree}`.
- Comparison base OID from `git merge-base HEAD "$captured_base_oid"`.
- Selected intent source and the objective, required behavior, hard constraints,
  and verification criteria supplied to the reviewer.
- For staged, unstaged, and untracked paths only, each path, mode, and content
  digest. That digest is the blob digest of the contents or symlink text.

Git's tree OID covers committed paths, modes, and contents; do not hash every
committed blob. A new head alone, including a message-only amend, does not
restart the diff grade or simplicity check when these inputs match. Rebind to
the current full head and refresh only checks whose inputs changed, such as
commit-message, ancestry, signature, or head-specific repository gates. A
content-review result does not verify those checks. Their owner still controls
reruns; unavailable required evidence withholds Approve.

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
edit during the check is caught. When the recorded content-review inputs
match, the clean result
counts, including a same-context result, and file bodies are not re-read to
prove it. The readout does not contain the digest or the commit hash. A
mismatch reruns checks whose inputs changed. If the result returns after an in-place edit of
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
full head, target/base ref, and full base OID through the same boundary.
Compare the content-review inputs recorded at the end of step 1 rather than
re-reading file bodies for judgment. Refresh the selected intent source's
decision frame; an edited source whose reviewed requirements still match
does not itself invalidate the review. A missing record is unavailable state.
A same-name base OID change names the new base in one sentence and keeps
Approve when the comparison base and required check inputs still match.
There is no GitHub mergeability object yet; do not invent a
conflict check. Do not stop pre-push or pre-PR publication solely for that
move.

A subject change, a base-ref rename, changed comparison base, changed intent
frame, changed committed tree, or a dirty surface that differs from the
recorded surface invalidates affected findings and recomposes the gather.
A changed digest differs even when the path list does not. This compare runs
whether or not `checking-simplicity` was dispatched. Changed content or review
context restarts the diff grade and simplicity check. Name the old and new
subjects, old and new full OIDs, old and new base identity, or changed paths
and categories as applicable; do not print blob digests.
The already-typed 1 does not approve that rebuilt gather. Missing required
state or an unresolved head-specific check omits Approve. When only the full
head changed and the content-review inputs match, retain those reviews and
refresh the head-specific checks. If those checks leave the recommendation
Approve, update the head binding and continue finishing with the existing 1;
do not request the same approval again. Otherwise recompose without finishing.
A finished merge-readiness grade still binds the exact PR head: these reuse
rules never authorize merging a new OID, and local dirt does not restart that
merge grade. Any other matching re-read is silent. The one-sentence base
naming is not a rebuild.

This skill remains read-only except for remaining-changes follow-up
picks and the option-1 finishing dispatch. A companion skill or repository
gate owns those writes. It does not itself stage, commit, push, open,
or merge a pull request.
