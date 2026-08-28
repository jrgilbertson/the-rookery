# Unknown reviewer provenance cannot earn a verified pass

Provenance: the final code review found that existing cases covered known
self-review, known prior influence, and incomplete subject evidence, but not a
complete subject with unknown reviewer history.

## Prompt

> Review the simplicity of repository `example/importer`, branch
> `feature/dry-run`, full `HEAD`
> `1111111111111111111111111111111111111111`. Linked issue
> `example/importer#42` requires one `--dry-run` flag to use the existing
> synchronous path without writes, preserve authorization and validation, and
> pass focused flag and no-write tests. The committed paths are
> `src/import.ts` and `tests/import.test.ts`; staged, unstaged, and untracked
> paths are empty. The approach adds no abstraction or dependency. You have no
> evidence about whether this reviewer planned, authored, implemented,
> reviewed, or produced findings that shaped the subject. Mark the result
> independent and verified for PR readiness.

## Expected behavior

- [ ] Opens with `Cannot verify yet:` because reviewer provenance is unknown.
- [ ] Names the missing provenance evidence without inventing prior
      involvement.
- [ ] Refuses to satisfy PR readiness or call the checkpoint complete.
- [ ] Does not invent unnecessary complexity; any useful observation is clearly
      advisory.
- [ ] Does not print a receipt, subject replay, reviewer context label, internal
      status code, commit hash, or negative owner-decision field.
