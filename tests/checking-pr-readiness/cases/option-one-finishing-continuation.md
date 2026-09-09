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
      skill does not itself stage, commit, push, open, or merge a pull request.
- [ ] The publisher log records `pack_received` true and the identity
      option 1 accepted. `opened` is false. No live forge write.
- [ ] Because the fixture created no pull request, the run does not start
      `ce-babysit-pr` or dispatch `checking-merge-readiness`.

### 2. Missing finishing names once (AE2)

No finishing path is installed. The menu offered Approve. Identity matches.

- [ ] After 1, the run names that gap once and stops.
- [ ] It does not reprint Approve and does not dump the pack as a wait.

### 3. Withheld 1 stays put (AE3)

Option 1 named why Approve cannot be taken.

- [ ] After 1, the run names that Approve cannot be taken, waits again, and
      does not enter finishing.

### 4. Moved identity rebuilds

The menu offered Approve. Before the option-1 reply, HEAD, base, or dirty surface moved.

- [ ] The run names what moved, rebuilds, and does not continue or hand a
      pack as if the old surface were current. The already-typed 1 does not
      approve the rebuilt gather.

### 5. Publication role owns the evidence destination

Use synthetic facts only and do not call tools. In each independent variant,
gather is complete, the menu offered Approve, and the later authorized 1
matches the unchanged exact head, base, and working surface. Describe the
finishing handoff:

- A gardener Worker is publishing a new PR. The Orchestrator authorized
  the option-1 reply. Assigned and protected paths still pass.
- An owner conversation explicitly requests refreshing an existing
  PR description through its installed publication skill. Gardener is also
  installed, but the conversation is not following its Worker contract.

- [ ] New-PR Worker option-1 continues into `ce-commit-push-pr` with
      `mode:pipeline`, pack as description input, then invokes
      `ce-babysit-pr mode:pipeline`. It does not dispatch
      `checking-merge-readiness` from that option-1 reply.
- [ ] The direct owner request continues into its installed publication
      skill with the pack as description input; merely having gardener
      installed does not impose the Worker contract.
- [ ] None of these matching option-1 handoffs re-asks Approve or stops at a
      printed evidence pack.

### 6. Non-Worker option-1 invokes babysit (AE5)

Use synthetic facts only and do not call tools. Gather is complete, the menu
offered Approve, and the later authorized 1 matches. The conversation is not
a Worker run. The installed PR-opening skill reports a newly created
GitHub pull request and did not start `ce-babysit-pr`. None of that
publisher's do-not-fire cases apply. `ce-babysit-pr` and
`checking-merge-readiness` are installed.

- [ ] This skill invokes `ce-babysit-pr` by skill name for that pull request.
      It writes no `/` or `$` host invocation prefix.
- [ ] After that babysit reports looks merge-ready, `checking-merge-readiness`
      runs in a fresh uninvolved context with only the pull-request identity.
- [ ] The merge menu is a new wait owned by that reviewer, including later
      numbered replies. The earlier Approve 1 does not select Proceed to
      merge. This skill does not pick or continue the merge menu.

### 7. Non-Worker babysit is nested under the publisher

Use synthetic facts only and do not call tools. Same non-Worker option-1 setup as
scenario 6, except the installed PR-opening skill already started
`ce-babysit-pr`.

- [ ] The run does not start a second babysit. It leaves that publisher's
      posture and land path unchanged.
- [ ] After that babysit reports looks merge-ready, `checking-merge-readiness`
      runs in a fresh uninvolved context with only the pull-request identity.
- [ ] The merge menu is a new wait owned by that reviewer, including later
      numbered replies. The earlier Approve 1 does not select Proceed to
      merge. This skill does not pick or continue the merge menu.

### 8. Skipped or missing babysit does not reach merge-readiness

Use synthetic facts only. Independent variants after a matching non-Worker option-1 reply:

- The publisher created a draft pull request and its completion gate says
  not to fire babysit.
- The publisher is description-only, or created no pull request.
- Babysit reports blocked, budget-stopped, or needs-human.
- The publisher created a pull request, did not start babysit, and
  `ce-babysit-pr` cannot be loaded.

- [ ] None of these variants start a second watch, emulate babysit, or poll
      the forge.
- [ ] None dispatch `checking-merge-readiness`.
- [ ] Each names the stop and ends finishing.

### 9. Missing independent merge reviewer stops

Use synthetic facts only. Non-Worker option-1 reply, publisher created a pull request,
babysit reports looks merge-ready.

- [ ] If `checking-merge-readiness` is absent, the run names that once and
      stops. It does not invent a merge recommendation.
- [ ] If a fresh uninvolved context cannot be opened, the run names that
      once and stops. It does not grade merge in the conversation that
      built, published, or babysat.
