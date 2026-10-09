# Sweep Classes

Step 6 of the gate reads this file and works the classes below in the listed
order. Every class carries one verdict from its own enumerated set in the
captured gather. A class that fired names where it fired — the file and line
for a line-scoped finding, the file alone for a file-level one, and the
repository surface for a repository-level finding such as a missing changelog
entry. Record every class in the gather. The brief in SKILL.md step 7 names
only classes that drive the recommendation. When a class cannot be checked,
record `not run` with the reason rather than dropping it.

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

Check by judgment. Compare each document the diff changed against the
documents that describe the same behavior, and resolve every path, filename,
and skill or command name the diff mentions against the working surface. A
name that exists only in prose, with no matching file, is stale.

Verdicts: consistent / contradiction found / stale reference found / not
applicable.

## 3. Branch changelog entry

The branch's own work does not appear in the repository's changelog, in a
repository that keeps one.

Check by judgment against the step 1 surface. When the repository keeps a
changelog and the surface changes shipped content, look for an entry the
branch added that describes this work.

Verdicts: present / missing / no changelog / covered by repo gate / not
applicable.

## 4. Evidence or test records predating the final edit

A log, run record, or recorded result is older than the last edit of the thing
it describes, so it attests to a version that no longer exists.

Check by judgment using commit ancestry, never committer timestamps or file
modification times: a checkout or copy rewrites mtimes, and a skewed or
rewritten committer clock can date a later commit earlier. A record is fresh
only when every described path's last commit is an ancestor of the record's
last commit (`git merge-base --is-ancestor`). A described path with
uncommitted changes makes the record stale.

Verdicts: fresh / stale record found / no records / covered by repo gate.

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
