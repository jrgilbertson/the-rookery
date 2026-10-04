# Creating Portable Skills evaluation

The initial suite defines two bounded tasks:

- [CPS-ACT-001](cases/activation-near-miss.md): a generic grader request should
  not activate the skill creator merely because it mentions a grader.
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
transport newline. ACT is `Build a grader and rubric for judging model outputs.`
AUD is `Use creating-portable-skills for a read-only comparison of this skill and
the supplied vendor guide. Which guidance should we adopt while keeping the skill
usable across harnesses and models?` Supply AUD's two fixture files at their named
relative paths; do not append fixture hints or isolation prose to the paragraph.
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
success rates, positive activation reliability or portability across unmeasured
hosts. Private traces and review pages are not suite dependencies and must not
be committed here.

## Check existing native captures

The stdlib capture checker reads Codex `native-requests.jsonl` and
`native-events.jsonl`, or Grok `stdout.ndjson` plus native `chat_history.jsonl`
from the matching session-ID directory. Grok query identity comes from native
`prompt_index` metadata; unclassified user context stays Unmeasured.
It checks actual text against canonical case input, successful native completion,
matching session/turn identity, duplicate or retyped native item identities,
outstanding work and successful reads outside the
approved read roots. Codex also requires a matching post-completion thread read.
Report flags, saved prompt hashes and process exit codes do not replace native
evidence. Supply only executor-approved workspace and skill roots, never a parent
containing criteria, coordination files or other runs. A successful grading or
coordination read invalidates the capture. An opaque successful tool or missing
native evidence is conservatively Unmeasured. Codex command reads are checked
even when the aggregate command fails: a read may succeed before a later error.
Codex `commandActions` are best-effort, lossy display metadata, not an exhaustive
filesystem read audit. Unclassified actions and missing paths remain Unmeasured;
a missing path is not evidence of an observed outside-root read. A valid completed
native `sleep` display item is non-reading, but still requires matching identity
and no outstanding work. These checks do not parse opaque commands or scripts to
infer safe reads. The CLI exits 1 for inadmissible or
incomplete evidence; it does not assign a behavioral Fail.

```sh
python3 tests/creating-portable-skills/validate_capture.py codex aud "$capture_dir" --allowed-root "$eval_workspace"
```

Set all paths outside the public worktree. A capture-check Pass covers these
objective observations only. Verify frozen skill identity/discovery and native
filesystem confinement separately before admitting a run. Keep C3's file
observation separate even when a run is excluded from behavioral comparisons.

Host setup remains a prerequisite.
The private launcher must refuse model execution until native confinement is
verified; permission mode and isolation prose cannot replace it. Codex's inspected
captures contain extra input text and therefore do not measure these exact cases.
These setup findings are not repaired-host claims or grounds for model retries.
A resolved Codex read-only/never policy alone does not prove read confinement.
The inspected native thread also inherited user-level instructions. Filesystem
read confinement and acceptable inherited instruction exposure remain separate,
unverified admission prerequisites. The checker retains Grok support only for
inspecting historical captures; no new Grok execution or sandbox repair is planned.

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
Passing these tests validates the objective checkers, not the creator's behavior
or a subjective judge's human alignment.
