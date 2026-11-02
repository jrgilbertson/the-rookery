# Repository tests

This directory holds deterministic tests of shipped skill helpers and the
repository checks. Behavioral evaluation follows
[SKILLS.md](../SKILLS.md#evaluation-workflow) through the evals plugin's
`evals-start` routing. The
[Creating Portable Skills checks](creating-portable-skills/README.md) exercise
its shipped signal scanner. Report native host behavior separately from
repository checks.
The [Managing Issues checks](managing-issues/README.md) distinguish deterministic
text and configuration checks from the graph and lifecycle behavioral case
definitions.

Run the complete repository gate:

```bash
lefthook run pre-push --force
```

The gate runs package/catalog validation, repository text and link checks,
secret scanning, and the fixture roster in
[scripts/checks/fixtures.sh](../scripts/checks/fixtures.sh). Fixture checks
exercise the shipped signal scan and issue configuration helper, published
text contracts, and the shipped personal-chief-of-staff source-map sample
against the version 3 shape in
[source-bindings.md](../skills/personal-chief-of-staff/references/source-bindings.md).
The repository-integrity tests also exercise malformed packages and unsafe
paths.

Repository text checks reject concrete local home-directory paths. Generic
placeholders and exact, file-scoped portable setup examples remain allowed;
context-dependent privacy review is still necessary.

Each fixture runner creates disposable state and requires no model calls.
Retain synthetic fixture inputs that these tests consume. Add a runner to the
explicit roster when adding a deterministic helper test; discovery checks that
the roster is complete. Fixtures in this public repository must be synthetic
and safe to publish. Private session logs and generated review artifacts belong
outside the repository.
