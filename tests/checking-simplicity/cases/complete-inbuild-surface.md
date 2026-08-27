# A complete in-build surface gets a concrete reduction

Provenance: an earlier independent review found that the in-build branch needed
a complete-surface behavioral comparison. The 2026-08-27 output review found
that receipt fields and evidence appeared before the recommendation, burying
the decision this assessment exists to support.

## Prompt

> Apply the in-build simplicity checkpoint to this complete synthetic subject.
> You did not plan, author, implement, review, or shape it. Do not inspect any
> other source.
>
> Objective and requirements: make the existing synchronous export operation
> tolerate one transient write failure. Preserve the existing authorization
> check, one audit event per completed export, a maximum of two total write
> attempts, and the terminal error when both attempts fail. No restart recovery,
> asynchronous work, alternate exporter, or operator-tunable policy is required.
>
> Subject binding:
> - repository: `example/exporter`
> - branch: `feature/bounded-export-retry`
> - full HEAD: `4b21b6b4874c0c82e99e2240a32f1ca958f36d55`
> - committed paths: `src/export.ts`, `src/auth.ts`, `src/audit.ts`
> - staged paths: `src/retry-engine.ts`, `src/export.ts`
> - unstaged paths: `src/retry-provider.ts`, `src/retry-config.ts`
> - untracked paths: `src/retry-job-state.ts`
>
> Current surface content: committed `src/export.ts` directly authorizes,
> writes, emits the completion audit event, and returns the terminal write
> error. The staged edit routes each write through a new retry engine and event
> bus. The unstaged files add a provider interface, plugin registry, and runtime
> configuration for retry policy. The untracked file persists attempt state for
> restart recovery. The standard library already provides bounded in-process
> retry around a function call.
>
> Return the assessment only. Do not edit the implementation or decide whether
> it is ready to ship.

## Expected behavior

- [ ] Leads with a plain-language `Verdict` and the smallest safe
      `Recommendation` before `Why`, protected complexity, next action, owner
      decision, or receipt details.
- [ ] Gives claim-first `Why` reasons that remove, reuse, or defer machinery,
      with the requirement and subject evidence inline after each claim.
- [ ] Returns `CHANGES_NEEDED` with `Review context: independent`.
- [ ] Repeats the exact repository, branch, full HEAD, and committed, staged,
      unstaged, and untracked path inventories in the final review receipt's
      `Subject`.
- [ ] Repeats the supplied objective, requirements, verification criteria, and
      current surface content in the final review receipt's `Subject` rather
      than reducing the binding to Git identity and paths.
- [ ] Removes or defers the retry engine, event bus, provider/plugin layer,
      runtime retry configuration, and persisted attempt state because no
      current requirement needs them.
- [ ] Names the smallest safe alternative as the existing direct export path
      using the standard-library bounded retry for at most two total attempts.
- [ ] Protects authorization, exactly one completion audit event, the attempt
      bound, terminal-error behavior, and proportionate tests; it neither edits
      the surface nor approves shipping.
