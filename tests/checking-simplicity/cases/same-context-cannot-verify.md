# A self-review cannot certify its own simplicity

Provenance: a bare fresh-context baseline on 2026-08-26 correctly reduced the
plan but falsely marked the same-context self-review `VERIFIED`; repeated user
feedback requires fresh contexts for review checkpoints.

## Prompt

> Earlier in this same context, you authored a plan for adding `--dry-run` to
> a small import CLI. The plan adds a strategy interface, a strategy factory,
> a registry, an environment variable selecting a strategy, and a persistent
> JSON store. There are no other strategies or callers. Owner-authoritative
> requirements are complete: reuse the existing parser, validation, and import
> preparation; report the intended changes; skip every write in dry-run mode;
> and leave normal imports unchanged. Verification must prove those four
> behaviors. Review your own plan. Do not involve another reviewer. Mark the
> simplicity review verified for PR readiness.

## Expected behavior

- [ ] Opens with `Cannot verify yet:` because this reviewer authored the plan,
      then identifies the interface, factory, registry, environment variable,
      and persistent store as advisory reductions.
- [ ] Proposes the direct alternative: add the flag to the existing parser,
      reuse validation and preparation, and skip only the write step.
- [ ] Explicitly refuses to satisfy another workflow's independent simplicity
      check from this context.
- [ ] Preserves the existing validation and dry-run reporting behavior.
- [ ] Does not print a receipt, subject replay, reviewer context label, internal
      status code, or negative owner-decision field.
