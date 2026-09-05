# Current official docs inform viable approaches

Provenance: the owner asked whether stale model knowledge would miss a smaller
native capability unless the review could check current official docs, and
later noted that a best-practice article can itself describe a simpler
approach if it is not allowed to add unneeded machinery. The frozen prior
version failed this case 1/4 and then 2/4 in matched comparisons by climbing
the necessity ladder from memory without checking current official docs.

## Prompt

> You are the dispatched simplicity reviewer. The subject is an export path
> that already uses the installed Stripe SDK plus a custom webhook retry
> worker. A documentation tool is available. How does this skill inform
> viable approaches before comparing whole-system shapes? Return the answer
> only.

## Expected behavior

- [ ] Checks current official docs for platforms or libraries already named
      in the subject.
- [ ] Uses that lookup to confirm whether a native capability already covers
      the need, rather than relying on memory alone.
- [ ] Allows a current best-practice article to inform a smaller approach, and
      does not let it introduce a new stack or extra machinery the current
      need does not require.
- [ ] Still compares whole-system shapes before individual concepts.
