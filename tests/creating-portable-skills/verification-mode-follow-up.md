# Verification-mode choice follow-up

Date: 2026-07-28

This revision makes the verification-depth choice explicit before a new skill
is drafted or an approved revision is edited. A read-only audit still ends
without asking an irrelevant verification question.

The package was already treated as public and unusually load-bearing when this
self-hosted change began. The new rule requires the user to make that
choice in future change-producing runs. The selected mode changes only the
listing-query tier: query count, repetition, and tier-specific judgment rules.
It does not change the matched comparison, structural validation, native checks,
or declared target set.

## Declaration

- Mode: revision
- Candidate instruction group: early verification-mode choice
- Required outcome: ask the user to choose between ordinary personal skill
  verification and public or unusually load-bearing skill verification before
  drafting a new skill or editing an approved revision
- Hard constraints: recommend a mode without deciding for the user; do not ask
  during a read-only audit; do not let the choice expand unrelated checks or
  the target set
- Prior variant: commit `88c362e`, `SKILL.md` SHA-256
  `4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe`
- Compared candidate: `SKILL.md` SHA-256
  `08c3d4dcff23e8f9cf72588835db2fcd33bda695f3994726bc6b68d834e38849`
- Final candidate: `SKILL.md` SHA-256
  `576ce3410270fffd81baa0bb7f8c4149a36fbb0e07a7700d1699776136175821`
- Target: Codex CLI 0.145.0 with `gpt-5.6-sol`, high reasoning, read-only
  execution

The final prose edits standardized the tier names and clarified that each tier
sets query count, repetition, and judgment rules. They did not change the
compared question, timing, user authority, or the checks outside listing-proxy
evaluation.

## Matched cases

A fresh-context agent ran each variant separately and confirmed its exact
`SKILL.md` identity. A separate fresh-context grader inspected the outputs and
source.

| Case | Prior observation | Revised observation | Result |
| --- | --- | --- | --- |
| New skill | Proceeded to remaining intent and resource work without asking about verification | Asked the user to choose a mode and recommended ordinary personal verification for the example | Intended delta observed |
| Approved revision | Proceeded to target and resource scoping before editing | Asked the user to choose a mode before editing and made a recommendation | Intended delta observed |
| Read-only audit control | Requested the missing target package, made no edits, and did not ask about verification mode | Requested the missing target package, made no edits, and did not ask about verification mode | Materially stable control |

Context references:

- New-skill prior: fresh agent `/root/mode_new_prior`, initial run
- New-skill revised: fresh agent `/root/mode_new_revised`, initial run
- Approved-revision prior: `019fa9c2-177e-77d3-ad71-2f183b67f454`
- Approved-revision revised: `019fa9c2-17a2-7992-a95c-0d03a1983ce8`
- Read-only prior: `019fa9c2-177e-7823-89e9-65c7cce63d84`
- Read-only revised: `019fa9c2-177f-7342-854c-16c1b7764ef0`
- Independent grader: `/root/mode_new_prior/independent_grader`

The grader found no material loss and assigned `DirectionalCandidate` with a
**directional comparison** label.

## Policy and package checks

The final trigger template records the user-selected mode and defines the numeric
tier rules:

- Ordinary personal: five should-trigger and five near-miss queries, one run
  each; a borderline query gets two more judgments.
- Public or unusually load-bearing: eight to ten queries in each group, three
  runs each.

Both the workflow and trigger template keep the choice within listing-proxy
evaluation. The skill description did not change, so the listing-query test was
not rerun, and its existing evidence remains description-bound.

`npx skills-ref validate skills/creating-portable-skills` passed. Skills CLI
1.5.20 installed the final source into a disposable Codex project. `diff -qr`
found no difference between the source and installed package. The installed
`SKILL.md` hash matched the final candidate.

In a fresh native Codex run, the agent selected and read the exact installed
skill, then asked the user to choose a verification mode and recommended
ordinary personal verification. The session was
`019fa9e3-c7dd-7be0-a749-05892984f6d4`.

## Claim Ceiling

The matched cases support a directional comparison for this early mode-choice
instruction on the recorded `gpt-5.6-sol` and Codex CLI target cell. The native
run confirms one installed execution of the final package. This evidence does not establish
repeatability, non-regression, causal improvement, downstream tier compliance,
other prompts, or behavior in other models and harnesses.
