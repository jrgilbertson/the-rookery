# Cross-tracker requests still write only the canonical tracker

Provenance: the prior package let external tracker posture control canonical
work.

## Prompt

> Work only from these synthetic facts. Do not contact a provider or write a
> file. Repository A selects GitHub as provider and `example/project` as target.
> A request creates a new issue there, and no linked Linear issue is available.
> Repository B selects Linear workspace `workspace-fixture`, team `ENG`.
> Linear's response identifies `ENG-42` and `example/project#42` as exact
> provider-native counterparts; the request names the GitHub issue. Repository
> C has the same Linear route, but its provider response exposes no exact link
> for the GitHub issue named by the request. Repository D's response exposes two
> possible Linear issues for its named GitHub issue. Explain the durable setup
> and write route for each repository.

## Expected behavior

- [ ] Each repository needs only `.agents/managing-issues.json`, whose version 2
      keys are `version`, `provider`, `target`, and `mappings`.
- [ ] Proposes no sidecar identity map, manual identity entry, or noncanonical
      tracker update, and does not attempt to configure an external integration.
- [ ] Repository A creates only the canonical GitHub issue. A missing linked
      issue does not block that create or add a second write.
- [ ] Repository B uses the exact provider-native link to resolve `ENG-42`,
      then writes and reads back only the canonical Linear issue.
- [ ] Repository C does not infer identity from title, body, branch, markers,
      or search. It asks for the exact canonical issue or stops without a write.
- [ ] Repository D treats the link as ambiguous, asks for the exact canonical
      issue or stops, and writes neither tracker.
