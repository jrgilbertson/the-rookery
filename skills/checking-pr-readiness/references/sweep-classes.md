# Sweep Classes

Step 6 of the gate reads this file and works the classes below in the order
they appear, which is observed-frequency order from the pull request forensics
behind this gate. Surface findings in that same order, so the class that most
often drives another automated-review round is read first. Every class carries
one verdict from its own enumerated set, and a class that fired names where it
fired — the file and line for a line-scoped finding, the file alone for a
file-level one, and the repository surface for a repository-level finding such
as a missing changelog entry or an aggregate file-cap excess.

The list comes from forensics across three repositories: branches with green
continuous integration that still burned seven to sixteen automated-review
rounds, with each round's findings sorted into classes. The merge-gate sibling
refreshes it from observed review history as evidence packs accumulate, so a
class that stops appearing loses its place and a class the reviewers keep
raising earns one.

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

The diff touches more files than an automated reviewer will read, so that
reviewer skips the pull request or truncates its review.

Check by running `scripts/surface-report.sh --cap <reviewer>=<n>` with one
`--cap` per automated reviewer configured on the host repository, and read the
verdict line directly; the helper compares the counts itself.

Cap values are repository-specific, never universal: each reviewer's limit
comes from its configuration in the host repository or from the plan the
repository runs it on, so resolve the applicable value at run time — the
reviewer's config file in the repository, or its vendor documentation for the
plan in use. A finding names the affected reviewer and where its cap value came
from. The helper itself reports `cap unverified` when no cap was supplied, and
when the committed category could not be measured, because a cap cannot be
called met against a count that is unknown. Report it by judgment for the same
reason when a configured reviewer's applicable cap cannot be confirmed at run
time.

Verdicts: under caps / `exceeds cap for <reviewer>` / cap unverified /
no changes on surface / covered by repo gate / not run.

## When a helper cannot run

A helper that is absent, not executable, or exits without producing its output
does not remove its class from the sweep. Check that class by judgment against
the class description above, and report it as `not run → judgment` so the
readout shows which verdicts came from the helper and which came from reading.
