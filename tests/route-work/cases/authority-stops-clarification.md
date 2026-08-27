# Clarification, availability, and authority stop cleanly

Provenance: explicit authority invariant — routing may narrow supplied evidence
once but cannot infer permission, availability, or external state.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as an independent explicit routing request.
>
> 1. An issue-shaped request could mean tracker cleanup or implementing an
>    accepted change; no further discriminator is supplied.
> 2. After the router's one question, the answer remains equally ambiguous.
> 3. A named primary plan cannot be read.
> 4. The selected owner is available, but its primary profile is stated
>    unavailable.
> 5. All three profiles are stated unavailable.
> 6. The selected workflow itself is stated unavailable.
> 7. A grill is requested without document-write authority; separately, an
>    implementation is authorized but commit and publication are unstated.

## Expected behavior

- [ ] Item 1 asks one question that distinguishes tracker truth from
      implementation; item 2 returns `Insufficient input` without another.
- [ ] Item 3 returns `Insufficient input` with no owner, profile, or kickoff.
- [ ] Item 4 preserves the owner and selects its secondary profile; item 5
      returns `Profiles exhausted`; item 6 returns `Owner unavailable`.
- [ ] Every stop gives a reason and next prerequisite but no executable kickoff.
- [ ] Item 7 permits only the supplied work: no domain-model or ADR write for
      the grill, and no commit, push, PR, publish, or merge for implementation.
- [ ] No item probes availability, persists state, or escalates effort.
