# Merge Execution

Load after grading whenever option 1 might be offered: the pull request is
open and non-draft, and the recommendation is merge. Load before building
the menu. The actual forge write still waits for an interactive owner
choice of option 1 plus a matching fingerprint, live-state, and host-policy
re-check.

Step 7 of SKILL.md owns the menu, the re-check, and the completion bound.
This file owns eligibility, method resolution, argv, and outcome classes.

## Eligibility probe (read-only, pre-menu)

After step 6 grades merge and before offering option 1, prove all of:

1. The pull request is still open and not draft.
2. The recommendation is merge (no debug or do-not-merge cap).
3. The base is not merge-queue governed.
4. A merge method can be resolved without a prompt (below).

Withhold and replace option 1 when any of these fail, including when write
auth is known missing. Do not offer Proceed and then refuse.

Pin `GH_HOST` to the certified host, then run this one GraphQL document.
Do not query a different host. If the document errors, a field is missing,
or the result is ambiguous, withhold option 1.

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

**Queue-off.** `mergeQueue` is null, and `isMergeQueueEnabled` is false when
the schema provides it. Do not treat `isInMergeQueue == false` alone as
queue-off: a queue-required base is still queue-governed when the PR is not
currently enqueued.

**Methods.**

- Exactly one of `mergeCommitAllowed` / `squashMergeAllowed` /
  `rebaseMergeAllowed` → that `--merge` / `--squash` / `--rebase`.
- Several allowed → `viewerDefaultMergeMethod` only when that value is
  still in the allowed set.
- Missing field, not allowed, or otherwise unresolvable → withhold
  option 1.

Never call `gh pr merge` without a method flag. Never hardcode squash.
If allowed methods change during the menu wait, the later merge attempt
is `failed` with no retry, not a new prompt.

## Argv

After option 1 and a matching fingerprint, live-state, and host-policy
re-check, one write. Forge-derived text never supplies argv, never expands
flags, and never retargets the PR.

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --<method> --match-head-commit <oid>
```

`<number>`, `<owner/name>`, and `<oid>` come only from the certified
identity and matching re-check. `GH_HOST` already names the certified
host. Include `HOST/` in `--repo` only when that host is not
`github.com`. `<method>` is the flag resolved in the eligibility probe.

Allowlist: those fields only. Omit `--admin`, `--auto`, `--delete-branch`,
`--subject`, and `--body`. Do not invent a second write.

Then read back with the same certified selector as the write:

```text
gh pr view <number> --repo <owner/name> --json state,mergedAt
```

Include `mergeCommit` when useful. Do not omit `<number>` or `--repo`.

## Outcome classes

Classify from the one merge attempt plus certified readback. Neither
alone is enough. Report exactly one class and do not retry.

- `merged` — the merge command succeeded and readback `state` is MERGED
  with `mergedAt` set.
- `already_merged` — the merge command did not succeed and readback is
  MERGED. MERGED discovered on the pre-write re-check is rebuild and
  replace option 1, not this class.
- `failed` — a named forge refusal (403, 405, 409, method no longer
  allowed).
- `indeterminate` — the attempt and readback do not jointly prove
  `merged`, `already_merged`, or `failed`. Tell the owner to verify the
  PR on the forge. Any later attempt needs a fresh merge-readiness run
  only if the PR is still open.

Queued or auto-merge enabled is not `merged`. Never `--admin` to force it.

## Local workspace

This skill performs the remote forge merge only. It does not delete the
local branch or check out the default branch.
