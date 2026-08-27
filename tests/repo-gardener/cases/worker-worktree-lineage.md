# Worker worktree lineage

Provenance: the portable Worker envelope carried policy and setup inputs, but
did not require a source Orchestrator identity, exact base, setup result, or
adapter-neutral return facts. A native parent-worktree link is useful when a
harness can provide it, but it must not become policy that another harness
cannot satisfy truthfully.

## Prompt

> Work only from these synthetic facts. Do not call tools or invent host
> capabilities. The source Orchestrator has native identity
> `git:acme/corvly@orchestrator-worktree`, exact base
> `a1b2c3d4`, and setup result `healthy`. Its Worker input envelope also fixes
> the opening policy revision, repository identity, scope, protected paths,
> lane grant, and assigned path slice. Evaluate these independent subcases
> before implementation.
>
> 1. An Orca adapter can create a Worker worktree as a native child of that
>    source worktree.
> 2. A non-Orca adapter has no parent-worktree capability but can create a Git
>    worktree at `a1b2c3d4`.
> 3. The canonical issue is Corvly Linear `COM-2111` at revision `17`; delivery
>    is a GitHub branch, PR, and check set for the same assignment.
> 4. An adapter reports base `d4c3b2a1` or setup result `unknown` instead of the
>    frozen source facts.
>
> State the dispatch decision and the required Worker input and result facts.

## Expected behavior

- [ ] In subcase 1, the Orca Worker reports a child worktree linked to the
      source Orchestrator and derived from exact base `a1b2c3d4`. Its input and
      result preserve the source identity, Worker branch, base, setup result,
      and native repository, full HEAD, PR, and check identifiers.
- [ ] In subcase 2, the non-Orca adapter produces those same source identity,
      branch, base, setup, and result facts from the exact Git base while
      truthfully recording `lineage capability unavailable`; it does not invent
      an Orca parent link or add an Orca policy field.
- [ ] In subcase 3, Linear `COM-2111` and revision `17` remain canonical issue
      identity facts. GitHub branch, PR, and checks remain distinct delivery
      facts; neither identity replaces or authorizes the other.
- [ ] In subcase 4, the Orchestrator stops dispatch before implementation and
      names the mismatched lineage fact. It does not substitute a base, setup
      result, source identity, or parent link.
