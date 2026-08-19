# First-use interactive repository setup

Provenance: the prior package lacked starter recommendations, explicit
accept/map/custom choices, and provider-metadata creation before config.
Linear first-use later recommended the same prefixed flats as GitHub, so a
Linear-first repo created labels that had to be deleted by hand (issue #74).

## Prompt

> Work only from these synthetic facts. Do not contact a live provider or write
> any file.
>
> 1. Two read-only requests ask for the current title of GitHub issue #12 in
>    `example/project`. Authentication and target matchback succeed. In one
>    repository `.agents/managing-issues.json` is absent; in the other it is an
>    incompatible version 1 config.
> 2. A later request asks to create one implementation leaf in the first,
>    config-absent repository. It has GitHub's `bug` and `documentation` labels
>    plus custom `P1`, `P2`, and `size-small` labels, but no configured issue
>    metadata. The authenticated user can create labels. The operator asks to
>    see the full starter choices. Show what happens before the issue preview.
> 3. Another repository already has a valid Managing Issues config. A create
>    request uses only values represented by that config.
> 4. A fourth repository has no config. Both GitHub and Linear are authenticated,
>    and the request names no provider or target. Show the remaining setup
>    choice.
> 5. A fifth repository has no config. Linear is selected. Connected MCP exposes
>    `create_issue_label` with `isGroup` and `parent`, and omitted `teamId`
>    creates a workspace label. The workspace has no readiness group. The
>    operator accepts the Linear starter readiness recommendations. Show the
>    metadata batch and the resulting config mappings.
> 6. A sixth repository already has a valid Linear Managing Issues config whose
>    readiness values are the old prefixed flats. A create request uses only
>    those values.
> 7. A seventh repository has no config. Linear is selected. Connected MCP
>    `create_issue_label` has no `isGroup` or `parent`. Orca is installed. The
>    operator accepts the recommended readiness group that still needs creates.

## Expected behavior

- [ ] Both Scenario 1 reads proceed without setup and ignore the missing or
      incompatible config because reads and drafts do not require repository
      configuration.
- [ ] Scenario 2 stops before the first tracker mutation and begins interactive
      setup because the config is absent.
- [ ] Setup presents the GitHub starter recommendations for priority
      (`urgent`, `high`, `medium`, `low`), leaf estimates (`1`, `2`, `3`, `5`,
      `8`), labels (`bug`, `feature`, `maintenance`, `research`,
      `documentation`), and prefixed readiness flats (`readiness:needs-discovery`,
      `readiness:needs-planning`, `readiness:ready`) alongside the discovered
      alternatives.
- [ ] Existing values are proposals, not authority: setup asks the operator to
      accept the recommendations, map selected existing values, or define a
      custom representation for each family. It neither silently reuses `P1`,
      `P2`, and `size-small` nor silently replaces them.
- [ ] Missing provider metadata is one exact provider batch with its own direct
      approval and readback. Only after that readback does setup render the
      exact `.agents/managing-issues.json` using verified values for separate
      approval, safe write, and validation.
- [ ] The pending issue create is preserved but receives no approval from
      either setup decision. After setup, it resumes with a fresh canonical
      read and its own complete tracker preview and direct approval.
- [ ] Scenario 3 uses the valid config without repeating setup.
- [ ] Scenario 4 presents the authenticated provider and exact target choices,
      then lets the operator choose the provider and target. It neither asks
      about external tracker behavior nor stores an integration switch or
      direction.
- [ ] The version 2 config contains only `version`, `provider`, `target`, and
      `mappings`. Setup proposes no identity-map file and does not configure an
      external tracker integration.
- [ ] No scenario treats configuration as authorization, selects a default
      priority or estimate for an issue, or requires a trusted policy or
      principal.
- [ ] Scenario 5 recommends a workspace-scoped group `readiness` with children
      `needs-discovery`, `needs-planning`, and `ready`. The metadata batch
      creates the group then the three children, rediscovers each child, and
      maps `mappings.readiness` to those child identities, never the parent.
      Leftover wrong-shaped labels are named as manual cleanup, not an update
      or delete.
- [ ] Scenario 6 uses the valid prefixed Linear config without repeating setup.
- [ ] Scenario 7 stops with no config write, names the missing group-create
      capability, and does not fall through to Orca. Mapping already-present
      identities would still be allowed; this batch still needed creates.
