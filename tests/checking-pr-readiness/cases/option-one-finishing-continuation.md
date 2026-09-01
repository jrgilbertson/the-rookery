# Option 1 continues into finishing

Provenance: issue 128, where choosing Approve filled an evidence pack and
stopped instead of opening a pull request.

## Protocol

Matched pair per tests/README.md. The skilled prompt installs
`checking-pr-readiness` from current source. Do not reply `1` yourself.
After the menu, wait for a later user turn. Owner `1` is a second user
turn. The activating prompt never includes it.

A blind independent grader sees one run's output and this checklist.

## Scenarios

Treat each scenario as independent. Prompt: "I think this branch is ready
for a PR."

### 1. Live Approve continues (AE1)

An owner publisher is present. Gather is complete and the menu offered
Approve.

- [ ] After the owner replies 1, identity re-read is silent when unchanged.
- [ ] The spoken reply is not an evidence-pack wait or a second numbered
      Approve.
- [ ] The same conversation continues into that publisher. This skill does
      not itself stage, commit, push, or open a pull request.
- [ ] The publisher receives the filled pack as unpublished pull-request-body
      input. The pull request that opens is the identity option 1 accepted.

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
