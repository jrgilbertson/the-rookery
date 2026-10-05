# Creating Portable Skills evaluation

The suite defines five bounded tasks:

- [CPS-ACT-001](cases/activation-near-miss.md): a generic grader request should
  not activate the skill creator merely because it mentions a grader.
- [CPS-ACT-002](cases/activation-authoring.md): implicit skill authoring should
  load the creator through ordinary discovery.
- [CPS-ACT-003](cases/activation-explicit-review.md): naming the creator in a
  normal review request should load it without a forced skill attachment.
- [CPS-ACT-004](cases/activation-writing-near-miss.md): reusable meeting
  instructions should stay an ordinary writing task.
- [CPS-AUD-001](cases/vendor-guidance-audit.md): compare a supplied small skill
  with synthetic vendor guidance without narrowing its portability or editing
  the supplied files.

These definitions alone do not establish host coverage or validated behavioral
results. The synthetic hook in the fixture does not describe a real vendor API.
Updating and migrating skills are not covered.

The target harnesses are Claude and Codex. Grok is outside the current testing
scope; its earlier capture findings are historical evidence, not a coverage
requirement or a blocker for this suite.

## Prepare and capture a run

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow). Agree on the case inputs,
criteria, host, model, execution limits, authentication and budget before model
runs. Send exactly the case's `INPUT` paragraph, optionally followed by one
transport newline. Read each input from its linked case's `INPUT` section.
Supply AUD's two fixture files at their named
relative paths; do not append fixture hints or isolation prose to the paragraph.
Use the exact INPUT paragraph from ACT-002/003/004 as well, with no native skill
attachment. These cases grade native activation only; a draft or review
response is not a behavioral evaluation of a generated skill. The capture
checker names these cases `author`, `review`, and `writing`, respectively.
Record necessary host instructions separately. Keep executor input separate from criteria and answer material. Use native
host tools and disposable storage outside the repository; do not execute the
supplied or generated skill as a second task.

Record exact package, input and grader hashes, resolved host/model, all exposed
instructions and skills, native run identity, complete tool events, output,
elapsed time and available usage. Verify the measured creator package was
available through normal discovery for ACT and explicitly loaded for AUD.
Unsupported discovery, incomplete capture or unverified completion is
Unmeasured. A routing proxy cannot establish native activation.

For the audit, copy the [synthetic inputs](fixtures/vendor-guidance) into the
temporary workspace. Capture the actual input files before dispatch and after
verified completion, using the same workspace for both snapshots:

```sh
python3 tests/creating-portable-skills/evaluate_read_only.py snapshot "$eval_workspace" > "$before_capture"
# Run the approved audit with native host tools; verify completion.
python3 tests/creating-portable-skills/evaluate_read_only.py snapshot "$eval_workspace" > "$after_capture"
python3 tests/creating-portable-skills/evaluate_read_only.py compare "$before_capture" "$after_capture"
```

Set those variables to paths outside this public worktree. The comparator emits
the C3 criterion ID, Pass/Fail/Unmeasured and a reason. Its process exit status
does not represent the grade. Contents, file identity and modification metadata
must remain unchanged. Missing baseline or unreadable evidence is Unmeasured;
observed deletion or replacement fails. Snapshots do not prove that every
transient side effect was captured; retain native tool events and the workspace
change record for review. A snapshot Pass alone does not establish run completion.

Grade AUD C1, C2 and C4 through independent criterion review of the corresponding
output and reference criteria. Preserve each decision, quoted output evidence,
and reviewer feedback. Provisional LLM review is permitted and must be identified
as such; independent human calibration remains required to claim alignment. Do
not substitute keyword matching for whether advice is portable. No exact wording
is required, and unchanged requirements need not be repeated.

Report each host and criterion separately. Exclude incomplete captures from
completed comparisons and leave unavailable usage/cost unknown. This small pilot
can check case clarity and capture reliability; it cannot establish population
success rates, activation reliability beyond the cases run or portability across unmeasured
hosts. Private traces and review pages are not suite dependencies and must not
be committed here.

## Check existing native captures

Claude capture admission uses manual native-trace review; the automated capture
checker below supports Codex and historical Grok captures only. For Claude,
place an unchanged copy of the creator package under the disposable workspace's
`.claude/skills/creating-portable-skills/`, retain its file hashes, and confirm
normal discovery. Capture the approved text with the native CLI's print mode,
`--output-format stream-json --verbose`, a fresh session ID, and the agreed
read-only tool and permission configuration. Retain stdout, stderr, the native
session transcript, effective settings and before/after workspace manifests
outside the repository. Do not supply criterion text or force a skill attachment
for activation cases.

Review the native evidence before assigning behavior grades:

- Require exactly one matching init and successful result, the expected session
  identity throughout, and the exact canonical user input in persisted history.
- Verify the frozen package was discovered, exposed tools and instructions were
  recorded, and every tool call has its matching result with no outstanding or
  delegated work. Record unavailable host context explicitly.
- Inspect all reads against the approved workspace and skill roots. Missing,
  ambiguous or successful outside-root reads make admission Unmeasured.
- Count activation only when a successful native Skill load or body read exposes
  the frozen body. Verify any native wrapper or argument suffix against the
  actual call; discovery metadata, path listings and failed attempts are separate.

This procedure does not depend on a private launcher or prior session. A manual
admission decision must name its evidence and limitations; it is not a verdict
from `validate_capture.py`.

The stdlib capture checker reads Codex `native-requests.jsonl` and
`native-events.jsonl`, or Grok `stdout.ndjson` plus native `chat_history.jsonl`
from the matching session-ID directory. Grok query identity comes from native
`prompt_index` metadata; unclassified user context stays Unmeasured.
It checks actual text against canonical case input, successful native completion,
matching session/turn identity, duplicate or retyped native item identities,
outstanding work and successful reads outside the
approved read roots. Codex also requires a matching post-completion thread read
with `includeTurns` absent or false, idle status and no turn history; this confirms
identity and idleness, not a complete second tool inventory.
Report flags, saved prompt hashes and process exit codes do not replace native
evidence. Supply only executor-approved workspace and skill roots, never a parent
containing criteria, coordination files or other runs. A successful grading or
coordination read invalidates the capture. An opaque successful tool or missing
native evidence is conservatively Unmeasured. Codex command reads are checked
even when the aggregate command fails: a read may succeed before a later error.
Codex `commandActions` are best-effort, lossy display metadata, not an exhaustive
filesystem read audit. Unclassified actions and missing paths remain Unmeasured;
a missing path is not evidence of an observed outside-root read. Without an
enforcement receipt, listing/search paths and paths containing unresolved tilde,
dollar, backtick, brace or wildcard expansions, quotes or backslash escapes remain
Unmeasured even when they look lexically inside a root.
A valid completed
native `sleep` display item is non-reading, but still requires matching identity
and no outstanding work. These checks do not parse opaque commands or scripts to
infer safe reads. The CLI exits 1 for inadmissible or
incomplete evidence; it does not assign a behavioral Fail.

```sh
python3 tests/creating-portable-skills/validate_capture.py codex aud "$capture_dir" --allowed-root "$eval_workspace"
```

Set all paths outside the public worktree. A capture-check Pass covers these
objective observations only. Verify frozen skill identity/discovery separately,
and native filesystem confinement through the receipt below or other host
evidence, before admitting a run. Keep C3's file observation separate even when
a run is excluded from behavioral comparisons.

### Optional Codex enforcement receipt

A Codex command with unknown or path-less `commandActions` is admissible only
with a verified same-server enforcement receipt:

```sh
python3 tests/creating-portable-skills/validate_capture.py codex aud "$capture_dir" --allowed-root "$eval_workspace" --enforcement "$enforcement_plan"
```

This adapter targets the inspected Codex 0.160.0 protocol. Freeze the actual
native executable and invoke its absolute path. Direct tool calls use the raw
native call-to-command identity checks below. CodeMode's synchronous `exec`
facades additionally require the native trace bundle described in the next
section. A direct-tool catalog override is a distinct configuration; report it
separately from native CodeMode. Unmapped calls remain Unmeasured.

The plan is the operator's frozen JSON, not a result: `version` 1, `profile`
`preflight`, the single approved workspace `cwd`, the exact app-server `argv`,
`launcher_sha256`, `binary_sha256`, `config_sha256` for pinned non-secret inputs,
canonical `command/exec` `probe_params` with matching `probe_expectations`
(`exitCode`, exact `stdout`, `stderr_contains`), the required
`expected_tool_configuration`, and `protected_paths`. Allow probes return a
canary. Deny probes must expect exit 1 with a permission error, never a missing
path, and every protected path needs a deny probe. Case files, coordination
files, prior outputs, the plan and the capture must resolve outside the
workspace.

The enforcement adapter accepts one workspace root only. Copy the unchanged
creator package into `.agents/skills/creating-portable-skills/` within that root
so ordinary Codex discovery and instruction reads stay inside it. Put case
definitions, criteria, captures and all coordination material outside the root.
Verify discovery and the copied package's hashes separately.

Use a native app-server recorder, not transcript text copied from a terminal.
The recorder must preserve each client request in `native-requests.jsonl` and
each server response or notification in `native-events.jsonl`, with native IDs
and ordering intact. It must reject approvals, apply the frozen settings before
the turn, verify the effective configuration, perform the planned probes, wait
for native completion and idle `thread/read`, then close and reap the server.
The maintained checker is a consumer, not a capture launcher; an operator may
implement this recorder with the stdlib or existing native orchestration tools.
Its required companion records are:

```text
launch.json: {argv, cwd, binary_sha256, launcher_sha256, config_before}
result.json: {config_after, process_exit_code: 0, completion_verified: true}
final native-events.jsonl row:
  {capture_trailer: true, stdout_lines: N, unparsed_lines: 0}
```

Hash maps use absolute non-secret input paths and SHA-256 digests. `argv` is the
exact native invocation; `cwd` is the approved workspace. `N` counts every
preceding native stdout row, excluding the trailer. Missing or unparsed rows
cannot be replaced with successful completion flags. The recorder's projected
`config/read` response must expose `safeConfiguration` with the exact `PROFILE`
and `TOOLS` contract in [validate_capture.py](validate_capture.py); preserve the
original effective settings separately. Freeze the recorder itself and the
native executable before execution. These are operator-bound facts, not proof
that an arbitrary third-party recorder is trustworthy.

The checker recomputes the receipt from the native streams and spawns nothing.
It requires the same probe block before `turn/start` and after the native
`turn/completed`, with matching exact responses. It also requires the effective
`preflight` profile (`:read-only`, `:root` deny, `:minimal` and
`:workspace_roots` read, `:tmpdir` and `:slash_tmp` deny, network off), approval
`never`, runtime roots equal to `cwd`, and the launcher's redacted
`safeConfiguration` matching the fixed tool surface. Only approved client methods
may appear, with one initialize and one turn. Each request needs exactly one
response. Server requests may receive only paired error replies. The capture
needs a final trailer row covering every native stdout line, with none
unparsed. For direct tools, raw `rawResponseItem/completed` events must show
only `exec_command`, `write_stdin` and `clock.sleep` calls, without elevated
sandbox permissions. Each exec `call_id` must equal a completed
`commandExecution` item ID inside the workspace, and each `write_stdin` must
name the process of an earlier command. CodeMode facades instead require the
native child graph below. The started and completed command payloads must agree.
The checker does not interpret command text to infer reads. An action that names
a path outside the approved roots is still excluded.

`launch.json` and `result.json` hash facts are trusted launcher records bound to
the plan, not independent receipts. Probes sample named paths. They do not audit
every read, and `:minimal` keeps ambient OS, loader, library and device access,
so a receipt does not show the runtime is free of secrets. Without
`--enforcement`, the lossy-action rules above apply unchanged.

Host setup remains a prerequisite. The launcher must verify native confinement
before model execution; permission mode and isolation prose cannot replace it.
A Codex read-only/never policy alone does not prove read confinement. Record
inherited instructions separately and confirm that discovery and any instruction
body loads identify the frozen package. Preserve excluded historical captures
under their original setup and input labels; do not relabel them as repaired
runs. Grok support remains only for historical inspection.

### Native CodeMode trace bundle

For synchronous CodeMode `exec` cells, retain exactly one native bundle under
`$capture_dir/traces/`, containing `manifest.json`, `trace.jsonl` and the referenced
`payloads/` files. The checker consumes any present trace directory, including
zero-tool captures, and requires one when raw `exec` facades appear. No JavaScript
execution or interpretation is involved. The existing
`--enforcement` receipt remains required. Graph provenance does not establish
filesystem confinement by itself.

Enable the native `executed_tool_call_metadata` feature and launch the recorder's
native process with `CODEX_ROLLOUT_TRACE_ROOT` pointing at that case's private
trace directory. Preserve the complete native bundle after shutdown. Record the
exact instrumentation and launch environment: this feature can enrich later
inference history, so describe the run as instrumented native CodeMode even
when the model, effort and catalog keep their configured defaults.

The native schema must expose the facade's model-visible call ID, runtime cell
ID, each child's broker tool-call ID, invocation and result payloads, and the
command's process identity. Multiple children may run concurrently within a
cell; runtime child IDs are local to their cell and may repeat across cells.
The checker follows explicit native links and compares exact payloads against
the app-server command events and later outgoing inference metadata. Payload
references must resolve inside the bundle. Missing, duplicate, foreign, altered,
or unsupported evidence is Unmeasured rather than a behavioral Fail.

The schema is pinned to native Codex 0.160.0's
[raw trace events](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/rollout-trace/src/raw_event.rs)
and [CodeMode output](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/core/src/tools/code_mode/output.rs).
Recheck this contract when changing native versions. The bundle must contain
schema version 1, the matching root thread/rollout identity, contiguous event
sequence numbers, paired terminal lifecycles and a closed inventory of confined
payload references. Every facade output must follow its terminal cell and match
the native result. User messages in the first inference request must match the
app-server user inventory; canonical input and selected skill identities must
match `turn/start`. Other host instructions are not fully attested. Native
capture is operator-supplied evidence, not a proof
of authenticity against a malicious recorder.

Support is bounded to completed synchronous cells with `exec_command` children.
Yielded cells, waits, stdin, sleeps, failed dispatches and other nested tools
remain Unmeasured. A command process may exit nonzero if its complete terminal
result is preserved; capture admission does not require every command to succeed.
A zero-tool capture with a trace bundle still requires consistent native
request and message records. Frozen package discovery and native body loading
remain separate activation observations; a capture Pass does not
grade output quality or establish human alignment.

## Provisional subjective judges

[Criterion prompts](judges/) and [synthetic challenges](judges/validation-cases.json)
are provisional. Independent human labels and calibration remain required to
claim human alignment. Check already recorded judge output with:

```sh
python3 tests/creating-portable-skills/judges/validate_results.py CPS-AUD-001.C1 "$verdicts_file"
```

Use C2 or C4 for the other criteria. The checker requires complete unique IDs,
Pass/Fail verdicts and nonempty critiques, and compares the frozen synthetic
challenge labels. Synthetic challenge agreement is not human TPR/TNR or a
validated judgment of actual model behavior. Preserve provisional decisions and
quoted output separately; missing calibration is Unmeasured.

For each criterion packet, strip its `C1.`, `C2.` or `C4.` prefix from the six
synthetic challenge IDs. Optional actual-output candidates use `response-a` and
`response-b`; those verdicts are checked for schema but excluded from synthetic
agreement counts. Keep their source output identities in the separate packet.

## Check the deterministic evaluators

```sh
python3 tests/creating-portable-skills/fixtures/run-eval-checks.py
lefthook run pre-push --force
```

These tests use disposable copies of synthetic inputs. They verify acceptable
reads, changed/restored/deleted files, symlink replacements and unavailable
evidence. Native-format synthetic captures additionally exercise altered input,
wrong identities, cancelled results, external reads and missing native evidence;
judge checks exercise schema failures and deliberately swapped challenge labels.
Passing these tests exercises the objective checkers, not the creator's behavior
or a subjective judge's human alignment.

## Human calibration remains separate

LLM verdicts and synthetic challenge labels cannot stand in for independent
human labels. Freeze the criterion prompt, source output and reviewer label
separately. Present the exact output and criterion to the reviewer without the
LLM verdict. Use Pass, Fail or Defer; a deferred or missing label is not a Fail.
Separate few-shot training examples, development labels and a held-out test
before tuning. Report per-criterion TPR/TNR and disagreements only when labels
cover both classes; small sets have wide uncertainty. Run the held-out test once,
and do not tune against it. Until that evidence exists, keep subjective results
provisional and human alignment Unmeasured.
