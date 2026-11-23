# Daily Learning Skill Eval

Each synthetic Eval Case runs against a fresh Claude Baseline (`claude-baseline`) and against the same revision of `daily-learning` in Claude (`claude-skill`) and Codex (`codex-skill`). All fixtures under `fixtures/` are strictly synthetic and safe to publish; dependency stand-ins (bare Git vault mirror, Obsidian CLI stand-in, ephemeral loopback AnkiConnect stand-in, remote session stand-in, and disposable `automation-runs` repo) belong strictly in the eval execution environment rather than inside `skills/daily-learning/`.

- [Case 01: Overnight read-only assessment and prompt-injection resistance](cases/01-overnight-readonly-and-injection/README.md)
- [Case 02: Degraded sources and quiet-day honest null](cases/02-degraded-sources-and-quiet-honest-null/README.md)
- [Case 03: Closed-Obsidian mirror-mapped strategy, skew detection, and Anki pulse](cases/03-closed-obsidian-mirror-strategy-and-skew/README.md)
- [Case 04: Interactive Phase 2 pretest, skeleton, 5W triage, and approval gates](cases/04-phase2-pretest-skeleton-5w-and-approval/README.md)
- [Case 05: Continuity recovery, hypothesis verification, and Flow 3 unsuspension](cases/05-continuity-recovery-hypothesis-and-f3-unsuspend/README.md)
- [Case 06: First-run private config setup and non-Orca on-demand portability](cases/06-first-run-config-and-non-orca-ondemand/README.md)

The current six-case set SHA-256 is `839fbeaae3ad76661a1b029fb346330827e15da52f839779ad981b3c0e6629a3`. From this directory, reproduce it with:

```sh
find cases fixtures -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

## Environment isolation for live runs

Live model invocations require explicit operator approval and never run as part of `lefthook run pre-push --force`. Before executing any approved live arm:

1. **Stage only synthetic fixtures in a private temporary workspace** outside the repository and outside `/tmp` shared locations, verifying no path overlap or symlink into this repository or the operator's personal vault.
2. **Isolate AnkiConnect on an ephemeral loopback port:** Bind the synthetic AnkiConnect stand-in to the port in `fixtures/daily-learning-config.json` (`http://127.0.0.1:18765` or a fresh ephemeral loopback port) and verify live port `8765` is unreachable from the eval sandbox so Case 05 can never send `unsuspend` or `removeTags` calls to a real Anki collection.
3. **Isolate Codex native state explicitly:** Point Codex `sqlite_home` to the per-run temporary directory so ephemeral eval runs do not write to the operator's host SQLite logs.
4. **Drive multi-turn cases sequentially:** Cases `01`, `02`, `03`, and `06` use single-turn `prompt.md`. Cases `04` and `05` use ordered `turns.json` scripts so the runner verifies zero Obsidian/Anki writes after pre-approval turns before delivering the operator's approval turn and verifying live readback, Anki sync/unsuspension, and incremental `automation-runs` logging.
5. **Prove loaded skill identity:** Verify the transcript actually loaded the candidate `skills/daily-learning/SKILL.md` (not a same-name host install) before grading.

## Recording results and adding deterministic checks

Once the operator approves a live baseline-vs-skill run:

- Drop any Eval Case that passes cleanly on `claude-baseline` without `daily-learning` (per [SKILLS.md](../../SKILLS.md#skill-evals)).
- Add runner-coupled deterministic check scripts (`check.mjs`) and replay self-tests (`check-fixtures.mjs`) only against observed real runner transcripts for objective invariants (zero prohibited writes, `<= 5` cap, zero Leverage scores, redaction sentinel absence, run ending, approval-before-write trace ordering), keeping qualitative pedagogical judgment in operator Eval Labels.
- Commit sanitized Eval Records under `records/<YYYY-MM-DD>-<slug>/README.md` with model IDs, reasoning effort, skill revision commit, case-set SHA-256, baseline arm, runner version, repeats, token/cost summary, and operator Eval Labels, keeping raw transcripts and credentials outside the repository.
