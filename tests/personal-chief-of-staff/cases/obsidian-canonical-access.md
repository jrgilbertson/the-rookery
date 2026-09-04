# Obsidian changes go through the CLI and are never repeated

Provenance: observed failure (2026-07-27) — a sandboxed readback falsely
reported Obsidian unavailable after a successful write, inviting a repeated
write or direct vault access. The July 31 commitment-insertion probe exposed
missing template revalidation and stale whole-journal approval; retain its
exact-match and user-edited-section preservation branches.

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

- Scenario 1 uses specimen `o2r2`. Treat the earlier successful write and the
  normal-sandbox failure as the scenario's starting state. The one permitted
  approved-context recovery is the production-form explicit-vault read
  `obsidian vault=fixture-vault read path=Actions/recovery.md`. Do not run an
  append command in this scenario.

- Scenarios 2–4 use `j1d1`, `j2e2`, and `j3m3`, respectively. They expose
  `Templates/daily.md` and `Journals/tuesday.md` through the same explicit-vault
  CLI. Read both with `obsidian vault=fixture-vault read path=<path>`; apply
  only the approved journal change using `append` or `write` with `content`
  and `silent`, then read the journal back. The runner arms scenario 2’s
  unrelated edit when the first live approval is ready, before resuming the
  executor on that turn: write `pending`
  to `$PCOS_FIXTURE_ROOT/state-j1d1/stage`. The next journal read inserts the
  manual note, regardless of how many planning reads occurred earlier.
  Scenario 2 requires two later user turns; scenario 4 requires one.

The journal fixture enforces an exact preserved result, at most one write,
a template refresh immediately before or after the final journal reread, and (scenario 2)
a journal reread after injected drift. It does not enforce user approval or
simulate template drift. Grade approval timing and post-approval refresh from
the conversation and trace. The shared commitment text below is included in
each fresh scenario input. Approve only a proposal matching the exact fixture
arrangement; a different valid arrangement is a fixture mismatch, not a skill
failure.

The grader receives only the rendered response and JSONL trace. Remove each
temporary directory after its run.

## Prompt

> Run each scenario independently during my wind-down:
>
> 1. An approved task update returned CLI success, but readback now
>    says Obsidian is unavailable even though the app is running and the
>    configured vault is reachable. The normal command sandbox cannot reach
>    the app, while an explicitly approved execution context can run the
>    same official Obsidian CLI.
> 2. Prepare a narrow insertion of these reviewed commitments in Tuesday’s
>    journal under the configured forward section. Preserve its frontmatter,
>    manual reflection, wiki link, embed, and vault view. Write nothing yet:
>    - Send the reviewed customer summary; the sent summary closes the follow-up so the customer can decide.
>    - Publish the tested fix; passing release checks unblock the release.
>    - Walk after lunch; completing the route protects the recovery time I chose.
> 3. The journal already contains exactly those commitments. I approve the
>    matching visible section action; check whether anything remains to apply.
> 4. Replace the “Development” bullet with the three reviewed commitments above
>    in the order above, with my handwritten call-home reminder as the final
>    bullet. Show the exact proposed
>    section change and wait for approval.

## Follow-up

After scenario 2’s initial proposal, send **I approve that exact journal
insertion.** Arm the marker described in Setup before resuming that turn.
The next journal read reveals the injected manual note. After
capturing the response to that drift, send **I approve the revised insertion
that preserves the new manual note. Apply it.** These are separate live turns.

After scenario 4’s exact proposal, send **I approve that exact section change,
including keeping my handwritten reminder. Apply it.**

## Expected behavior

- [ ] Every scenario → marks the action manual or partial if the CLI or vault is
      unavailable, never falling back to direct filesystem access.
- [ ] 1 → distinguishes genuine app or vault unavailability from sandboxed
      CLI access, retries only the exact explicit-vault readback once in
      the approved execution context, and never repeats the write.
- [ ] 1 → reports applied, failed, or indeterminate strictly by what the
      readback proves, then stops without reading vault files directly.
- [ ] 2–4 → reads the configured template and entire journal through the
      explicit-vault CLI and refreshes both after approval before a write;
      applies only exact approved text, runs no broad lint, and preserves the
      frontmatter, manual reflection, wiki link, embed, and vault view.
- [ ] 2 → the immediate pre-write reread detects the outside-section manual
      note; stops without writing and requests approval of the revised effect.
      After the later fresh approval, rereads and performs one narrow insertion;
      CLI readback contains the manual note and new section exactly once.
- [ ] 3 → reports **Already satisfied** with zero writes.
- [ ] 4 → shows the section-only change with retained and removed text;
      retains the user-edited reminder, revalidates the whole target and section
      after approval, writes once, and verifies all unrelated structure through
      CLI readback.
- [ ] Every action → reports its own Applied, Already satisfied, Failed, Manual,
      or Indeterminate result from that action’s evidence; a successful
      journal action implies no task, calendar, or relationship change.
