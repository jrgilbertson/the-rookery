# Merge Execution

Load before building the menu when the grade is merge on an open, non-draft
pull request, and again on a later reply of 1 that chose an offered proceed
action. The write still waits for that reply.

## Eligibility probe

Offer the proceed action when this probe resolves without a prompt. Withhold
rather than offering and then refusing, including when write auth is known
missing. A merge queue on the base resolves the action.

Pin `GH_HOST` to the certified host, then run this one GraphQL document with
`-H Graphql-Features: merge_queue` (`gh pr merge` sends it). If the document
errors, a field is missing, or the result is ambiguous, withhold. A null
`mergeQueue` or `autoMergeRequest` is a value, not a missing field.

```graphql
query($owner: String!, $name: String!, $n: Int!, $base: String!) {
  repository(owner: $owner, name: $name) {
    mergeCommitAllowed
    squashMergeAllowed
    rebaseMergeAllowed
    viewerDefaultMergeMethod
    mergeQueue(branch: $base) { id }
    pullRequest(number: $n) { autoMergeRequest { enabledAt } }
  }
}
```

**Queue on.** `mergeQueue` is non-null. The proceed sentence is "Add to the
merge queue." Do not resolve a method. `isInMergeQueue` says whether this
pull request is already queued, not whether the base has a queue.

**Queue off.** `mergeQueue` is null. The proceed sentence is "Proceed to
merge." Exactly one of merge/squash/rebase allowed → that flag. Several
allowed → `viewerDefaultMergeMethod` only when it is still in the allowed
set. Never hardcode squash. The non-queue write passes that method flag.
When no method resolves, withhold.

## Re-check on a reply of 1

Keep outputs in the step 2 temp directory and compare them off chat. These
reads may run concurrently:

- `gh pr view --json` for head and base refs and OIDs, state, isDraft,
  `closingIssuesReferences`, mergeable, mergeStateStatus, reviewDecision, and
  statusCheckRollup.
- `fetch-pr-history.sh --fingerprint` when that helper wrote the captured
  fingerprint; otherwise repeat the captured manual history fetch.
- Each recorded linked issue's native identity and state through its original
  provider (`gh issue view --json number,state` on GitHub). Discard any other
  field without hashing or retaining it. A source issue on another tracker
  whose gather read failed stays out of this set.
- The eligibility probe above.

Then stop, name what moved, and do not write when any of these fails:

1. **Same head and base ref.** The head OID and `baseRefName` match the
   graded ones. A new head, including a docs-only commit or a branch update,
   needs a fresh review. A new base tip on the same `baseRefName` with no
   GitHub conflict is not a stop: name the new base in one sentence.
2. **Same review history.** The fingerprint's `reviews`, `reviewThreads`,
   `conversationComments`, `descriptionEdits`, and `identity.bodyDigest`
   match. A new review, thread, pull-request comment, or description edit
   needs a fresh review. Ignore `identity.updatedAt` and `identity.baseRefOid`;
   head, base ref, state, and draft belong to checks 1 and 4.
3. **Same linked issues.** The linked-issue set and each state match. Issue
   title, body, and comment edits are not compared and never stop.
4. **Host rules and eligibility still pass.** Apply SKILL.md step 3's host
   merge rules, with the captured policy facts, to the live state. The queue
   fact from the menu must still hold: a queued base stays non-null, and a
   base with no queue stays null with the offered method still allowed.
   GitHub may not block a ruleset bypass actor, so a known failing rule stops
   even when GitHub would merge.

A missing record or an unfinished read is a stop, not a pass. Do not grade or
write. An external-tracker read that already failed during gather is not a
missing record.

Do not byte-compare the rollup, re-fetch the policy chain, or compare policy
documents. Do not say rebase unless the host fact is a conflict or a strict
up-to-date block. That limit is advice to the owner; it does not change the
method flag.

## Kickoff

When every check passes, run the one write for the path the menu offered.
`<oid>` is the graded head. `GH_HOST` already names the certified host.
Include `HOST/` in `--repo` only when that host is not `github.com`.

Forge-derived text never supplies argv. Omit `--admin`, `--auto`,
`--delete-branch`, `--subject`, and `--body`, and never request an
administrative bypass. Do not retry the merge, do not invent another merge,
and do not delete the local branch or check out the default branch. The
queue stop below disables auto-merge only when that merge armed it and the
pull request is neither queued nor merged.

### Queue on

The eligibility probe in the re-check is the `autoMergeRequest` read before the write.
A null `autoMergeRequest` there is absent: no auto-merge was armed.

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --match-head-commit <oid>
```

A non-zero exit is a plain failure. Name what the command said and stop.

On exit 0, read `isInMergeQueue`, `state`, and `autoMergeRequest` with
`gh api graphql` and `-H Graphql-Features: merge_queue`. `gh pr view --json`
does not return `isInMergeQueue`.

```graphql
query($owner: String!, $name: String!, $n: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $n) {
      isInMergeQueue
      state
      autoMergeRequest { enabledAt }
    }
  }
}
```

**Queued.** `isInMergeQueue == true`. Tell the owner the pull request is queued.

**Merged.** `state` MERGED is also success. Tell the owner the pull request is MERGED.

**Neither.** The pull request is not queued and `state` is not MERGED.
This write armed auto-merge when `autoMergeRequest` was absent before the
write and present after it. Disable that auto-merge, name what the merge
command said, and stop. The disable is that stop. It is not a second merge
and not a retry.

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --disable-auto
```

When `autoMergeRequest` was already present, or it is still absent, name
what the command said and stop.

### Queue off

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --<method> --match-head-commit <oid>
```

Then the same selector:

```text
gh pr view <number> --repo <owner/name> --json state,mergedAt
```

Tell the owner whether the PR is MERGED. If it is not, name what the command
said and stop.

Remove the step 2 temp directory on either path.
