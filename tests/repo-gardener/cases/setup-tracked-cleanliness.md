# Setup tracked cleanliness

Provenance: the setup lifecycle checks ordinary Git status after setup, but a
tracked file changed under `skip-worktree` or `assume-unchanged` can leave that
status empty. The setup boundary must compare working-tree bytes and index
flags with its clean starting index without repairing any reported change.

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
> 3. A successful setup edits `tracked.txt` after setting either
>    `skip-worktree` or `assume-unchanged`, so ordinary status is empty.
> 4. A successful setup creates ignored `runtime/output.txt`, then separately
>    creates non-ignored `sibling.txt`.

## Expected behavior

- [ ] Before setup, the Worker captures the clean starting index and relevant
      index flags. After setup returns and its process tree stops, it combines
      ordinary staged, unstaged, and untracked checks with a comparison of
      every tracked working-tree byte and relevant flag against that snapshot.
- [ ] In subcase 1, both setup invocations pass and dependent work may begin.
- [ ] In subcase 2, each exact changed path is reported and only the affected
      dependent work stops. The separate Worker continues its safe work.
- [ ] In subcase 3, `tracked.txt` is reported even though ordinary status is
      empty. `skip-worktree` and `assume-unchanged` are never treated as a
      cleanliness exception.
- [ ] In subcase 4, ignored runtime output is allowed, while `sibling.txt` is
      reported as a non-ignored untracked path.
- [ ] No subcase restores, ignores, stages, commits, substitutes, retries, or
      otherwise repairs setup-created dirt. A later fresh setup may proceed
      only after the host fixes the output or explicitly ignores it.
