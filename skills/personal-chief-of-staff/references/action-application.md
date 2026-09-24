# Action Application

Use this reference before numbering the first proposed action in a review and
before applying any decided action. It owns what an approval binds and how an
approved effect is revalidated, applied, and read back.
[Source access](source-access.md) still governs every read and write.

## Bind approval to the exact action

Each proposed action states in plain language:

- the acting identity or account;
- the destination, recipients, or authoritative system;
- the exact record, file, event, thread, or other target;
- repository visibility when a repository is involved;
- the complete proposed content or precise effect;
- the supporting evidence and why the change matters now.

Approval applies only to that displayed combination. Number actions within the
current bundle so the user can approve, edit, defer, or skip them independently.
An edit creates a revised proposal that needs approval; approval of one action
does not authorize another.

The initial action surface is deliberately narrow. Reply text written in the
conversation is not a Gmail draft and creates no external change. Creating or
updating a Gmail draft is its own proposed external action with an acting
identity, thread, recipients, and complete content. Sending that draft or any
message is a separate action requiring separate approval and a verified send
interface. Make destructive calendar changes and production interventions
manual unless the user explicitly approves a bounded action and the active
interface can re-read, apply, and verify it. For repository work, show the
repository visibility, exact target, and proposed content before approval. For
any other source, propose only a write verb supported by its current interface.
Label an unsupported write as manual instead of implying it can be applied.

Completion: approval identifies one exact effect, identity, and target without
relying on conversational inference.

## Revalidate, apply, and read back

Finish one approved action's re-read, write, and readback before starting the
next. This keeps each write adjacent to its own revalidation.

Immediately before each approved action:

1. For an update, re-read the current target through the same authoritative
   interface. For a create, re-read the authoritative destination, parent, or
   thread where the new target will be created. A re-read that fails, is
   refused, or returns nothing you can compare is not a completed re-read;
   step 3 applies.
2. Revalidate the acting identity, destination or recipients, exact target,
   visibility when relevant, approved content or effect, and closure evidence
   against the exact approved proposal. For a create, confirm the proposed
   target's identity and exact effect within that destination, parent, or
   thread.
3. If any approved action field, including closure evidence, changed, cannot
   be distinguished, or became ambiguous, stop and present a revised proposal
   for new approval. Never redirect an approval to a different account or
   target. Leave the action unapplied until the revised proposal is approved.
4. If readback shows the approved effect already exists, report **already
   satisfied** and do not duplicate it.
5. Otherwise apply the approved action once through the supported interface.
6. Read the created or updated target again through that interface.

Report each action's current basis, exact approved effect, and whether its
approved closure evidence was observed. An immediate mutation result is not
completion of its outcome: report closure only when observed evidence meets
the approved closure evidence.

Classify each action independently:

- **Applied:** readback shows the intended effect.
- **Already satisfied:** pre-write readback showed the intended effect.
- **Failed:** post-write readback confirms the intended effect is absent.
- **Indeterminate:** the interface or readback cannot establish whether the
  effect occurred. Stop and ask the user how to proceed; do not retry blindly.
- **Manual:** the interface does not support the approved write safely.
- **Deferred** or **skipped:** the user chose not to apply it now.

Mixed outcomes do not roll back or conceal successful independent actions.
Report what changed and what remains unapplied. A **Failed**, **Indeterminate**,
or **Manual** outcome blocks only its own action. An **Indeterminate** action
stops and asks as classified above while the remaining actions and the rest of
the mode continue, and the closing recap names every unapplied action.

Completion: every action has a classified outcome, each attempted supported
write has a readback-backed result or an indeterminate stop, and no action was
redirected or retried blindly.
