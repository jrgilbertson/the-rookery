# Catch-up

Read this reference only for a one-time Person-note cleanup, triage,
reconstruction, merge, deletion, or migration request. Catch-up stays in one
visible conversation; it is not a background workflow.

## Confirm and prove the source inventory

Before triage, propose every relevant source for user confirmation. For each
source state:

- relationship role;
- active interface and account or identity;
- required or optional classification;
- supported read operations;
- stable identifiers and native timestamps;
- accessible time range;
- enumeration or search behavior;
- pagination or result limits;
- one representative boundary query; and
- observed probe result.

Run read-only probes only after the proposed scope is clear. Mark breadth that
cannot be established as **Indeterminate** rather than complete. A failed or
indeterminate required source ends **Blocked by preflight** and no triage bundle
is prepared. An unavailable optional source is disclosed, omitted, and narrows
only affected reconstruction claims. The user must confirm the final inventory
before stage one begins.

Completion: every confirmed source has an honest breadth result, all required
sources passed, and omitted optional coverage is explicit.

## Stage one: triage every Person note

Obtain a fresh Person-path inventory through the Obsidian CLI. Order the work
by evidence of recent contact or current relevance, then active-looking legacy
records, then the remainder. This ordering is not a stored priority score and
does not exempt any note.

Present up to 25 people per bundle, typically 15 to 25 when that many remain.
A final or otherwise smaller bundle may contain fewer than 15 people. Include
enough bounded evidence to choose one independent disposition:

- `active`, `dormant`, `reference`, or `ended`;
- `merge`, naming the candidate survivor and unresolved checks; or
- `delete`, for an empty, duplicate, or disposable record with no meaningful
  history, links, expertise, or provenance.

Use `reference` when a non-maintained record preserves meaningful history,
links, expertise, or provenance. A `merge` or `delete` is only a reviewed
classification; application follows the reversible-cleanup contract after a
separate exact proposal.

After each reviewed bundle, keep a compact conversational recap containing
Person-note path and disposition. Do not copy source evidence into the recap or
create a cursor, ledger, database, cache, progress note, or hidden queue.

Completion: every person in the bundle has an independent reviewed disposition
or remains explicitly pending, and no destructive action occurred during
triage.

## Stage two: reconstruct only retained relationships that need it

Skip rich reconstruction for records approved for deletion and references the
user judged already sufficient. For each other retained relationship, gather
only the available history needed to establish identity, recent contact,
durable meaning, cadence fields, and open commitments. Present:

- bounded source evidence and coverage limits;
- proposed target fields and concise anchored prose;
- uncertainty and identity conflicts;
- focused questions for unwritten context; and
- independently numbered destination effects.

The user reviews the person-level interpretation and each effect. A correction
may improve later proposals in this visible conversation, but creates no
feedback database or durable workflow rule. Apply only exact approvals under
the skill's approval contract.

Stage-two review may pause once each retained relationship is reconstructed,
confirmed already sufficient, or explicitly deferred, with every applied effect
read back. A deferred reconstruction remains outstanding catch-up work and does
not make the relationship completion-eligible.

## Resume from canonical evidence

On every resume, obtain a fresh CLI Person-path inventory and compare it with
the visible recap. Canonical Person notes prove applied outcomes; the recap
supplies only pending, deferred, already-sufficient, and no-change judgments.

If the recap is unavailable in a fresh conversation, disclose that unapplied
judgments cannot be recovered. Return every unproven path to review and ask the
user to establish the restart boundary; never estimate progress or infer it
from ordering.

End a catch-up turn as **Ready for review**, **Blocked by preflight**,
**Partial**, **Paused**, or **Catch-up complete**. Claim completion only after
the fresh inventory shows every existing Person path has a reviewed disposition
and every retained relationship that needs reconstruction is reconstructed or
confirmed already sufficient. A deferred stage-two reconstruction remains
outstanding work and prevents **Catch-up complete**. End **Partial** when that
work remains actionable in the catch-up, or **Paused** when continuation depends
on user action. Every reviewed `merge` or `delete` disposition must also meet one
of these conditions:

- its cleanup was proven **Applied** or **Already satisfied** through canonical
  readback; or
- the user revised it to `active`, `dormant`, `reference`, or `ended`, so no
  cleanup remains expected.

A cleanup that is **Pending**, **Manual**, **Failed**, **Indeterminate**,
**Deferred**, or **Skipped** prevents **Catch-up complete**. End **Partial**
when reviewed work remains actionable in the catch-up, or **Paused** when
continuation depends on user action or a safe cleanup path becoming available.

Completion: progress is reproducible from canonical notes plus visible user
decisions, with no hidden continuity state.
