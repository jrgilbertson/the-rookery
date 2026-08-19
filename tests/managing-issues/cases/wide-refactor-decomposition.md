# A wide refactor uses expand–migrate–contract

Provenance: covers the prior skill's missing exception for cross-cutting
migrations that cannot remain working when divided into ordinary vertical
slices.

## Prompt

> Break the approved account-ID migration into Linear issues in workspace
> `acme`, team `ENG`. Billing, ledger, and reporting currently read an integer
> account ID. The approved replacement is an opaque string ID. Changing the
> shared type in place would break all callers, and the services cannot migrate
> in one reviewable pull request. The system must stay working throughout.
> Priority choices are `high` and `normal`; this migration is approved as
> `high`. Labels are `migration`, `accounts`, and `backend`. Estimates are 1, 2,
> 3, and 5; planning evidence sizes expand and contract as 2 and every service
> migration as 3. Readiness mappings are `needs-discovery`, `needs-planning`,
> and `ready`. Show the issue family and dependencies, but do
> not create anything yet. Authenticated provider discovery confirms that the
> workspace and team are active, every named metadata value exists, and native
> issue creation, parent/child, and blocker relationships are available. The
> operator selected the Orca CLI for this session. Its installed version-matched
> `orca-linear` guide is loaded and confirms the exact create, metadata,
> parent/child, and blocker syntax needed for this batch.

## Expected behavior

- [ ] Recognizes that ordinary vertical slices cannot keep the repository
      working and uses expand–migrate–contract rather than layer tickets.
- [ ] Expands by introducing the new ID form alongside the old without breaking
      existing callers.
- [ ] Divides migration into independently safe, reviewable consumer batches and
      keeps batches parallel unless a real blocker exists.
- [ ] Contracts by removing the old form only after every migration batch is
      complete.
- [ ] Shows a compact decomposition check for every leaf with its demonstrable
      outcome, why it remains separate, and every blocker with its reason.
- [ ] Gives every leaf independently observable Verification and estimates only
      childless implementation leaves.
- [ ] Shows the parent, children, native blocking edges, metadata analysis, and
      complete ordered preview, then asks for direct approval without beginning
      implementation or tracker writes.
