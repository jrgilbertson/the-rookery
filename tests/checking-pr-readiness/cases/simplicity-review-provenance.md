# PR readiness treats simplicity as an early check with a late backstop

Provenance: repeated sessions required fresh reviewers; the 2026-08-26 bare
baseline verified self-review and omitted approach-level simplicity.

## Prompt

> At interactive PR-readiness step 3, the subject is repository
> `example/importer`, branch `feature/dry-run`, full `HEAD`
> `1111111111111111111111111111111111111111`, with committed paths
> `src/import.ts` and `tests/import.test.ts`; all other surface categories are
> empty. Linked issue `example/importer#42` requires one `--dry-run` flag to use
> the existing synchronous path without writes, preserve authorization and
> validation, and pass focused flag and no-write tests. Valid receipts cover
> code review, cleanup, tests, and learnings; no path touches a user interface.
> The implementation added a strategy registry, environment selection, and a
> JSON state store with no second caller or current variation.
>
> Complete committed `src/import.ts` contents:
>
> ```ts
> import { readFile, writeFile } from "node:fs/promises";
> import { authorize, validate, prepare, writeImport } from "./existing-import";
> import type { ImportResult, PreparedImport, User } from "./types";
>
> interface ImportStrategy {
>   run(prepared: PreparedImport): Promise<ImportResult>;
> }
>
> class DryRunStrategy implements ImportStrategy {
>   async run(prepared: PreparedImport): Promise<ImportResult> {
>     return { intendedChanges: prepared.changes, writes: 0 };
>   }
> }
>
> class LiveStrategy implements ImportStrategy {
>   async run(prepared: PreparedImport): Promise<ImportResult> {
>     await writeImport(prepared);
>     await writeFile(".import-state.json", JSON.stringify({ mode: "live" }));
>     return { intendedChanges: prepared.changes, writes: prepared.changes.length };
>   }
> }
>
> const strategies = new Map<string, () => ImportStrategy>([
>   ["dry-run", () => new DryRunStrategy()],
>   ["live", () => new LiveStrategy()],
> ]);
>
> export async function runImport(argv: string[], user: User): Promise<ImportResult> {
>   authorize(user);
>   validate(argv);
>   const prepared = prepare(argv);
>   const requested = argv.includes("--dry-run") ? "dry-run" : "live";
>   const selected = process.env.IMPORT_STRATEGY ?? requested;
>   const previous = await readFile(".import-state.json", "utf8").catch(() => "{}");
>   void previous;
>   return strategies.get(selected)!().run(prepared);
> }
> ```
>
> Complete committed `tests/import.test.ts` contents:
>
> ```ts
> import { runImport } from "../src/import";
> import { writeImport } from "../src/existing-import";
> import {
>   authorizedUser,
>   expectedChanges,
>   expectedPreparedImport,
>   unauthorizedUser,
> } from "./fixtures";
>
> jest.mock("../src/existing-import", () => ({
>   ...jest.requireActual("../src/existing-import"),
>   writeImport: jest.fn(),
> }));
>
> test("dry run reports intended changes without import writes", async () => {
>   const result = await runImport(["--dry-run", "records.csv"], authorizedUser);
>   expect(result.intendedChanges).toEqual(expectedChanges);
>   expect(result.writes).toBe(0);
>   expect(writeImport).not.toHaveBeenCalled();
> });
>
> test("dry run keeps authorization and validation", async () => {
>   await expect(runImport(["--dry-run", "records.csv"], unauthorizedUser))
>     .rejects.toThrow("forbidden");
>   await expect(runImport(["--dry-run"], authorizedUser))
>     .rejects.toThrow("invalid input");
> });
>
> test("normal import still writes prepared records", async () => {
>   const result = await runImport(["records.csv"], authorizedUser);
>   expect(result.writes).toBe(expectedChanges.length);
>   expect(writeImport).toHaveBeenCalledWith(expectedPreparedImport);
> });
> ```
>
> The implementer self-reviewed the approach. Inventory the upstream steps and
> statuses, give the next action, why its timing is a backstop, and the exact fresh-review
> dispatch, acceptance, and continuity requirements. Then explain how the gate
> handles a matching cannot-assess result, a fresh result that needs a user
> decision, a fresh result that recommends simplifying first, and a later
> read-only result that the current approach is fine when no requirement or
> file changed. Do not run a companion check.

## Expected behavior

- [ ] Inventories code review, code simplification, solution simplicity,
      browser testing, design critique or audit, and learnings capture.
- [ ] Marks solution simplicity `not verified`; the implementer's same-context
      statement is advisory, not evidence or attestation.
- [ ] Offers a fresh `checking-simplicity` run as the late backstop and says the
      intended checkpoint was before the machinery landed.
- [ ] Supplies issue `example/importer#42`, its objective, behavior,
      constraints, verification, repository, branch, full `HEAD`, all four
      surface categories, and their complete current contents to the fresh
      reviewer without requiring that binding to be replayed in the human
      response.
- [ ] Requires a fresh reviewer with no prior review or findings that shaped the
      surface; a cannot-assess result stays not verified.
- [ ] Correctly marks browser testing and design critique `not applicable` from
      the supplied non-UI classification, while preserving the valid statuses
      for the other supplied receipts.
- [ ] Keeps a result that needs a user decision failed until that decision is
      resolved and the resulting subject is checked again.
- [ ] Keeps a result that recommends simplifying first failed until the
      approach is revised and the resulting subject receives a new clean
      independent check.
- [ ] Refreshes step 3 from the later read-only result after confirming the
      complete requirements and full working-surface content are unchanged in
      an uninterrupted handoff, rather than checking path names or requiring a
      changed path.
- [ ] Names the live fresh dispatch and unchanged subject as the supporting
      evidence for the verified solution-simplicity status; it does not require
      or claim a durable simplicity receipt.
