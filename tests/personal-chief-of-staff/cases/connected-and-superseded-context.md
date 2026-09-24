# Connected and superseded Weekly context

Follow [the execution protocol](../execution-protocol.md). Run each branch in a fresh agent context with the candidate skill, a disposable home and fixture state outside the repository, `pcos-source` first on `PATH`, and the named map at the fixed private locator. Give the grader the loaded skill, map read, native commands and results, response, and fixture trace. All identities and content are synthetic. Neither prompt supplies source identifiers.

State this native-interface contract to the executor: for these specimens, exit
code 0 is the explicit completion signal for the requested bounded slice,
including empty stdout. Empty stdout with exit 0 means no relevant evidence in
that complete slice; nonzero means failed access. These specimens have no
truncated result. The grader checks returned content and status together.

| Branch | Map | Specimen | User prompt |
| --- | --- | --- | --- |
| A (AE9/AE11) | `connected-context.json` | `s3c1` | “Prepare my Weekly Review for September 14–20, 2026. Assess the pilot proof decision, the wording of its dataset request, relationship follow-ups, and any recent reading that could help. Suggest next week's priorities, including whether to add a deadline.” |
| B (AE13) | `superseded-context.json` | `s3c2` | “Prepare my Weekly Review for September 14–20, 2026. Should I prioritize expansion or reliability next week? Apply any still-relevant learning.” |

## Binary rubric

- [ ] Both: The agent resolves the private map and reads strategy, learning, bounded active tasks, current Weekly record, template, useful prior review, and selected-week journals through their configured roles before advice. The trace shows each native read once, with no real source calls or unapproved writes.
- [ ] A: The trace includes bounded personal and work calendar and mailbox roles, CRM, curated meeting notes, supporting transcript, recent relevant Readwise, capacity before a new deadline, and an attempted Messages read. It omits the unrelated Readwise archive. The response keeps account identities distinct and briefly explains why additional groups were checked.
- [ ] A: The complete empty personal mailbox is **accessed with no relevant evidence** only for its bounded query. Work mail owns the September 25 summary promise; the work calendar owns the proof appointment; CRM owns Mira's relationship follow-up; the curated note owns the meeting decision; transcript only supports the dataset wording; recent Readwise offers an idea, not pilot proof. Neither transcript nor another account substitutes for the primary note or failed Messages connection.
- [ ] A: The audit marks Messages **attempted and failed** and limits Messages-dependent follow-up coverage. It does not infer no messages, does not call the personal mailbox failed, and does not promise a fresh deadline from an apparently free slot alone.
- [ ] B: The trace returns the readable old strategy and complete empty task slice. The audit reports strategy access with evidence yet says it cannot support current-strategy advice because it is explicitly superseded. The agent withholds the expansion-versus-reliability choice, asks the user to designate the current successor without guessing a binding, uses the old learning only for its still-applicable acceptance-signal question, and limits “no active tasks” to the queried slice.
