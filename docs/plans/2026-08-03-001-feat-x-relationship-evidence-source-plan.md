---
title: "X Relationship Evidence Source - Plan"
type: feat
date: 2026-08-03
topic: x-relationship-evidence-source
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
origin: https://github.com/jrgilbertson/the-rookery/issues/28
---

# X Relationship Evidence Source - Plan

## Goal Capsule

- **Objective:** Update the existing Personal Chief of Staff and Personal CRM skills so authenticated Grok X search is one more optional, read-only evidence source (including self-activity-first discovery), with a few synthetic tests and a clear split from issue #12.
- **Product authority:** Product Contract (R/A/F/AE/KD) is authoritative for behavior. Planning Contract keeps the HOW as a skill revision, not a new product or subsystem.
- **Product Contract preservation:** Product Contract meaning and IDs unchanged from the requirements-only brainstorm; planning adds HOW only.
- **Open blockers:** None.
- **Execution profile:** Markdown skill + test case edits only. No new skill package, service, database, or automation.

---

## Product Contract

### Summary

Treat authenticated Grok X search as a normal optional evidence source for Personal Chief of Staff and Personal CRM. CoS may query X for review context; Person notes, contact dates, and relationship Tasks still follow CRM rules. When no stronger pointer exists, discovery defaults to the user's own recent directed posts and replies, then matches interlocutors against known people. Grok and X stay read-only. Engagement scanning and catch-up X inventory stay out of scope.

### Problem Frame

Jason increasingly builds relationships on X. Chief of Staff and Personal CRM can miss useful relationship context when the exchange lives on X rather than email, calendar, meetings, Messages, or existing Person notes.

A recent inbox-triage case showed the value: a self-emailed X post led to confirming a prior exchange, creating a Person note, and routing a real follow-up. Authenticated Grok was the useful way to inspect that conversation. Without treating X as a peer source, those workflows keep under-serving X-native relationships while either inventing ad hoc checks or ignoring the channel.

Issue #12 covers a different job—finding posts to read or contribute to—and must not be conflated with relationship evidence.

### Key Decisions

- KD1. **Peer source, not special case.** X via Grok is a normal optional evidence source for CRM updates and CoS review, not a special bolt-on, firehose, or engagement product. `(session-settled: user-directed — chosen over special-casing X as unique CRM logic: user asked for clarity that this is treated like any other CRM source.)` Governs R1, R2, R3, R4, R8.
- KD2. **CoS may query X without the CRM companion.** CoS can use X for review context and coverage when material, even when not embedding CRM. `(session-settled: user-directed — chosen over CRM-gateway-only: user selected CoS independent query.)` Governs R5, R6.
- KD3. **Non-CRM CoS use is context only.** X content may inform orientation, conflicts, and partial coverage. Person-note, contact-date, and relationship Task effects still require CRM rules (companion when available). `(session-settled: user-approved — chosen over any CoS action type or CRM effects without CRM skill: agent recommended review-context-only; user accepted.)` Governs R5, R6, R7.
- KD4. **Material-evidence query bar.** Query X only when it can change identity, contact, durable meaning, relevance, or a review conclusion. A URL or known handle helps but is not a hard gate when context already points at X. `(session-settled: user-approved — chosen over URL/handle-required, user-requested-only, or always-scan-active-people.)` Governs R3, R5.
- KD5. **Same substantive-contact contract.** What counts as contact and durable meaning follows the existing relationship contract: direct exchanges count; likes, passive ambient activity, and broadcasts do not. `(session-settled: user-approved — chosen over replies/DMs-only, broader public-exchange, or user-decides-each-time.)` Governs R4, R8.
- KD6. **Peer source approach over CRM-only gateway or separate X skill.** Product shape is CoS + CRM source coverage with a read-only Grok capability bound. `(session-settled: user-approved — chosen over CRM gateway only or hold for separate X skill with #12.)` Governs R1–R10.
- KD7. **Self-activity-first discovery default.** When X is material and no stronger pointer (URL, known handle, or named interlocutor already in evidence) is present, start from the user's own recent directed posts and replies, learn who they engaged, then apply conservative CRM matching. `(session-settled: user-approved — chosen over pointer-only queries or CoS-only self-scan: agent recommended default path; user accepted.)` Governs R3, R15, R16.

### Requirements

**Source parity**

- R1. Authenticated Grok X search is an optional, read-only evidence capability for Personal Chief of Staff and Personal CRM, not a durable CRM database and not a general social-listening product.
- R2. Source roles match other interaction evidence: X supplies interaction evidence and native timestamps; Person notes hold approved durable relationship meaning; Tasks hold dated commitments.
- R3. Query X only under the material-evidence bar in KD4. Do not run opportunistic feed scans or “interesting posts” discovery.
- R4. Apply the same relationship contract as other channels for substantive direct contact, ambient non-contact, durable meaning, and raw-history retention (KD5).
- R15. When X is material and no stronger pointer already exists in evidence, the default discovery path is self-activity-first (KD7): retrieve a bounded slice of the user's own recent directed posts and replies; identify interlocutors from those exchanges; then evaluate known-person matches under R9.
- R16. Stronger pointers win over self-activity discovery: an X URL, known handle, or named interlocutor already in the current evidence scopes the query to that pointer first. Self-activity remains available as corroboration when it can change a named conclusion.

**Chief of Staff**

- R5. CoS may capability-check and query Grok X when X is material to the selected review, even when the CRM companion is unavailable (KD2).
- R6. When CoS uses X without routing a CRM effect, X evidence supports review context and coverage only (KD3). It must not by itself authorize Person-note writes, contact-date advances, or relationship Tasks outside CRM rules.
- R7. When relationship effects are warranted from X evidence and the CRM companion is available, CoS uses embedded CRM for those effects and keeps CoS action numbering, approval, and completion ownership. If the companion is unavailable, do not invent CRM substitutes; report reduced relationship coverage when it limits a material conclusion.

**CRM (direct and embedded)**

- R8. Direct and embedded CRM may use confirmed X exchanges to propose a Person note, monotonic contact-date update, durable-meaning prose or Comment, or a canonical Task when those outcomes are warranted under the relationship contract.
- R9. Identity binding stays conservative: known handle, canonical profile link, second stable corroborator, or explicit user confirmation. Ambiguous handle matching produces no Person write and asks for confirmation only when ambiguity changes the result.
- R10. Every returned interaction distinguishes observed evidence from inference and carries enough identity and timestamp information for safe local contact-date derivation when a contact date is proposed.

**Safety and degradation**

- R11. No X mutation capability is introduced: no like, follow, reply, post, DM send, or other write through this source.
- R12. Grok unavailability, authentication failure, incomplete history, or unresolved identity narrows only conclusions that depend on X (Partial coverage). Other authoritative sources may still support their own conclusions.
- R13. All CRM writes and CoS external actions remain exact-proposal and human-approved; X evidence does not weaken approval binding.
- R14. Documentation clearly distinguishes this relationship-evidence source from issue #12 engagement scanning (contribute + interesting).

### Actors

- A1. **User** — owns judgment, approval, identity confirmation, and all durable writes.
- A2. **Personal Chief of Staff** — selects mode, queries material sources including optional X, prepares the review bundle, and may embed CRM for relationship effects.
- A3. **Personal CRM** — in direct or embedded mode, binds identity, evaluates contact and durable meaning, and proposes Person/Task effects under approval.
- A4. **Grok X capability** — read-only search/inspect interface over X when authenticated and available; never mutates X.

### Key Flows

- F1. CoS review with material X context
  - **Trigger:** User runs morning, wind-down, weekly, or another CoS mode where X is material under R3 (including self-activity-first when no stronger pointer exists).
  - **Actors:** A1, A2, A4 (A3 when relationship effects are warranted).
  - **Steps:** CoS establishes source coverage; capability-checks Grok; chooses pointer-first or self-activity-first per R15–R16; runs the smallest useful X slice; uses results as review context; if relationship effects are warranted and CRM is available, embeds CRM; presents independently approvable actions; applies only exact approvals.
  - **Outcome:** Review covers X when material, or reports Partial coverage when Grok/X is unavailable, without inventing contact or Person edits.
  - **Covered by:** R1, R3, R5, R6, R7, R11, R12, R13, R15, R16.

- F2. Direct CRM capture from an X exchange
  - **Trigger:** User asks to capture a relationship interaction involving X (URL, handle, described exchange, or recent self-activity).
  - **Actors:** A1, A3, A4.
  - **Steps:** CRM binds identity conservatively; queries bounded X evidence via pointer-first or self-activity-first per R15–R16; evaluates substantive contact and durable meaning; proposes Person and/or Task effects or reports no relationship action; applies only exact approvals.
  - **Outcome:** Confirmed exchanges may update contact date, Person meaning, or Tasks; raw X stays in X; no mutation of X.
  - **Covered by:** R2, R3, R4, R8, R9, R10, R11, R13, R15, R16.

- F3. Embedded CRM discovery from CoS with X evidence
  - **Trigger:** CoS evidence includes an X URL, known handle, self-activity interlocutor, or other material X context that may justify a relationship effect.
  - **Actors:** A1, A2, A3, A4.
  - **Steps:** CoS retrieves X when material; embeds CRM with current evidence; CRM proposes only supported effects into the CoS bundle; CoS retains numbering and approval.
  - **Outcome:** Relationship effects appear as ordinary CoS actions; zero effects remain valid.
  - **Covered by:** R5, R7, R8, R9, R12, R13, R15.

- F4. Self-activity-first interlocutor match
  - **Trigger:** X is material and evidence has no URL, known handle, or named interlocutor yet.
  - **Actors:** A1, A2 or A3, A4.
  - **Steps:** Query a bounded slice of the user's own recent directed posts and replies; identify who those exchanges were directed at; for each candidate, attempt conservative CRM match (e.g. known person such as Morgan); only matched or user-confirmed identities may receive Person/Task proposals; unmatched candidates stay unlinked or ask only when ambiguity changes the result.
  - **Outcome:** Known people surface from the user's own directed X activity without scanning the public feed for interesting posts.
  - **Covered by:** R3, R4, R9, R15, R16.

### Acceptance Examples

- AE1. Self-emailed X thread reveals a prior relationship
  - **Covers:** R4, R5, R7, R8, R10.
  - **Given:** Wind-down or inbox-adjacent CoS evidence includes a self-emailed X post URL, and Grok confirms a prior direct exchange with a bindable person.
  - **When:** CoS runs with CRM available.
  - **Then:** The run may propose Person create/update, contact-date advance, and/or a Task for a real follow-up when warranted; raw thread text is not copied into the Person note as an activity log.

- AE2. Multiple confirmed exchanges with the same person
  - **Covers:** R4, R8, R10.
  - **Given:** Several confirmed direct X exchanges with one safely bound person fall on different local dates.
  - **When:** CRM evaluates contact date.
  - **Then:** One monotonic contact-date proposal uses the latest reliable local interaction date; multiple sources describing the same interaction count as one contact observation.

- AE3. Ambiguous identity
  - **Covers:** R9, R12.
  - **Given:** An X handle or display name could match more than one Person note or lacks corroboration.
  - **When:** CRM or CoS considers a Person write.
  - **Then:** No Person write proceeds; candidates are shown; confirmation is requested only if the ambiguity changes the result.

- AE4. Unavailable or incomplete Grok results
  - **Covers:** R12.
  - **Given:** Grok is unauthenticated, errors, or returns incomplete history for a material X question.
  - **When:** CoS or CRM prepares conclusions.
  - **Then:** Coverage is Partial for X-dependent claims; conclusions supported only by other authoritative sources still proceed; the run does not claim “no interaction occurred” from a failed query.

- AE5. Follow-up routes to Tasks
  - **Covers:** R2, R8.
  - **Given:** A confirmed X exchange contains a dated commitment.
  - **When:** CRM proposes effects.
  - **Then:** The dated commitment is proposed as a canonical Task, not as Person metadata or a substitute for Tasks.

- AE6. No durable meaning
  - **Covers:** R4, R8.
  - **Given:** A confirmed X exchange is small talk or ambient and adds no relationship-load-bearing fact.
  - **When:** CRM decides outcomes.
  - **Then:** No Person prose change is proposed; contact date advances only if the exchange still qualifies as substantive direct contact under the relationship contract; zero effects remain valid when nothing is warranted.

- AE7. CoS review context without CRM effects
  - **Covers:** R5, R6.
  - **Given:** CoS needs X to resolve a review conclusion, and no Person/Task effect is warranted or CRM is unavailable.
  - **When:** CoS presents the review.
  - **Then:** X may appear as evidence under the claim it supports; no Person write is invented; reduced relationship coverage is mentioned only when it limits a material conclusion.

- AE8. No X mutation
  - **Covers:** R11.
  - **Given:** Any CoS or CRM run that used Grok X evidence.
  - **When:** The run completes.
  - **Then:** No like, follow, reply, post, or DM send was performed or proposed as an automatic side effect of approval for CRM/CoS destination actions.

- AE9. Self-activity discovers a known person
  - **Covers:** R15, R16, R8, R9.
  - **Given:** No X URL is in current evidence; Grok returns the user's recent reply to a handle that already matches a known Person note (e.g. Morgan) under conservative binding.
  - **When:** CoS or CRM runs with X material under R3.
  - **Then:** The known person may receive contact-date, durable-meaning, or Task proposals when warranted; strangers from the same self-activity slice are not written without confirmation when identity is ambiguous; the run does not surface unrelated public posts for engagement.

### Scope Boundaries

**In**

- CoS source and relationship guidance so X can participate under the material-evidence bar.
- CRM source and relationship guidance so X participates as peer interaction evidence in direct and embedded modes.
- Self-activity-first discovery when no stronger pointer exists, then interlocutor matching against known people.
- Read-only Grok capability check, bounded query intent, identity/contact/durable-meaning participation, and degradation behavior.
- Synthetic tests for direct CRM, embedded CRM, CoS context-only, self-activity discovery, and degradation/identity/no-mutation cases.
- Clear documentation distinction from issue #12.

**Out / deferred**

- General “interesting posts” discovery, contribute/reply suggestions, continuous monitoring, or full-history X import (issue #12 territory).
- Catch-up inventory or reconstruction of X history.
- Automated posting, replies, likes, follows, or DMs.
- Treating X as an authoritative CRM database or copying activity logs into Obsidian.
- A standalone X engagement skill (product decision reserved to #12).

### Dependencies / Assumptions

- Authenticated Grok CLI (or equivalent host Grok/X read tools) is the intended capability surface when available; absence degrades per R12.
- Existing relationship contract and CRM/CoS approval model remain authoritative; this work extends source coverage rather than inventing parallel CRM semantics.
- Issue #12 remains a separate open product decision and does not gate this relationship-evidence work.

### Outstanding Questions

None blocking. Implementation-time choices (exact Grok tool names per harness, numeric recency defaults if a host needs them) stay with the implementer inside KTD bounds.

### Sources / Research

- Origin issue: https://github.com/jrgilbertson/the-rookery/issues/28
- Related non-goal decision surface: https://github.com/jrgilbertson/the-rookery/issues/12
- Existing patterns verified in-repo: `skills/managing-personal-crm/references/source-behavior.md`, `relationship-contract.md`, `apple-messages-cli.md`; `skills/personal-chief-of-staff/references/source-behavior.md` (embedded CRM; no X source today); tests for Messages bounds, degraded coverage, identity collision, and relationship discovery boundaries.
- Testing convention: `tests/README.md` (synthetic cases, no private data; test seam stays out of shipped skills per `docs/solutions/conventions/keep-the-test-seam-out-of-the-shipped-skill.md`).

---

## Planning Contract

### Summary

This is a **skill update**, not a new skill or system. Edit the existing CoS and CRM instruction surfaces so X via Grok is listed and used like Messages/email/meetings already are. Prefer small edits to `source-behavior.md` (and CRM `SKILL.md` load text). Add a short CRM-only reference file only if X/Grok query bounds would bloat `source-behavior.md` the way Messages needed `apple-messages-cli.md`. Add a **few** synthetic test cases—not a full parallel suite.

### Key Technical Decisions

- KTD1. **Extend existing skills only.** No new skill directory, companion product, automation, or shared “X platform” package. Touch `managing-personal-crm` and `personal-chief-of-staff` (plus their tests).
- KTD2. **Prefer in-place source-behavior edits.** Put X in the existing source-role lists and material-query / identity / degradation rules. Add `references/grok-x-source.md` only if capability-check + self-activity bounds need a Messages-sized CLI reference; otherwise keep bounds in `source-behavior.md`.
- KTD3. **Reuse existing CRM semantics.** Do not rewrite `relationship-contract.md` or invent X-specific contact/durable-meaning rules. Cite the contract; at most one clarifying ambient-vs-direct X example if misreads show up while drafting.
- KTD4. **CoS stays thin.** List X as a peer source; state read-only, material bar, self-activity-first, and Partial degradation. Relationship effects keep using embedded CRM. No new CoS mode and no mode-file sprawl unless one sentence is truly needed.
- KTD5. **Minimal tests.** One multi-scenario CRM case file and one multi-scenario CoS case file (or at most three short cases total) covering the discriminating AEs: self-activity known person, ambiguous identity, unavailable Grok, Task not Person metadata, no mutation, CoS context-only / embedded handoff. Follow `tests/README.md`; no test seams in shipped skills.
- KTD6. **#12 is one exclusion line.** State “not engagement scanning (#12)” where X is introduced. Do not build contribute/interesting flows.

### Sequencing

1. CRM skill text (U1).
2. CoS skill text (U2).
3. Synthetic tests (U3).

### Assumptions

- Authenticated Grok/X tools already available on the host are enough; this work does not introduce a new dependency product.
- Catch-up stays untouched.

---

## Implementation Units

### U1. Update CRM skill for X as peer evidence

- **Goal:** CRM treats Grok X like other interaction sources for direct and embedded work.
- **Requirements:** R1–R4, R8–R16, R11–R14; KD1, KD4–KD7; KTD1–KTD3, KTD6
- **Dependencies:** None
- **Files:**
  - Modify: `skills/managing-personal-crm/references/source-behavior.md`
  - Modify: `skills/managing-personal-crm/SKILL.md` (compatibility + load-when-querying-X, only if a separate ref is added)
  - Create only if needed: `skills/managing-personal-crm/references/grok-x-source.md` (short; Messages-shaped, not a framework)
- **Approach:**
  1. Add X/Grok to the existing interaction-evidence role list.
  2. Document: material bar, self-activity-first when no stronger pointer, observed vs inference, conservative identity, read-only, Partial on failure, #12 out.
  3. If bounds are long, park them in a short `grok-x-source.md` and load it only when querying X (same pattern as `imsg`).
  4. Leave catch-up and relationship-contract core rules alone.
- **Patterns to follow:** Existing Messages integration in CRM `SKILL.md` + `source-behavior.md` + optional `apple-messages-cli.md`
- **Test scenarios:** Covered by U3
- **Verification:** A reader of CRM source-behavior (and optional ref) sees X as one more source, not a new workflow.

### U2. Update CoS skill for X as peer evidence

- **Goal:** CoS may use X for review context; CRM effects still go through the existing companion path.
- **Requirements:** R5–R7, R11–R14, R15–R16; KD2–KD3; KTD1, KTD4, KTD6
- **Dependencies:** U1 for shared wording (can draft in parallel)
- **Files:**
  - Modify: `skills/personal-chief-of-staff/references/source-behavior.md`
- **Approach:**
  1. Add X/Grok to the native source roles list.
  2. Short rules: material bar, self-activity-first, read-only, Partial degradation, #12 exclusion.
  3. Keep “relationship judgment as companion” for Person/Task/contact-date; context-only when no CRM effect or companion unavailable.
  4. Do not add a CoS mode, schedule, or separate X skill.
- **Patterns to follow:** Existing companion and degradation sections in CoS source-behavior
- **Test scenarios:** Covered by U3
- **Verification:** CoS guidance stays a source-behavior delta, not a new branch of the skill.

### U3. Add a few synthetic skill cases

- **Goal:** Prove the skill update on discriminating scenarios without suite bloat.
- **Requirements:** AE1–AE9 class coverage (compressed); R9–R13, R15–R16
- **Dependencies:** U1, U2
- **Files:**
  - Create: `tests/managing-personal-crm/cases/x-relationship-evidence.md` (multi-scenario battery)
  - Create: `tests/personal-chief-of-staff/cases/x-relationship-evidence.md` (multi-scenario battery)
- **Approach:**
  1. One CRM battery: self-activity → known person; ambiguous identity; Grok unavailable; Task not Person metadata; no mutation / no ambient contact.
  2. One CoS battery: pointer or self-emailed thread with embedded CRM effects; context-only without CRM write; companion unavailable; degraded Grok.
  3. Synthetic handles only; provenance line per `tests/README.md`.
- **Patterns to follow:** `messages-adapter-bounds.md`, `relationship-discovery-boundaries.md`, `degraded-source-coverage.md`
- **Test scenarios:**
  - CRM: known-person contact/meaning/Task when warranted; no Person write on ambiguous handle; Partial when Grok fails; Task for dated commitment; refuse X mutation; ambient/likes not contact.
  - CoS: relationship effects only via embedded CRM into existing bundle; X as review context without Person invent; Partial when Grok fails; no nested CRM ending.
- **Verification:** Two case files, binary checklists, privacy-clean; matched comparison for the skill revision when running the suite.

---

## Verification Contract

| Gate | What it proves | When |
| --- | --- | --- |
| Skill text review | X is peer evidence in both skills; read-only; self-activity-first; #12 excluded; no new skill/mode | After U1–U2 |
| CRM case battery | U3 CRM checklist | After U3 |
| CoS case battery | U3 CoS checklist | After U3 |
| Privacy scan | No real accounts or vault paths in tests | Before merge |

Authority: `tests/README.md`. No app build.

---

## Definition of Done

- Existing CoS and CRM skills document X as optional peer evidence under the Product Contract; no new skill or subsystem shipped.
- U1–U3 complete; two synthetic batteries cover the discriminating AEs.
- No X mutation path; catch-up and #12 engagement remain out.
- Product Contract IDs stable; no silent scope expansion.
