# Review Checklist

Use this rubric for package audits and authorized revisions. Read the intended
outcome, host instructions, package resources, actual outputs, and relevant
traces. Return prioritized findings with file evidence, impact, and the proposed
correction. Mark unrelated items not applicable.

## Mechanical pre-check

Where a shell is available, run [scripts/signal-scan.sh](../scripts/signal-scan.sh)
on the package. It reads `SKILL.md` and `references/`; inspect `assets/` directly.
A hit is a candidate, not a verdict. Judge it against the item's purpose and
record why a retained hit stands.

## System-Owned Invariants

Keep hard constraints explicit when the user or surrounding system owns them:
package contracts, authority and approvals, privacy and safety boundaries,
exact formats, deterministic validation, and fragile operation order.

An instruction is not an invariant just because it says "must" or "always."
Judge a relaxation against the required outcome and available evidence. Leave
unresolved attribution unverified and preserve required host judgments.

## Invocation and triggering

The description follows the Agent Skills specification: 1–1024 characters
stating what the skill does and when to use it. The scope matches the package's
actual job. Invocation controls specific to a harness belong in its optional
adapter. When a description change addresses routing failures, evaluate the
relevant user requests and near misses through the upstream evaluation workflow.

## Information hierarchy

Keep the main body under the specification's recommended 500 lines. Conditional
resources have a read-trigger and resolve inside the package. Long references
have headings or another way to find the needed material. Completion is visible
in an artifact or observed state, not only an executor's declaration.

## Instruction economy

- No-ops: every instruction protects a constraint, resolves an observed failure,
  or supplies information the agent cannot infer from the task. Remove generic
  thinking scaffolds and reminders about being graded.
- Specificity matches fragility: prefer outcomes over a prescribed reasoning
  cadence; preserve exact steps where order or format determines correctness.
- Duplication: each rule has one owner; other files link to it.
- Steering is positive: state the desired behavior. Reserve prohibitions and
  emphasis for hard guardrails rather than unsupported model-trait claims.
- Qualifiers are operationalized: abstract quality words and hedged requirements
  have an observable meaning.
- Examples resolve ambiguity or demonstrate a required format without narrowing
  the job to one example.

## Failure-mode scan

- Sediment: instructions state current rules. Remove migration-relative history,
  incident identifiers, model-specific workarounds, and superseded caveats. A
  sentence describing a current domain fact stands, including wording such as
  "the customer no longer exists." Historical evidence records remain records.
- Sprawl: the package's job fits one sentence without joining independent jobs.
- Unsupported facts: command flags, versions, paths, and interface claims have
  a source of truth or were verified. Changing data has one source where possible.

## Evidence integrity

Inspect outputs directly. A judgment cites evidence for the outcome rather than
a heading or claimed filename. Checks measure the visible contract, permit
valid alternative implementations, and distinguish behavior failures from
assertion errors and capture gaps. Keep original grades when recording a
correction. Taste remains human feedback rather than a mechanical verdict.

The host owns required independent review and release judgments. Author
inspection does not replace those judgments. The upstream evaluation guides
own case construction, grader validation, and measurement.

## Portability

Frontmatter follows the specification; local links resolve and bundled scripts
carry or declare dependencies. Core instructions use one set of rules, with
optional harness adapters separate. No owner-specific path, private identifier,
local alias, or undeclared credential is required. Claims stay within the
revisions, cases, models, and harnesses actually checked.
