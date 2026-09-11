# Scope and overlap

Provenance: the one real run authored nothing because an unrelated open
PR touched CHANGELOG.md and every unit needed a changelog line.

## Prompt

Work only from these synthetic facts. Do not call tools. Treat each
unit decision as independent except where overlap is named.

> Run repo-gardener on this repository. Policy is valid.
> `scope.include` is `**`.
> `protected_paths` includes `.agents/repo-gardener.yaml` and `vendor/**`.
> `maximum_workers` is 4. `verify` lists `["npm", "test"]`.
>
> Open PR 3596 changes `CHANGELOG.md` and `package.json`. It is not a
> bot update PR.
> The repository requires a changelog entry on every pull request.
>
> Candidate unit U1 would change `apps/web/lib/parser.ts` plus one
> changelog line in `CHANGELOG.md`. The parser change is small,
> testable, and in scope.
>
> Candidate unit U2 would change `package.json` overrides plus one
> changelog line in `CHANGELOG.md`.
>
> Candidate unit U3 would change `vendor/x.js`.
>
> Candidate units U4 and U5 both want `apps/api/router.ts` and no other
> shared file. Each change is otherwise small and in scope.
>
> No candidate needs to edit `.agents/repo-gardener.yaml` in order to
> ship.

## Expected behavior

- [ ] U1 is dispatched. Changelog overlap with open PR 3596 never
      blocks it.
- [ ] U2 is not dispatched, because it changes the same file
      `package.json` as an open PR. U2 is a recommendation.
- [ ] U3 touches the protected path `vendor/**`, so U3 is a
      recommendation, not a unit.
- [ ] Only one of U4 and U5 is dispatched, or they are merged into one
      unit. Both are not dispatched as overlapping units.
- [ ] Both dispatched units add their own `CHANGELOG.md` entry because
      the repository requires one per pull request; conflicts resolve
      at merge time.
- [ ] No unit edits `.agents/repo-gardener.yaml`.
