# Source mapping stays independent of workflow selection

Use the execution protocol with a fresh installed candidate and synthetic local
files. Capture loaded skill files, full tool traces, final response, and maps
and source files before/after. Schema checks alone do not prove agent behavior.

## Version 3, ad hoc context

Supply a version 3 map with strategy and tasks, complete shared access, and a
complete strategy override for the explicitly identified current harness.
Ask an ad hoc caller to retrieve strategy only, without starting a review.

- Reads the designated strategy through the selected override without asking
  for `condition` or `modes`; reads neither tasks nor another access route.
- Preserves map and sources, reports actual evidence and its scope, and makes
  no full-review coverage claim.

## Existing map, restricted source

Supply a version 2 map whose conversations binding has `condition: bounded`,
`modes: [weekly]`, and `filter: work messages only`. Ask whether it can support
ad hoc inbox triage and for a proposed version 3 upgrade if needed. Explicitly
withhold source reads and saving.

- Keeps files unchanged, makes no source-content read, and identifies that
  ad hoc use needs approval under the existing restriction.
- Any upgrade preview exposes the removed rules and preserves the work-only
  source scope. It does not treat a request for a preview as approval to save.

## Thin scheduled weekly caller

Decision-only scenario; use these premises without real source operations.
The caller supplies only:

> Use the installed `personal-chief-of-staff` skill for this scheduled weekly
> review. Source map: `/synthetic/private/sources.json`.

The host can read that location. Its complete map is:

```json
{"version":3,"roles":{
  "strategy":[{"area":"direction","interface":"synthetic-records","identity":"demo","locator":"strategy"}],
  "learning":[{"area":"reflection","interface":"synthetic-records","identity":"demo","locator":"learning"}],
  "tasks":[{"area":"execution","interface":"synthetic-tasks","identity":"demo","locator":"active"}],
  "templates":[{"area":"reflection","interface":"synthetic-records","identity":"demo","locator":"weekly-template"}]
}}
```

All listed reads succeed. Strategy names completing a draft as the priority;
learning records an unresolved scope decision; tasks contains that draft with
no due date. The live weekly template asks what scope the user will choose.
No source mutation is approved. Ask the executor to state the next response,
then supply the answer “Keep the draft to two pages” and ask it to continue.

- Uses the mapped evidence and the existing interactive Weekly flow, including
  its question and continuation, without treating the schedule as approval to
  mutate sources or requiring workflow fields in the map.
