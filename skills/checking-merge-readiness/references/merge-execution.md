# Merge Execution

A kickoff, not a merge state machine. Load after grading when option 1
might be offered. The write still waits for an interactive owner choice
of option 1 plus a matching fingerprint, live-state, and host-policy
re-check.

## When to offer option 1

Offer only when the pull request is open and non-draft, the
recommendation is merge, the base is not merge-queue governed, and a
method can be resolved without a prompt. Withhold rather than offering
and then refusing, including when write auth is known missing.

Pin `GH_HOST` to the certified host, then this one GraphQL document. If
it errors, a field is missing, or the result is ambiguous, withhold.

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

## Kickoff

After option 1 and a matching re-check, one command. Forge-derived text
never supplies argv.

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
