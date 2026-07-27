# Trigger and activation test: [skill-name]

This record keeps structural validation, listing judgment, and native harness
behavior separate. Every check uses exactly one state: **passed**, **failed**,
or **unverified**. A passed listing proxy never satisfies native discovery,
installation, content identity, loading, or triggering.

## Declaration

- Package source and revision: [local path plus revision/hash]
- Declared model-harness target cells: [target cell IDs]
- Listing-query tier: [routine: 5+5 once / public or load-bearing: 8-10+8-10 three times]

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
context that sees the skill's name and description, but not its body. Record the
target cell on every judgment. An unsure or hedged judgment is borderline.

Routine tier: five should-trigger and five near-miss queries, one run each. On a
borderline result, run that query twice more and use the majority. Public or
unusually load-bearing tier: eight to ten queries per table, three runs each; a
should-trigger needs two of three, and any near-miss activation fails the set.

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
| [target-a] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [result summary and raw-enough excerpt or reference] |
| [target-b, if declared] | [YYYY-MM-DD] | [exact model ID] | [harness, version] | [material settings] | [passed / failed / unverified] | [result summary and raw-enough excerpt or reference] |

## Native package-harness checks

Native discovery and local installation may be shared only by target cells using
the same package revision and harness. Verify that the installed content came
from the declared local source before using it as evidence.

| Package-harness cell | Date | Harness and version | Native discovery state | Local-source install state | Installed-content identity state | Evidence or limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [package+harness-a] | [YYYY-MM-DD] | [harness, version] | [passed / failed / unverified] | [passed / failed / unverified] | [passed / failed / unverified] | [commands, revision/hash comparison, output excerpt, or reason unavailable] |

## Native model-harness checks

Native load and native trigger remain attributable to each exact model-harness
target, even when discovery or installation evidence is shared.

| Target cell | Date | Exact model | Harness and version | Configuration | Native load state | Native trigger state | Evidence or limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

- Earned evidence label: [none / smoke-tested / directional comparison]
- Overall limitation: [missing cells and what remains unverified]

When target states conflict, preserve each state. Do not average a failure or an
unavailable cell into a pass.

## Tuning

Fix listing failures by front-loading trigger words and describing when to use
the skill, not by summarizing the workflow. After any description edit, rerun
the complete query set because the edit can activate a near-miss, and rerun the
affected behavioral comparison because a description change is substantive.

## Waiver (only when shipping with an unavailable native check)

A waiver changes shipment authority only. It does not change a failed or
unverified state, turn listing evidence into native evidence, raise the evidence
label, or authorize an unsupported instruction removal.

- Waived by the user: [yes, quote or paraphrase the explicit waiver]
- Unavailable check and reason: [check, target cell, and reason]
- Shipment status: [unverified candidate]
- Date: [YYYY-MM-DD]
