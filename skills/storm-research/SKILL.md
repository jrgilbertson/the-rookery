---
name: storm-research
description: "Use only for requests whose deliverable is a full research briefing, a STORM-style investigation, or an evidence review across multiple independent perspectives. The work compares competing evidence, maps contradictions and blind spots, and supports decisions, investments, negotiations, long-form writing, presentations, or learning a new domain."
---

# Storm Research

Produce a grounded research briefing by establishing baseline facts, finding
perspectives suggested by the sources, asking independent lens-specific questions,
preserving disagreement, and auditing reliability and source quality.

Material means capable of changing the answer, confidence, or next action.

Read [references/lens-charter.md](references/lens-charter.md) before framing the
research. Its research-depth guidance applies throughout the run; its isolation
and return rules apply to each lens executor.
Read [references/analysis-methods.md](references/analysis-methods.md) for the
evidence checks that deepen questions and synthesis without dictating output
sections.

## Workflow

### 1. Frame the target

Resolve the research topic and create one self-contained **framed topic** with:

- the question and requested deliverable;
- the user's role or intended use;
- scope, time horizon, geography or domain, and what the answer must cover to be
  useful;
- user constraints and authority boundaries;
- permitted resource identifiers and access boundaries, such as URLs, file
  paths, repository names, dataset IDs, or an explicit public-source allowance.

Retrieve missing context when possible. Ask only when ambiguity would change
the research direction. Freeze this framed-topic block before dispatch and use
it verbatim for every lens.

### 2. Establish baseline facts (`p0`)

Fetch current sources when the topic depends on current facts, vendor behavior,
law, finance, health, APIs, prices, benchmarks, or news. Prefer primary sources
such as official documents, papers, filings, standards, repositories, published
data, and direct product pages. Distinguish evidence from inference.

Create a short, sourced baseline that does not favor any lens. Include:

- definitions and scope boundaries;
- foundational facts, assumptions, and constraints that material claims must
  respect;
- key actors, systems, examples, and terms of art;
- timeline and current state when relevant;
- what is known, disputed, and unknown;
- citations or permitted resource identifiers for its claims;
- source-access caveats.

Freeze one baseline block before dispatch and use it verbatim for every lens.
It is shared orientation, not a substitute for each executor's own sourcing. If
required source access is unavailable, mark the run degraded, label factual lens
work an **unverified perspective simulation**, and keep factual confidence low.

### 3. Scan sources and lock the lens set

Inspect three to five sources most likely to reveal a missing perspective that
could change the answer, confidence, or next action. Use the five canonical
lenses unless the user narrows the set:

| Lens | Contribution | Failure mode it catches |
| --- | --- | --- |
| **Practitioner** | Daily operating reality | Advice that ignores implementation friction |
| **Academic** | Research, formal models, and measurement quality | Anecdotes or narratives unsupported by evidence |
| **Skeptic** | The strongest counterargument | Confirmation bias and one-sided enthusiasm |
| **Economist** | Incentives, constraints, market structure, and opportunity cost | Narratives that hide resource trade-offs |
| **Historian** | Precedents, cycles, analogies, and failure patterns | Treating old mechanisms as unprecedented novelty |

Add a topic-specific lens, such as a regulator, customer, clinician, operator,
technical architect, adversary, ethicist, educator, community, or geopolitical
perspective, only when omitting it could change the answer, confidence, or next
action. Topic-specific lenses add to the non-narrowed canonical set; they do
not replace it.

Lock the intended lens set in an internal run record. The canonical lenses left
after user narrowing and every user-required lens are required. A topic-specific
lens is required only when the research would be unusable without it; otherwise,
record it as supplemental. Record the narrowing, required and supplemental
lenses, source-access state, and any degradation before dispatch.

### 4. Dispatch one isolated executor per lens

Use the host's agent runner to start one clean executor context per lens,
dispatching concurrently when possible and queueing when capacity is limited.
Start a generic executor rather than a preconfigured role whose hidden task
instructions would contaminate the exact four-part seed below.

After dispatch, the orchestrator stops doing lens research. Each executor
researches its own lens. The orchestrator collects the raw returns and later
synthesizes them; it does not act as another lens.

Give every executor exactly four seed parts:

1. the common lens charter content;
2. the identical frozen framed topic from step 1;
3. that executor's lens and no other lens;
4. the identical sourced `p0` baseline from step 2.

Required system policy and tool instructions may remain outside the task seed,
but no inherited task conversation or sibling work may enter the context. Do
not summarize an earlier return into a queued seed. Record the context-launch
and queue isolation mechanism in the internal run record.

If a context contains sibling work, discard its return and restart that lens in
a clean context. When clean contexts are unavailable or their cleanliness
cannot be verified, use the best available separation, label the result a
**single-context synthesis**, state the separation used, and lower confidence.
An intended required lens that fails or returns no usable result stays failed.
Continue with partial research when useful, but mark the run degraded and
record each limitation, its effect on coverage or confidence, and what would
upgrade the result. For unverified cleanliness, name the signal or mechanism
needed to prove that no inherited task conversation or sibling work entered
each executor.

Collect every return unchanged and retain the raw returns for fidelity review.
This step is complete when every intended lens is recorded as completed or
failed, every completed return is retained unchanged, and the internal run
record captures the isolation mechanism and verification state, queue handling,
source access, and degradation state.

### 5. Map contradictions and gaps

From the raw returns, answer:

1. Where do lenses directly conflict?
2. Which conflicts matter most for the intended use?
3. Which side has the strongest evidence, and which is weakest?
4. What does every completed lens agree on?
5. What did none of the completed lenses address?
6. Which question would resolve the largest uncertainty?

Keep each conflicting conclusion and its evidence. Do not replace disagreement
with a vague hedge. A missing or failed lens is a coverage gap, not agreement.

Use the Lens Charter's research-depth questions while mapping the record:
clarify the foundations and mechanisms behind material claims, and examine
relevant relationships, patterns over time, and downstream effects. Carry these
findings into the sections where they help the reader. Do not manufacture a
dynamic or a separate analysis section when the evidence adds nothing material.

### 6. Audit sources

Create a source audit internally for every task. Include it in the deliverable
when the work is consequential, current, disputed, or source-heavy:

| Claim | Best source | Source type | Bias or tone risk | Missing counter-source | Confidence |
| --- | --- | --- | --- | --- | --- |
| `<claim>` | `<source or none found>` | Primary/secondary/tertiary/none | `<risk>` | `<needed source>` | High/Medium/Low |

Audit promotional, institutional, ideological, geographic, and political bias.
Several sources with the same incentives do not count as independent
confirmation. This step is complete when every material user-facing claim has a
best source, source type, bias or tone risk, missing counter-source, and
confidence. An unsupported claim still gets a complete row: record no supporting
source and no source type, mark the claim unverified, name the evidence needed,
and keep confidence low.

### 7. Synthesize the requested form

For an article, paper, blog post, presentation, or report, read
[references/briefing-template.md](references/briefing-template.md) and produce
its long-form outline before prose.

For other work, synthesize directly into the user's requested briefing,
recommendation, preparation notes, negotiation questions, learning path, or
other research-backed form. The intended use controls the ending: include an
actionable implication or verdict when it helps that purpose, and do not force
one into an exploratory briefing.

Build material claims from sourced facts, explicit assumptions, constraints,
and supported mechanisms. Include relevant system relationships and downstream
effects where they change the answer, confidence, or next action. Integrate
this reasoning into the reader's natural sections rather than adding mandatory
first-principles or systems-thinking sections.

### 8. Emit the briefing

Unless the user requested a shorter or custom form, read
[references/briefing-template.md](references/briefing-template.md) and use its
full-briefing structure. For short or custom outputs, preserve compact
citations and compress presentation without dropping a material contradiction,
finding or uncertainty, confidence limit, degradation, frontier question, or
reliability finding.

Keep the internal run record out of a normal reader-facing deliverable. Include
only the research limitations that materially affect interpretation. Provide
the full record when the user requests an audit, trace, or execution details.

Before fidelity review, reconcile the Source Audit against the draft. Add or
update a complete row for every material claim introduced or changed during
analysis and synthesis, including unsupported claims.

### 9. Review curation fidelity

First check the draft for its weakest claim, overreliance on one lens, a weak
version of the skeptic's case, vague incentives, historical analogies that do
not share the same mechanism, unanswered gaps, unsupported connections, vivid
examples applied too broadly, source bias repeated in the briefing, and poor fit
with the user's intended use.

Then read [references/fidelity-check.md](references/fidelity-check.md) and start
one independent reviewer in a clean context. Give it every artifact listed in
that file, but not the orchestrator's synthesis reasoning. Apply only the check
defined there.

The report is binding. For every finding, restore a lost disagreement to the
contradiction map or Source Audit, or state in the briefing why it was set
aside; remove or correct invented tension; for an analytical finding, add the
missing evidence trace or explicit inference label and calibrated confidence.
A finding may not be accepted while the briefing remains unchanged. Rerun the
same fidelity check on each revised briefing in a new clean reviewer context
until it reports clean. If a clean recheck is unavailable, disclose the reduced
verification, lower confidence, and record that state internally. Update the
fidelity history and overall state after every attempt. When no
clean independent reviewer is available for the initial check, state that the
check did not run and lower confidence.

## Completion check

- `p0` is sourced, and the perspective scan considered additional lenses.
- The intended set reflects user narrowing; every completed lens used a clean,
  identical four-part seed except for its own lens.
- Raw returns are retained, and failed lenses remain visible in the internal
  run record.
- Each lens-specific contribution is evidence-backed or states that it adds
  nothing beyond the findings; the briefing does not manufacture novelty.
- Contradictions, agreement, gaps, source risk, confidence, the frontier
  question, and reliability findings survive output adaptation.
- Every material user-facing claim has a complete source-audit row; unsupported
  claims name the missing evidence, are classified as unverified, and carry low
  confidence.
- Research questions and synthesis test material foundations, mechanisms,
  relationships, patterns over time, and downstream effects when relevant;
  material claims remain evidence-traceable or explicitly inference-labeled
  with calibrated confidence.
- The briefing integrates those findings where they help the reader and does
  not add mandatory analytical sections or unsupported dynamics.
- Long-form work has an outline before prose.
- The fidelity report changed the briefing when it found a defect and each
  revision was rechecked until clean, or reduced verification is disclosed as
  degradation with lower confidence.
- The internal run record states lens, isolation, source-access, fidelity, and
  overall status without claiming capabilities that did not run. Normal output
  omits that telemetry and discloses material degradation concisely.
