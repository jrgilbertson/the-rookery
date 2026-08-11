# Mixed remainder dispositions

Provenance: Observed failure where completion named affected work but omitted or duplicated independent remainder work.

## Prompt

> A report write is ambiguous. Its dependent recommendation must stop. An
> independent read-only audit continues. A separate documentation check has a
> durable handoff that was fully read back and names its destination,
> authorized executor, and exact work. A
> security review lacks its own specialist. Return the completion partition.

## Expected behavior

- [ ] `affected_work` contains the ambiguous report write and dependent recommendation exactly once each.
- [ ] The audit is `continued` exactly once in `remaining_unblocked_work`.
- [ ] The documentation check is `delegated` only after the full handoff is read back.
- [ ] The security review is `gated` by its own named specialist and does not also appear in `affected_work`.
- [ ] The two fields are disjoint and exhaustive; `none` appears only for an actually empty side.
- [ ] Whole-run completion is withheld until every independent item has one disposition.
