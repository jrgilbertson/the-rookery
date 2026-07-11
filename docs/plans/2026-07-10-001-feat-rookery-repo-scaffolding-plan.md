---
title: The Rookery Repository Scaffolding - Plan
type: feat
date: 2026-07-10
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-plan-bootstrap
execution: code
---

# The Rookery Repository Scaffolding - Plan

## Goal Capsule

- **Objective:** Turn this empty repository into the public, installable v1 shelf of The Rookery — community files, install surface, thin README + WORKFLOWS.md, and GitHub publication — with no skills content yet.
- **Authority:** The Product Contract below (owner-confirmed scope) governs. Where it is silent, repo conventions and the owner's in-session direction govern.
- **Stop conditions:** Surface to the owner instead of guessing when (a) a step needs a GitHub account decision beyond the settings named in R15, (b) any content would violate the same-door rule (R1), or (c) README section drafting hits disagreement — U3 is explicitly interactive.
- **Execution profile:** Work lands on a branch and merges to `main` via one scaffold PR, plus one small follow-up PR that documents the post-publish install-probe observations (`main` is the store shelf). U3 requires synchronous owner review; the other units can proceed autonomously.

---

## Product Contract

### Summary

Ship the v1 skeleton of The Rookery: root community files under MIT, issue/PR templates, a thin workflow-first README backed by a single WORKFLOWS.md, a flat `skills/` layout with the `npx skills add` install path front and center, and a public GitHub repo configured with light protection — everything held to the same-door rule.

### Problem Frame

The owner is publishing his first OSS repo: an always-up-to-date, opinionated repository of AI development, shared so peers and people he's onboarding can adopt his workflows and, later, install his skills individually across harnesses (Claude Code, Codex, and others). His prior private toolkit died of junk accumulation and an overgrown README, so the structure must prevent recurrence without heavy process. Layout and community files are decide-once choices every future skill inherits; this plan lands them before any content arrives.

### Requirements

**Identity and content rules**

- R1. Same-door rule: the owner installs from this repo the same way strangers do, so no repo content may depend on context absent from a stranger's machine — no absolute or home-directory paths, no private repository names, no employer-specific identifiers or examples. Applies to every file, including working docs and this plan.
- R2. Working docs ship public: `docs/plans/` (and future `docs/solutions/`, `docs/ideation/`) are committed, not ignored — the process is part of the product.

**Install surface and layout**

- R3. Flat `skills/<name>/SKILL.md` layout. At v1 the `skills/` directory exists with a short README explaining that skills are arriving and how installs work.
- R4. `npx skills add <owner>/the-rookery --skill <name>` is the documented front door; cloning is a demoted power-user note. No Claude Code marketplace manifest at v1 (see Scope Boundaries).

**README and docs**

- R5. README is a thin shelf: banner placeholder, one-paragraph promise, the 10-minute install, short teasers of the named workflows, and credits. It must not regrow into a manual — depth lives in WORKFLOWS.md.
- R6. WORKFLOWS.md is a structured skeleton at v1: the owner's named workflows (IDE-driven development with Orca, compound-engineering as the development spine, impeccable for UI work, last30days for staying current) with short teasers and honest "content arriving" notes — not fully-authored walkthroughs.
- R7. Explicit linked credits to the projects the system builds on (compound-engineering, impeccable, last30days, Orca), naming their authors/maintainers.

**Community files**

- R8. LICENSE: MIT.
- R9. CONTRIBUTING states the boundary plainly and kindly: fixes, portability, and hardening PRs are welcome; new skills start as an issue with no merge promise; no support SLA. Also documents the main-is-the-shelf rule: `main` stays install-clean, experiments live on branches.
- R10. CODE_OF_CONDUCT: Contributor Covenant 2.1.
- R11. SECURITY.md: a short private-reporting channel.
- R12. CHANGELOG.md in Keep a Changelog format; entries mirrored into GitHub Releases.
- R13. `.github/` holds two issue templates (bug/fix report; skill proposal) and a light PR template.

**Publication and settings**

- R14. Public repo on the owner's personal GitHub account, public from this first scaffold — build in the open, no launch gate.
- R15. Repo settings: branch protection on `main` blocking force-pushes and branch deletion (the configurable subset on a personal account — non-owner direct pushes are already impossible with zero collaborators), squash-merge as default, Discussions off. Repo topics and the social-preview image are deferred until the banner exists.
- R16. Versioning: repo-level semver tags with GitHub Releases at meaningful milestones; the scaffold completion is tagged `v0.1.0`.

**Success criterion:** within 10 minutes of landing, a visitor understands what The Rookery is, how installs will work in their own harness, and what's coming — and once skills exist, can install one and use it. At v1 (zero skills) the install path must resolve and the zero-skill state must be explained honestly.

### Scope Boundaries

**Deferred to Follow-Up Work**

- `.claude-plugin/marketplace.json` — deferred until the first plugin exists. The marketplace mechanism is plugin-only, and the cross-harness front door is `npx skills add`; shipping an empty manifest now adds an unverified surface with no consumer.
- Declare-vs-vendor for cross-skill dependencies — must be settled before the first skill lands; not needed for the empty shelf.
- Repo topics + social-preview image — land with the banner (separate narrative-kit effort).
- Skill and plugin migration; per-skill standards/CI enforcement; Huginn and Muninn skill design; banner/narrative execution — each is its own later effort.
- SUPPORT.md, FUNDING, CODEOWNERS — five-minute additions if ever needed.

### Outstanding Questions

- Deferred (non-blocking here): dependency handling for skills that reference other skills or shared assets — declare in a manifest vs vendor per-skill. Blocks the first skill's arrival, not this scaffold.

---

## Planning Contract

### Key Technical Decisions

- **KTD1 — No marketplace manifest at v1.** The manifest is a plugin-distribution mechanism; The Rookery ships skills first and must stay harness-neutral. Revisit when the first plugin lands. Reverses the earlier day-one-manifest lean after the owner's cross-harness call.
- **KTD2 — Thin README + single WORKFLOWS.md.** Structural (not disciplinary) fix for the README-regrowth failure: depth has somewhere else to live. Splits into `docs/workflows/` pages only if the single file outgrows.
- **KTD3 — Same-door rule enforced as a verification gate, not a convention.** A pre-merge sweep greps for home-directory paths and owner-environment identifiers (the identifier list is supplied by the owner at execution time and deliberately not written into this public doc).
- **KTD4 — GitHub-side setup executes via the `gh` CLI** (repo creation, visibility, protection, merge settings), with each applied setting echoed in the PR description so the owner can audit. Any setting `gh` cannot reach becomes a one-line manual checklist item in the PR.
- **KTD5 — CHANGELOG.md is the canonical release record; GitHub Releases mirror it.** A file in the repo survives platform UI changes and is agent-readable; Releases provide the announce surface.

### Assumptions

- The blindspot-pass defaults the owner accepted stand: light branch protection, Discussions off, squash-merge default.
- `npx skills add` behavior against an empty `skills/` directory is unknown; U7 verifies it against scratch targets before any install copy is written, and U6 re-verifies end-to-end against the real repo.
- The GitHub repo already exists (private, `origin` configured, `main` pushed — verified at plan time); the owner's `gh` CLI is authenticated with permission to change its visibility and settings.

### Sequencing

U1 (community files) and U2 (templates) are independent. U7 (install-path spike) runs before U3 so the install command is verified before it is documented. U3 (README) follows U1 and U7, and runs interactively with the owner. U4 (WORKFLOWS.md) pairs with U3 — the shelf-vs-depth boundary is decided per section during U3. U5 (layout + sweep) can run any time before U6. U6 (publish + configure + release) is last, followed only by the probe-documentation follow-up PR it defines.

---

## Implementation Units

### U1. Root community files

- **Goal:** The five root files that make the repo a legible open-source citizen.
- **Requirements:** R8, R9, R10, R11, R12
- **Dependencies:** none
- **Files:** `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`
- **Approach:** MIT text verbatim with owner name and year. CONTRIBUTING carries the contribution boundary (R9) in plain, kind language, the skill-proposal-by-issue path, the no-SLA statement, and the main-is-the-shelf rule. CODE_OF_CONDUCT is Contributor Covenant 2.1 verbatim with a contact method. SECURITY.md names one private reporting channel (GitHub private vulnerability reporting) in a few sentences. CHANGELOG.md opens in Keep a Changelog format with an Unreleased section.
- **Patterns to follow:** Contributor Covenant 2.1 and Keep a Changelog official texts; MIT from choosealicense.
- **Test scenarios:** Test expectation: none — static documents. Verified by U6's community-profile check.
- **Verification:** Every file renders on GitHub without formatting breakage; CONTRIBUTING states all four elements of R9.

### U2. Issue and PR templates

- **Goal:** Route incoming contributions per the boundary before the first one arrives.
- **Requirements:** R13
- **Dependencies:** none
- **Files:** `.github/ISSUE_TEMPLATE/bug-report.yml`, `.github/ISSUE_TEMPLATE/skill-proposal.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/pull_request_template.md`
- **Approach:** GitHub issue-form YAML. Bug/fix report asks for the skill, harness, and observed vs expected behavior. Skill proposal frames the no-merge-promise expectation from R9 and asks what the skill does and which harnesses it was tested in. `config.yml` disables blank issues. PR template is a short checklist echoing the boundary and the same-door rule.
- **Patterns to follow:** GitHub issue-forms schema.
- **Test scenarios:** Test expectation: none — templates. Behavior verified post-publish by opening a draft issue of each type.
- **Verification:** Both templates render as forms on GitHub; blank issues are disabled.

### U7. Install-path verification spike

- **Goal:** The `npx skills add` command shape is verified empirically before any README documents it.
- **Requirements:** R4 (de-risks)
- **Dependencies:** none
- **Files:** none — throwaway probe outside the repo
- **Approach:** From a clean temp directory, run the CLI against a scratch public repo containing an empty `skills/` directory and against a known populated skills repo. Record: whether bare `<owner>/<repo>` resolves, the `--skill` flag syntax, list behavior, and empty-shelf behavior. Findings feed U3's install copy and `skills/README.md` wording.
- **Test scenarios:**
  - CLI against the empty-`skills/` scratch repo → observed behavior recorded (graceful list or failure vs destructive error).
  - CLI against a populated skills repo → per-skill install syntax confirmed working as it will be documented.
- **Verification:** A short note of observed behaviors exists for U3 to consume; no install command is documented anywhere until this unit completes.

### U3. README — the thin shelf

- **Goal:** The front page: promise, install, workflow teasers, credits — nothing buried, nothing overgrown.
- **Requirements:** R4, R5, R7
- **Dependencies:** U1 (links to CONTRIBUTING/LICENSE resolve), U7 (install command shape verified before it is documented)
- **Files:** `README.md`
- **Approach:** Sections in order: banner placeholder comment (sized slot for the future image), one-paragraph promise (always-up-to-date, opinionated AI development), Install (npx front door per R4, zero-skill state stated honestly, clone path as a footnote), The Workflows (one short teaser per named workflow, linking into WORKFLOWS.md anchors), Credits (R7, linked, naming maintainers), and a one-line pointer to CONTRIBUTING.
- **Execution note:** Author this section-by-section with the owner, approving each section before the next — the owner explicitly wants to steer what stays on the shelf versus what moves to WORKFLOWS.md.
- **Test scenarios:** Test expectation: none — documentation. The 10-minute read-through in U6 is the behavioral check.
- **Verification:** Owner has approved every section; all links resolve; the README stays a single screen-ish shelf rather than a manual.

### U4. WORKFLOWS.md skeleton

- **Goal:** The depth layer the README teasers point into, honest about what's written vs arriving.
- **Requirements:** R6, R7
- **Dependencies:** U3 (section boundary decided during README review)
- **Files:** `WORKFLOWS.md`
- **Approach:** One H2 per named workflow with a consistent internal shape (what it's for, tools involved with credit links, status note). Sections the owner hasn't authored yet carry a one-line honest placeholder rather than generated filler.
- **Test scenarios:** Test expectation: none — documentation.
- **Verification:** Every README teaser anchor resolves; no section contains invented walkthrough content the owner didn't approve.

### U5. Layout scaffold and same-door sweep

- **Goal:** The directory shape every future skill inherits, and a repo verified clean of machine-local context.
- **Requirements:** R1, R2, R3
- **Dependencies:** none (sweep re-runs after U3/U4 content lands)
- **Files:** `skills/README.md`, `.gitignore`
- **Approach:** `skills/README.md` explains the flat layout, that the flock is arriving, and the per-skill install command shape. `.gitignore` covers OS/editor noise only — deliberately does not ignore `docs/` (R2). Sweep: grep the full tree for home-directory path patterns and the owner-supplied private-identifier list (KTD3); fix any hits.
- **Test scenarios:** Test expectation: none — scaffolding. The sweep itself is the check.
- **Verification:** Sweep reports zero hits on the final tree; `docs/plans/` is tracked.

### U6. Publish, configure, and cut v0.1.0

- **Goal:** The repo is public, protected, and carries its first release.
- **Requirements:** R14, R15, R16
- **Dependencies:** U1–U5, U7
- **Files:** `CHANGELOG.md` (v0.1.0 entry, added on the scaffold branch before merge); a follow-up PR updates `skills/README.md` with observed probe behavior; the rest is GitHub-side configuration
- **Approach:** The repo already exists (private, `origin` configured, `main` pushed) — there is no creation step. In order: add the v0.1.0 CHANGELOG entry on the scaffold branch; flip the repo to public via `gh repo edit --visibility public` (build-in-the-open means the flip precedes the merge); merge the scaffold branch to `main` via squash PR; apply R15 settings via `gh`, echoing each applied setting in the PR description, with anything unreachable via CLI becoming a manual checklist line; tag `v0.1.0` and create the GitHub Release mirroring the CHANGELOG entry; run the install probe from a clean temp directory; land the probe observations in `skills/README.md` via one small follow-up PR.
- **Execution note:** This unit takes the owner's repo public — confirm with the owner immediately before the visibility flip.
- **Test scenarios:**
  - From a clean temp directory, `npx skills add <owner>/the-rookery` (and `--list` if supported) → resolves the repo; zero-skill behavior observed and documented in `skills/README.md`.
  - GitHub community-standards profile → all shipped files detected (license, CoC, contributing, security, templates).
  - Force-push to `main` → rejected by protection.
- **Verification:** Repo is public; settings match R15; `v0.1.0` tag + Release exist and mirror CHANGELOG; the 10-minute walkthrough (land → understand → attempt install) completes with the zero-skill state clearly explained.

---

## Verification Contract

| Gate | Command / check | Applies to |
|---|---|---|
| Same-door sweep | `grep -rn` for home-directory path patterns + owner-supplied identifier list across the tree; zero hits | U3, U4, U5, all content |
| Link integrity | All intra-repo links and WORKFLOWS anchors resolve (manual click-through or link checker) | U3, U4 |
| Community profile | GitHub community-standards page shows license, CoC, contributing, security, issue/PR templates | U1, U2, U6 |
| Install probe | `npx skills add <owner>/the-rookery` from a clean temp dir; behavior documented | U6 |
| Settings audit | `gh api` readback of force-push/deletion protection on `main`, merge method, and Discussions state matches R15 | U6 |

No unit tests apply — the deliverable is documents and configuration; the gates above are the proof.

---

## Definition of Done

- All units merged to `main` via the scaffold squash PR plus the single probe-documentation follow-up PR; `main` contains only install-clean scaffold content.
- Repo is public on the owner's personal account with R15 settings verified by readback.
- `v0.1.0` tagged with a GitHub Release mirroring the CHANGELOG entry.
- Same-door sweep is clean on the final tree; `docs/plans/` (including this file) ships public.
- README approved section-by-section by the owner; every teaser resolves into WORKFLOWS.md.
- No scratch files, placeholder lorem, or abandoned drafts anywhere in the tree.
