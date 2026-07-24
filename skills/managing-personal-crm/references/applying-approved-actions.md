# Applying Approved Actions

Read this reference before interpreting approval or applying a relationship
effect. Approval binds to one exact visible effect, not to a person or bundle.

## Bind each decision

Each numbered effect must show acting identity, authoritative destination,
exact target or creation location, complete content or effect, evidence and
reason, and dependencies. The user may approve, edit, defer, or skip each one.
An edit creates a revised numbered proposal that needs approval.

An unnumbered approval applies only when exactly one visible effect has exactly
one interpretation. With multiple effects or any ambiguity, write nothing and
ask for action numbers. Approval of a dependent effect does not approve its
prerequisite, and approval never transfers to another identity, destination,
target, visibility, content, or effect.

Completion: every selected action maps to one exact displayed proposal and all
prerequisites have independent decisions.

## Recheck before application

Immediately before each approved effect, use the authoritative interface to:

1. Re-read the exact target for an update or the exact parent, destination,
   thread, or backlog for a create.
2. Search for an equivalent effect using stable identity and complete meaning,
   not title similarity alone. Equivalent means the same owning identity,
   canonical destination, target or subject, commitment or durable fact, and
   material content; superficial wording differences do not make a duplicate
   novel.
3. Revalidate identity, destination, target, content, visibility, and
   prerequisites against the approved proposal.

If the equivalent exists, write nothing and report **Already satisfied**. If a
material field drifted, invalidate only that approval and present a revised
effect. If the complete read or comparison cannot run safely, report
**Manual**; do not redirect the effect.

Completion: each approved effect is still necessary, unambiguous, and bound to
the current destination.

## Apply once and read back

Apply ready effects in dependency order. One effect that combines changes to a
single target must use an operation that produces the complete approved result
or no result. If the interface cannot do that, split it into separate proposals
and obtain approval before either write.

For every Person-note read, search, create, edit, move, rename, merge, trash,
restore, or readback, use the Obsidian CLI with explicit configured-vault and
target selection. Preserve unrelated metadata, manual prose, wikilinks,
embeds, and Comments. Never substitute direct vault-file access or broad vault
linting.

Apply each supported effect once, then read the target back through the same
authoritative interface. Use exactly one result:

- **Applied:** readback shows the complete approved effect.
- **Already satisfied:** the pre-write check found an equivalent effect.
- **Failed:** readback confirms the effect is absent.
- **Indeterminate:** readback cannot establish whether it occurred.
- **Manual:** no available interface can safely apply and verify it.
- **Deferred:** the user chose to revisit it later.
- **Skipped:** the user declined it or its prerequisite was not satisfied.

Never retry an **Indeterminate** effect blindly. A failed or indeterminate
prerequisite skips dependent effects while unrelated approvals may continue.
Keep a successful independent effect even when a later effect fails; report the
partial result and propose only a bounded repair.

Communication text remains in the conversation and is never sent or created
as an external draft by this skill. If approved unchanged, report **Already
satisfied** because the editable text is already visible. Unsupported external
writes are **Manual**.

Completion: every decided effect has one readback-backed result or safe stop,
and no effect was redirected, duplicated, or retried blindly.

## Keep cleanup reversible

A catch-up `merge` or `delete` disposition authorizes no destructive action.
A later proposal must identify the survivor, duplicate, exact content and link
effects, and every alias or identity collision.

Before any cleanup application, prove the active vault's trash behavior with a
disposable CLI-created note that can be trashed, restored, and read back intact.
For a merge, apply and read back the survivor first, review backlinks and
aliases, then move the duplicate to verified Obsidian trash. A delete likewise
moves only the reviewed target to verified trash. Permanent deletion is not an
available action.

If trash and restore cannot be proven, mark cleanup **Manual** and leave every
note intact.

Completion: the survivor is complete, links and identities are accounted for,
and any removed note remains recoverable from verified trash.

## Report only observed outcomes

List a result for every selected or explicitly decided effect and list all
other visible effects as **Pending**. Pending is not an application outcome.
State what remains unapplied for every failed, indeterminate, manual, deferred,
or skipped effect.

Applied Person notes and destination records prove durable outcomes. Do not
create a transaction log, workflow ledger, or private application state.

Completion: the user can verify every claimed effect in its authoritative
system and knows exactly what still needs review.
