# Canonical routing with first-use configuration

Provenance: the baseline treated repository markers and branch-policy facts as
write authority, and an early candidate hid resolved policyless preview fields.

## Prompt

> Work only from these synthetic facts and explain the next issue-management
> action for each scenario. Do not contact a live provider.
>
> 1. `.agents/managing-issues.json` is absent. The operator explicitly selected
>    GitHub repository `Example/Project`, authenticated `gh` discovery confirms
>    `example/project`, issue `#42`, and the exact requested existing label
>    `priority:high` is uniquely available. The operator asked for a body update
>    and that label. Show the setup choices before the pending tracker preview.
> 2. The same body update names GitHub but not a repository, and provider
>    discovery cannot associate the working directory with one repository.
> 3. Config version 2 selects Linear workspace `workspace-fixture`, team `ENG`.
>    Linear's provider response exposes the exact provider-native link between
>    `ENG-42` and GitHub issue `example/project#42`. The request names the
>    GitHub issue.
> 4. A present version 1 config names Linear team `OPS`. Discovery now finds
>    `ENG`, and the original request is to update `ENG-7`. Describe the approval
>    boundary through the resumed tracker batch.
> 5. The config destination's `.agents` directory is a symlink outside the
>    repository.

## Expected behavior

- [ ] Scenario 1 preserves the requested update but stops before its first
      tracker mutation for interactive setup. It shows the starter
      recommendations and the exact discovered `priority:high` alternative
      without choosing either, then keeps config approval separate from the
      pending tracker preview.
- [ ] Scenario 2 preserves the update request and asks for the exact repository.
      After that choice, it begins first-use setup. Config approval does not
      approve the pending tracker update.
- [ ] Scenario 3 resolves `ENG-42` as canonical, proposes no GitHub mutation or
      sidecar-map update, and may preview an authenticated Linear update after
      exact team and issue matchback.
- [ ] Scenario 4 does not reuse version 1. It offers a version 2 config containing
      only schema-required fields, validates it after separate config approval,
      resumes the original
      `ENG-7` request, and asks separately for approval of the complete tracker
      batch.
- [ ] Scenario 5 refuses the config write before mutation and reports the
      symlinked path component.
- [ ] No scenario writes both trackers, applies a recommended priority or
      estimate to an issue by default, or treats repository configuration as
      user authorization.
