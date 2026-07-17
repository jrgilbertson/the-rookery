# Review Checklist

The built-in rubric for step 0 (audit) and step 7 (review). Work every item top to bottom. Each item states a pass criterion; an item that fails becomes a fix-list entry naming what is wrong, why it matters, and the risk of fixing it. The review is done when every item passes or carries a recorded, deliberate exception.

## Invocation and triggering

- The description says when to use the skill, not how it works. Pass: no step from the body is restated in the description; removing the body would leave an agent knowing when to fire the skill but not the process.
- Triggering conditions lead. Pass: the first clause is a "Use when..." trigger, not an identity statement or feature list.
- Trigger keywords are front-loaded. Pass: the words a user would actually type appear in the first sentence, since some harnesses truncate long descriptions.
- Near-misses are named. Pass: the description or a "do not use for" clause excludes at least the closest adjacent task the skill should not handle.
- Each trigger is a distinct branch. Pass: no two trigger phrases are synonyms for the same case; collapsing any pair would lose a real branch.
- The invocation choice is deliberate. Pass: the skill is model-invoked because the agent (or another skill) must reach it on its own. A skill only ever fired by hand drops agent invocation where the host harness offers an invocation-control field (a vendor extension, kept in the harness adapter or under `metadata`); where none exists, its description says it is run by hand, which is the portable fallback.

## Information hierarchy

- The body fits its budget. Pass: `SKILL.md` body is at most 500 lines, and near 200 unless the extra lines each survive the delete test below.
- Branch-specific detail is disclosed, one level deep. Pass: material only some runs need lives in a bundled file behind an explicit read-trigger ("Read references/x.md when Y"), never a bare "see references/", and no disclosed file points onward to a second level.
- Inline content is universal. Pass: everything left in the body is needed by every path through the skill.
- Steps end on completion criteria. Pass: each step closes with a checkable condition (the agent can tell done from not-done), and the condition is exhaustive where it matters ("every X accounted for", not "produce a list").

## Instruction economy

- Every line survives the delete test. Pass: for each line, the agent would plausibly get something wrong without it; lines restating default model behavior are cut.
- Every rule traces to evidence. Pass: each prescriptive rule maps to an observed failure, a with/without behavioral difference, or a named fragile operation; anticipatory rules are cut.
- Steering is positive. Pass: instructions state the target behavior ("write one-line comments"), with prohibitions kept only as hard guardrails that cannot be phrased positively, and even then paired with what to do instead.
- Specificity matches fragility. Pass: fragile operations get exact steps or commands; open-ended ones get a heuristic plus the reason, not a rigid directive.
- One meaning, one home. Pass: no guidance appears in two places; each behavior is a one-place edit.
- Qualifiers are operationalized. Pass: every abstract adjective the skill leans on (thorough, clean, fast, bold) is backed by concrete behavior or a checkable criterion; an undefined qualifier becomes a fix-list entry.

## Failure-mode scan

- Premature completion: no step invites an early exit. Pass: no step's completion condition is vague enough that "declare done and move on" satisfies it.
- Duplication: no repeated meaning. Pass: no sentence restates another sentence's content in different words, in the body or between body and description. Exempt: a "When to use" section restating the description's trigger contract, since the two load at different times (the description at listing time, the body at run time).
- Sediment: superseded text is removed, not stacked. Pass: no line describes behavior, tooling, or structure the skill no longer has; edits replaced old text rather than appending around it.
- Sprawl: the skill does one job. Pass: the skill's job fits one sentence without "and"; content serving a second job is split out or cut.
- No-ops: every sentence steers. Pass: each sentence, read alone, would change agent behavior versus the default; a sentence that fails is deleted whole, not trimmed.

## Portability

- Frontmatter is portable. Pass: only `name`, `description`, `license`, `compatibility`, and `metadata` appear; vendor-specific fields live under `metadata` if kept at all.
- Prose is capability-based. Pass: the body names capabilities ("run the prompts in a fresh agent context"), not vendor tool or product names, outside an explicitly vendor-scoped reference file.
- The package is self-contained. Pass: every bundled resource the skill references (templates, references, assets) resolves inside the skill directory, and the skill never depends on another skill being installed. Host-project paths the skill operates on (source files, configs, test directories) are exempt.
- No environment assumptions. Pass: no absolute paths, no personal or machine-specific names, no assumption of private repos, local aliases, or preconfigured credentials beyond what `compatibility` declares.

## Beyond this checklist

This checklist is the floor. For the deeper review vocabulary (predictability, leading words, context and cognitive load, the full failure-mode taxonomy), install `writing-great-skills` from [mattpocock/skills](https://github.com/mattpocock/skills) and run its pass as well.
