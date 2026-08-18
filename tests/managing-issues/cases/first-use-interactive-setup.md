# First-use interactive repository setup

Provenance: the prior package lacked starter recommendations, explicit
accept/map/custom choices, and provider-metadata creation before config.

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
>    metadata. The authenticated user can create labels. Show what happens
>    before the issue preview.
> 3. Another repository already has a valid Managing Issues config. A create
>    request uses only values represented by that config.
> 4. A fourth repository has no config. Both GitHub and Linear are authenticated,
>    the request names no canonical target, and synchronization has not been
>    discussed.

## Expected behavior

- [ ] Both Scenario 1 reads proceed without setup and ignore the missing or
      incompatible config because reads and drafts do not require repository
      configuration.
- [ ] Scenario 2 stops before the first tracker mutation and begins interactive
      setup because the config is absent.
- [ ] Setup presents the GitHub starter recommendations for priority
      (`urgent`, `high`, `medium`, `low`), leaf estimates (`1`, `2`, `3`, `5`,
      `8`), labels (`bug`, `feature`, `maintenance`, `research`,
      `documentation`), and readiness (`needs-discovery`, `needs-planning`,
      `ready`) alongside the discovered alternatives.
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
      lets the operator choose the canonical provider and target, and asks
      whether synchronization is off or on with off recommended. Existing
      repository metadata does not make that choice for the operator.
- [ ] If the operator turns synchronization on, setup lets them select an
      existing identity map or proposes the bundled empty map at
      `.agents/managing-issues-sync.json`; the exact map and config files form
      one separately approved repository-setup batch.
- [ ] No scenario treats configuration as authorization, selects a default
      priority or estimate for an issue, or requires a trusted policy or
      principal.
