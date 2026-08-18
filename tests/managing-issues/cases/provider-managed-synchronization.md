# Native issue synchronization stays provider-managed

Provenance: the prior package introduced a repository sidecar map for identities
that GitHub and Linear native Issues Sync already own.

## Prompt

> Work only from these synthetic facts. Do not contact a provider or write a
> file. Repository A uses GitHub as canonical and has native GitHub/Linear
> Issues Sync turned off. Repository B uses Linear as canonical and has native
> sync turned on. Linear's response identifies `ENG-42` and
> `example/project#42` as exact synchronized counterparts. Repository C also
> records native sync on, but its available provider response exposes no exact
> synchronized counterpart for the GitHub issue named by the request. Explain
> the durable setup and write route for each repository. Repository D is being
> set up with Linear as canonical, but the confirmed native integration is
> one-way from GitHub to Linear rather than two-way. Name every durable setup
> file and explain how the native sync direction constrains the canonical
> provider choice.

## Expected behavior

- [ ] Each repository needs only `.agents/managing-issues.json`; its required
      boolean `synchronization` records whether provider-managed sync is on.
- [ ] Proposes no sidecar identity map, manual identity entry, or mirrored
      tracker update, and does not attempt to configure native Issues Sync.
- [ ] Repository A writes only the canonical GitHub issue; sync-off adds no
      cross-provider behavior.
- [ ] Repository B uses the exact native provider linkage to resolve `ENG-42`,
      then writes and reads back only the canonical Linear issue.
- [ ] Repository C does not infer identity from title, body, branch, markers,
      or search. It asks for the exact canonical issue or stops without a write.
- [ ] Repository D does not record synchronization on or promise a GitHub
      projection from a Linear create. It asks the operator to keep sync off,
      enable two-way sync, or select GitHub as canonical.
