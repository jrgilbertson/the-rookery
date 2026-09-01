---
title: Do not split human and agent skill products
date: 2026-08-31
category: conventions
module: checking-pr-readiness
problem_type: convention
component: documentation
severity: high
applies_when:
  - "Authoring or retuning a skill that a human owner and a later agent both invoke"
  - "Considering a second end-of-run API such as assessment-only, agent-mode, a ready token, a no-menu path, or don't-wait"
  - "A caller stalled on a numbered menu, or the skill is about to pick in the same turn that wrote it"
  - "Unattended runs are about to get a stricter ready bar than interactive ones"
  - "Reviewing checking-pr-readiness or checking-merge-readiness completion clauses"
symptoms:
  - "The skill grows a second product so agents get a disposition token and humans get a menu"
  - "Callers stall on menus, or the skill duplicates print contracts across SKILL.md and a mode reference"
  - "Unattended mode omits numbered live options or uses a different ready bar"
  - "The skill picks option 1 in the same turn that wrote the menu"
  - "Assessment-only or agent-mode files restate a different completion clause than SKILL.md"
related_components:
  - checking-merge-readiness
  - testing_framework
tags:
  - skill-authoring
  - presentation-contract
  - checking-pr-readiness
  - checking-merge-readiness
  - numbered-options
  - assessment-only
  - agent-mode
---

# Do not split human and agent skill products

## Context

`checking-pr-readiness` and `checking-merge-readiness` used to end a run
differently depending on who was talking. Humans got a brief, numbered live
options, and a wait. Agents got a second product: assessment-only, agent-mode,
`ready` / `action-required` tokens, a "don't wait" path, and a stricter
unattended ready bar. The same gather still ran. The print contract forked.

That fork overcomplicated the skills and stalled callers. A caller that
expected a token hung on a menu. A caller that expected a menu treated a token
as approval. Maintainers then had two APIs to keep in lockstep, plus special
cases for unattended ready bars that the interactive path did not use.

This work is pending on branch `jrgilbertson/Checking-feels-overcomplicated`.
It is unmerged. The Unreleased changelog already names the contract: one
process, wait for a numbered reply from whoever is talking, later `1` is
Approve or Proceed, and the skill does not pick in the same turn.

The current skills encode that one process. PR readiness briefs, then waits.
Merge readiness does the same. Identity bind lives in
`identity-and-argv.md`. The skill never self-selects merge.

This is the end-of-run API. The spoken brief's shape is a separate contract:
answer first, then reasons, then only the evidence those reasons need.

## Guidance

Keep one end-of-run API for every caller of a checking skill.

1. **Same brief, numbered live options, then wait.** After gather and grade,
   print the recommendation and currently available numbered options. Wait
   for a numbered reply from whoever is talking. A turn is one reply: this
   reply writes the menu and stops; the next message is the pick. Do not
   pick an option in the same turn that wrote the menu.
2. **Later `1` is Approve or Proceed, after identity re-read.** Accept option
   1 only after the identity re-read. For PR readiness that is HEAD,
   merge-base, and staged, unstaged, and untracked content. For merge
   readiness that is the fingerprint, live merge state, host policy, and
   linked-issue re-check. The activating utterance never authorizes option 1.
3. **Do not keep a second product in the checking skill.** Do not add
   assessment-only, agent-mode, report-only, disposition tokens, "don't
   wait," or a stricter unattended ready bar as a parallel print contract.
4. **Keep the checks. Change only who decides.** The gather, identity bind,
   sweep classes, and whole-change review still run. Incomplete gather still
   cannot offer Approve or recommend merge. What collapsed is the second
   ending, not the evidence work.
5. **A caller token is caller policy.** If a caller such as `repo-gardener`
   still wants `ready` / `action-required`, or a report-only agent form, that
   is that caller's policy. Follow it up in the caller. Do not keep a
   parallel API in the checking skill.

## Why This Matters

Two end-of-run APIs look like a convenience for unattended callers. They
become a stall. The checking skill has to guess which product the caller
wanted. The caller has to guess which product it received. A token that
means "you may proceed without waiting" collides with a menu that means
"do not pick." A stricter unattended ready bar then silently disagrees with
the interactive recommendation for the same head.

The fork also splits print contracts. Owner-facing prose, coverage close,
and numbered options live on one path. Machine tokens and "don't wait" live
on the other. Batteries, changelog lines, and helper references have to
describe both. A later edit to the brief shape or the identity re-read has
to land twice, or one caller ships the old ending.

One wait from whoever is talking keeps authority in the later numbered
reply. Humans and agents use the same menu. Option 1 still requires the
identity re-read. Callers that need a token can interpret the brief under
their own policy, or be followed up, without a second product inside the
gate.

## When to Apply

Apply this when a skill ends in a recommendation plus a decision, and a
proposal appears to give agents a different ending than humans: a
disposition token, a report-only mode, a "don't wait" clause, or a stricter
ready bar that only unattended runs use.

It applies when retuning `checking-pr-readiness` or
`checking-merge-readiness`, and when a caller such as `repo-gardener` still
describes those dual modes. Change the caller. Do not reopen a parallel API
in the checking skill.

It does not apply to the spoken brief's pyramid shape, which is already
documented separately. It does not apply to identity binding, helper argv,
or sweep-class evidence. Those stay as gather rules, not as a second
product.

## Examples

**One process on both gates.** PR readiness description, body, and step 7
all say the same thing: brief, numbered live options, wait, later `1` is
Approve, do not pick in the same turn. Merge readiness matches: brief
merge, debug, or do not merge, wait, later `1` is Proceed to merge after
the matching re-check, and a bare merge request still waits. The stub
fixture now greps that one-process contract rather than a report-only merge
path (`tests/checking-merge-readiness/fixtures/run-stub-checks.sh`).

**Identity is not a second product.** `identity-and-argv.md` binds one
native subject, full head, target/base ref, and full base OID, then re-reads
that identity immediately before option 1. The fail-closed case expects the
one process: brief each variant with numbered live options and wait. The
skill does not name a forge command until a later reply of 1.

**Caller leftover, not a second skill product.** An ownerless gardener
Worker still asks installed `checking-pr-readiness` for a same-session
`ready` or `action-required` result, and still tells merge readiness to run
in a report-only agent form with no menu. Those lines are caller policy on
this pending branch. They are not a license to keep dual modes in the
checking skills. Follow up the gardener so it consumes the one process. Do
not put the token API back into the gate.

## Related

- [Answer-first natural prose for owner-facing skill readouts](../best-practices/answer-first-natural-prose-for-owner-facing-skill-readouts.md) — pyramid print shape, not the end-of-run API
- [Put the test seam in the environment, not in the shipped skill](keep-the-test-seam-out-of-the-shipped-skill.md) — numbered option 1 is a later write, not a second product
- Skills: `skills/checking-pr-readiness/SKILL.md`, `skills/checking-merge-readiness/SKILL.md`
- Caller leftover: `skills/repo-gardener/SKILL.md` (ownerless `ready` / `action-required` and report-only merge form)
- Related issue: [keep helper skills from presenting owner menus in unattended Workers](https://github.com/jrgilbertson/the-rookery/issues/88)
