# Applying Approved Actions

Read this reference before interpreting approval or applying any proposed
meeting action. Approval is bound to the exact visible effect, not to the
meeting, category, or bundle as a whole.

## Require unambiguous approval

Every action must already show:

- its visible action number;
- the acting identity or account;
- the exact authoritative destination and target;
- visibility when relevant, including repository visibility;
- the complete content or precise effect;
- the evidence and reason for the change; and
- every prerequisite action by visible number, or `None`.

The user may approve, edit, defer, or skip actions independently. Apply only
the action numbers the user unambiguously approved. A general response such as
`looks good`, `go ahead`, or `approved` writes nothing when more than one
visible action or interpretation remains possible; ask which action numbers it
applies to. An edit creates a revised numbered proposal whose exact new content
must be approved.

Approval of a dependent action never implies approval of its prerequisite.
Approval does not transfer to a different identity, destination, target,
visibility, content, or effect.

Completion: each selected action maps to one exact displayed proposal and all
required prerequisites have their own decisions.

## Re-read before writing

Immediately before each approved action, use the authoritative interface to:

1. Re-read the exact target for an update, or the destination, parent, thread,
   or calendar for a create.
2. Search for an equivalent task, issue, note change, event, draft, or other
   effect using stable identity and content as the destination supports.
3. Revalidate the acting identity, destination, target, visibility, approved
   content or effect, and prerequisite state.

If the approved effect already exists, make no write and report **Already
satisfied**. If a material field changed, cannot be distinguished, or became
ambiguous, invalidate only that action and present a revised proposal. Other
approved actions may continue when their own reads and prerequisites remain
valid.

Completion: each write is still necessary, targets the approved object, and
has not been redirected by changed state.

## Apply once in dependency order

Order selected actions by their explicit dependencies, not by category. A
prerequisite is satisfied only when its outcome is **Applied** or **Already
satisfied**. Apply each ready supported action once, then read the created or
updated target back through the same authoritative interface.

Classify each action using exactly one outcome:

- **Applied:** post-write readback shows the approved effect.
- **Already satisfied:** pre-write read found the approved effect.
- **Failed:** post-write readback confirms the approved effect is absent.
- **Indeterminate:** the interface or readback cannot establish whether the
  effect occurred.
- **Manual:** no current interface can safely perform and verify the effect.
- **Deferred:** the user chose to revisit the action later.
- **Skipped:** the user declined it or a required prerequisite was not
  satisfied.

Do not retry an **Indeterminate** action. Stop that action and ask how to
proceed. A **Failed** or **Indeterminate** prerequisite makes each dependent
action **Skipped**, with the prerequisite named. Unrelated approved actions may
continue.

Completion: every selected or decided action has one outcome, every attempted
write has authoritative readback, and no effect was applied twice.

## Preserve partial success

Treat canonical artifacts and their dependent links as separate effects. If a
task, issue, note, event, or draft succeeds but a dependent backlink fails or
is indeterminate, keep the successful artifact as canonical. Report both
outcomes, retain the partial success, and propose a bounded repair when useful.

Do not roll back a successful prerequisite, recreate it, or retry a dependent
effect blindly. If the meeting note depends on a task or issue link that did
not succeed, write only the note content that remains truthful under the
approved proposal; otherwise skip the dependent note action and return a
revision.

Completion: successful work remains visible once, broken links stay explicit,
and repair does not risk duplication.

## Report the application result

Report every visible action number with its outcome and the readback evidence
that supports it. For **Failed**, **Indeterminate**, **Manual**, **Deferred**,
or **Skipped**, state what remains unapplied and the next safe choice. Do not
describe a conversational draft as an external draft or a proposed action as a
completed change.

End with a compact recap of what changed, what was already satisfied, and what
still needs review or repair. The approved meeting note and each downstream
artifact remain ordinary records in their owning systems; create no workflow
ledger, transaction record, or private application state.

Completion: the user can verify each effect in its authoritative system and
knows exactly what remains.
