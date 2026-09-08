# Remaining work is one first-menu option that tees up items

Provenance: issue 140, a withheld-Approve menu where Request changes and
Run a missing step both read as leftover work. The quoted pairing was
"Request the Rookery fixes and recheck readiness" next to "Run the
outstanding validation and review steps."

## Prompt

> Apply the supplied PR-readiness skill to synthetic facts only. The
> recommendation is request changes. Gather is complete. Blocking source
> findings: a `CHANGELOG.md` conflict with main, and `CHANGELOG.md:20`
> disagrees with `README.md:63` terminology. A present companion skill
> owns one gap: actionlint ran past five minutes and was stopped. Brief
> the recommendation plus numbered live options and wait. Do not pick in
> the same turn. After the owner replies 2, continue from that pick.

## Expected behavior

- [ ] The first menu keeps option 1 as withheld Approve, then one
      remaining-work option. It does not print two leftover-work
      sentences. The quoted live pairing would fail this item.
- [ ] Later first-menu actions stay action types (explain, show checks,
      file follow-up), not one numbered row per finding.
- [ ] After the remaining-work pick, the run names those items once and
      waits. It does not start the conflict fix or the terminology edit.
- [ ] The follow-up is a question, not the decision menu: a reply of 1
      is not Approve. Dispatchable companions are numbered actions, at
      most one per pick. Source findings stay in the question prose.
- [ ] A leave-the-remaining-changes choice is offered on that follow-up.
      The first menu's remaining-work line is an action, not a recap that
      says the run will skip the work.
