# Dependencies, drift, and failed pre-writes stay contained

Provenance: U2 regression contract. Folds the declined-prerequisite,
failed-prerequisite, target-drift, and pre-write-validation variants. The
bare package had no application contract.

## Prompt

> Approved actions from one visible bundle: Action 1 creates a canonical
> issue; Action 2 creates a calendar block that explicitly depends on Action
> 1; Action 3 is an unrelated durable-context update. For each situation,
> state each action's reported outcome and any write that occurs.
>
> 1. The user approves Actions 2 and 3 but declines Action 1.
> 2. All three approved; Action 1's write fails, or its readback is
>    indeterminate.
> 3. All three approved; before application, Action 3's target note changed
>    materially since the proposal.
> 4. All three approved; the authoritative re-read for Action 1 is
>    unavailable, while Action 3's pre-write validation succeeds.

## Expected behavior

- [ ] 1 → Action 1 is not applied (user-declined) with no write; Action 2 is
      **Skipped** (prerequisite unsatisfied) with no orphan event and no
      implicit issue; Action 3 applies once with readback.
- [ ] 2 → Action 1 reports **Failed** when the write is confirmed absent, or
      **Indeterminate** when readback cannot establish it — an indeterminate
      result is reconciled, never blindly retried and never assumed written
      or unwritten; Action 2 is **Skipped**; Action 3 applies once with
      readback.
- [ ] 3 → Action 3 is not applied and returns as a revised proposal requiring
      approval of its new exact content; Action 1 applies once, then Action 2
      applies with its prerequisite satisfied.
- [ ] 4 → Action 1 performs no mutation and is **Manual**; Action 2 is
      **Skipped** (its prerequisite was not applied); Action 3 applies once
      after its own pre-write validation succeeds.
