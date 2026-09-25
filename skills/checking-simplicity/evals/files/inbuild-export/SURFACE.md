# Bounded export retry: subject surface

## Objective and requirements

Make the existing synchronous export operation tolerate one transient write
failure. Preserve the existing authorization check, one audit event per
completed export, a maximum of two total write attempts, and the terminal
error when both attempts fail. No restart recovery, asynchronous work,
alternate exporter, or operator-tunable policy is required.

## Subject binding

- repository: `example/exporter`
- branch: `feature/bounded-export-retry`
- full HEAD: `4b21b6b4874c0c82e99e2240a32f1ca958f36d55`
- committed paths: `src/export.ts`, `src/auth.ts`, `src/audit.ts`
- staged paths: `src/retry-engine.ts`, `src/export.ts`
- unstaged paths: `src/retry-provider.ts`, `src/retry-config.ts`
- untracked paths: `src/retry-job-state.ts`

## Supplied contents

Every file in this directory is the complete current content of one path:

| File here | Path | State |
| --- | --- | --- |
| `auth.ts` | `src/auth.ts` | committed |
| `audit.ts` | `src/audit.ts` | committed |
| `export.head.ts` | `src/export.ts` | committed at HEAD |
| `export.staged.ts` | `src/export.ts` | staged in the index |
| `retry-engine.ts` | `src/retry-engine.ts` | staged |
| `retry-provider.ts` | `src/retry-provider.ts` | unstaged |
| `retry-config.ts` | `src/retry-config.ts` | unstaged |
| `retry-job-state.ts` | `src/retry-job-state.ts` | untracked |

## Platform note

The platform standard library provides `retry(operation, { attempts })` and
stops after the first success.
