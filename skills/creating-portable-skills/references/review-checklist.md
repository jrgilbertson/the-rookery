# Review Checklist

Use this rubric for an existing-skill audit, a final review, and every proposed instruction relaxation. A separate fresh-context agent that did not author the candidate performs the review. Give it the intended outcome, hard constraints, skill package, evidence record, actual artifacts, and relevant traces without the author's conclusions. Work top to bottom. A failure becomes a fix-list item that names the problem, impact, and change risk. Review is complete when every item passes or has a recorded, user-approved exception.

## System-Owned Invariants and candidate decisions

A **System-Owned Invariant** is a hard constraint that must remain explicit because the surrounding system or the user, rather than model judgment, owns it. The complete categories are:

- Canonical package structure and installability requirements.
- User authority boundaries, required approvals, and irreversible-action limits.
- Exact output formats, schemas, protocols, templates, and resource contracts.
- Deterministic validation and mechanical checks.
- Genuinely fragile ordered operations where reordering can change safety or correctness.

An instruction is not a System-Owned Invariant merely because it uses words such as "must" or "always." Generic reminders about thinking, checking, or narrating work are candidate choreography when the intended outcome and its deterministic check are already explicit.

Before changing one candidate instruction group, name its affected hard constraint and required outcome. Use these qualifiers consistently:

- **Material** means capable of changing a required outcome, trigger boundary, user authority, exact output format, deterministic check, package installability, or fragile sequence.
- An **affected target** is a predeclared model-harness cell in which the candidate could change that named behavior. An **affected case** is a predeclared discriminating or control case that exercises it.
- A **discriminating case** should expose the intended behavioral difference. A **control** should remain materially stable.
- An **invariant loss** is an observed violation of the named required outcome or hard constraint. Different wording, reasoning style, or implementation approach is not a loss by itself.
- **Material divergence** means declared targets differ on the candidate decision or a named invariant, not merely in presentation.
- **Available evidence** comes from the declared target and configuration, in a fresh context, with the intended variant confirmed loaded. A substitute, contaminated context, or listing judgment does not qualify.

Apply the following decision rule:

1. Run the same predeclared discriminating and control cases separately in every affected target cell.
2. For a revision, retain the current instruction when the discriminating-case result is `same`, or when any affected result is worse, unavailable, or shows an invariant loss. An unchanged or materially stable control is expected and does not independently force retention. A waiver may authorize shipment with an unavailable check, but cannot authorize that instruction's removal or relaxation.
3. For a new skill, use `NewSkillCandidate`: a draft with no prior version. The state alone implies neither behavioral evidence nor shipment status. If a required target is unavailable, keep that cell unverified; a waiver may set shipment to `UnverifiedCandidate`, but cannot make the candidate `DirectionalCandidate`.
4. For a revision, remove or relax an instruction only when the intended delta appears, the control stays materially stable, and there is no observed named-invariant loss in the predeclared affected-target cases. This supports only the recorded cases; it is not proof outside them and is not non-regression evidence.
5. If targets materially diverge, make an invariant-preserving revision, validate it, and rerun all affected cells. If material divergence remains, retain the current instruction for a revision; for a new skill, keep `NewSkillCandidate` without a cross-target pass. Either mode may ask the user to narrow the target set.

Pass: every prescriptive instruction protects a named invariant, responds to observed evidence, or covers a named fragile operation; every relaxation satisfies the rule above within an explicit Claim Ceiling.

## Invocation and triggering

- The description says when to use the skill, not how it works. Pass: no body step is restated in the description; without the body, an agent would know when to activate but not the process.
- Triggering conditions lead. Pass: the first clause is a "Use when..." trigger, not an identity statement or feature list.
- Trigger keywords are front-loaded. Pass: words a user would type appear early enough to survive listing truncation.
- Near-misses are named. Pass: the description excludes the closest adjacent task the skill should not handle.
- Each trigger is a distinct branch. Pass: no two trigger phrases are synonyms whose collapse would preserve the same cases.
- Invocation policy is deliberate. Pass: portable description text is sufficient for model invocation; any harness-specific invocation control stays optional metadata outside the canonical behavior contract.

## Information hierarchy

- The body fits its budget. Pass: `SKILL.md` is at most 500 lines, with every line beyond the concise core earning its place.
- The body respects the context target. Pass: it aims below 5,000 tokens; because tokenizers vary, this is an authoring target rather than a portable validation claim.
- Branch-specific detail is disclosed one level deep. Pass: material needed only on some runs lives in a bundled file behind an explicit read-trigger, and that file does not disclose another layer.
- Long references are navigable. Pass: a reference longer than 300 lines has a table of contents.
- Inline content is universal. Pass: everything left in the body is needed by every path.
- Completion criteria are observable. Pass: each workflow stage closes on an exhaustive, checkable state where early completion would be visible.

## Instruction economy

- Every line survives the delete test. Pass: removing it would plausibly lose required behavior; text that only restates default reasoning is cut.
- Guidance is grounded. Pass: domain rules and gotchas trace to real project evidence, observed execution, or a named hard constraint rather than generic model knowledge.
- Steering is positive. Pass: instructions state the target behavior, with prohibitions reserved for hard guardrails and paired with the safe alternative where useful.
- Specificity matches fragility. Pass: fragile operations retain exact steps or commands; open-ended work names the required outcome and only its hard constraints instead of prescribing a cognitive cadence.
- Tool and approach selection is clear. Pass: when the skill names several tools or approaches, it gives a default or a selection rule rather than an equal menu; otherwise it leaves the implementation choice open.
- Examples earn their space. Pass: an example resolves a real ambiguity or demonstrates an exact format and does not narrow the general procedure to one case.
- One meaning has one owner. Pass: a rule is defined in one place and cited elsewhere rather than paraphrased.
- Qualifiers are operationalized. Pass: abstract words such as thorough, clean, fast, bold, reliable, compatible, and improved map to concrete behavior or an observable check.

## Failure-mode scan

- Premature completion. Pass: no completion condition can be satisfied by declaring success without the required artifact or observable state.
- Duplication. Pass: no sentence restates another sentence's meaning in the description, body, or bundled files. A `When to use` section may echo the listing-time trigger contract because it loads at a different time.
- Sediment. Pass: superseded behavior is removed instead of being surrounded by new caveats.
- Sprawl. Pass: the skill's job fits one sentence without joining two independent jobs.
- No-ops. Pass: each sentence changes behavior versus the default or protects a System-Owned Invariant.

## Evidence integrity

- Review context is independent. Pass: a separate fresh-context agent that did not author the candidate or produce the artifacts inspects and grades each matched case. Another fresh-context agent performs the final checklist and holistic review. Deterministic scripts may perform mechanical checks. When either independent context is unavailable, the affected review stays unverified until a separate session completes it.
- Artifacts are inspected directly. Pass: the reviewer opens the relevant outputs instead of relying on the executor's summary or claimed filenames.
- Every pass has substance. Pass: each judgment cites concrete artifact or trace evidence that demonstrates the outcome, not a heading, filename, or other surface compliance.
- Checks are reviewed too. Pass: no objective check is trivial, unverifiable from the available evidence, or missing a material part of the required outcome.
- Subjective judgment stays subjective. Pass: taste, polish, and whether an output feels right are handled through specific human feedback or an explicitly scoped blind comparison, not presented as deterministic pass or fail.
- Traces inform revision. Pass: wasted paths, ignored or ambiguous instructions, repeated corrections, and repeatedly reinvented helper work are considered when deciding what to remove, clarify, add to `Gotchas`, or bundle in `scripts/`.

## Portability

- Frontmatter is canonical. Pass: only `name`, `description`, `license`, `compatibility`, and `metadata` appear.
- Prose is capability-based. Pass: the canonical body names capabilities rather than vendor products or proprietary tools.
- The package is self-contained. Pass: every referenced template, reference, asset, and script resolves inside the skill directory, with no requirement that another skill be installed. Host-project files the skill operates on are allowed.
- Environment requirements are explicit. Pass: no absolute owner path, personal identifier, private-repository assumption, local alias, or undeclared credential is required.
- Package behavior matches its stated intent. Pass: bundled content, side effects, requested access, and authority remain within the job described to the user.
- Claims match evidence. Pass: canonical structure and successful installation are not presented as equivalent behavior across untested models or harnesses; proxy and native checks remain distinct.
