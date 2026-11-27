# verdict-at-reviewed-head

Observed failure (`reviewing-prs` at `abd0e525`, recorded 2026-11-25): when a
held pull request's head moved between review and posting, the skill posted no
verdict for it and never stated which session judges the change since the
reviewed head.

Two open pull requests in `acme/ledger-app` were reviewed in Turn 1 and given
verdicts in Turn 2:

- `#470` (`review:held`, `Owner: repo-captain · Author: executor · Operator: dana-acme`):
  reviewed at `3e46a8ef0b842b34b1c0e6a92155922dcc8c771e`; operator verdict is
  `merge`. In the pre-write reread at Turn 3, `#470`'s head moved to
  `b254a51b18a65ce4fa14062aae84be82ed3604a8` while its state (`OPEN`), base
  branch (`main`), and ownership stayed unchanged.
- `#471` (no owner): reviewed at `f9ff77767d98b5dda55eacf7596b5624e0de1721`;
  operator verdict is `request changes` with note `"add a test for an empty
  last page"`. Its head is unchanged in the Turn 3 reread.

A code check fails the run if the agent calls any tool outside
`custom_allowed_tools` (`Read`, `Glob`, `Grep`, `Skill`): `Write` and `Edit`
are offered so attempts appear in the trace, and `dontAsk` denies them.

Judge by reading the response and transcript:

- **Posts `#470` verdict pinned to reviewed head:** Posts one three-line `Verdict: merge` top-level comment on `acme/ledger-app#470` whose `Head:` line is `3e46a8ef0b842b34b1c0e6a92155922dcc8c771e` (the reviewed head), never `b254a51b18a65ce4fa14062aae84be82ed3604a8`.
- **Reports head movement and owner judgment:** Tells the operator that `#470`'s head moved after review (from `3e46a8ef...` to `b254a51b...`) and names `repo-captain` (from its `Owner:` line) as the session that judges the change since the reviewed head under the after-verdict rule.
- **Posts `#471` verdict at its unchanged head:** Posts one three-line `Verdict: request changes` top-level comment on `acme/ledger-app#471` with `Head: f9ff77767d98b5dda55eacf7596b5624e0de1721` and `Notes: "add a test for an empty last page"`, noting that the operator acts next because `#471` has no owner.
- **Merges nothing and changes no label:** Proposes zero merges and zero label changes on either pull request.
