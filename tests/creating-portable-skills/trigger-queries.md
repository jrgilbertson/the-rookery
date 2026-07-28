# Trigger query test: creating-portable-skills

Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10
near-misses. Judge each query 3 times at the listing level in a fresh agent
context: show the context only the skill's name and description alongside
the query and ask whether it would activate, requiring a plain yes, no, or
unsure. Live harness-native discovery is recorded separately (see
`results.md`) as stronger evidence.

Pass rule: each should-trigger query must activate in at least half its runs,
meaning 2 of 3. Any near-miss activation fails the whole set.

Date: 2026-07-16 | Harness: Claude Code subagents (fresh context per judge) | Models: Haiku 4.5, Sonnet, Fable 5

Re-run 2026-07-16 after the description revision from the writing-great-skills review (workflow-summary sentence removed, migrate/port branch collapsed): identical results, every should-trigger at rate 1.0, zero near-miss activations.

Re-run 2026-07-16 after the rename to creating-portable-skills: identical results again, full-rigor tier, three model families.

## Should-trigger queries

| Query | Run 1 | Run 2 | Run 3 | Rate |
| --- | --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | yes | yes | yes | 1.0 |
| I want to write an agent skill that enforces our commit message style | yes | yes | yes | 1.0 |
| Review my deploy-checks skill and tell me what's wrong with it | yes | yes | yes | 1.0 |
| Update the description on my notes skill so it triggers more reliably | yes | yes | yes | 1.0 |
| Port this skill from my old toolkit repo into this collection | yes | yes | yes | 1.0 |
| Migrate the data-validation skill over here and fix it up during the move | yes | yes | yes | 1.0 |
| My skill never fires when I ask about invoices — fix its triggers | yes | yes | yes | 1.0 |
| Turn this prompt I keep pasting into a proper reusable skill | yes | yes | yes | 1.0 |
| Is my skill's SKILL.md structured right? Audit it | yes | yes | yes | 1.0 |
| Make this skill work in Codex too, not just Claude Code | yes | yes | yes | 1.0 |

## Near-miss queries (expected: no trigger)

| Query | Expected | Run 1 | Run 2 | Run 3 |
| --- | --- | --- | --- | --- |
| Design evals for my dataset | no trigger | no trigger | no trigger | no trigger |
| Create a plugin for my editor that adds a slash command | no trigger | no trigger | no trigger | no trigger |
| Review my README for clarity | no trigger | no trigger | no trigger | no trigger |
| Build a grader and rubric for judging model outputs | no trigger | no trigger | no trigger | no trigger |
| Help me write better prompts for my chatbot | no trigger | no trigger | no trigger | no trigger |
| Set up an MCP server for our internal API | no trigger | no trigger | no trigger | no trigger |
| Create a GitHub Action that lints markdown | no trigger | no trigger | no trigger | no trigger |
| What skills should I install for web development? | no trigger | no trigger | no trigger | no trigger |
| Summarize what this skill does | no trigger | no trigger | no trigger | no trigger |
| Write documentation for our API endpoints | no trigger | no trigger | no trigger | no trigger |

## Tuning

Fix failures by front-loading trigger words and describing when to use the
skill. Do not summarize the workflow. A description that summarizes the steps
makes agents follow the summary and skip the body. After tuning, rerun the full
set.

## 2026-07-27 frontier-retune case definitions

These are predeclared checks, not run results. Keep the 2026-07-16 observations
above unchanged. Append actual states and evidence after running against the
final description and local-source package revision.

### Declared current target set

| Target cell | Exact model | Harness and configuration | Query set |
| --- | --- | --- | --- |
| opus-5 | `claude-opus-5` | Resolve and record exact harness, version, and configuration before running | Reuse the ten should-trigger and ten near-miss queries above |
| sol-5.6 | `gpt-5.6-sol` | Resolve and record exact harness, version, and configuration before running | Reuse the ten should-trigger and ten near-miss queries above |

For each target, judge every unchanged query three times in a fresh context
that sees only the final skill name and description. This is a listing proxy:
it passes when every should-trigger query receives at least two `yes` judgments
and no near-miss receives any `yes`. It does not satisfy a native check.

### Separate evidence states to record

| Check | Attribution | State to append after execution | Required evidence |
| --- | --- | --- | --- |
| Structural validation | Final package revision | [passed / failed / unverified] | Validator, version, command, and output or limitation |
| Listing proxy | Each model-harness target cell | [passed / failed / unverified] | Per-query judgments and exact target metadata |
| Native discovery | Each package-harness cell | [passed / failed / unverified] | Native discovery observation or limitation |
| Local-source install | Each package-harness cell | [passed / failed / unverified] | Local source revision and install output or limitation |
| Installed-content identity | Each package-harness cell | [passed / failed / unverified] | Diff, checksum, or equivalent source-identity proof |
| Native load | Each model-harness target cell | [passed / failed / unverified] | Exact target metadata and native load observation |
| Native trigger | Each model-harness target cell | [passed / failed / unverified] | Representative query and native activation observation |

Discovery, installation, and identity evidence may be shared only when target
cells use the same package revision and harness. Load and trigger evidence stay
separate for `opus-5` and `sol-5.6`.

### TR-P1: Listing/native split

- Input: every listing-proxy query passes, but native trigger access is
  unavailable for one declared target.
- Expected transition: listing proxy is passed for that target and native
  trigger remains unverified. Overall status cannot claim native activation or
  behavioral compatibility for the missing cell.

### TR-P2: Waiver

- Input: the user explicitly waives an unavailable required listing judgment
  or unavailable required native check for shipment.
- Expected transition: shipment may proceed only as an unverified candidate.
  The unavailable evidence remains unverified, failed evidence cannot be
  waived, and the waiver raises neither the evidence label nor Claim Ceiling.
  It cannot support an unrelated instruction removal.

### TR-P3: Three-target split

- Input: a future declared set contains three target cells where native trigger
  passes in one, fails in one, and is unavailable in one.
- Expected transition: record passed, failed, and unverified separately. Do not
  collapse them into a harness-wide or cross-target pass.

## 2026-07-27 listing-proxy observations

Final listing at revision `c1ec71a` was judged in three fresh, tool-less
contexts per target. Each context saw the candidate name, final description,
and the unchanged twenty-query set above. This is listing-proxy evidence only.

Actual targets:

- `gpt-5.6-sol`, Codex CLI 0.145.0, high reasoning, ephemeral read-only
  execution with user config ignored. The colliding user-level
  `creating-portable-skills` path was disabled for these listing judgments.
- `claude-opus-5`, Claude Code 2.1.220, high effort, no session persistence,
  no tools, project setting source in an empty disposable repository.

### Should-trigger judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | yes / yes / yes | yes / yes / yes | passed |
| I want to write an agent skill that enforces our commit message style | yes / yes / yes | yes / yes / yes | passed |
| Review my deploy-checks skill and tell me what's wrong with it | yes / yes / yes | yes / yes / yes | passed |
| Update the description on my notes skill so it triggers more reliably | yes / yes / yes | yes / yes / yes | passed |
| Port this skill from my old toolkit repo into this collection | yes / yes / yes | yes / yes / yes | passed |
| Migrate the data-validation skill over here and fix it up during the move | yes / yes / yes | yes / yes / yes | passed |
| My skill never fires when I ask about invoices — fix its triggers | yes / yes / yes | yes / yes / yes | passed |
| Turn this prompt I keep pasting into a proper reusable skill | yes / yes / yes | yes / yes / yes | passed |
| Is my skill's SKILL.md structured right? Audit it | yes / yes / yes | yes / yes / yes | passed |
| Make this skill work in Codex too, not just Claude Code | yes / yes / yes | yes / yes / yes | passed |

### Near-miss judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Design evals for my dataset | no / no / no | no / no / no | passed |
| Create a plugin for my editor that adds a slash command | no / no / no | no / no / no | passed |
| Review my README for clarity | no / no / no | no / no / no | passed |
| Build a grader and rubric for judging model outputs | no / no / no | no / no / no | passed |
| Help me write better prompts for my chatbot | no / no / no | no / no / no | passed |
| Set up an MCP server for our internal API | no / no / no | no / no / no | passed |
| Create a GitHub Action that lints markdown | no / no / no | no / no / no | passed |
| What skills should I install for web development? | no / no / no | no / no / no | passed |
| Summarize what this skill does | no / no / no | unsure / unsure / no | Sol passed; Opus failed under the current public-tier rule because it received only one categorical `no` |
| Write documentation for our API endpoints | no / no / no | no / no / no | passed |

Every should-trigger received three of three `yes` judgments in both targets.
No near-miss received a `yes`, but the Opus `Summarize what this skill does`
result received only one categorical `no`. Under the current public-tier rule,
the historical listing proxy is **passed** for Sol and **failed** for Opus.
Native discovery, loading, and triggering remain separate states in
`results.md`.

The final evidence states below rely on the later 2026-07-28 full rerun, not
this historical Opus result. That rerun recorded three categorical `no`
judgments for every near-miss in both targets.

### Final evidence states

| Check | Codex / `gpt-5.6-sol` | Claude Code / `claude-opus-5` |
| --- | --- | --- |
| Structural validation | passed (shared final package) | passed (shared final package) |
| Listing proxy | passed | passed |
| Local-source install | passed | passed |
| Installed-content identity | passed | passed |
| Native discovery | passed | passed |
| Native load | passed | passed |
| Native trigger | passed | passed |

The detailed commands, paths, hashes, target configuration, and Claim Ceiling
are recorded in `results.md`. No proxy result was used to fill a native state.

## 2026-07-28 writing-great-skills follow-up

The complete unchanged twenty-query set was rerun after the skill description
changed. The final package `SKILL.md` SHA-256 was
`4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe`.
The listing text was:

> Use when creating, updating, or migrating an Agent Skill, or when finding
> problems in its description, triggers, structure, portability, or evidence.
> Produces prioritized findings or a portable, installable Agent Skills
> package. Explanation-only requests stay with general reasoning.

Each judgment ran in a separate fresh process that saw only the skill name,
description, and one query. Sol used `gpt-5.6-sol`, Codex CLI 0.145.0, high
reasoning, ephemeral read-only execution, and ignored user config. Opus used
`claude-opus-5`, Claude Code 2.1.220, high effort, no session persistence, safe
mode, and no tools.

The first candidate description activated for `Summarize what this skill does`
in all three Sol judgments. That failed the full set. The final positive
destination for explanation-only requests corrected the observed ambiguity.
The full set was then rerun from the beginning.

### Final should-trigger judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | yes; `019fa997-98b1-7c61-b14d-61b74c013822`<br>yes; `019fa997-98bd-76f2-b519-a3d8ab23ad2e`<br>yes; `019fa997-98bc-72d2-9325-7658e331a5e8` | yes; `f27e56dd-31af-419e-83eb-4d110b27fd5a`<br>yes; `674b45fb-d01b-4f04-ac90-ab35196df7d0`<br>yes; `0fb4b9b5-9d3a-4b96-a390-5afcaa1e0696` | passed |
| I want to write an agent skill that enforces our commit message style | yes; `019fa997-98bf-71e1-935b-7b6aaf33e21c`<br>yes; `019fa997-c658-7f40-b41f-ea5138952134`<br>yes; `019fa997-c637-78c3-8a55-2a8e15952585` | yes; `d6d6b3ed-6b3c-473e-837b-99c4058bfc5a`<br>yes; `91277495-e318-4789-b3a6-aff4d2f72532`<br>yes; `bdfc8b2d-f1ba-4d0f-a873-77a3002823a4` | passed |
| Review my deploy-checks skill and tell me what's wrong with it | yes; `019fa997-c676-78a0-aa5d-c5f719c1d66c`<br>yes; `019fa997-c658-7603-8dd8-179c58d6d92d`<br>yes; `019fa997-e915-7fc2-a7e8-e963dea54f40` | yes; `48dd1bba-887b-4fe7-935e-d1f47ad2d8cc`<br>yes; `2c583293-c8bd-4b04-8273-359a59d6fd69`<br>yes; `49aea68e-09e2-4ab0-8678-f58e91766358` | passed |
| Update the description on my notes skill so it triggers more reliably | yes; `019fa997-e8df-70a1-ade9-ab5195367d6e`<br>yes; `019fa997-e8f9-7413-8123-8b46fcbcde45`<br>yes; `019fa997-e8e9-7021-8bf2-fc9f415a21f2` | yes; `9738336d-6a09-4636-b0b9-9b9674cf10e8`<br>yes; `289b412c-c6a0-436e-9675-fe7c6d5f1914`<br>yes; `3e9a2b4e-409c-45dd-a9c2-7de40f66679d` | passed |
| Port this skill from my old toolkit repo into this collection | yes; `019fa998-0972-70d1-b76b-d720262b6935`<br>yes; `019fa998-0940-7d92-8ec7-0b86a6f4a64d`<br>yes; `019fa998-092b-7fa2-9b49-ad2f1083638e` | yes; `fcde607e-0fa1-4136-8765-a72d6b856906`<br>yes; `f7dc62fc-d398-442b-8106-de5b8e3547b7`<br>yes; `1ce706e1-dd6f-48df-b782-23169b7d5437` | passed |
| Migrate the data-validation skill over here and fix it up during the move | yes; `019fa998-093c-73a2-a1f8-a737fd248ba8`<br>yes; `019fa998-2808-7e92-9005-0b681ea9636f`<br>yes; `019fa998-2807-79e0-a701-48817fc7e185` | yes; `2530016d-1caf-40a1-b6be-8e324932cc12`<br>yes; `8a6d5554-6cbc-49d3-91e5-375bbc11c8e1`<br>yes; `0fa5fdc6-4f4e-4e82-8385-0819a96f8fbe` | passed |
| My skill never fires when I ask about invoices | yes; `019fa998-27f5-7b90-84e9-065f4229f598`<br>yes; `019fa998-27e3-7c21-905c-ad372e6de7e5`<br>yes; `019fa998-4256-7120-8533-fc85b208b559` | yes; `00ed6a2e-8e9b-4f52-8202-02f51f7cbc45`<br>yes; `f4240899-d444-477e-a20a-047b39f79ba5`<br>yes; `6ea2165f-d232-490b-a0c5-157bc509f159` | passed |
| Turn this prompt I keep pasting into a proper reusable skill | yes; `019fa998-4242-7143-889f-a6ef99b91e35`<br>yes; `019fa998-422c-7da0-b83b-28c35fdb6eac`<br>yes; `019fa998-4266-7bf0-82cb-8cf89142294b` | yes; `bd7104ae-528f-46e2-a7aa-2036f990a416`<br>yes; `7b6ad064-9519-4ff0-8868-87266cdc71d6`<br>yes; `23f62a6f-ebfa-4bf6-b727-d20ddab76c84` | passed |
| Is my skill's SKILL.md structured right? Audit it | yes; `019fa998-6345-7050-bc34-75e0c567b26e`<br>yes; `019fa998-6364-72c0-a7fe-78e17c1b8504`<br>yes; `019fa998-6350-7083-a21a-9e442efa9db3` | yes; `fd7ce991-f747-463c-9ac4-3d2a5c48421e`<br>no; `4e75b1d3-3998-4663-bbeb-a1f814f277b6`<br>yes; `079d4838-ba18-4185-a290-d3b046f902b7` | passed |
| Make this skill work in Codex too, not just Claude Code | yes; `019fa998-6345-7d72-b1d6-169de7702cae`<br>yes; `019fa998-850c-7e71-a06c-0ab9a14bdb7b`<br>yes; `019fa998-8517-7252-a761-0abcffb6199c` | yes; `7c8157a9-c2b9-41e0-b5a6-effe5edae251`<br>yes; `dcf494da-8700-45dc-8b2f-e0345bbe57ee`<br>yes; `f219eac8-687b-4e8e-9423-322c68fdb10c` | passed |

### Final near-miss judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Design evals for my dataset | no; `019fa998-8517-71a3-9806-9175531e586f`<br>no; `019fa998-8520-7041-81e5-82ee5c2be0f2`<br>no; `019fa998-aa20-7120-a24e-73ed4bdc42e1` | no; `a0a0a004-3a3c-4bd4-9dbb-ea35ddc5736f`<br>no; `7e105b5d-e5b2-4992-91db-2b6837779db8`<br>no; `5daf4649-4d5c-44a3-9ecb-d4f12cb3abf1` | passed |
| Create a plugin for my editor that adds a slash command | no; `019fa998-aabf-77e1-acfc-8f88b1fac7d2`<br>no; `019fa998-aa9e-72a1-83b4-e3cf8cd3a5ba`<br>no; `019fa998-aa51-7d50-a7b2-b93dcb8d7723` | no; `5ab0c278-40a5-40ee-800b-4277fd47e071`<br>no; `03d44691-2fff-45e2-8afe-1eee2ed28409`<br>no; `661efe4f-c2af-40d5-8910-d0b5af76e48c` | passed |
| Review my README for clarity | no; `019fa998-cd22-7092-879c-0922b1859f9f`<br>no; `019fa998-cd28-7942-a347-1a798c3b44b4`<br>no; `019fa998-cd2b-77a1-9b60-49eafa1d1eb9` | no; `81cf97b7-c1f5-49cb-8737-6fdfd9229f21`<br>no; `4268c60f-b2a9-488e-9881-b1c7751fc618`<br>no; `64b18800-ec5e-4bd0-a4b1-91587e9c04c6` | passed |
| Build a grader and rubric for judging model outputs | no; `019fa998-cd2c-71b3-a7f1-45d75e04fe1f`<br>no; `019fa998-e998-70a3-8929-354e1ee82fc6`<br>no; `019fa998-e99b-74b3-842c-33c1261beba5` | no; `98e7f026-d986-4423-b2b8-dd8730c29ddb`<br>no; `a5aa05c4-11e3-4e1f-9952-5c48d433b45b`<br>no; `93fd0f88-ed4f-47ff-a08e-5e9f1f8af6e1` | passed |
| Help me write better prompts for my chatbot | no; `019fa998-e9b0-7f73-a7e2-c106b7b78ad7`<br>no; `019fa998-e99b-7400-bc3b-e3f77c456d73`<br>no; `019fa999-09db-71b1-9a85-3673323b140a` | no; `cbe3b979-c8cc-4529-90c1-3619376a14f3`<br>no; `d475ba52-d26d-42c7-873b-e5adc7768d2a`<br>no; `63122133-9f60-4743-9ad5-da2447a753ed` | passed |
| Set up an MCP server for our internal API | no; `019fa999-09eb-7501-8767-3a03c78912d7`<br>no; `019fa999-09e2-7c93-b04a-9d6642e54439`<br>no; `019fa999-09d4-72f2-810c-5cb96cdb55a3` | no; `5edf49b8-dff9-487b-b0be-0e460f9fd430`<br>no; `c4e2a166-93cf-4322-991f-5aa82d23ee3b`<br>no; `8e1f2bf7-17f3-47e7-9c92-40206231860c` | passed |
| Create a GitHub Action that lints markdown | no; `019fa999-2148-76a3-ad20-eb2fc1a43b30`<br>no; `019fa999-2143-7192-b890-279476ad7067`<br>no; `019fa999-2158-7742-a424-018698b5b54d` | no; `1ad7c631-0e20-4c09-afc7-f44bf9ba6d24`<br>no; `7cf053a9-a480-4489-866b-36ea75a6d7d9`<br>no; `ab6f78f6-26b5-4a6c-a54d-434e056ad689` | passed |
| What skills should I install for web development? | no; `019fa999-214b-7fc3-b723-e3ce68eb5cbe`<br>no; `019fa999-3f72-7c12-a1b7-86378480fe26`<br>no; `019fa999-3f71-7003-9a38-e9cbd3a31c08` | no; `7ad52afa-9da8-40bb-a9a5-5dd2ef551d6f`<br>no; `0a1fc8b2-87bf-40ad-8a4e-9dac13809684`<br>no; `17aee165-2873-4e06-bf2d-70bf2e9a97a3` | passed |
| Summarize what this skill does | no; `019fa999-3f85-73e1-b202-834823327bfe`<br>no; `019fa999-3f6f-7b82-8200-931f12d544e8`<br>no; `019fa999-5aa6-7e83-8569-a617c8da62e2` | no; `e9b6d823-9e67-435d-a7c4-d8889751f582`<br>no; `a9717a13-6cff-43f7-ba64-f14463ab582b`<br>no; `641fb4e1-a621-430e-8fed-1e17526ad022` | passed |
| Write documentation for our API endpoints | no; `019fa999-5a89-7bc1-a47a-7896725ec12c`<br>no; `019fa999-5a5e-7b90-b80a-74738fe4e350`<br>no; `019fa999-5a72-7613-a790-c48fc2ef0cc2` | no; `afb2e116-1e68-442f-88c2-b43739922e3c`<br>no; `665bd36a-522a-451a-bae5-391891e3ca43`<br>no; `ccf7d9fa-7927-4941-bc6b-211500455b49` | passed |

Every Sol should-trigger query received three `yes` judgments. Nine Opus
should-trigger queries received three; the `SKILL.md` structure audit received
two of three and passed the declared majority threshold. Every near-miss
received three categorical `no` judgments in both targets. The final listing
proxy passed in both targets.
Later body and resource edits did not change the listing text, so these
description-bound judgments still apply to the final package hash above.

## 2026-07-28 verification-mode choice follow-up

- Verification mode for this self-hosted change: public or unusually
  load-bearing, continuing the package's existing classification
- Tested verification-mode `SKILL.md` SHA-256:
  `576ce3410270fffd81baa0bb7f8c4149a36fbb0e07a7700d1699776136175821`
- Historical matched target: Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning,
  read-only execution
- Other branch target: Claude Code / `claude-opus-5`; behavior, native load,
  and native trigger were unverified for this historical package hash
- Structural validation: passed
- Listing proxy: passed using the unchanged description and the preceding
  description-bound judgments
- Local-source installation: passed with Skills CLI 1.5.20
- Installed-content identity: passed; `diff -qr` was clean and the installed
  `SKILL.md` hash matched the source
- Native discovery, load, and trigger: passed; in fresh session
  `019fa9e3-c7dd-7be0-a749-05892984f6d4`, the agent selected and read the exact
  installed skill before asking for the verification-mode choice

The matched-comparison summary and its limits are recorded in `results.md`.
These checks do not extend the Claim Ceiling beyond the recorded target and
cases.

## 2026-07-28 pre-PR evidence-contract fixes (`af7861b`)

- Verification mode: public or unusually load-bearing
- Description: unchanged, so the complete listing-query results above remain
  the applicable description-bound evidence
- Target configuration: the Opus matched comparison used a safe-mode,
  tool-less cell; the Opus native check used a separate project-settings cell
  with only the native `Skill` tool
- Structural validation: passed
- Local-source installation: passed for both harnesses with Skills CLI 1.5.20
  in disposable workspace `/tmp/rookery-portable-skill-final.GzaDdV`
- Installed-content identity: passed; both installed directories matched the
  six-file source package byte for byte
- Same-name inventory: user copies existed in `~/.agents/skills` and
  `~/.claude/skills` with a different `SKILL.md` hash
- Codex native discovery, load, and trigger: passed in fresh
  `gpt-5.6-sol` thread `019faa6c-4a59-7b01-a832-a44492b3b130`; the trace read
  the exact disposable `.agents` path, providing deterministic load
  provenance; the distinctive first body sentence only corroborated it
- Claude native discovery, load, and trigger: passed in fresh
  `claude-opus-5` session `6e03ff90-7bfe-48fe-afd3-587b9154a1bb`; the native
  `Skill` tool reported the exact disposable `.claude` base directory,
  providing deterministic load provenance; the same sentence only corroborated
  it

The tested `SKILL.md` SHA-256 was
`7530e42fe64c306cc86f97c17b223dd1385ce3b9256a94b57b9708c2a93120df`.
The tested trigger-template SHA-256 was
`ba79352f96e35c1d0c3ac2812335ca266887ad1ec11acde4b15b7aa5b03630c7`.
No proxy result was used to fill a native state, and no native state from a
superseded package revision was carried forward.

## 2026-07-28 final post-review native recheck (`c9eb5e1`)

- Verification mode: public or unusually load-bearing
- Description: unchanged, so the complete listing-query results above remain
  the applicable description-bound evidence
- Structural validation: passed with `skills-ref` 0.1.5
- Local-source installation: passed for Codex and Claude Code with Skills CLI
  1.5.20 in disposable workspace
  `<post-review-portable-skill-disposable-workspace>`
- Installed-content identity: passed; `diff -qr` found no differences between
  the six-file source package and either installed project-local copy
- Codex native discovery, load, and trigger: passed with Codex CLI 0.145.0 and
  `gpt-5.6-sol` at high reasoning in fresh ephemeral thread
  `019faaa7-f98c-7633-9457-7f4a1e3b28d0`; the tool trace read the exact
  installed `.agents` `SKILL.md`, providing deterministic load provenance; the
  response asked for the verification mode, and its first-body-sentence quote
  only corroborated that provenance
- Claude native discovery, load, and trigger: passed with Claude Code 2.1.220
  and `claude-opus-5` at high effort in fresh non-persistent session
  `5b144a80-c9fe-43ac-89ee-392ad3716d1c`; initialization listed the skill,
  the native `Skill` tool loaded the exact installed `.claude` base directory,
  providing deterministic load provenance; the response asked for the same
  decision, and its sentence quote only corroborated that provenance

The tested `SKILL.md` SHA-256 was
`1ba4b97ad9e5a9fcbb3d27e4e69070d46683716fdb29d959709ffe90bf99af0f`.
The tested trigger-template SHA-256 was
`a486e99101002d5bf531bc62a9008c8e3f7ad9fff548712dd2ab412a6ee3a960`.
No proxy result was used to fill a native state, and no native evidence from an
earlier package revision was carried forward.

## 2026-07-28 current review-fix state

The description is unchanged, and the later full listing rerun still passes
the current public-tier threshold: every near-miss received three categorical
`no` judgments. The historical `unsure` / `unsure` / `no` Opus result is
failed under the current rule and is not used for the final listing state.

Substantive edits changed the baseline template, trigger template, and
portability reference after the `c9eb5e1` native recheck. For the current
package, local-source installation, installed-content identity, native
discovery, native load, and native trigger are **unverified** until rerun. This
pass did not attempt a native check; missing deterministic load provenance is
unverified rather than failed. The current trigger-template SHA-256 is
`c06b1dbea5a2b7f4814e6cd8c8eac814a3471f3c0607e6617d8c76cb85669375`.
