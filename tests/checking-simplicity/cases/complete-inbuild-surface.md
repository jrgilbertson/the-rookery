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
> Complete supplied contents follow.
>
> Committed `src/auth.ts`:
>
> ```ts
> export function authorize(canExport: boolean): void {
>   if (!canExport) throw new Error("forbidden");
> }
> ```
>
> Committed `src/audit.ts`:
>
> ```ts
> export function recordExportCompleted(exportId: string): void {
>   audit.record("export.completed", { exportId });
> }
> ```
>
> Committed `src/export.ts` at `HEAD`:
>
> ```ts
> import { authorize } from "./auth";
> import { recordExportCompleted } from "./audit";
>
> export async function runExport(input: ExportInput): Promise<void> {
>   authorize(input.canExport);
>   try {
>     await input.writer.write(input.rows);
>   } catch {
>     throw new Error("export write failed");
>   }
>   recordExportCompleted(input.exportId);
> }
> ```
>
> Staged `src/retry-engine.ts`:
>
> ```ts
> export class RetryEngine {
>   constructor(private events: RetryEventBus, private policy: RetryPolicy) {}
>
>   async run(operation: () => Promise<void>): Promise<void> {
>     this.events.emit("retry.started");
>     for (let attempt = 1; attempt <= this.policy.attempts; attempt += 1) {
>       try {
>         await operation();
>         this.events.emit("retry.completed");
>         return;
>       } catch (error) {
>         if (attempt === this.policy.attempts) throw error;
>         this.events.emit("retry.scheduled");
>       }
>     }
>   }
> }
>
> class RetryEventBus {
>   emit(event: string): void {
>     retryEvents.publish(event);
>   }
> }
> ```
>
> Staged `src/export.ts` in the index:
>
> ```ts
> import { authorize } from "./auth";
> import { recordExportCompleted } from "./audit";
> import { retryProvider } from "./retry-provider";
>
> export async function runExport(input: ExportInput): Promise<void> {
>   authorize(input.canExport);
>   try {
>     await retryProvider().run(() => input.writer.write(input.rows));
>   } catch {
>     throw new Error("export write failed");
>   }
>   recordExportCompleted(input.exportId);
> }
> ```
>
> Unstaged `src/retry-provider.ts`:
>
> ```ts
> import { retryPolicy } from "./retry-config";
> import { RetryEngine } from "./retry-engine";
>
> export interface RetryProvider {
>   run(operation: () => Promise<void>): Promise<void>;
> }
>
> const providers = new Map<string, () => RetryProvider>();
> providers.set("default", () => new RetryEngine(retryEvents, retryPolicy));
>
> export function retryProvider(): RetryProvider {
>   return providers.get(process.env.RETRY_PROVIDER ?? "default")!();
> }
> ```
>
> Unstaged `src/retry-config.ts`:
>
> ```ts
> export const retryPolicy = {
>   attempts: Number(process.env.RETRY_ATTEMPTS ?? 2),
>   backoff: process.env.RETRY_BACKOFF ?? "linear",
> };
> ```
>
> Untracked `src/retry-job-state.ts`:
>
> ```ts
> export async function saveAttempt(exportId: string, attempt: number) {
>   await stateStore.put(`export:${exportId}`, { attempt });
> }
> ```
>
> The platform standard library provides `retry(operation, { attempts })` and
> stops after the first success.
>
> Return the assessment only. Do not edit the implementation or decide whether
> it is ready to ship.

## Expected behavior

- [ ] Leads with a recommendation to simplify, then gives the smallest safe
      alternative before its supporting reasons.
- [ ] Gives grouped reasons that remove or reuse machinery, with only
      decision-driving evidence inline.
- [ ] Remains clear as plain text without relying on rendered Markdown.
- [ ] Does not print a review receipt, subject replay, reviewer context label,
      internal status code, commit hash, or negative owner-decision field.
- [ ] Removes or defers the retry engine, event bus, provider/plugin layer,
      runtime retry configuration, and persisted attempt state because no
      current requirement needs them.
- [ ] Names the smallest safe alternative as the existing direct export path
      using the standard-library bounded retry for at most two total attempts.
- [ ] Protects authorization, one completion audit event after success, an
      immediate stop after a successful first write, at most two total attempts,
      terminal-error behavior, and proportionate tests; it neither edits the
      surface nor approves shipping.
