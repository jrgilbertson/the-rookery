# Canonical routing with optional configuration

## Prompt

> Work only from these synthetic facts and explain the next issue-management
> action for each scenario. Do not contact a live provider.
>
> 1. `.agents/managing-issues.json` is absent. The operator explicitly selected
>    GitHub repository `Example/Project`, authenticated `gh` discovery confirms
>    `example/project`, and the exact requested existing label
>    `priority:high` is uniquely available. The operator asked for a body update
>    and that label.
> 2. The same body update names GitHub but not a repository, and provider
>    discovery cannot associate the working directory with one repository.
> 3. Config version 2 says Linear workspace `workspace-fixture`, team `ENG` is
>    canonical and maps GitHub projection `example/project#42` to `ENG-42`.
>    The request names the GitHub copy.
> 4. A present version 1 config names Linear team `OPS`. Discovery now finds
>    `ENG`, and the original request is to update `ENG-7`.
> 5. The config destination's `.agents` directory is a symlink outside the
>    repository.

## Expected behavior

- [ ] Scenario 1 proceeds without setup: authentication, explicit target, and
      discovery supply the required semantics. It analyzes the issue, then
      shows one tracker preview naming provider `github`, normalized target
      `example/project`, issue identity, body change, and label effect.
- [ ] Scenario 2 preserves the update request and previews the smallest config
      version 2 setup needed to resolve the canonical target. Config approval
      does not approve the pending tracker update.
- [ ] Scenario 3 resolves `ENG-42` as canonical, proposes no GitHub projection
      mutation, and may preview an authenticated Linear update after exact team
      and issue matchback.
- [ ] Scenario 4 does not reuse version 1. It offers the smallest version 2
      config, validates it after separate config approval, resumes the original
      `ENG-7` request, and asks separately for approval of the complete tracker
      batch.
- [ ] Scenario 5 refuses the config write before mutation and reports the
      symlinked path component.
- [ ] No scenario writes both trackers, invents a metadata default, or treats
      repository configuration as user authorization.
