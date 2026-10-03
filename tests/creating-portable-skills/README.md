# Creating Portable Skills evaluation

The initial suite defines two bounded tasks:

- [CPS-ACT-001](cases/activation-near-miss.md): a generic grader request should
  not activate the skill creator merely because it mentions a grader.
- [CPS-AUD-001](cases/vendor-guidance-audit.md): compare a supplied small skill
  with synthetic vendor guidance without narrowing its portability or editing
  the supplied files.

These are case definitions, not validated behavioral results. Claude, Codex, and
Grok pilot coverage is not yet measured. The synthetic hook in the fixture does
not describe a real vendor API. Updating and migrating skills are not covered.

## Prepare and capture a run

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow). Agree on the case inputs,
criteria, host, model, execution limits, authentication and budget before model
runs. Keep executor input separate from criteria and answer material. Use native
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

Grade AUD C1, C2 and C4 through independent human review of the corresponding
output and reference criteria. Preserve each decision, quoted output evidence,
and reviewer feedback. No automated subjective judge has been calibrated; do
not substitute keyword matching for whether advice is portable. No exact wording
is required, and unchanged requirements need not be repeated.

Report each host and criterion separately. Exclude incomplete captures from
completed comparisons and leave unavailable usage/cost unknown. This small pilot
can check case clarity and capture reliability; it cannot establish population
success rates, positive activation reliability or portability across unmeasured
hosts. Private traces and review pages are not suite dependencies and must not
be committed here.

## Check the deterministic evaluator

```sh
python3 tests/creating-portable-skills/fixtures/run-eval-checks.py
lefthook run pre-push --force
```

These tests use disposable copies of synthetic inputs. They verify acceptable
reads, changed/restored/deleted files, symlink replacements and unavailable
evidence. Passing them validates the comparator, not the creator's behavior.
