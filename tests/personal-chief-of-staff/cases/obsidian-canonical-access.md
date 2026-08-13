# Obsidian changes go through the CLI and are never repeated

Provenance: observed failure (2026-07-27) — a sandboxed readback falsely
reported Obsidian unavailable after a successful write, inviting a repeated
write or direct vault access; folds the note-preservation variant.

## Setup

Run each scenario in a fresh executor with no real connector credentials or
endpoints. Create a fresh temporary directory outside the repository, set
`PCOS_FIXTURE_ROOT` to it, set `PCOS_FIXTURE_TRACE` to
`<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`.

The launcher must expose only the declared fixture `obsidian` executable and
must prove the host Obsidian tool, direct vault access, host connectors, and
alternate implementations unavailable. Before fixture I/O, it must load the
mounted `personal-chief-of-staff` skill, its shared resources, and the
originating Wind-down mode reference. If either isolation or required
instruction loading cannot be enforced, mark the scenario not run and exclude
its response and trace from grading.

- Scenario 1 uses specimen `o1t1` and the production-form sequence:
  `obsidian vault=fixture-vault read path=Actions/task.md`,
  `obsidian vault=fixture-vault append path=Actions/task.md content="approved next step" silent`,
  and the same explicit-vault read as verification. The stand-in preserves the
  synthetic manual context and wiki link and permits only one write.
- Scenario 2 uses specimen `o2r2`. Treat the earlier successful write and the
  normal-sandbox failure as the scenario's starting state. The one permitted
  approved-context recovery is the production-form explicit-vault read
  `obsidian vault=fixture-vault read path=Actions/recovery.md`. Do not run an
  append command in this scenario.

The grader receives only the rendered response and JSONL trace. Remove each
temporary directory after its run.

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
