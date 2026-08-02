# Trigger contract: storm-research

Judged per the protocol in [`tests/README.md`](../README.md): fresh context,
name + description + query only, binary judgment, any near-miss `yes` fails.

## Should trigger

| Query | Reason |
| --- | --- |
| Research the evidence for and against congestion pricing, using multiple independent perspectives and current sources | Explicit deep, source-backed, multi-perspective investigation. |
| Use STORM to give me a full briefing on why antibiotic resistance is accelerating | Explicit STORM research request. |
| I need deep research on whether our city should replace diesel buses with electric ones; surface contradictions and blind spots before recommending anything | A decision that explicitly requires new evidence, independent perspectives, and contradiction mapping. |
| Research how the printing press changed scientific institutions and give me a cited briefing, not a verdict | Broad historical research with a requested research deliverable. |
| Prepare a source-backed article outline on commercial fusion using competing practitioner, academic, economic, skeptical, and historical views | Research-heavy pre-writing using the canonical perspective pattern. |
| Investigate the strongest evidence on four-day workweeks and tell me what would change the answer | Deep research with source quality, disagreement, and a frontier question. |
| What are the hidden assumptions and higher-order effects in the global shift to heat pumps? Do the underlying research first | Explicit analytical synthesis over a research task. |
| Before we choose a database vendor, run a multi-perspective evidence review of the market and technical tradeoffs | An adoption decision explicitly asking for fresh external research. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Read this architecture proposal and give me a decisive recommendation on whether our repository should adopt it | `ce-pov` for a bounded, project-grounded verdict. |
| Review this finished launch plan for gaps, ambiguity, and conflicting requirements | `ce-doc-review` for an existing artifact. |
| Audit this CSV for missing values, duplicates, and schema drift | Dataset-quality workflow. |
| What is the current UTC offset in Tokyo? | Routine authoritative lookup. |
| Turn the recommendation above into three bullets for the executive team | Direct compression of an existing recommendation. |
| Brainstorm ten names for a new note-taking app | Ideation without a research request. |
| Explain first-principles thinking with a simple example | Explanation, not source-backed investigation. |
| Map the feedback loops in the process diagram I supplied, using only that diagram | Direct systems analysis of a supplied artifact, not deep research. |
