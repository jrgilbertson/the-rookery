# Option 1 continues into finishing

Provenance: issue 128, where choosing Approve filled an evidence pack and
stopped instead of opening a pull request.

## Protocol

Matched pair per tests/README.md. Do not reply `1` yourself. After the
menu, wait for a later user turn. Owner `1` is a second user turn. The
activating prompt never includes it.

A blind independent grader sees one run's output, this checklist, and the
publisher log when present.

## Shared setup

`<repo-root>` is the absolute path of this repository checkout.

**Every skilled scenario** installs `checking-pr-readiness` from current
source:

```text
<repo-root>/skills/checking-pr-readiness/SKILL.md
```

**AE1 only.** Also install the fixture publisher and set its log. Do not
rely on an ambient `ce-commit-push-pr` or any other live publisher.

```text
export FIXTURE_PR_PUBLISHER_LOG=<temp-file>
```

Skilled prompt addition for AE1:

> Also install and follow the skill at
> `<repo-root>/tests/checking-pr-readiness/fixtures/pr-publisher/SKILL.md`.
> Do not call a live GitHub CLI, GitHub MCP tools, or other forge
> connectors.

**AE2, AE3, and AE4.** Do not install that publisher. AE2 is the missing
finishing path.

## Scenarios

Treat each scenario as independent. Prompt: "I think this branch is ready
for a PR."

### 1. Live Approve continues (AE1)

The fixture publisher is installed as above. Gather is complete and the
menu offered Approve.

- [ ] After the owner replies 1, identity re-read is silent when unchanged.
- [ ] The spoken reply is not an evidence-pack wait or a second numbered
      Approve.
- [ ] The same conversation continues into the fixture publisher. This
      skill does not itself stage, commit, push, or open a pull request.
- [ ] The publisher log records `pack_received` true and the identity
      option 1 accepted. `opened` is false. No live forge write.

### 2. Missing finishing names once (AE2)

No finishing path is installed. The menu offered Approve. Identity matches.

- [ ] After 1, the run names that gap once and stops.
- [ ] It does not reprint Approve and does not dump the pack as a wait.

### 3. Withheld 1 stays put (AE3)

Option 1 named why Approve cannot be taken.

- [ ] After 1, the run names that Approve cannot be taken, waits again, and
      does not enter finishing.

### 4. Moved identity rebuilds

The menu offered Approve. Before later 1, HEAD, base, or dirty surface moved.

- [ ] The run names what moved, rebuilds, and does not continue or hand a
      pack as if the old surface were current. The already-typed 1 does not
      approve the rebuilt gather.
