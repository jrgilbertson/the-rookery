---
name: storm-research
description: "Use only for requests whose deliverable is a full research briefing, a STORM-style investigation, or an evidence review across multiple independent perspectives. The work compares competing evidence, maps contradictions and blind spots, and supports decisions, investments, negotiations, long-form writing, presentations, or learning a new domain."
---

# Storm Research

Produce a grounded research briefing by establishing baseline facts, discovering
source-implied perspectives, asking independent lens-specific questions,
preserving disagreement, and auditing reliability and source quality.

Material means capable of changing the answer, confidence, or next action.

## Workflow

### 1. Frame the target

Resolve the research topic and create one self-contained **framed topic** with:

- the question and requested deliverable;
- the user's role or intended use;
- scope, time horizon, geography or domain, and useful-enough success criteria;
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

Create a concise, sourced, lens-neutral grounding record covering:

- definitions and scope boundaries;
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

Inspect three to five source surfaces most likely to expose a material missing
perspective. Use the five canonical lenses unless the user narrows the set:

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
action. Supplemental lenses add to the non-narrowed canonical set; they do not
replace it.

Lock the intended lens set in the execution manifest. The canonical lenses left
after user narrowing and every user-required lens are required. Mark a
source-discovered lens supplemental unless the research target makes it
material to usable coverage. Record the narrowing, required and supplemental
lenses, source-access state, and any degradation before dispatch.

### 4. Dispatch one isolated executor per lens

Read [references/lens-charter.md](references/lens-charter.md). It applies
unchanged to every lens in the locked set. Use the harness's capability for
starting isolated executor contexts, dispatching concurrently when possible
and queueing when capacity is limited. Start a generic executor context rather
than a preconfigured role whose hidden task instructions would contaminate the
exact four-part seed below.

The orchestrator's orientation ends before dispatch. After dispatch, each lens
executor owns its substantive research; the orchestrator retains and curates
returns rather than becoming an additional lens.

Give every executor exactly four seed parts:

1. the common lens charter content;
2. the identical frozen framed topic from step 1;
3. that executor's lens and no other lens;
4. the identical sourced `p0` baseline from step 2.

Required system policy and tool instructions may remain outside the task seed,
but no inherited task conversation or sibling work may enter the context. Do
not summarize an earlier return into a queued seed. Record the context-launch
and queue isolation mechanism in the manifest.

If a context contains sibling work, discard its return and restart that lens in
a clean context. When clean contexts are unavailable or their cleanliness
cannot be verified, use the best available separation, label the result a
**single-context synthesis**, state the separation used, and lower confidence.
An intended required lens that fails or returns no usable result stays failed.
Continue with partial research when useful, but mark the run degraded and
record each limitation, its effect on coverage or confidence, and what would
upgrade the result. For unverified cleanliness, name the harness signal or
mechanism needed to confirm that no inherited task conversation or sibling work
entered each executor.

Collect every return unchanged and retain the raw returns for fidelity review.
This step is complete when every intended lens is recorded as completed or
failed, every completed return is retained unchanged, and the manifest records
the isolation mechanism and verification state, queue handling, source access,
and degradation state.

### 5. Map contradictions and gaps

From the raw returns, answer:

1. Where do lenses directly conflict?
2. Which conflicts matter most for the intended use?
3. Which side has the strongest evidence, and which is weakest?
4. What does every completed lens agree on?
5. What did none of the completed lenses address?
6. Which question would resolve the largest uncertainty?

Preserve the force and evidence of dissent rather than flattening it into a
generic hedge. A missing or failed lens is a coverage gap, not agreement.

### 6. Audit sources

Create a source audit internally for every task. Include it in the deliverable
when the work is consequential, current, disputed, or source-heavy:

| Claim | Best source | Source type | Bias or tone risk | Missing counter-source | Confidence |
| --- | --- | --- | --- | --- | --- |
| `<claim>` | `<source or none found>` | Primary/secondary/tertiary/none | `<risk>` | `<needed source>` | High/Medium/Low |

Audit promotional, institutional, ideological, geographic, and political bias.
Source clusters with the same incentives do not constitute independent
confirmation. This step is complete when every material user-facing claim has a
best source, source type, bias or tone risk, missing counter-source, and
confidence. An unsupported claim still gets a complete row: record no supporting
source and no source type, mark the claim unverified, name the evidence needed,
and keep confidence low.

### 7. Run both cross-lens analyses

Read [references/analysis-methods.md](references/analysis-methods.md). After
contradiction mapping and the source audit, run both the first-principles and
systems-thinking passes for every routed task. Each pass uses the sourced `p0`,
all raw returns, contradiction map, and source audit. These are curator-owned
cross-lens analyses, not new lenses; never send them to lens executors or feed
their results back into lens research.

Retain evidence links, inference labels, calibrated confidence, and degraded
limits in the internal analytical record. A full briefing renders both analyses
under the exact headings `First-principles analysis` and `Systems thinking and
higher-order effects`, including an honest null result or degraded limit. A
short or custom form may omit the headings, but it must preserve every material
analytical finding and uncertainty.

### 8. Synthesize the requested form

For an article, paper, blog post, presentation, or report, read
[references/briefing-template.md](references/briefing-template.md) and produce
its long-form outline before prose.

For other work, synthesize directly into the user's requested briefing,
recommendation, preparation notes, negotiation questions, learning path, or
other research-backed form. The intended use controls the ending: include an
actionable implication or verdict when it helps that purpose, and do not force
one into an exploratory briefing.

### 9. Emit the briefing

Unless the user requested a shorter or custom form, read
[references/briefing-template.md](references/briefing-template.md) and use its
full-briefing structure. For short or custom outputs, preserve compact
citations and compress presentation without dropping a material contradiction,
analytical finding or uncertainty, confidence limit, degradation, frontier
question, or reliability finding.

Before fidelity review, reconcile the Source Audit against the draft. Add or
update a complete row for every material claim introduced or changed during
analysis and synthesis, including unsupported claims.

### 10. Review curation fidelity

First self-review the draft for its weakest claim, lens dominance, skeptic
steelman quality, concrete incentives, mechanism-comparable historical
analogies, unaddressed gaps, unsupported associations, overgeneralized vivid
examples, source-bias transfer, and fit to the user's intended use.

Then read [references/fidelity-check.md](references/fidelity-check.md) and start
one independent reviewer in a clean context. Give it the fidelity instructions,
the final briefing, sourced `p0`, source audit, all raw lens returns, and the
execution manifest, but not the orchestrator's synthesis reasoning. The
reviewer checks only whether the briefing lost or invented disagreement and
whether every material analytical assumption, mechanism, and causal-chain link
is evidence-traceable or explicitly inference-labeled with calibrated
confidence. It does not judge conclusion correctness or general quality.

The report is binding. For every finding, restore a lost disagreement to the
contradiction map or Source Audit, or state in the briefing why it was set
aside; remove or correct invented tension; for an analytical finding, add the
missing evidence trace or explicit inference label and calibrated confidence.
A finding may not be accepted while the briefing remains unchanged. Rerun the
same fidelity check on each revised briefing in a new clean reviewer context
until it reports clean. If a clean recheck is unavailable, disclose the reduced
verification, lower confidence, and record that state in the manifest. Update
the fidelity history and overall state after every attempt. When no
clean independent reviewer is available for the initial check, state that the
check did not run and lower confidence.

## Completion check

- `p0` is sourced, and the perspective scan considered additional lenses.
- The intended set reflects user narrowing; every completed lens used a clean,
  identical four-part seed except for its own lens.
- Raw returns are retained, and failed lenses remain visible in the manifest.
- Each lens-specific contribution is evidence-backed or states that it adds
  nothing beyond the findings; the briefing does not manufacture novelty.
- Contradictions, agreement, gaps, source risk, confidence, the frontier
  question, and reliability findings survive output adaptation.
- Every material user-facing claim has a complete source-audit row; unsupported
  claims name the missing evidence, are classified as unverified, and carry low
  confidence.
- Both analytical passes used the sourced `p0`, all raw returns, contradiction
  map, and source audit; material claims remain evidence-traceable or explicitly
  inference-labeled with calibrated confidence.
- Every full briefing has both exact analytical headings, including honest null
  or degraded limits; compressed forms preserve every material analytical
  finding and uncertainty.
- Long-form work has an outline before prose.
- The fidelity report changed the briefing when it found a defect and each
  revision was rechecked until clean, or reduced verification is disclosed as
  degradation with lower confidence.
- The final execution manifest states lens, isolation, source-access, fidelity,
  and overall status without claiming capabilities that did not run.
