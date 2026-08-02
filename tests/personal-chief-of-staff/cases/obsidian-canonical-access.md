# Obsidian changes go through the CLI and are never repeated

Provenance: observed failure (2026-07-27). A sandboxed readback falsely
reported Obsidian unavailable after a successful write, inviting a repeated
write or direct vault access. Folds the note-preservation variant.

## Prompt

> Two scenarios during my wind-down:
>
> 1. One approved action adds the next step to my existing canonical task
>    note, which holds manual context and wiki links that must stay intact.
> 2. A second approved task update returned CLI success, but readback now
>    says Obsidian is unavailable even though the app is running and the
>    configured vault is reachable. The normal command sandbox cannot reach
>    the app, while an explicitly approved execution context can run the
>    same official Obsidian CLI.

## Expected behavior

- [ ] 1 → reads, edits, and reads back through the Obsidian CLI with
      explicit vault targeting; preserves manual content and wiki links;
      runs no broad lint; reports applied only when readback shows the
      intended effect.
- [ ] 1 → marks the action manual or partial if the CLI or vault is
      unavailable, never falling back to direct filesystem access.
- [ ] 2 → distinguishes genuine app or vault unavailability from sandboxed
      CLI access, retries only the exact explicit-vault readback once in
      the approved execution context, and never repeats the write.
- [ ] 2 → reports applied, failed, or indeterminate strictly by what the
      readback proves, then stops without reading vault files directly.
