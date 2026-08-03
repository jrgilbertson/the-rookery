---
name: storm-research
description: "Use only for requests whose deliverable is a full research briefing, a STORM-style investigation, or an evidence review across multiple independent perspectives. The work compares competing evidence, maps contradictions and blind spots, and supports decisions, investments, negotiations, long-form writing, presentations, or learning a new domain."
---

# Storm Research

Produce a grounded research briefing by establishing baseline facts, discovering
source-implied perspectives, asking independent lens-specific questions,
preserving disagreement, and auditing reliability and source quality.

## Research contract

Run the five canonical lenses unless the user narrows the lens set. Honor an
explicit narrowing exactly; a perspective scan may identify omitted coverage,
but it does not override the user's scope.

| Lens | Contribution | Failure mode it catches |
| --- | --- | --- |
| **Practitioner** | Daily operating reality | Advice that ignores implementation friction |
| **Academic** | Research, formal models, and measurement quality | Anecdotes or narratives unsupported by evidence |
| **Skeptic** | The strongest counterargument | Confirmation bias and one-sided enthusiasm |
| **Economist** | Incentives, constraints, market structure, and opportunity cost | Narratives that hide resource trade-offs |
| **Historian** | Precedents, cycles, analogies, and failure patterns | Treating old mechanisms as unprecedented novelty |

Before dispatch, scan sources for load-bearing topic-specific lenses such as a
regulator, customer, clinician, operator, technical architect, adversary,
ethicist, educator, community, or geopolitical perspective. Supplemental lenses
add to the non-narrowed canonical set; they never replace it.

The research orchestrator owns framing, bounded orientation, dispatch, and
curation. Orientation consists only of the `p0` baseline and perspective scan,
and ends before lens dispatch. Each lens executor independently performs the
substantive research. After dispatch, the orchestrator curates returns rather
than becoming a privileged additional lens.

## Isolation and degradation

Independence is part of correctness. Start every lens, including every queued
lens, in a genuinely clean executor context containing the common seed and no
inherited conversation, sibling questions, sources, findings, or returns. A
custom prompt added to an inherited context is not isolation. Reusing a
concurrency slot is acceptable only when it starts a new clean context rather
than resuming or repurposing an earlier executor context.

If a seed or context contains sibling work, discard its return and restart that
lens cleanly. If clean contexts are unavailable, use the best available
separation, label the result a **single-context synthesis**, state what
separation actually occurred, and lower confidence. Never represent that run as
independent multi-perspective research.

Treat the run as degraded when any of these applies:

- clean executor contexts are unavailable or cannot be verified;
- source access needed for a required claim or lens is unavailable;
- an intended required lens fails or returns no usable result, including after
  the user narrows the intended set;
- the independent disagreement-fidelity check cannot run.

Continue with useful partial research when possible, but name each limitation,
its effect on coverage or confidence, and what would upgrade the result. If
source access is unavailable, label factual lens work an **unverified
perspective simulation** and keep factual confidence low.

Maintain a concise execution manifest throughout the run. It is an auditable
record for the final briefing and fidelity reviewer, not checkpoint or resume
machinery. Record:

- intended lenses, distinguishing required and supplemental lenses and noting
  any user narrowing;
- completed lenses and failed lenses with reasons; a failed lens is never
  counted as completed;
- the isolation mechanism and whether clean context was verified, including
  how queued executors were kept clean;
- source-access state and material limits;
- fidelity state and review history: pending, completed-clean,
  completed-with-binding-findings applied, or unavailable, including whether a
  revised briefing received a clean recheck;
- overall normal or degraded state and every degradation reason.

## Grounding and budget

Lenses generate questions; sources provide evidence. Fetch current sources when
the topic depends on current facts, vendor behavior, law, finance, health, APIs,
prices, benchmarks, or news. Prefer primary sources such as official documents,
papers, filings, standards, repositories, published data, and direct product
pages. Distinguish evidence from inference, and audit promotional,
institutional, ideological, geographic, and political source bias.

The research budget is per executor, not per run. Each lens stops when its own
questions are answered and cannot economize based on sibling work it cannot
see. Stop collection when key claims have strong sources, contradictions are
clear, and more sources repeat rather than change the answer. Continue only
when the weakest claim, frontier question, or user-facing conclusion remains
materially unsupported.

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

Create a concise, sourced, lens-neutral grounding record covering:

- definitions and scope boundaries;
- key actors, systems, examples, and terms of art;
- timeline and current state when relevant;
- what is known, disputed, and unknown;
- citations or permitted resource identifiers for its claims;
- source-access caveats.

Freeze one baseline block before dispatch and use it verbatim for every lens.
It is shared orientation, not a substitute for each executor's own sourcing.

### 3. Scan sources and lock the lens set

Inspect three to five useful source surfaces when available: official documents,
papers, adjacent articles, high-quality explainers, filings, repositories, or
domain-specific sources. Ask which perspectives the canonical five miss, and
add only load-bearing lenses for the topic or intended use. Respect explicit
user narrowing while doing this scan.

Lock the intended lens set in the execution manifest. The canonical lenses left
after user narrowing and every user-required lens are required. Mark a
source-discovered lens supplemental unless the research target makes it
necessary for usable coverage; record that decision before dispatch.

### 4. Dispatch one isolated executor per lens

Read [references/lens-charter.md](references/lens-charter.md). Use the harness's
capability for starting isolated executor contexts, dispatching concurrently
when possible and queueing when capacity is limited. Start a generic executor
context rather than a preconfigured role whose hidden task instructions could
add a fifth seed part.

Give every executor exactly four seed parts:

1. the common lens charter content;
2. the identical frozen framed topic from step 1;
3. that executor's lens and no other lens;
4. the identical sourced `p0` baseline from step 2.

Required system policy and tool instructions may remain outside the task seed,
but no inherited task conversation or sibling work may enter the context. Do
not summarize an earlier return into a queued seed. Record the context-launch
and queue isolation mechanism in the manifest.

Collect every return unchanged and retain the raw returns for fidelity review.
Update completed and failed lens state without silently shrinking the intended
set.

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
| `<claim>` | `<source>` | Primary/secondary/tertiary | `<risk>` | `<needed source>` | High/Medium/Low |

Use the audit to lower confidence rather than decorate the output. Source
clusters with the same incentives do not constitute independent confirmation.

### 7. Run both cross-lens analyses

Read [references/analysis-methods.md](references/analysis-methods.md). After
contradiction mapping and the source audit, run both the first-principles and
system-dynamics passes for every routed task. Each pass uses the sourced `p0`,
all raw returns, contradiction map, and source audit. These are curator-owned
cross-lens analyses, not new lenses; never send them to lens executors or feed
their results back into lens research.

Retain evidence links, inference labels, calibrated confidence, and degraded
limits in the internal analytical record. A full briefing renders both analyses
under the exact headings `First-principles analysis` and `System dynamics and
higher-order effects`, including an honest null result or degraded limit. A
short or custom form may omit the headings, but it must preserve every material
analytical finding and uncertainty. Here, material means capable of changing
the answer, confidence, or next action.

### 8. Synthesize the requested form

For an article, paper, blog post, presentation, or report, produce an outline
before prose. Include a working thesis, section sequence, key claim and needed
evidence per section, the contradiction or objection each section resolves,
and the caveat or reliability note that must survive drafting.

For other work, synthesize directly into the user's requested briefing,
recommendation, preparation notes, negotiation questions, learning path, or
other research-backed form. The intended use controls the ending: include an
actionable implication or verdict when it helps that purpose, and do not force
one into an exploratory briefing.

### 9. Emit the briefing

Unless the user requested a shorter or custom form, produce a full briefing
with this structure:

```text
Answer or bottom line: <one-paragraph answer suited to the intended use>

Baseline facts:
- <definitions / actors / current state / scope constraints>

Perspective scan:
- <Lens>: <question asked + grounded answer + confidence>

Contradictions that matter:
1. <conflict + evidence on each side + why it matters>

What all completed lenses agree on: <shared finding>
What none addressed: <gap / blind spot>

First-principles analysis
- <verified facts, assumptions, irreducible constraints, main mechanism,
  necessary conditions, evidence or inference labels, and confidence>

System dynamics and higher-order effects
- <boundary and time horizon; material relationships and causal chains with
  link-level evidence or inference labels and confidence; supported dynamics
  or an honest null finding and its limiting boundary/evidence>

Most reliable findings:
1. <finding> — supported by <lenses/sources>; confidence <High/Medium/Low>

Hidden connection: <non-obvious synthesis, only when source-supported>
Actionable implication: <when the intended use calls for one>
Frontier question: <the question that would change the answer most>

Reliability check:
- Weakest claim: <claim + why weak>
- Source/bias risk: <source skew, tone transfer, missing counter-source>
- Missing perspective: <failed or underrepresented lens/source>
- What to verify next: <evidence that would change confidence>

Execution manifest:
- Intended / completed / failed lenses: <auditable state>
- Isolation: <mechanism, queue handling, and clean/degraded state>
- Source access: <state and limitations>
- Fidelity: <state>
- Overall state: <normal or degraded, with reasons>

Sources used:
- <source/link or permitted resource identifier> — <claim it supports>
```

Include the long-form outline when applicable. Preserve compact citations for
external factual claims. For short or custom outputs, compress presentation
without dropping a material contradiction, analytical finding or uncertainty,
confidence limit, degradation, frontier question, or reliability finding.

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
the fidelity history and overall state honestly after every attempt. When no
clean independent reviewer is available for the initial check, state that the
check did not run and lower confidence.

## Completion check

- `p0` is sourced, and the perspective scan considered additional lenses.
- The intended set reflects user narrowing; every completed lens used a clean,
  identical four-part seed except for its own lens.
- Raw returns are retained, and failed lenses remain visible in the manifest.
- Contradictions, agreement, gaps, source risk, confidence, the frontier
  question, and reliability findings survive output adaptation.
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
