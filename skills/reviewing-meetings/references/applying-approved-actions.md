# Applying Approved Actions

Read this reference before interpreting approval or applying any proposed
meeting action. Approval is bound to the exact visible effect, not to the
meeting, category, or bundle as a whole.

## Require unambiguous approval

Apply only a visible numbered action whose displayed identity, authoritative
target, visibility, complete effect, reason, and dependencies leave exactly one
interpretation. Missing or ambiguous approval-binding information writes
nothing and returns to proposal review.

The user may approve, edit, defer, or skip actions independently. Apply only
the actions the user unambiguously approved. When exactly one visible action
has exactly one interpretation, an unnumbered response such as `looks good`,
`go ahead`, or `approved` may approve that sole action. The same response writes
nothing when more than one visible action or interpretation remains possible;
ask which action numbers it applies to. An edit creates a revised numbered
proposal whose exact new content must be approved.

Approval of a dependent action never implies approval of its prerequisite.
Approval does not transfer to a different identity, destination, target,
visibility, content, or effect.

A deferred action remains the same numbered proposal in the visible bundle. It
is not terminal and must not be replaced or recomputed by an overlapping
meeting check. At the user's explicit revisit point, or when the user asks to
recover it, return that existing action to review and perform fresh pre-write
checks only after approval.

Completion: each selected action maps to one exact displayed proposal and all
required prerequisites have their own decisions.

## Re-read before writing

Immediately before each approved writable action, use the authoritative
interface to:

1. Re-read the exact target for an update, or the destination, parent, thread,
   or calendar for a create.
2. Search for an equivalent task, issue, note change, event, or other supported
   effect using stable identity and content as the destination supports.
3. Revalidate the acting identity, destination, target, visibility, approved
   content or effect, and prerequisite state.

If the approved effect already exists, make no write and report **Already
satisfied**. If a material field changed, cannot be distinguished, or became
ambiguous, invalidate only that action and present a revised proposal. Other
approved actions may continue when their own reads and prerequisites remain
valid.

If any required authoritative re-read or search is unavailable, fails, returns
ambiguous results, or cannot establish the complete validation, make no write
and report that action **Manual**. Do not proceed with it until a later
re-read and search establish the target, duplicate, and prerequisite state.
Unrelated approved actions may continue when their own validation succeeds.

Completion: each write is still necessary, targets the approved object, and
has not been redirected by changed state.

## Apply relationship effects through their canonical owners

For an approved Person-note or relationship Task effect, use the available
`managing-personal-crm` companion semantics for the pre-write equivalence check,
identity validation, canonical destination, and readback. Every Person-note
operation must use the Obsidian CLI with explicit configured-vault and target
selection. A dated relationship follow-up belongs in the configured canonical
relationship task system; unrelated work remains with the issue or task owner
selected during routing.

The companion remains optional for meeting completion. If it is unavailable or
cannot establish the complete safe write path, report that relationship action
**Manual** and leave it unapplied. Do not redirect it, edit the vault directly,
or treat approval of the meeting note as approval of the relationship effect.

Completion: each approved relationship effect is applied by its authoritative
owner or stops safely without changing the rest of the meeting review.

## Apply once in dependency order

Order selected actions by their explicit dependencies, not by category. A
prerequisite is satisfied only when its outcome is **Applied** or **Already
satisfied**. Apply each ready supported action once, then read the created or
updated target back through the same authoritative interface.

Before changing a target, validate the complete approved mutation against the
current target without writing. When one action combines multiple edits to one
target, apply them with one supported operation that either produces the whole
approved effect or produces no effect. If the authoritative interface cannot
do that, split the edits into separately numbered proposals and obtain exact
approval for each before writing any part. Do not implement one approved action
as a sequence that can leave an unreviewed partial target state.

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

Communication proposals are non-writing actions. When the user approves one
unchanged, keep its exact text in the conversation, create no external draft,
send nothing, and report **Already satisfied** because the approved text is
already visible. An edit remains a revised proposal that requires approval.

Do not retry an **Indeterminate** action. Stop that action and ask how to
proceed. A **Failed** or **Indeterminate** prerequisite makes each dependent
action **Skipped**, with the prerequisite named. Unrelated approved actions may
continue.

Completion: every selected or decided action has one outcome, every attempted
write has authoritative readback, and no effect was applied twice.

## Preserve partial success

Treat canonical artifacts and their dependent links as separate effects. If a
task, issue, note, or event succeeds but a dependent backlink fails or is
indeterminate, keep the successful artifact as canonical. Report both
outcomes, retain the partial success, and propose a bounded repair when useful.

Do not roll back a successful prerequisite, recreate it, or retry a dependent
effect blindly. If the approved meeting note content depends on a task or
issue link that did not succeed, skip the dependent note action and return a
revised proposal showing the exact linkless content or another repair. Write
linkless note content only after the user explicitly approves that revised
effect. An independently approved note action whose content does not depend on
the failed link may still proceed.

Completion: successful work remains visible once, broken links stay explicit,
and repair does not risk duplication.

## Report the application result

Report an application outcome only for each action number the user selected or
explicitly decided, with the readback evidence that supports it. List every
other visible action separately as **Pending** for review. **Pending** is not an
application outcome and performs no write. For **Failed**, **Indeterminate**,
**Manual**, **Deferred**, or **Skipped**, state what remains unapplied and the
next safe choice. Do not describe a conversational draft as an external draft
or a proposed action as a completed change.

When every visible action for one meeting has an explicitly terminal outcome
and no pending, deferred, failed, indeterminate, manual, revised, or otherwise
review-needed action remains, identify that meeting as **Reviewed in this
conversation** in the visible recap. **Applied**, **Already satisfied**, and an
explicitly terminal **Skipped** action can close a bundle. A skip caused by an
unresolved prerequisite is not terminal while a repair choice remains. This
conversational disposition prevents a later overlapping run from regenerating
the bundle, but it is not a whole-meeting dismissal and creates no durable
state.

End with a compact recap of what changed, what was already satisfied, and what
still needs review or repair. The approved meeting note and each downstream
artifact remain ordinary records in their owning systems; create no workflow
ledger, transaction record, or private application state.

Completion: the user can verify each effect in its authoritative system and
knows exactly what remains.
