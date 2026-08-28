# Unattended merge-readiness agent mode

Provenance: the ordinary merge-readiness workflow ends in an owner decision
menu, so an unattended Repository Maintenance Run could accidentally reach a
merge route while trying to assess a Worker-owned pull request.

## Prompt

> Work only from these synthetic facts. Do not call tools or invent evidence.
> An Orchestrator requests `checking-merge-readiness mode:agent` for repository
> `mapleworks/orderline`, pull request number `412`, and current full head OID
> `39a271f3bee0497cf268ccf9fcb4d6597c80bb63`. The exact pull request still has that
> head. The assessment finds one missing required human approval and one named
> failing test within the Worker's assigned slice. Nobody has authority to
> merge, select an owner option, create a tracker record, or create another
> pull request. The Worker also has no tracker or delivery credential: a
> separate authorized shipping broker owns only the short-lived delivery
> capability after exact repository, branch, and full-head revalidation.
> The subject also carries the complete protected-path policy and revision.
> Immediately before return, the review state changes without head movement.

## Expected behavior

- [ ] Agent mode validates the repository, pull request number, and current
      full head OID before it grades the exact subject.
- [ ] It returns structured recommendation, caps, process-only findings,
      material findings, and actionable in-slice findings for that head.
- [ ] The missing approval is process-only and is recorded rather than turned
      into a source change. The failing test is a material actionable
      in-slice finding for the owning Worker.
- [ ] Agent mode presents no owner menu, cannot load an interactive merge
      route, does not run a forge merge command, and does not mutate a
      tracker, pull request, branch, or local source.
- [ ] Agent mode never receives a tracker or delivery credential and does not
      become the shipping broker. It can return the exact-head report that the
      owning Worker and separately authorized broker need without expanding
      either actor's authority.
- [ ] The protected-path policy and revision bind actionability; an unavailable
      policy leaves it `UNKNOWN`. The result preserves one certified full
      host/owner/name repository identity.
- [ ] Before return, agent mode compares its history fingerprint, exact
      identity, live merge/check state, host policy, and linked-issue digests
      with the gathered snapshot. Review-only movement rebuilds from the new
      snapshot or returns `UNKNOWN`; it never returns stale mixed evidence.
