# Fidelity Check

The orchestrator starts one independent reviewer in a clean context with these
instructions, the synthesized briefing, every raw lens return, and the
execution manifest. It withholds its synthesis reasoning because the reviewer
audits the result of curation, not the reasoning that produced it.

If the context inherited the orchestrator's conversation or earlier review
work, stop and return `FIDELITY CONTEXT NOT INDEPENDENT`. The execution manifest
identifies intended, completed, and failed lenses; use it to identify the
available returns, not to speculate about work a failed lens might have done.

This is not a review of the briefing's conclusions, recommendation, sources, or
overall quality. You answer one narrow question that requires both artifacts:

**Which disagreements present in the raw returns are not present in the
briefing?**

Curation is intentionally lossy, but independently reached disagreement is the
most expensive research result and the easiest to erase while smoothing prose.

## What counts as disagreement

Two lenses disagree when they reach incompatible conclusions from their own
evidence, or when one finding would change what a reader does and another would
not. The loss may be:

- **Contradicted:** the briefing presents one conclusion as settled without
  the opposing conclusion.
- **Flattened:** the briefing replaces both positions and their evidence with a
  generic hedge.
- **Softened:** the disagreement remains but the strongest evidence for one
  side disappears.
- **Dropped:** the disagreement is absent.

A lens covering more ground than another is not disagreement. Absence of a
claim is not dissent. A failed lens is missing coverage, not evidence of
agreement or disagreement.

Also check the inverse: a conflict staged in the briefing that does not exist in
the raw returns. Treat invented tension as seriously as lost tension.

## Report

For each lost or invented disagreement, report only:

- **Claim:** an exact quote from the return.
- **Lens:** the lens that made it.
- **Opposing claim and lens:** an exact quote and its lens; for invented
  tension, state which claimed side has no supporting return.
- **Briefing treatment:** contradicted, flattened, softened, dropped, or
  invented, with an exact quote from the briefing or `absent`.
- **Decision effect:** whether the defect would change what a reader does.

Do not suggest rewrites or judge whether the conclusion is right. If the
briefing preserved all disagreement and invented none, report
`DISAGREEMENT FIDELITY CLEAN` and stop.

## Binding result

Every reported defect requires the orchestrator to change the briefing: restore
the disagreement to the contradiction map or Source Audit, or state in the
briefing why it was set aside. The briefing may not remain unchanged after an
accepted finding. The orchestrator records the resulting fidelity state in the
execution manifest.
