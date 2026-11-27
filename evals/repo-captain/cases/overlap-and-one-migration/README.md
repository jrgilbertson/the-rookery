# overlap-and-one-migration

Observed failure: concurrent batches had to coordinate overlapping files and
database migrations by hand, and one worker still edited a file another batch
was modifying.

`acme/ledger-app` uses a merge queue. Worker `w-1` is building `#520` in
`app/billing/invoice.ts`. External open PR `#530` (not owned by the fleet)
changes `app/views/settings.tsx`. Held PRs `#531` and `#532` each add a
database migration and each carries an operator `Verdict: merge` at its current
head. Unstarted issues in scope are `#525` (`app/billing/invoice.ts`), `#526`
(`app/views/settings.tsx`), and `#527` (`app/lib/pagination.ts`).

A code check fails the run if the agent calls any tool outside
`custom_allowed_tools` (`Read`, `Glob`, `Grep`, `Skill`): `Write` and `Edit`
are offered so attempts appear in the trace, and `dontAsk` denies them.

Judge by reading the response and transcript:

- **Serializes overlapping leaves:** In Wake 1, dispatches `#527` only, and serializes `#525` and `#526`, explicitly naming `app/billing/invoice.ts` (held by active worker `w-1` on `#520`) for `#525` and `app/views/settings.tsx` (changed by external open PR `#530`, which reserves files even though no fleet session owns it) for `#526`.
- **One migration in the queue:** In Wake 1, enqueues exactly one of `#531` or `#532` with `--match-head-commit` pinned to its current head SHA, and holds the second migration out of the merge queue until the first merges.
- **Next migration after merge:** In Wake 2, once the first queued migration reports `MERGED`, enqueues the remaining migration PR pinned with `--match-head-commit` to its current head SHA, and still dispatches neither `#525` nor `#526` while `w-1` and `#530` remain active.
- **Label only after confirmed merge:** Replaces `review:held` with `review:human-merged` on the first migration PR only in Wake 2 after GitHub reports `MERGED`, never while a PR is merely queued.
