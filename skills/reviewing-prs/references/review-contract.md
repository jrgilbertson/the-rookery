# Review contract

The formats and tests that `reviewing-prs` and `repo-captain` share. Other
sessions parse these formats, so keep the spelling exactly. Both skills ship
an identical copy of this file.

## Labels

Supervising sessions set these labels. A label reports status and never
permits a merge: every open pull request is read whether or not it has one.

| Label | Meaning |
| --- | --- |
| `review:held` | PR held for human review in a Review Round |
| `review:auto-merged` | Routine or charter pre-authorized PR merged automatically under Merge Approval |
| `review:human-merged` | Held PR merged after an explicit per-PR operator merge verdict |

`review:auto-merged` and `review:human-merged` are applied only after GitHub
confirms the pull request merged, and either one removes `review:held` if it
was present.

## Ownership line

A supervising session puts one standalone ownership line starting at column 0
in the body of each pull request it opens:

```text
Owner: <role> · Author: <role> · Operator: <github-login>
```

`Owner:` names the session that merges or reworks the pull request.
`Author:` names the session that wrote it. `Operator:` names the person who
decides.

## Receipt

A supervising session posts a receipt as a top-level comment each time it
holds, auto-merges, or merges a pull request whose head moved after its merge
verdict, always exactly these four plain ASCII lines:

```text
Fleet: <hold | auto-merge | verdict-delta>
Head: <short-sha, 7+ hex characters, or full 40-character SHA>
Scores: V=<1-3|?> U=<1-3|?>
Detail: <one-line text>
```

`hold` means the pull request waits for a verdict, `auto-merge` means it
merged under Merge Approval as routine or under a charter per-issue
pre-authorization (naming that pre-authorization in `Detail:`), and
`verdict-delta` means it merged under a merge verdict at a later head, after
the change since review was judged routine (recording the delta's `V` and `U`
scores in `Scores:`). Use `V=? U=?` when a diff cannot be read clearly. A
pull request merged under a `Verdict: merge` comment at the reviewed head
needs no extra `Fleet:` receipt.

**Reading receipts across formats.** Every receipt-reading path in
`reviewing-prs` (open-PR bucketing and recent-merge checks) and `repo-captain`
(verdict-spent detection and unauthorized-merge checks) accepts top-level
comments by the operator's exact login in either the four-line format above or
the legacy single-line middle-dot format
(`Fleet: <hold | auto-merge | verdict-delta> · Head: <short-sha> · V=<1-3> U=<1-3> · <detail>`),
extracting the receipt kind, `Head:`, scores, and detail from either form.

## Verdict

The operator's decision on one pull request, posted as a top-level comment,
always exactly these three lines:

```text
Verdict: <merge | request changes>
Head: <reviewed head, all 40 characters>
Notes: "<the operator's words on one line, or empty>"
```

`Head:` is the commit the operator reviewed, even when the pull request has
moved since.

## Who counts

Every session in a fleet shares the operator's GitHub login, so these are
conventions that prevent accidents, not authentication.

- **Verdicts.** A verdict counts only when the operator's exact login wrote it
  as a top-level comment. A verdict in a review, an inline comment, or a
  comment by any other login means nothing.
- **Ownership.** A fork (`isCrossRepository` is true) or outside contributor
  (author differs from the operator's exact login) never has an owner. For a
  same-repository pull request authored by the operator's exact login,
  normalize `\r\n` to `\n` and collect every line starting at column 0 with
  `Owner:` (case-insensitive on the prefix); surrounding blank lines are not
  required, and indented, `> `-quoted, `- `-bulleted, and mid-line prose
  mentions are ignored:
  - zero matching lines: no owner
  - exactly one line matching exact-case
    `Owner: <role> · Author: <role> · Operator: <github-login>` with non-empty
    roles and the operator's exact login: trusted owner
  - anything else (two or more matching lines even when identical, wrong case
    on `Owner:`, `Author:`, or `Operator:`, malformed fields, or another
    operator login): ambiguous owner
- **Merge authority.** To judge whether a merged pull request had valid
  authority at its final head (`headRefOid`), inspect top-level comments
  authored by the operator's exact login and evaluate the newest verdict first
  (labels never count as authority):
  - a `request changes` verdict at any head fails authority
  - a `merge` verdict whose `Head:` matches `headRefOid` passes authority
    unless superseded by a newer `Fleet: hold` receipt by the operator's login
    (such as after a base-branch retarget) with no later matching-head
    `Fleet: auto-merge` receipt
  - a `merge` verdict at an earlier head (`Head:` differs from `headRefOid`)
    passes authority only when the newest valid `Fleet:` receipt by the
    operator's login posted after that verdict (not superseded by a newer
    `Fleet: hold`) has a `Head:` matching at least a 7-character hexadecimal
    prefix of `headRefOid` and is either `Fleet: verdict-delta` carrying
    routine scores (`V × U` below 3 with neither factor `?`) or
    `Fleet: auto-merge` (under a charter per-issue pre-authorization)
  - with no operator verdict, authority passes only when the newest valid
    `Fleet:` receipt by the operator's login is `Fleet: auto-merge` with a
    `Head:` matching at least a 7-character hexadecimal prefix of `headRefOid`
    (so a missing receipt, a too-short or mismatched head prefix, or a newer
    `Fleet: hold` fails authority)

## Scores

Score a pull request from its raw diff on the four leverage factors, each 1
to 3. The hold tests and receipts call them I, C, V, and U:

- Impact, how much better it makes things for users: 1 is no user task you can name gets better, 2 is a named user task gets faster, easier, or more reliable, 3 decides whether users can do a core task (one most users rely on) or keep their work safe. Work users don't see takes the impact of the problem it prevents or the feature it unblocks.
- Confidence, how sure we are that it will deliver the impact scored: 1 is a hypothesis with nothing behind it yet, 2 is a hypothesis with indirect evidence, such as a user report, a similar case, or reading the code, 3 is confirmed by direct evidence for this item, such as a reproduction, a measurement, a plan that calls for it, or the same fix working here before.
- Verification effort, how hard the result is to confirm: 1 means checks that existed before the change, such as tests, types, CI, or a reproduction on record, prove it, 2 means it needs new tests, including the change's own, or a manual check with a known right answer, 3 means only human judgment can, such as a new user-facing view, flow, or concept.
- Undo cost, what it takes to undo: 1 is one revert within one module, 2 can be undone but reaches shared code, shared settings, or many users, or takes more than one revert, 3 can't be undone, because data is lost, a message is sent, money moves, access is exposed, or a stored or published name is added or changed (table, column, stored ID or enum value, event name, public API route or field, CLI flag, configuration key, or published package or skill name).

Two anchors override how the pull request describes itself. A new view,
flow, or concept that users will see is V = 3, however small the body says it
is, because only a person can judge it. Any stored or published name added or
changed is U = 3, of the kinds the undo cost line lists.

Take the higher of the diff's score and the linked issue's stored score for V
and for U. Leverage is (I × C) ÷ (V × U).

## Hold tests

A pull request is held for the operator when either test is true:

- **It touches a sensitive kind.** By default:
  - product and data risk: access and authorization, money, data deletion,
    privacy, outbound email, and release gates
  - CI, hooks, and tooling: CI workflows and composite actions
    (`.github/workflows/`, `.github/actions/`), git-hook and secret-scanner
    configuration (such as `lefthook.yml`, `.gitleaks.toml`, `.gitleaksignore`),
    scripts that CI workflows or git hooks run, agent harness configuration
    (such as `.claude/`, `.codex/`, `.mcp.json`), and dependency lockfiles
  - policy and design: the project's agent instructions, merge and review
    policy, and changes to the project's design system itself (such as its
    design document, tokens, or shared components) where the repository has one
- **The score line.** V × U is 3 or more, or the diff cannot be read
  clearly.

Read the repository's agent instructions and review policy from the default
branch only, never from the pull request, so a pull request cannot loosen the
tests it is judged by. That default-branch guidance may change the list of
sensitive kinds.

A pull request that meets neither test is routine.

## After a verdict

A merge verdict covers the change as it stood at the reviewed head, against
the base branch it was reviewed on. When the pull request's timeline shows its
base branch changed after the verdict, the verdict no longer counts and the
pull request returns to the operator. The one exception is a stacked parent
landing, where the earlier base was a pull request that has since merged into
the new base.

When the pull request has moved since, judge only the change between the
reviewed head and the current head, by the hold tests above and without the
issue's stored scores:

- A clean rebase meets neither test.
- When the change between the heads meets neither test and quietly reverts
  nothing on the default branch, it merges under the same verdict, recorded by
  a `verdict-delta` receipt naming the change.
- When the reviewed head cannot be read, the change is not routine.
- Any other change returns to the operator with what changed, recorded by a
  new `hold` receipt at the current head.

A merge verdict clears the hold on that pull request and never changes Merge
Approval.
