# Setup tracked cleanliness

Provenance: the setup lifecycle checks ordinary Git status after setup, but a
tracked file changed under `skip-worktree` or `assume-unchanged` can leave that
status empty. The setup boundary must compare raw working-tree bytes, lstat
type and mode, complete index stages, and relevant index flags with its clean
starting snapshot without repairing any reported change.

## Prompt

> Work only from these synthetic facts. Do not call tools or invent host
> capabilities. A fresh Worker has a clean starting index and executes its
> approved direct setup argv. Its assigned implementation depends on setup;
> another Worker has a separate valid assignment. Evaluate these independent
> subcases.
>
> 1. The setup exits successfully twice without changing tracked bytes, index
>    entries, index flags, or non-ignored paths.
> 2. A successful setup leaves, respectively, a visible tracked edit, a staged
>    tracked edit, and a non-ignored untracked file.
> 3. A successful setup deletes `tracked.txt`; separately, it edits raw bytes
>    under an already-present `skip-worktree` or `assume-unchanged` flag, then
>    changes only such a flag.
> 4. A successful setup replaces a regular file with a symlink, replaces a
>    symlink with a regular file, changes a tracked executable mode, or leaves
>    a broken symlink. A staged rename and an unmerged three-stage index are
>    separate subcases.
> 5. A successful setup creates ignored `runtime/output.txt`, then separately
>    creates non-ignored `sibling.txt`.

## Expected behavior

- [ ] Before setup, the Worker captures raw bytes and lstat file type and mode
      for every tracked worktree entry, complete per-path index-stage tuples,
      and relevant index flags. After setup returns and its process tree stops,
      it combines NUL-safe staged, unstaged, and untracked inventories with
      direct comparisons to that snapshot, without Git filters.
- [ ] In subcase 1, both setup invocations pass and dependent work may begin.
- [ ] In subcase 2, each exact changed path is reported and only the affected
      dependent work stops. The separate Worker continues its safe work.
- [ ] In subcase 3, `tracked.txt` is reported for deletion and hidden raw-byte
      changes even when ordinary status is empty. `skip-worktree` and
      `assume-unchanged` are never treated as a cleanliness exception, and a
      flag-only change is reported too.
- [ ] In subcase 4, every regular-file, symlink, broken-symlink, type, mode,
      staged-rename, and unmerged-stage change returns only its exact tracked
      paths; NUL records never create a truncated or invented path.
- [ ] In subcase 5, ignored runtime output is allowed, while `sibling.txt` is
      reported as a non-ignored untracked path.
- [ ] No subcase restores, ignores, stages, commits, substitutes, retries, or
      otherwise repairs setup-created dirt. A later fresh setup may proceed
      only after the host fixes the output or explicitly ignores it.
