# Sweep Classes

Step 6 of the gate reads this file and works the classes below in the listed
order. Every class carries one verdict from its own enumerated set in the
captured gather. A class that fired names where it fired — the file and line
for a line-scoped finding, the file alone for a file-level one, and the
repository surface for a repository-level finding such as a missing changelog
entry or a review-coverage gap. Record every class in the gather. The brief in SKILL.md step 7 names only
classes that drive the recommendation.

## 1. Underspecified rules in prose and instruction files

A rule says what happens on the yes branch and leaves the no or unclear branch
undefined.

Check by judgment. For every rule the diff writes, ask what happens on the no
branch and on the unclear branch. Look for a named path when the input the rule
reads is absent, and for a named owner when two rules could both apply to the
same case.

Verdicts: clear / underspecified / not applicable.

## 2. Cross-document contradictions and stale cross-references

Two documents state different things about the same behavior, or a name, path,
or filename is referenced that no longer matches what shipped.

Check by judgment, with helper support: `evidence-freshness.sh --check-name
<name> <search-root>` covers plan-named artifacts that no longer match what
shipped, by existence — it reports `consistent` when a file whose basename or
path suffix is that literal name exists under the search root, and `stale
reference found` when none does, so a name carried only in prose reads as
stale. By judgment, compare each document the diff changed against the
documents that describe the same behavior, and resolve every path, filename,
and skill or command name the diff mentions against the working surface.

Verdicts: consistent / contradiction found / stale reference found / not
applicable.

## 3. Branch changelog entry

The branch's own work does not appear in the repository's changelog, in a
repository that keeps one.

Check with `helper: changelog-union.sh`.

Verdicts: present / changed without entry / missing / no changes on surface /
no changelog / covered by repo gate / not run.

## 4. Evidence or test records predating the final edit

A log, run record, or recorded result is older than the last edit of the thing
it describes, so it attests to a version that no longer exists.

Check with `helper: evidence-freshness.sh`. Comparisons use commit ancestry,
never committer timestamps or file modification times: a checkout or copy
rewrites mtimes, and a skewed or rewritten committer clock can date a later
commit earlier. A record is fresh only when every described path's last commit
is contained in the history of the record's last commit; when checking by
judgment, apply the same ancestry rule.

Verdicts: fresh / stale record found / record unverifiable (dirty) / no records
/ covered by repo gate / not run.

## 5. Duplicated source-of-truth literals

A sentinel string, identifier, path, or threshold is copied into a second file
instead of referenced from the one place that owns it.

Check by judgment. Look for literals the diff introduces in more than one file,
for a value restated in prose that also exists in code or configuration, and
for a threshold written into both a check and its documentation.

Verdicts: single-sourced / duplicate found / not applicable.

## 6. Partial-failure cleanup and resource-lifecycle gaps

State is created and then orphaned when a later step throws, or a handle is
opened and never closed.

Check by judgment. Look for a step that writes or creates before a step that
can fail, for an opened file, process, connection, or temporary directory
without a matching close on every exit path, and for a retry that repeats a
create without removing the prior attempt.

Verdicts: handled / gap found / not applicable.

## 7. Exit-code truthfulness

A command computes a failure and exits zero anyway, or never prints what it
found.

Check by judgment. Look for a failure counted or collected and then discarded,
for a pipeline whose exit status comes from the last stage rather than the
failing one, and for a check whose only output is on the pass path.

Verdicts: truthful / untruthful exit found / not applicable.

## 8. Tests asserting a copy instead of the production artifact

A test exercises a fixture that duplicates the thing under test, or the gate a
test exists to cover is monkeypatched away in every test that touches it.

Check by judgment. Look for fixture content that restates production logic or
data, for an import of the production artifact that no assertion reaches, and
for a patch or stub applied to the exact behavior the test names.

Verdicts: exercises production artifact / copy-assertion found / not
applicable.

## 9. Markdown and lint basics not covered by repo hooks

A heading level, list, code fence, or link in the diff is malformed in a way an
automated reviewer will raise.

Check by judgment when no repository hook covers it; report `covered by repo
gate` when step 2 found a hook or task runner that owns markdown or lint. Look
for skipped heading levels, unclosed or unlabeled code fences, and links whose
target does not resolve.

Verdicts: clean / finding / covered by repo gate / not applicable.

## 10. Mechanically checkable invariants that exist only as prose

A document states a rule a script, hook, or test could enforce, and nothing
enforces it.

Check by judgment. For each rule the diff states, ask what would fail if
someone broke it, and look for whether any check in the repository reads the
same input the rule reads.

Verdicts: enforced / prose-only invariant found / not applicable.

## 11. Diff size against automated-reviewer file caps

File counts and known reviewer limits identify potential review-coverage risk.
Read them from step 1's full surface report. When a limit is already available
from repository configuration or supplied evidence, optionally pass
`--cap <reviewer>=<n>`; record its source and read the helper's comparison.
Numeric caps are optional diagnostics. There is no required vendor or plan
research, or new cap configuration, to complete this class.

When no automated reviewer is configured, record `not applicable`. Otherwise
retain the helper's size verdict, including `cap unverified` when no cap was
supplied. With a complete inventory, unknown or exceeded caps alone are
informational: they neither fail the check nor withhold Approve, require a
split, or prove that review ran. Assess actual review coverage from the
required reviews and their receipts in steps 2 and 3. An actual required-review
failure or omission without replacement coverage remains a named unresolved
finding; complete independent required coverage can coexist with an optional
reviewer's exceeded cap.

Read the inventory detail as well as the size verdict. `cap unverified` can
also accompany an unmeasurable committed category, and `exceeds cap` may
compare only a measured subset. Missing or failed git inventory and unresolved
base identity remain step 1 blockers, even when the helper exits zero.

Verdicts: under caps / `exceeds cap for <reviewer>` / cap unverified /
no changes on surface / covered by repo gate / not run / not applicable.

## Helper exit → status word (SSOT)

A helper's verdict and the gate's status words are two layers: the verdict says
what the class found; the status word says whether the check happened. Read both
off the helper's exit code and its `verdict:` line (script headers list the
verdicts; this table maps execution).

| Exit | Meaning | Status word |
| --- | --- | --- |
| 0 | Class carried a verdict from its enumerated set | **verified** with the verdict line as named evidence, or **failed** when the verdict is a finding. Class 11's informational cap verdicts follow its coverage and inventory rules above; they do not verify that a review ran. |
| 2 with absent-input verdict (`no changelog`, `no records`) | Input missing | **unavailable** |
| 2 with `not run` / usage error | Helper could not run as invoked | **not run**. Fall back to the class's model-instruction check and record that judgment as the class verdict. |
| 3 | `--defer` to a repository gate | **skipped**, naming that gate |
| 4 | Helper hard failure | **not run**. Fall back to the class's model-instruction check and record that judgment as the class verdict. |

## When a helper cannot run

A helper that is absent, not executable, or exits without producing its output
does not remove its class from the sweep. Check that class by judgment against
the class description above. Record the status as `not run` and store the
model judgment as the class verdict, so helper verdicts stay distinct from
judgment verdicts.
