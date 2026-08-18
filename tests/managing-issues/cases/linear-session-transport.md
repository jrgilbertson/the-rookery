# Linear transport remains session-local

Provenance: the prior package required Orca for Linear and had no connected-MCP
path or transport-boundary priority conversion.

## Prompt

> Work only from these synthetic facts. Do not contact Linear.
>
> 1. Repository config selects provider `linear`, workspace `workspace-fixture`,
>    and team `ENG`. Connected authenticated Linear MCP tools expose the exact
>    reads and writes required for one issue update. Orca is also installed.
>    The operator did not name a transport.
> 2. The same capabilities exist, but the operator explicitly says to use the
>    Orca CLI.
> 3. MCP was selected and an approved create returns no confirmable issue
>    identity. Orca remains installed and authenticated.
> 4. Config maps the canonical priority `high` to `high`. The selected MCP
>    update schema requires a numeric priority and documents `0=None`,
>    `1=Urgent`, `2=High`, `3=Medium`, and `4=Low`.

## Expected behavior

- [ ] Scenario 1 selects Linear MCP, treats its runtime tool schemas as command
      authority, and does not load or invoke Orca.
- [ ] Scenario 2 honors the explicit Orca choice, loads the full
      version-matched `orca-linear` guide, and uses no MCP write.
- [ ] Repository config remains transport-neutral; neither `mcp` nor `orca` is
      added to `.agents/managing-issues.json`.
- [ ] Both paths require authenticated workspace, team, and issue matchback and
      every capability needed by the complete preview.
- [ ] Scenario 3 reports the create as `indeterminate`, performs no Orca retry or
      similarity match, and stops every later effect.
- [ ] Changing transports after a failure requires a fresh canonical read,
      complete preview, and new direct approval.
- [ ] Scenario 4 previews and sends numeric priority `2`; it does not pass the
      config string `high` to the MCP or store MCP-specific numbers in config.
