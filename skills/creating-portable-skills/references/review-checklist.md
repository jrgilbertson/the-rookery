# Review Checklist

Use this rubric for an existing-skill audit, a final review, and every proposed instruction relaxation. `SKILL.md` owns route selection and reviewer independence: audits and full validation use the whole rubric; focused validation uses the applicable items for direct artifact inspection. Give it the intended outcome, hard constraints, skill package, evidence record, actual artifacts, and relevant traces without the author's conclusions. For a whole-package review, work top to bottom. A failure becomes a fix-list item that names the problem, impact, and change risk. Review is complete when every applicable item passes.

## Mechanical pre-check

Where a shell is available, run [scripts/signal-scan.sh](../scripts/signal-scan.sh) on the package as a first pass; it reads `SKILL.md` and `references/`, owns the patterns, and names the item that judges each signal. Read `assets/` by hand, because templates quote patterns on purpose.

A hit is a candidate. It fails only when its named item fails: description text may carry calibrated emphasis for routing, a System-Owned Invariant keeps its exact steps and prohibitions, and ordinary domain prose may use a flagged phrase.

Pass: every hit is a fix-list item or has a one-line reason it stands.

## System-Owned Invariants

A **System-Owned Invariant** is a hard constraint that must remain explicit because the surrounding system or the user, rather than model judgment, owns it. The complete categories are:

- Canonical package structure and installability requirements.
- User authority boundaries, required approvals, and irreversible-action limits.
- Applicable safety, security, privacy/confidentiality, legal/compliance, and domain-safety boundaries.
- Exact output formats, schemas, protocols, templates, and resource contracts.
- Deterministic validation and mechanical checks.
- Genuinely fragile ordered operations where reordering can change safety or correctness.

An instruction is not a System-Owned Invariant merely because it uses words such as "must" or "always." Generic reminders about thinking, checking, or narrating work are candidate choreography when the intended outcome and its deterministic check are already explicit.

Before changing one candidate instruction group, use the hard constraint,
required outcome, and cases declared for the selected validation route. Use these
qualifiers consistently:

- **Material** means capable of changing a required outcome, trigger boundary, user authority, exact output format, deterministic check, package installability, or fragile sequence.
- An **invariant loss** is an observed violation of the named required outcome or hard constraint. Different wording, reasoning style, or implementation approach is not a loss by itself.
- **Available evidence** meets the selected validation route's execution and inspection requirements with the intended variant confirmed loaded. A substitute or listing judgment does not qualify as behavioral evidence.

The baseline comparison template owns the selected route's behavior checks;
apply it rather than restating it here.

Pass: every prescriptive instruction protects a named invariant, responds to observed evidence, or covers a named fragile operation; every relaxation meets its selected route's verification requirements.

## Invocation and triggering

- The description says when to use the skill, not how it works. Pass: no body step is restated in the description; without the body, an agent would know when to activate but not the process.
- Triggering conditions are clear. Pass: the description opens with an imperative "Use when…" clause that identifies its owned capability and when to activate.
- Trigger keywords are front-loaded. Pass: words a user would type appear in the description's first sentence.
- The description leans pushy. Pass: the description names the work and phrasings the skill should catch; adjacent jobs live in near-miss queries, and an exclusion appears only where trigger runs showed misrouting.
- Each trigger is a distinct branch. Pass: no two trigger phrases are synonyms whose collapse would preserve the same cases.
- Runtime routing is co-located. Pass: a body routing section appears only when invocation leads to distinct execution branches, and it sits with those branch instructions instead of restating the description.
- Invocation policy is deliberate. Pass: portable description text is sufficient for model invocation; any harness-specific invocation control stays optional metadata outside the canonical behavior contract.
- Trigger testing has one owner. Pass: [skills.md](skills.md) supplies the query format and thresholds, and the trigger contract template supplies the procedure; other files point to them instead of restating them.

## Information hierarchy

- The body fits its budget. Pass: `SKILL.md` is at most 500 lines, with every line beyond the concise core earning its place.
- Context use is justified. Pass: required context fits declared host limits and each instruction earns its load. Character count divided by four below 5,000 is an authoring target, not a failure threshold; justified required content may exceed the estimate.
- Branch-specific detail is discoverable. Pass: conditional material has an explicit read-trigger, including at each further reference link; nesting serves the task rather than hiding required instructions.
- Long references are navigable. Pass: headings, search terms, an index, or a table of contents let the agent locate relevant material without loading unrelated content; length alone does not dictate the mechanism.
- Inline content is universal. Pass: everything left in the body is needed by every path.
- Completion criteria are observable. Pass: each workflow stage closes on an exhaustive, checkable state where early completion would be visible.

## Instruction economy

- Every line survives the delete test. Ask of each line whether the model could already know it. Pass: what stays is what only the author knows (the audience, environment facts, the quality bar, resource contracts, hard judgment calls, and the reasons behind constraints) or text whose removal would plausibly lose required behavior; text that only restates default reasoning is cut, and length alone never justifies a cut.
- Guidance is grounded. Pass: domain rules and gotchas trace to real project evidence, observed execution, or a named hard constraint rather than generic model knowledge, and a rule learned from one run's stumble would have helped most runs.
- Facts are durable. Pass: each hardcoded path, flag, version, and interface claim points to its source of truth or was verified against that source during this review.
- Steering is positive. Pass: instructions state the target behavior, with prohibitions reserved for hard guardrails and paired with the safe alternative.
- Specificity matches fragility. Pass: fragile operations retain exact steps or commands; open-ended work names the required outcome and only its hard constraints instead of prescribing a cognitive cadence.
- Tool and approach selection is clear. Pass: when the skill names several tools or approaches, it gives a default or a selection rule rather than an equal menu; otherwise it leaves the implementation choice open.
- Examples earn their space. Pass: an example resolves a real ambiguity or demonstrates an exact format and does not narrow the general procedure to one case.
- One meaning has one owner. Pass: a rule is defined in one place and cited elsewhere rather than paraphrased.
- Qualifiers are operationalized. Pass: abstract words such as thorough, clean, fast, bold, reliable, compatible, and improved map to concrete behavior or an observable check.

## Failure-mode scan

- Premature completion. Pass: no completion condition can be satisfied by declaring success without the required artifact or observable state.
- Duplication. Pass: no sentence restates another sentence's meaning in the description, body, or bundled files.
- Sediment. Pass: the instructions read as if the current rules are the only rules that ever existed. Superseded behavior is removed instead of being surrounded by new caveats, and instructions carry no migration-relative phrasing, past-tense history, incident or pull-request identifiers, workarounds for a named model, or pinned model names. Sediment is the history of the instructions themselves: a sentence that describes the current facts of the skill's domain stands as current fact, not history, even when it uses a change word. Evidence logs and reference tables that state their review date are records, not instructions.
- Sprawl. Pass: the skill's job fits one sentence without joining two independent jobs.
- No-ops. Pass: each sentence changes behavior versus the default or protects a System-Owned Invariant.

## Evidence integrity

- Review context matches the route. Pass: grading and review contexts match what `SKILL.md` requires for the route; focused artifact inspection is identified as such and makes no independent-review claim. Deterministic scripts may perform mechanical checks.
- Artifacts are inspected directly. Pass: the reviewer opens the relevant outputs instead of relying on the executor's summary or claimed filenames.
- Every pass has substance. Pass: each judgment cites concrete artifact or trace evidence that demonstrates the outcome, not a heading, filename, or other surface compliance.
- Checks are reviewed too. Pass: no objective check is trivial, unverifiable from the available evidence, or missing a material part of the required outcome.
- Subjective judgment stays subjective. Pass: taste, polish, and whether an output feels right are handled through specific human feedback or an explicitly scoped blind comparison, not presented as deterministic pass or fail.
- Traces inform revision. Pass: wasted paths, ignored or ambiguous instructions, repeated corrections, and repeatedly reinvented helper work are considered when deciding what to remove, clarify, add to `Gotchas`, or bundle in `scripts/`.

## Portability

- Frontmatter is canonical. Pass: only the fields in the **Package format** table of `skills.md` appear, less any that the `portability.md` canonical-package rule leaves out.
- Prose is capability-based. Pass: the canonical body names capabilities rather than vendor products or proprietary tools.
- The package is self-contained. Pass: every referenced template, reference, asset, and script resolves inside the skill directory, with no requirement that another skill be installed. Host-project files the skill operates on are allowed.
- Environment requirements are explicit. Pass: no absolute owner path, personal identifier, private-repository assumption, local alias, or undeclared credential is required.
- Package behavior matches its stated intent. Pass: bundled content, side effects, requested access, and authority remain within the job described to the user.
- Claims match evidence. Pass: canonical structure and successful installation are not presented as equivalent behavior across untested models or harnesses; proxy and native checks remain distinct.
- Vendor-specific advice stays labeled. Pass: guidance that rests on one vendor's model or harness behavior is marked vendor-specific, scoped to that target, and kept out of the portable rules; the canonical instructions name no model. When assessing vendor guidance, state its model or harness scope in the recommendation.
