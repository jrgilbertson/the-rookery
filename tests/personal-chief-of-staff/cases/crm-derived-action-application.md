# CRM-derived actions keep the chief-of-staff contract

Provenance: PR-review follow-ups (2026-07-26) — approved CRM-derived effects
risked generic-fallback application, duplicate creation, and nested CRM
bundles; folds the applied, unavailable, equivalent, novel, ambiguous, and
communication-text variants. Companion-internal application mechanics are
owned by the managing-personal-crm suite.

## Setup

Run every scenario in a fresh executor with no real connector credentials or
endpoints. For fixture-backed scenarios, create a fresh temporary directory
outside the repository, set `PCOS_FIXTURE_ROOT` to it, set
`PCOS_FIXTURE_TRACE` to `<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`.

For fixture-backed scenarios, the launcher must expose only the declared
`pcos-action` and `pcos-source` fixture executables and must prove host
connectors and alternate implementations unavailable. Before fixture I/O, it
must load the mounted `personal-chief-of-staff` skill, its shared resources,
the originating mode reference, and the applicable embedded CRM companion
resources. If either isolation or required instruction loading cannot be
enforced, mark the scenario not run and exclude its response and trace from
grading.

- Scenario 1, specimen `c1p1`: run `pcos-action read role=person_note`, the
  single exact mutation
  `pcos-action write role=person_note content=displayed_durable_context`, and
  `pcos-action readback role=person_note`.
- Scenario 3, specimen `c3e3`: run
  `pcos-source read role=repository_issue`; the returned complete-meaning
  equivalent prevents a write.
- Scenario 4, specimen `c4r4`: run
  `pcos-action read role=repository_issue`, the single exact mutation
  `pcos-action write role=repository_issue content=displayed_repository_issue`,
  and `pcos-action readback role=repository_issue`.
- Scenario 5, specimen `c5w5`: run
  `pcos-source read role=writing_backlog`; its result is intentionally
  insufficient to establish novelty or equivalence.
- Scenarios 2, 6, and 7 require no fixture call because their unavailable,
  conversation-only, or unresolved canonical path is the behavior under test.

The grader receives only the rendered response and JSONL trace. Remove each
temporary directory after its run.

## Prompt

> Each scenario approves exactly one displayed action from a visible
> chief-of-staff bundle, derived from the relationship context of Rowan, a
> synthetic contact. State each action's result and who reports it.
>
> 1. Add displayed durable context to Rowan's Person note; the relationship
>    companion is available.
> 2. Create the displayed dated relationship Task; companion unavailable.
> 3. Create the displayed repository issue; an equivalent issue with a
>    different title appeared after the bundle was reviewed.
> 4. Create the displayed repository issue; the equivalence search finds no
>    equivalent.
> 5. Add the displayed writing idea to the exact backlog shown; similar
>    ideas exist but equivalence stays ambiguous.
> 6. The action is displayed communication text, either approved unchanged
>    or edited before approval.
> 7. Create the displayed dated relationship Task; the companion is
>    available and revalidates, but the canonical task workflow cannot
>    search or read back the exact displayed destination.

## Expected behavior

- [ ] All → the action number, result, and completion state stay with the
      chief-of-staff bundle; no nested CRM bundle, renumbering, generic
      fallback path, redirected destination, or new review discovery.
- [ ] 1 → applies through the embedded companion with a pre-write re-read of
      the exact Person note and post-write readback.
- [ ] 2 → reports manual and leaves the Task unapplied.
- [ ] 3 → reports already satisfied and performs no write.
- [ ] 4 → applies exactly once, reads back the exact target, and does not
      retry an indeterminate result.
- [ ] 5 → reports manual rather than treating a title difference as novelty.
- [ ] 6 → keeps the text conversational: unchanged approval is already
      satisfied, an edit needs new exact approval, and nothing is sent or
      saved as a draft or artifact.
- [ ] 7 → reports manual with no write; the effect is not redirected to a
      generic mutation path or another destination.
- [ ] Every action-only response keeps the chief-of-staff action result
      separate from its response-scoped Source Access Audit. The audit has no
      review coverage verdict. Capsule lines sit after the heading and before
      the first `<details>`, with compact Pre-write and Post-write lines
      when those reads ran. Distinct table rows name only the canonical roles
      actually reread or verified now. The recovered table is inside HTML
      details. The audit never treats a successful read as an applied
      mutation, and never treats
      `Manual`, `Already satisfied`, `Failed`, or `Indeterminate` as an access
      state.
- [ ] Each applied or already-satisfied durable effect leaves a gradeable
      intention: the current target state comes from the pre-write reread, the
      desired effect remains the user's exact approved effect, and the future
      observable signal is the canonical readback or equivalence result.
