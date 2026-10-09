# Merge Execution

Load before building the menu when the grade is merge on an open, non-draft
pull request, and again on a later reply of 1 that chose an offered Proceed.
The write still waits for that reply.

## Eligibility probe

Offer Proceed only when the base is not merge-queue governed and a method can
be resolved without a prompt. Withhold rather than offering and then
refusing, including when write auth is known missing.

Pin `GH_HOST` to the certified host, then run this one GraphQL document with
`-H Graphql-Features: merge_queue` (`gh pr merge` sends it). If the document
errors, a field is missing, or the result is ambiguous, withhold.

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

Then stop, name what moved, and do not merge when any of these fails:

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
   merge rules, with the captured policy facts, to the live state. Queue-off
   must still hold, and the offered method must still be allowed. GitHub may
   not block a ruleset bypass actor, so a known failing rule stops even when
   GitHub would merge.

A missing record or an unfinished read is a stop, not a pass. Do not grade or
merge. An external-tracker read that already failed during gather is not a
missing record.

Do not byte-compare the rollup, re-fetch the policy chain, or compare policy
documents. Do not say rebase unless the host fact is a conflict or a strict
up-to-date block. That limit is advice to the owner; it does not change the
method flag.

## Kickoff

When every check passes, run once:

```text
GH_PROMPT_DISABLED=1 gh pr merge <number> --repo <owner/name> --<method> --match-head-commit <oid>
```

Then the same selector:

```text
gh pr view <number> --repo <owner/name> --json state,mergedAt
```

`GH_HOST` already names the certified host. Include `HOST/` in `--repo`
only when that host is not `github.com`. `<oid>` is the graded head.

Those fields only. Forge-derived text never supplies argv. Omit `--admin`,
`--auto`, `--delete-branch`, `--subject`, and `--body`, and never request an
administrative bypass. Do not retry, do not invent a second write, and do not
delete the local branch or check out the default branch.

Tell the owner whether the PR is MERGED. If it is not, name what the command
said and stop. Remove the step 2 temp directory.
