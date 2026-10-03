# Merge Execution

Kick off one forge merge. Load after grading when option 1 might be
offered. The write still waits for a numbered reply of option 1. Classify
the live facts in the table below before `gh pr merge`.

## When to offer option 1

Offer only when the pull request is open and non-draft, the
recommendation is merge, the base is not merge-queue governed, and a
method can be resolved without a prompt. Withhold rather than offering
and then refusing, including when write auth is known missing.

Pin `GH_HOST` to the certified host, then this one GraphQL document.
Pass `-H Graphql-Features: merge_queue` (`gh pr merge` does). If the
document errors, a field is missing, or the result is ambiguous, withhold.

```graphql
query($owner: String!, $name: String!, $n: Int!, $base: String!) {
  repository(owner: $owner, name: $name) {
    mergeCommitAllowed
    squashMergeAllowed
    rebaseMergeAllowed
    viewerDefaultMergeMethod
    mergeQueue(branch: $base) { id }
    pullRequest(number: $n) { isMergeQueueEnabled }
  }
}
```

**Queue-off.** `mergeQueue` is null, and `isMergeQueueEnabled` is false
when the schema provides it. Do not treat `isInMergeQueue == false`
alone as queue-off.

**Method.** Exactly one of merge/squash/rebase allowed → that flag.
Several allowed → `viewerDefaultMergeMethod` only when it is still in
the allowed set. Never hardcode squash. Never call `gh pr merge`
without a method flag.

## Option-1 live facts

This table is the option-1 ending. Apply it before the merge command.
The finished grade stands while the pull request's own commit is unchanged,
GitHub reports no conflict, and an uncommitted surface change does not
restart it. Do not reprint that grade on a continue row.

The issue record is number, state, title digest, body digest, and each
comment's id plus body digest. Read the base tip from `baseRefOid`.

| # | Live fact | Grade | This turn | Directory |
| --- | --- | --- | --- | --- |
| 1 | Same baseRefName, new base tip, same head, mergeable MERGEABLE, no GitHub conflict. A patch change GitHub does not call a conflict uses this row. | Stands | Name the new base in one sentence and continue to the existing merge command. Do not reprint the grade. This turn does not grade. | Remove after the merge attempt |
| 2 | updatedAt only | Stands | Silent match. Continue to the existing merge command. | Remove after the merge attempt |
| 3 | Issue title, body, or comment add, edit, or remove | Stands | Continue to the existing merge command. Do not start a review. | Remove after the merge attempt |
| 4 | Head OID change, including a docs-only commit | Void | Stop. This turn does not grade. The next review of the new head grades once. | Remove |
| 5 | baseRefName change | Void | Stop. This turn does not grade. | Remove |
| 6 | Failing or pending required checks | Stands | Stop | Keep |
| 7 | GitHub conflict: mergeable CONFLICTING, or mergeStateStatus DIRTY | Kept, not voided. The finished-grade rule does not hold. | Stop. Do not void. DIRTY is a conflict without a second paragraph of evidence. | Keep |
| 8 | mergeStateStatus BLOCKED with a supporting host fact from the gather. Supporting facts are failing or pending required checks, review count, an unresolved thread the host requires, draft, or a strict up-to-date rule. | Stands | Stop | Keep |
| 9 | mergeStateStatus UNKNOWN and no other block | Stands | UNKNOWN does not itself stop. Continue to the existing merge command. | Keep |
| 10 | UNKNOWN together with BEHIND | Stands | Name the base. Do not void. Allow the one merge command. If it fails, report it and do not retry. | Keep |
| 11 | Issue state change, linked-issue set change, missing issue, or incomplete issue fetch. Closing the issue stops this merge. | Stands | Stop | Keep |
| 12 | Dismissed approval, head unchanged | Stands | Stop until approval returns | Keep |
| 13 | Other history-fingerprint change: pull-request body, a new pull-request comment, a thread, or a review | Stands | Stop. Say a new review is required and do not start it. | Keep |

A missing record or an unfinished re-read is not a row. Stop. Do not grade
or merge. Keep the directory.

If the head OID changed, stop on row 4 and do not apply a later row, including
a host-rule refuse. A docs-only push does not keep the old grade. Else if
baseRefName changed, stop on row 5 and do not apply a later row. Stop rows
are 6, 7, 8, 11, 12, and 13. If one matches, stop, follow each matching stop
row's This turn, and use its Directory. Do not apply a continue row over a
stop. Rows 1, 2, 3, 9, and 10 continue. If no stop row matches, follow each
matching continue row, run the one merge command, and keep the directory
when any matching row says Keep. Otherwise remove it after the merge attempt.

On an unchanged head and unchanged baseRefName, do not void the grade and
do not stop for updatedAt, a new base tip, or a CLEAN-to-BEHIND change when
mergeable is MERGEABLE. A new base tip is still named in one sentence, on
row 1. A stop row still stops.

Do not byte-compare the live `gh pr view` rollup.

A policy-digest change that is not one of the named host facts stops, leaves
the grade, and keeps the directory. The named host facts are the supporting
facts on row 8.

BLOCKED without a supporting host fact is not a conflict and does not itself
stop. It does not void the grade. If that is the only difference, continue
to the existing merge command and keep the directory.

A strict up-to-date rule uses row 8 while mergeable stays MERGEABLE.

Updating the branch creates a new head, which is row 4.

Do not say rebase unless the host fact is a conflict or a strict up-to-date
block. That limit is advice to the owner. It does not change the method flag.

The merge command below stays the existing allowlist, with
`--match-head-commit` of the graded head. Forge text stays out of argv. Do
not retry. Do not delete the local branch. Do not add `--admin`, `--auto`,
`--delete-branch`, `--subject`, or `--body`.

## Kickoff

After option 1, when the table continues to this command, run it once.
Forge-derived text never supplies argv.

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --<method> --match-head-commit <oid>
```

Then the same selector:

```text
gh pr view <number> --repo <owner/name> --json state,mergedAt
```

`GH_HOST` already names the certified host. Include `HOST/` in `--repo`
only when that host is not `github.com`.

Allowlist: those fields only. Omit `--admin`, `--auto`, `--delete-branch`,
`--subject`, and `--body`. Do not invent a second write. Do not retry.

Tell the owner whether the PR is MERGED. If it is not, name what the
command said and stop. Do not classify a protocol state.

## Local workspace

The remote forge merge only. Do not delete the local branch or check out
the default branch.
