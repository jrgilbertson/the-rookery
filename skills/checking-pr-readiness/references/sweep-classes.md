# Sweep Classes

Step 6 of the gate reads this file and works the classes below in the order
they appear, which is observed-frequency order from the pull request forensics
behind this gate. Surface findings in that same order, so the class that most
often drives another automated-review round is read first. Every class carries
one verdict from its own enumerated set, and a class that fired names where it
fired — the file and line for a line-scoped finding, the file alone for a
file-level one, and the repository surface for a repository-level finding such
as a missing changelog entry or an aggregate file-cap excess.

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

Resolve each configured reviewer's identity and authoritative cap lookup at the
exact head. Run `scripts/surface-report.sh --cap <reviewer>=<n>` separately for
each known cap, and read each verdict line directly; the helper compares the
counts itself. Do not combine reviewer caps into one result: a reviewer with no
cap must not hide an exceeded known cap for another reviewer.

First establish whether any automated reviewer is configured from repository
gate, workflow, app, or review-tool configuration. When no automated reviewer
is configured, class 11 is explicitly `not applicable`: run the surface helper
without caps for the full inventory required by step 1, but do not reinterpret
its mechanical `cap unverified` line as a class-11 gap. Absence of a reviewer is
not evidence of an unknown cap. Once a reviewer is configured, only a resolved
identity plus a successful authoritative `no cap` lookup may remain process-
only `cap unverified` evidence; never fabricate a cap to make the class
applicable.

Cap values are repository-specific, never universal: each reviewer's limit
comes from its configuration in the host repository or from the plan the
repository runs it on, so resolve the applicable value at run time — the
reviewer's config file in the repository, or its vendor documentation for the
plan in use. A resolved reviewer identity plus a successful authoritative
`no cap` lookup is the only process-only `cap unverified` evidence; name that
reviewer, source, and lookup outcome in the existing targeted-sweep result
summary. It does not add an unresolved finding or material gap. Transport,
authentication, permission, parsing, incomplete-result, or other lookup/read
failures, unresolved identities, and an unmeasurable surface fail closed as
those actual failures. The helper itself reports `cap unverified`
when no cap was supplied, and when the committed category could not be
measured, because a cap cannot be called met against a count that is unknown.

Verdicts: under caps / `exceeds cap for <reviewer>` / cap unverified /
no changes on surface / covered by repo gate / not run / not applicable.

## Helper exit → status word (SSOT)

A helper's verdict and the gate's status words are two layers: the verdict says
what the class found; the status word says whether the check happened. Read both
off the helper's exit code and its `verdict:` line (script headers list the
verdicts; this table maps execution).

| Exit | Meaning | Status word |
| --- | --- | --- |
| 0 | Class carried a verdict from its enumerated set | **verified** with the verdict line as named evidence, or **failed** when the verdict is a finding |
| 2 with absent-input verdict (`no changelog`, `no records`) | Input missing | **unavailable** |
| 2 with `not run` / usage error | Helper could not run as invoked | **not run** → fall back to the class's model-instruction check |
| 3 | `--defer` to a repository gate | **skipped**, naming that gate |
| 4 | Helper hard failure | **not run** → fall back to model-instruction check |

## When a helper cannot run

A helper that is absent, not executable, or exits without producing its output
does not remove its class from the sweep. Check that class by judgment against
the class description above, and report it as `not run → judgment` so the
readout shows which verdicts came from the helper and which came from reading.
