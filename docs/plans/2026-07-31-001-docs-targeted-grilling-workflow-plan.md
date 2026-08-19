---
title: Targeted Grilling Workflow - Plan
type: docs
date: 2026-07-31
topic: targeted-grilling-workflow
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
---

# Targeted Grilling Workflow - Plan

> **Current terminology (2026-08-17):** The workflow still uses targeted
> grilling, but the ordinary phrase no longer has its own `CONCEPTS.md` entry.
> References below to `Grilling Session` and `Shared Understanding Gate` record
> the original plan.

## Goal Capsule

- **Objective:** Add clear routing for targeted, stateless grilling without changing the seven-job workflow or creating a second planning and documentation system.
- **Product authority:** The existing workflow, repository vocabulary, and session-settled decisions in this Product Contract.
- **Open blockers:** None.

---

## Product Contract

### Summary

Document targeted grilling inside the existing Plan workflow, with `WORKFLOWS.md` as the operational owner.
Compound Engineering remains the normal planning path; `README.md`, `CONCEPTS.md`, and `CHANGELOG.md` receive only the synchronized summary, vocabulary, attribution, and change-history projections they own.

### Problem Frame

The workflow already distinguishes research, requirements discovery, implementation planning, and decisive project-grounded opinions, but it does not name the stricter recommend-and-react interview pattern available through `grill-me`.
Without routing guidance, the skill can either go unused when a plan needs pressure-testing or become extra ceremony on work that is already clear.

### Actors

- A1. **Workflow operator:** Chooses whether a decision cluster warrants grilling and remains the final authority on design intent.
- A2. **Planning agent:** Investigates discoverable facts, recommends concrete answers, asks one decision question at a time, and waits for confirmation before acting.
- A3. **Downstream planner:** Receives clarified intent through the existing Compound Engineering path without inheriting a second glossary, ADR system, or requirements artifact.

### Key Decisions

- **Keep the seven-job structure.** (session-settled: user-approved — chosen over a dedicated pressure-testing stage: grilling is a conditional move inside existing work, not a new job.) Governs R1, R7.
- **Keep Compound Engineering first and grill targeted soft spots second.** (session-settled: user-approved — chosen over starting most coding work with a grill or having no default route: the existing planning spine already handles normal clarification.) Governs R2, R3, R6.
- **Use stateless grilling only.** (session-settled: user-directed — chosen over domain-document integration: adapting competing glossary and ADR conventions would cost more than the expected value.) Governs R4, R8.
- **Synchronize the workflow's existing owners.** (session-settled: user-approved — chosen over editing only the long-form workflow or adding enforcement machinery: the public summary and canonical vocabulary should remain consistent without creating another system.) Governs R9, R10.

### Requirements

**Workflow routing**

- R1. The workflow must retain Research, Plan, Design, Build, Ship, Maintain, and Learn as its seven jobs, with no new pressure-testing stage.
- R2. The Plan guidance must keep `ce-brainstorm` as the normal route when product intent has open questions and `ce-plan` as the direct route when intent is clear.
- R3. The Plan guidance must route a targeted `grill-me` session after normal clarification when one compact decision cluster is consequential, tightly coupled, or still too soft for planning.
- R4. The workflow must describe `grill-me` as stateless and must not promise glossary, ADR, or requirements-document updates from it.
- R5. The workflow must say to skip grilling when requirements are already clear, the remaining choice is routine and reversible, or the apparent question is a fact the agent can discover itself.
- R6. A completed grill must return clarified intent to the existing workflow rather than starting implementation or creating a parallel planning path.

**Interaction contract**

- R7. The concise grilling guidance must cover dependent decisions, one recommended question at a time, discoverable fact lookup, user authority over decisions, and return to planning after the user confirms shared understanding.
- R8. The workflow must not recommend `grill-with-docs`, `domain-modeling`, `codebase-design`, or `improve-codebase-architecture` as part of this route.

**Synchronized guidance**

- R9. The repository's workflow summary must mention targeted grilling without implying that it replaces Compound Engineering or adds an eighth job.
- R10. The canonical glossary must define only the project-specific named process and gate introduced by this workflow, following its existing inclusion rules.

### Key Flows

- F1. Targeted pressure test
  - **Trigger:** Normal clarification leaves one consequential or interdependent decision cluster soft.
  - **Actors:** A1, A2, A3
  - **Steps:** A1 invokes `grill-me`; A2 resolves parent decisions before dependent ones; A1 reacts to each recommendation; A1 confirms shared understanding; the clarified intent returns to the existing planning path.
  - **Outcome:** Planning proceeds without the agent guessing about unresolved design intent.
  - **Covers:** R2, R3, R6, R7
- F2. Clear-work bypass
  - **Trigger:** Intent and acceptance boundaries are already clear, or only routine reversible choices remain.
  - **Actors:** A1, A3
  - **Steps:** The workflow skips grilling and proceeds through the existing direct planning route.
  - **Outcome:** Grilling does not become habitual ceremony.
  - **Covers:** R2, R5

### Acceptance Examples

- AE1. **Covers R3, R7.** Given a completed `ce-brainstorm` whose authentication ownership and session-lifetime decisions remain coupled, when the operator invokes `grill-me`, then the agent recommends an answer to the highest parent decision, asks only that question, and waits before descending the tree.
- AE2. **Covers R5, R7.** Given a grilling question whose answer is present in repository configuration, when the agent reaches that branch, then it reads the configuration instead of asking the operator to supply the fact.
- AE3. **Covers R6, R7.** Given that every material branch has been resolved, when the agent believes the grill is complete, then it asks for shared-understanding confirmation and does not implement until the operator confirms.
- AE4. **Covers R2, R5.** Given work with a precise objective, acceptance criteria, and no consequential open product decision, when the operator enters Plan, then the documented route bypasses grilling and proceeds to `ce-plan`.
- AE6. **Covers R4, R8.** Given a targeted grilling session in a repository with `CONCEPTS.md`, when terminology sharpens during the conversation, then this workflow does not instruct `grill-me` to create or update a competing domain document.

### Success Criteria

- A reader unfamiliar with the discussion can choose among `ce-brainstorm`, `ce-plan`, and targeted `grill-me` without further explanation.
- The documented grill preserves the recommend-and-react interaction and confirmation return.
- The workflow contains no active recommendation for the removed Matt Pocock skills.
- The long-form workflow, public summary, and canonical vocabulary describe the same route without duplicating normative rules.

### Scope Boundaries

- No domain-document interoperability layer, glossary migration, ADR migration, or maintained fork of third-party skills.
- No recurring architecture-review lane based on the removed architecture skills.
- No mandatory grill for ordinary feature work, bug diagnosis, or already-clear plans.
- No replacement of Compound Engineering's requirements-only plan or implementation-planning artifacts.

### Sources / Research

- `WORKFLOWS.md` — current seven-job workflow and Compound Engineering planning routes.
- `README.md` — public workflow summary and the repository's skill-minimization principle.
- `CONCEPTS.md` — canonical project vocabulary and inclusion rules.
- `AGENTS.md` — repository document ownership and vocabulary guidance.
- `CHANGELOG.md` — public record of notable unreleased workflow changes.
- `docs/plans/2026-07-18-001-docs-workflows-playbook-plan.md` — precedent for `WORKFLOWS.md` ownership, thin README projections, and manual documentation verification.
- `docs/solutions/best-practices/operationalize-abstract-qualifiers-in-instruction-review.md` — precedent for replacing subjective routing adjectives with observable cues.
- `docs/solutions/workflow-issues/verify-disposition-claims-before-landing-a-prune.md` — precedent for mechanically checking negative structural claims.
- `https://github.com/mattpocock/skills` — upstream source for `grill-me` and `grilling` behavior.

---

## Planning Contract

### Product Contract Preservation

The Product Contract's R-, F-, and AE-IDs retain their original meanings and ownership.
The enriched plan adds implementation detail without narrowing or expanding the confirmed behavior.

### Key Technical Decisions

- KTD1. **One normative operational owner.** `WORKFLOWS.md` owns the trigger, bypass, interview, confirmation, and return rules. `README.md` stays a routing summary, `CONCEPTS.md` stays semantic vocabulary, and `CHANGELOG.md` records the notable change. (session-settled: user-approved — chosen over editing only the long-form workflow or adding enforcement machinery: the public summary and canonical vocabulary must remain synchronized without becoming competing specifications.) Governs R9, R10.
- KTD2. **Operational routing cues, not adjectives alone.** The workflow defines a grill candidate as one coherent residual decision tree with at least one material cue: costly reversal or broad impact, an answer that constrains dependent answers, or an acceptance boundary the agent would otherwise guess. Multiple unrelated unknowns remain in `ce-brainstorm`; clear or routine reversible work proceeds to `ce-plan`. This applies R2, R3, and R5 without creating a second discovery system.
- KTD3. **User-invoked wrapper, protocol-owned behavior.** The planning agent may recommend `grill-me`, but the operator invokes it because the installed wrapper disables model invocation. The `grilling` skill remains the protocol owner; the workflow records only the operational contract needed to route and supervise it. Governs R3, R7.
- KTD4. **Keep the exit concise.** The workflow returns clarified intent to Compound Engineering after the user confirms shared understanding, then transitions directly into the end-to-end goal template. Detailed pause, abandonment, and prototype rules stay out of the public workflow. Governs R6 and R7.
- KTD5. **Manual and fresh-context verification, no new docs tooling.** Existing repository searches prove structural and negative claims. Rendered review proves the Markdown hierarchy and links. Fresh-context prompt traces prove the routing and interaction contract. Adding a documentation test framework is outside this plan.
- KTD6. **Run the voice edit on the finished public docs, not this plan.** After U1 and U2 settle the content, run `$no-ai-slop:no-ai-slop` in Edit mode across the four updated public documents. Apply only minimum voice-preserving edits, then rerun the contract checks so an editorial change cannot alter routing or scope. (session-settled: user-directed — chosen over reviewing the implementation plan or omitting the editorial pass: the shipped documentation is the reader-facing prose that must sound human.)

### Sequencing

Write the normative `WORKFLOWS.md` route first.
Derive the thinner README, glossary, attribution, and changelog language from that owner so the synchronized surfaces cannot introduce a second protocol.
Run the `no-ai-slop` edit only after those documents agree, then repeat every affected verification gate.

### Risks and Mitigations

- **Grilling appears mandatory or parallel to Compound Engineering.** Keep the CE entry points first, require one residual decision tree plus a material cue, and include clear bypass and broad-ambiguity examples.
- **The exit gets more space than the exceptional route warrants.** Keep confirmation and return to planning in one transition sentence.
- **The protocol drifts across public surfaces.** Keep mechanics in `WORKFLOWS.md`; constrain README and glossary changes to their existing summary and vocabulary roles.
- **External skills appear to be published by The Rookery.** Credit Matt Pocock under `README.md`'s upstream acknowledgements, not under the repository skill catalog.

---

## Implementation Units

### U1. Add the targeted grilling route to the Plan workflow

- **Goal:** Make the existing Plan section route, run, and exit a targeted Grilling Session without changing the seven-stage structure.
- **Requirements:** R1-R8; F1-F2; AE1-AE4; KTD2-KTD4.
- **Dependencies:** None.
- **Files:** `WORKFLOWS.md`.
- **Approach:**
  1. Preserve the existing Compound Engineering entry-point list and add the optional `grill-me` route immediately after it.
  2. Define the observable invoke, bypass, and remain-in-`ce-brainstorm` cues from KTD2, including one compact coupled example and one clear-work bypass example.
  3. State that the agent recommends the route, the operator invokes `grill-me`, discoverable facts are inspected, and user-owned decisions proceed parent-first with one recommended question at a time.
  4. Return confirmed intent to the Compound Engineering planning session and use that sentence to transition into the end-to-end goal template.
- **Patterns to follow:** The Plan section's rationale → tool routes → transition anatomy; canonical terms from `CONCEPTS.md`.
- **Test scenarios:**
  - Covers F1 / AE1. Given ordinary clarification leaves authentication ownership and session lifetime as one coupled cluster, a fresh reader routes to an operator-invoked `grill-me` session, starts with the parent decision, and returns confirmed intent to `ce-plan`.
  - Covers F2 / AE4. Given a precise objective, acceptance boundaries, and only routine reversible choices, a fresh reader bypasses grilling and routes directly to `ce-plan`.
  - Given several unrelated product unknowns remain, a fresh reader keeps the work in `ce-brainstorm` instead of turning grilling into broad requirements discovery.
  - Covers AE2. Given a branch premise exists in repository configuration, the documented agent inspects that fact and asks only any user-owned decision that remains.
  - Covers AE3. Given the user confirms shared understanding, the documented route returns clarified intent to Compound Engineering before introducing the end-to-end goal template.
- **Verification:** The Plan section still reads as one CE-owned planning path, contains concrete invoke and bypass cases, and preserves all seven stage headings and the existing `WORKFLOWS.md#plan` anchor.

### U2. Synchronize the public summary, vocabulary, attribution, and change history

- **Goal:** Project U1's route into each existing public owner without duplicating its normative rules.
- **Requirements:** R9, R10; AE6; KTD1, KTD5.
- **Dependencies:** U1.
- **Files:** `README.md`, `CONCEPTS.md`, `CHANGELOG.md`.
- **Approach:**
  1. Update only the README Plan bullet to keep Compound Engineering primary and name targeted grilling as the exceptional pressure test.
  2. Credit Matt Pocock and the upstream skills repository under `Standing on`; do not list `grill-me` as a Rookery-published skill.
  3. Preserve the in-progress `Grilling Session` and `Shared Understanding Gate` entries in `CONCEPTS.md`, reconciling only wording needed to match U1's canonical terms.
  4. Add a concise Unreleased `Changed` entry describing the new Plan routing.
- **Patterns to follow:** README's thin seven-bullet workflow index and upstream credit list; `CONCEPTS.md`'s term-plus-definition form; `CHANGELOG.md`'s Keep a Changelog `Changed` entries.
- **Test scenarios:**
  - Covers AE6. Given a reader opens `CONCEPTS.md`, the two terms define vocabulary but do not contain routing rules, ADR behavior, or document-generation promises.
  - Given a reader opens the README, the Plan bullet still describes one of seven jobs, leads with Compound Engineering, and presents grilling as optional.
  - Given a reader scans the repository skill catalog, `grill-me` is not presented as a skill published by The Rookery.
  - Given a returning reader opens the changelog, the targeted grilling route is discoverable under Unreleased without restating the protocol.
- **Verification:** README, glossary, credit, and changelog language agree with U1 while each remains within its established document role.

### U3. Review the finished documentation for AI-slop patterns

- **Goal:** Make the shipped workflow prose clearer and more human without changing its decisions, terminology, or document ownership.
- **Requirements:** R1-R10; F1-F2; AE1-AE4, AE6; KTD6.
- **Dependencies:** U1, U2.
- **Files:** `WORKFLOWS.md`, `README.md`, `CONCEPTS.md`, `CHANGELOG.md`.
- **Approach:**
  1. Invoke `$no-ai-slop:no-ai-slop` in Edit mode with only the four updated public documents as the draft set; do not include this implementation plan.
  2. Preserve the author's direct, first-person voice and the documents' existing structures while removing AI-slop patterns, repetition, and unclear phrasing.
  3. Reject any proposed edit that invents a claim, weakens a settled decision, changes canonical terminology, duplicates the protocol, or moves content between document owners.
  4. Apply the accepted minimum edits and rerun the Verification Contract from the beginning.
- **Execution note:** Treat this as the last content edit, after factual and structural review. Use the skill's `What changed` output to inspect the editorial delta before accepting it.
- **Patterns to follow:** The existing voice and cadence of each target document; KTD1's one-owner rule; the `no-ai-slop` skill's minimum-effective-edit and preserve-the-writer's-voice principles.
- **Test scenarios:**
  - Given the finished target docs, the edit removes identified AI patterns while preserving all routing, gate, attribution, and scope claims.
  - Given a suggested rewrite that changes `Grilling Session`, the confirmation transition, or Compound Engineering's precedence, the executor rejects that rewrite.
  - Given the completed voice edit, the structural searches and fresh-context behavior traces still produce the same results as before the edit.
- **Verification:** The accepted editorial diff changes prose quality only, the skill's change summary matches the applied delta, and every Verification Contract gate still passes.

---

## Verification Contract

| Gate | Method | Pass condition |
|---|---|---|
| Diff hygiene | `git diff --check` | No whitespace errors. |
| Seven-stage structure | `test "$(rg -c -e '^## Research$' -e '^## Plan$' -e '^## Design$' -e '^## Build$' -e '^## Ship$' -e '^## Maintain$' -e '^## Learn$' WORKFLOWS.md)" -eq 7` | The seven workflow stage headings remain present exactly once in aggregate, with no pressure-testing stage. |
| Removed-route sweep | `! rg -n -e 'grill-with-docs' -e 'domain-modeling' -e 'codebase-design' -e 'improve-codebase-architecture' WORKFLOWS.md README.md CONCEPTS.md` | Active workflow surfaces contain no recommendation for removed companion skills. |
| Cross-document vocabulary | `rg -n -e 'grill-me' -e 'Grilling Session' -e 'Shared Understanding Gate' WORKFLOWS.md README.md CONCEPTS.md` | Each term appears only where its document role requires it; human review confirms no duplicated normative protocol. |
| Markdown and links | Render `WORKFLOWS.md` and `README.md`; follow the README Plan link. | Lists and headings render correctly, and the link still resolves to `WORKFLOWS.md#plan`. |
| Routing behavior | Run the U1 fresh-context scenarios with only the finished workflow docs available. | Open intent routes to `ce-brainstorm`, clear intent routes to `ce-plan`, and one qualifying residual cluster routes to operator-invoked `grill-me`. |
| Interaction boundary | Run the fact, recommendation, user-authority, and confirmation-return traces from U1. | The agent investigates facts, asks one recommended parent decision at a time, leaves decisions with the user, and returns confirmed intent to Compound Engineering. |
| Voice and AI-slop review | Run `$no-ai-slop:no-ai-slop` in Edit mode on `WORKFLOWS.md`, `README.md`, `CONCEPTS.md`, and `CHANGELOG.md` after U2; inspect its `What changed` summary. | Accepted edits preserve the author's voice and all normative meaning; the plan file is not part of the review input. |
| Public-repo safety | Run `git status --short` and inspect every untracked path before staging. | Only repository source, docs, and configuration are present; no scratch, private, or generated user artifacts enter the repository. |

---

## Definition of Done

- U1, U2, and U3 satisfy their cited requirements, flows, acceptance examples, and verification outcomes.
- `WORKFLOWS.md` remains the single normative operational owner, with exactly seven workflow stages.
- Compound Engineering remains the default planning spine, and targeted grilling is optional, stateless, user-invoked, and limited to one qualifying residual decision tree.
- Confirmed intent returns to Compound Engineering through a concise transition into the end-to-end goal template.
- `README.md`, `CONCEPTS.md`, and `CHANGELOG.md` are synchronized without copying the full protocol or presenting external skills as Rookery catalog entries.
- The four updated public documents complete a final `$no-ai-slop:no-ai-slop` edit, and the plan itself remains outside that review.
- Every Verification Contract gate passes, including fresh-context routing and interaction traces.
- The final diff contains no abandoned wording, duplicate rules, unrelated cleanup, or non-repository artifacts.
