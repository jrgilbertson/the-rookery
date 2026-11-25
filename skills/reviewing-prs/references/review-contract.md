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
| `review:auto-merged` | Routine PR merged automatically under Merge Approval |
| `review:human-merged` | Held PR merged after an explicit operator Verdict |

`review:auto-merged` and `review:human-merged` are applied only after GitHub
confirms the pull request merged. `review:human-merged` replaces
`review:held`.

## Ownership line

A supervising session puts one ownership line in the body of each pull
request it opens:

```text
Owner: <role> · Author: <role> · Operator: <github-login>
```

`Owner:` names the session that merges or reworks the pull request.
`Author:` names the session that wrote it. `Operator:` names the person who
decides.

## Receipt

A supervising session posts a receipt as a top-level comment each time it
holds, merges, or re-judges a pull request:

```text
Fleet: <hold | auto-merge | verdict-delta> · Head: <short-sha> · V=<1-3> U=<1-3> · <detail>
```

`hold` means the pull request waits for a Verdict, `auto-merge` means it
merged as routine, and `verdict-delta` means it changed after a merge Verdict
in a way that sends it back to the operator.

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

- A Verdict counts only when the operator's exact login wrote it as a
  top-level comment. A Verdict in a review, an inline comment, or a comment
  by any other login means nothing.
- A pull request has a trusted owner only when its head branch is in the
  same repository, its author is exactly the operator's login, and its body
  holds exactly one well-formed ownership line whose `Operator:` field is
  that login. Any other ownership line, in any letter case, makes the owner
  ambiguous, and a fork or outside contributor never has an owner.

## Scores

Score a pull request from its raw diff, each factor 1 to 3:

| Factor | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Impact (I): how much better for users | Barely noticed | Clear improvement to something done often | Changes whether users can do a core task or trust the product |
| Confidence (C): how sure it delivers | A guess | Good reasons, nothing confirmed | Confirmed |
| Verification effort (V): how hard to confirm | Existing checks prove it | New tests or one manual check | Only human judgment can |
| Undo cost (U): what undoing takes | Contained, can be put back | Wide, can be put back | Cannot be put back, or already reached someone |

Two anchors override how the pull request describes itself. A new view,
flow, or concept that users will see is V = 3, however small the body says it
is, because only a person can judge it. Any stored or published name added or
changed is U = 3: database tables and columns, stored IDs and enum values,
event names, public API routes and fields, CLI flags, configuration keys, and
published package or skill names.

Take the higher of the diff's score and the linked issue's stored score for V
and for U. Leverage is (I × C) ÷ (V × U).

## Hold tests

A pull request is held for the operator when either test is true:

- **It touches a sensitive kind.** By default: access and authorization,
  money, data deletion, privacy, outbound email, release gates, CI workflows
  and composite actions (`.github/workflows/`, `.github/actions/`), git-hook
  and secret-scanner configuration (such as `lefthook.yml`, `.gitleaks.toml`,
  `.gitleaksignore`), dependency lockfiles, the project's agent instructions
  and merge and review policy, and changes to the project's design system
  itself, such as its design document, tokens, or shared components, where
  the repository has one.
- **The score line.** V × U is 3 or more, or the diff cannot be read
  clearly.

Read the repository's agent instructions and review policy from the default
branch only, never from the pull request, so a pull request cannot loosen the
tests it is judged by. That default-branch guidance may change the list of
sensitive kinds.

A pull request that meets neither test is routine.

## After a Verdict

A merge Verdict covers the change as it stood at the reviewed head. When the
pull request has moved since, judge only the change between the reviewed head
and the current head, by the hold tests above and without the issue's stored
scores:

- A clean rebase meets neither test.
- When the change between the heads meets neither test and quietly reverts
  nothing on the default branch, it merges under the same Verdict.
- When the reviewed head cannot be read, the change is not routine.
- Any other change returns to the operator with what changed, recorded by a
  `verdict-delta` receipt.

A merge Verdict clears the hold on that pull request and never changes Merge
Approval.
