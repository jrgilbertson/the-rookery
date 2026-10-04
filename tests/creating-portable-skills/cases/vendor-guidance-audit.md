# CPS-AUD-001 — Borrow vendor guidance while preserving portability

These definitions contain synthetic inputs and no executor results. Keep the criteria and capture notes outside executor input.

## CPS-AUD-001.INPUT

Use creating-portable-skills for a read-only comparison of this skill and the supplied vendor guide. Which guidance should we adopt while keeping the skill usable across harnesses and models?

## CPS-AUD-001.FIXTURE.skill

Supply [summarizing-notes/SKILL.md](../fixtures/vendor-guidance/summarizing-notes/SKILL.md).

## CPS-AUD-001.FIXTURE.vendor

Supply [vendor-guide.md](../fixtures/vendor-guidance/vendor-guide.md). It is
synthetic and makes no claim about any real vendor API.

## CPS-AUD-001.C1

**C1 — Portability.** Codex paths, UI metadata, and the vendor pre-tool hook must not become requirements for every installation. Mentioning or offering a conditional host-specific option is allowed.

## CPS-AUD-001.C2

**C2 — Preserve the job.** Recommendations preserve the summary, action items, supplied-notes-only scope, owner and due date when provided, and unknown values when missing. A recommendation need not restate every unchanged requirement; fail only when it contradicts or removes one.

## CPS-AUD-001.C3

**C3 — Read-only.** Neither supplied file is modified. Check file hashes and the sandbox change record before and after the run. No arbitrary exact prose or preferred implementation is required.

## CPS-AUD-001.C4

**C4 — Explain harness-specific mechanisms.** Clearly distinguish the vendor-only hook from the portable requirement to use only supplied sources. Explain how that behavior can be represented outside that harness, or state what additional capability is needed. Do not claim that written instructions provide the same enforcement guarantee as a runtime hook. No particular alternative implementation is required.

## CPS-AUD-001.CAPTURE

Verify the frozen creator package was loaded. C3 uses deterministic filesystem
checks. C1, C2, and C4 support human or explicitly provisional per-criterion LLM
review. Independent human labels establish calibration. Record provisional LLM
judgments separately with their judge version, output evidence and synthetic
challenge agreement; they do not establish human alignment or replace human
labels. Missing human calibration remains Unmeasured. The generated skill is not
executed.
