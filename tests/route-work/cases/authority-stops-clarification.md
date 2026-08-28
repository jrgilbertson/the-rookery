# Clarification, availability, and authority stop cleanly

Provenance: user feedback — routing asks the smallest independent question
batch that clarifies the starting setup without performing downstream discovery.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every response in
> order. Do not ask which item to assess.
>
> 1. An issue-shaped request could mean tracker cleanup or implementing an
>    accepted change. After the first routing question, the operator says the
>    tracker is correct and the work is outside it, but does not say whether
>    the product outcome is settled. After the next focused question, the
>    operator says the outcome and acceptance boundary are settled but no
>    execution plan exists.
> 2. The same initial request is supplied, but the operator says they cannot
>    determine whether tracker truth or source implementation must change.
> 3. A clarification answer requests a hands-off end-to-end delivery workflow
>    outside the supported startup owners.
> 4. A named primary plan cannot be read.
> 5. `ce-plan` is selected and available. Its primary orchestrator/planner
>    profile is stated unavailable; availability of the other profiles is
>    unknown.
> 6. All three profiles are stated unavailable.
> 7. The selected workflow itself is stated unavailable.
> 8. A grill is requested without document-write authority; separately, an
>    implementation is authorized but commit and publication are unstated.
> 9. Two coequal workstreams have no dependency order. The operator says the
>    work should move to a separate worktree but has not said whether the
>    current agent should supervise it through Orca or fully hand off ownership.

## Expected behavior

- [ ] Item 1 asks only the one currently answerable question in each response,
      then routes the settled unplanned outcome to `ce-plan`.
- [ ] Item 2 returns `Insufficient input` because the operator cannot supply
      the required routing fact.
- [ ] Item 3 returns `Unsupported in v1` with the public workflow-catalog URL
      and no further question.
- [ ] Item 4 returns `Insufficient input` with no owner, profile, or kickoff.
- [ ] Item 5 preserves the owner, selects its secondary profile, and marks
      the primary profile unavailable without marking the secondary profile
      `unverified`; item 6 returns `Profiles exhausted`; item 7 returns `Owner
      unavailable`.
- [ ] Every stop gives a reason and next prerequisite but no executable kickoff.
- [ ] Item 8 permits only the supplied work: no domain-model or ADR write for
      the grill, and no commit, push, PR, publish, or merge for implementation.
- [ ] Item 9 returns one clarification with exactly two numbered questions:
      which workstream starts first and whether the current agent should
      supervise through Orca or hand off ownership.
- [ ] No item probes availability, persists state outside the visible
      conversation, performs downstream discovery, or escalates effort.
