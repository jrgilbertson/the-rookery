# Trigger and activation test: [skill-name]

This record keeps structural validation, listing judgment, and native harness
behavior separate. Every check uses exactly one state: **passed**, **failed**,
or **unverified**. A passed listing proxy never satisfies native discovery,
installation, content identity, loading, or triggering.

This template is the authoritative source for listing-query construction, tier
selection, scoring, evidence states, and native-check recording.

## Declaration

- Package source and revision: [local path plus revision/hash]
- Declared model-harness target cells: [target cell IDs]
- User-selected verification mode: [ordinary personal skill / public or unusually load-bearing skill]
- Listing-query tier: [ordinary personal skill: routine 5+5 once / public or unusually load-bearing skill: 8-10+8-10 three times]
- Listing-judge mechanism: [separate agent and fresh context per query]

| Target cell | Exact model | Harness and version | Configuration, tools, and permissions |
| --- | --- | --- | --- |
| [target-a] | [exact model ID] | [harness, version] | [material settings] |
| [target-b, if declared] | [exact model ID] | [harness, version] | [material settings] |

## Structural validation

| Date | Validator and version | Command | State | Evidence or limitation |
| --- | --- | --- | --- | --- |
| [YYYY-MM-DD] | [tool, version] | [exact command] | [passed / failed / unverified] | [output excerpt, reference, or reason unavailable] |

## Listing proxy

Listing judgment tests the description contract only. Run each query in a fresh
context through a separate agent that did not author the description. Show that
agent the skill's name, description, and one query, but not its body or the
author's expected judgment. Record the target cell on every judgment. An unsure
or hedged judgment is borderline.

The selected verification mode changes only listing-proxy evaluation: query
count, repetition, and tier-specific judgment rules. It does not change the
required matched comparison, structural validation, native checks, or declared
model-harness target set.

Write realistic queries with concrete context. Vary length, formality, detail,
implied intent, abbreviations, and minor typing mistakes. Should-trigger cases
must represent work where the skill should change execution or output.
Near-misses should share its topic, artifact, or common wording but require a
different job.

Record the judgment and its context or transcript reference in each run cell,
for example `[yes; run-01]`. A bare judgment does not prove a fresh context.

For each target, its listing proxy passes only when every required query has an
available judgment, every should-trigger query passes under the selected tier,
and every near-miss query passes the selected tier's categorical-`no`
threshold. Record it as failed when an available should-trigger result misses
the tier threshold, a near-miss activates, or a completed near-miss result
misses its categorical-`no` threshold. Record it as unverified when a required
judgment is unavailable and no available result has already failed the set.

Routine tier: five should-trigger and five near-miss queries, one run each. A
clear first categorical judgment determines the query result: `yes` passes a
should-trigger and `no` fails it, while `no` passes a near-miss and `yes` fails
it. Only when the first judgment is borderline (`unsure` or hedged) run that
query twice more. An available borderline judgment is neither a `yes` nor a
`no` vote. The resulting three-run should-trigger needs at least two `yes`
judgments. The resulting three-run near-miss needs at least two categorical
`no` judgments, and any `yes` is an immediate failure. Any complete three-run
result that misses its threshold fails. Public or unusually load-bearing tier:
eight to ten queries per table, three runs each; a should-trigger needs two of
three. Every near-miss needs at least two categorical `no` judgments; any `yes`
is an immediate failure, and a complete three-run result without two
categorical `no` judgments fails.

### Should-trigger queries

| Target cell | Query | Run 1 | Run 2 | Run 3 | State |
| --- | --- | --- | --- | --- | --- |
| [target-a] | [phrasing 1] | | | | [passed / failed / unverified] |
| [target-a] | [phrasing 2] | | | | [passed / failed / unverified] |
| [target-a] | [phrasing 3] | | | | [passed / failed / unverified] |
| [target-a] | [phrasing 4] | | | | [passed / failed / unverified] |
| [target-a] | [phrasing 5, non-obvious] | | | | [passed / failed / unverified] |

Duplicate the rows for every declared target and add rows up to ten per target
for the public or load-bearing tier.

### Near-miss queries (expected: no trigger)

| Target cell | Query | Run 1 | Run 2 | Run 3 | State |
| --- | --- | --- | --- | --- | --- |
| [target-a] | [near-miss 1] | | | | [passed / failed / unverified] |
| [target-a] | [near-miss 2] | | | | [passed / failed / unverified] |
| [target-a] | [near-miss 3] | | | | [passed / failed / unverified] |
| [target-a] | [near-miss 4] | | | | [passed / failed / unverified] |
| [target-a] | [near-miss 5] | | | | [passed / failed / unverified] |

Duplicate the rows for every declared target and add rows up to ten per target
for the public or load-bearing tier.

| Target cell | Date | Actual model | Actual harness and version | Actual configuration | Listing-proxy state | Evidence or limitation |
| --- | --- | --- | --- | --- | --- | --- |
| [target-a] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [result summary and an excerpt that supports it, or a durable reference] |
| [target-b, if declared] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [result summary and an excerpt that supports it, or a durable reference] |

## Native package-harness checks

Native discovery and local installation may be shared only by target cells using
the same package revision, harness, install/discovery location, and material
discovery configuration. When project or working-directory context affects
discovery, it must also match; otherwise record discovery evidence separately.
Verify that the installed content came from the declared local source before
using it as evidence.

| Package-harness cell | Date | Harness and version | Native discovery state | Local-source install state | Installed-content identity state | Evidence or limitation |
| --- | --- | --- | --- | --- | --- | --- |
| [package+harness-a] | [YYYY-MM-DD] | [harness, version] | [passed / failed / unverified] | [passed / failed / unverified] | [passed / failed / unverified] | [commands, revision/hash comparison, output excerpt, or reason unavailable] |

## Native model-harness checks

Native load and native trigger remain attributable to each exact model-harness
target, even when discovery or installation evidence is shared.

Before native load can pass, inventory the applicable project, user, and
system locations for the same skill name. Isolate non-authoritative copies or
capture deterministic runtime provenance tied to the installed source: a
native load trace naming the exact installed path or base directory, or
equivalent runtime evidence linked to the installed content hash. Distinctive
output may corroborate that provenance, but cannot independently prove
loaded-copy identity. Installed-content identity alone also does not prove
which copy loaded. If deterministic runtime provenance is unavailable, keep
native load unverified rather than failed and record the limitation. Native
trigger for the declared package revision is also unverified when loaded-copy
identity is unverified; record an unattributed invocation only as an
observation. Keep installation identity, native discovery, native load, native
trigger, and behavioral evidence as separate states.

| Target cell | Date | Exact model | Harness and version | Configuration | Native load state | Native trigger state | Evidence or limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [target-a] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [passed / failed / unverified] | [native observation, excerpt/reference, or reason unavailable] |
| [target-b, if declared] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [passed / failed / unverified] | [native observation, excerpt/reference, or reason unavailable] |

## Evidence summary

| Evidence layer | Scope | State | Claim limit |
| --- | --- | --- | --- |
| Structural validation | [package revision] | [passed / failed / unverified] | Structure only |
| Listing proxy | [each target cell] | [passed / failed / unverified] | Description-routing proxy only |
| Native discovery | [each package-harness cell] | [passed / failed / unverified] | Discovery only |
| Local-source installation | [each package-harness cell] | [passed / failed / unverified] | Installation only |
| Installed-content identity | [each package-harness cell] | [passed / failed / unverified] | Confirms tested revision only |
| Native load | [each model-harness target cell] | [passed / failed / unverified] | Load only |
| Native trigger | [each model-harness target cell] | [passed / failed / unverified] | Observed trigger only |

- Baseline comparison record: [path or not applicable]
- Overall limitation: [missing cells and what remains unverified]

When target states conflict, preserve each state. Do not average a failure or an
unavailable cell into a pass.

Bind every native evidence row to the tested package revision. A later
substantive package edit invalidates native package-harness and model-harness
states recorded against the superseded revision until those cells rerun.

## Tuning

Fix listing failures by front-loading trigger words and describing when to use
the skill, not by summarizing the workflow. After any description edit, rerun
the complete query set because the edit can activate a near-miss, and rerun the
affected behavioral comparison because a description change is substantive.

## Shipment waiver (only for an unavailable required listing judgment or native check)

A waiver changes shipment authority only. It leaves unavailable evidence
unverified; failed evidence cannot be waived. It does not turn listing evidence
into native evidence, raise the evidence label or Claim Ceiling, or authorize
an unsupported instruction removal.

- Waived by the user: [yes, quote or paraphrase the explicit waiver]
- Unavailable required judgment/check and reason: [listing judgment or native check, target cell, and reason]
- Shipment status: [unverified candidate]
- Date: [YYYY-MM-DD]
