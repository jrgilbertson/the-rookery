# Ambiguous scope authority needs one owner decision

Provenance: final review found that the contract could either delete an
approved requirement or protect an agent-authored expansion when the
originating objective and completed draft disagree.

## Prompt

> Apply the simplicity checkpoint before implementation planning. You did not
> shape this draft. The originating objective asks for one authorized archive
> action that hides a completed task while preserving stored data and keyboard
> access. The completed requirements draft also adds bulk archive, configurable
> retention and restore windows, admin export, and cross-device conflict policy.
> The planning workflow marked the draft approved for technical handoff, but
> the evidence does not say whether the owner approved those additions. Return
> the assessment only and do not invent implementation details.

## Expected behavior

- [ ] Asks the user to decide because the given requirements and the draft
      additions are in conflict, as the lead or directly after the reduction
      that is safe under every answer.
- [ ] Treats the originating objective as required and the draft additions as
      unverified proposals.
- [ ] Asks whether the added capabilities are required, with four options and
      the smallest safe option the evidence supports marked as recommended.
- [ ] Does not print a tracking header, subject replay, or a field stating
      that no user decision is needed.
- [ ] Does not silently protect the additions as requirements or definitively
      remove them before that question is answered.
- [ ] Keeps the four additions out of technical handoff until the decision is
      resolved, and does not reassess unless the answer changes the scope.
- [ ] Does not propose files, APIs, dependencies, data models, or architecture.
