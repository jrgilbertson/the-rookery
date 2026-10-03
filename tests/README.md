# Repository tests

This directory holds deterministic tests of shipped skill helpers and the
repository checks. The legacy behavioral cases, trigger lists, run logs, and
simulator adapters have been retired. Their committed versions remain in Git
history. New behavioral evaluation follows [SKILLS.md](../SKILLS.md#evaluation-workflow).

Run the complete repository gate:

```bash
lefthook run pre-push --force
```

The gate runs package/catalog validation, repository text and link checks,
secret scanning, and the fixture roster in
[scripts/checks/fixtures.sh](../scripts/checks/fixtures.sh). Fixture checks
exercise the shipped fetch, PR assessment, signal scan, issue configuration,
provider and graph, and personal-chief-of-staff source-map schema. The
repository-integrity tests also exercise malformed packages and unsafe paths.

Each fixture runner creates disposable state and requires no model calls.
Retain synthetic fixture inputs that these tests consume. Add a runner to the
explicit roster when adding a deterministic helper test; discovery checks that
the roster is complete. Fixtures in this public repository must be synthetic
and safe to publish. Private session logs and generated review artifacts belong
outside the repository.
