# Transient plans stay useful without entering the durable record

Provenance: repository cleanup found that the gate treated a committed plan as
the preferred source and had no rule for distinguishing an ignored working
plan from one that would ship or remain cited after the worktree disappeared.

## Prompt

> Judge each scenario as an independent branch under a repository policy that
> ignores `/docs/plans/` and keeps durable outcomes in code, tests, issues, and
> maintained documentation.
>
> 1. `docs/plans/widget.md` exists only as an ignored file. No tracked file
>    cites it. The linked issue and final diff agree.
> 2. The same plan is staged for addition, or already exists as tracked content
>    in the branch's final tree.
> 3. The plan is ignored, but `docs/architecture.md` cites it as the authority
>    for the retry policy.
> 4. No plan exists. The linked issue states the intended behavior and the diff
>    delivers it.
> 5. An ignored plan says retries remain at three, but the linked issue, durable
>    operations guide, and final diff agree that retries are now two.
> 6. Scenario 4 is approved. Compose the comparison line for its evidence pack.

## Expected behavior

- [ ] 1 is allowed as ignored working material and excluded from the shipping
      surface and pull-request evidence.
- [ ] 2 is a readiness finding that must be removed before approval; a deletion
      of previously tracked plans would instead count as cleanup.
- [ ] 3 is a readiness finding until the durable document becomes
      self-contained or cites another durable source.
- [ ] 4 compares the issue to the delivered change and does not invent a
      missing-plan gap.
- [ ] 5 uses the linked issue as durable intent and does not let the stale
      ignored plan create false intent drift.
- [ ] 6 writes `Intent vs delivered` from the issue and does not call the
      comparison unavailable merely because no plan exists.
- [ ] No scenario adds a sweep class or copies transient contents into the
      evidence pack.
