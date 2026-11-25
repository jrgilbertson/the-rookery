# Repository tests

This directory holds deterministic tests of shipped skill helpers and the
repository checks. The
[Managing Issues checks](managing-issues/README.md) run its configuration
validator. Report native host behavior separately from repository checks.

Run the complete repository gate:

```bash
lefthook run pre-push --force
```

The gate runs package/catalog validation, repository text and link checks,
secret scanning, and the fixture roster in
[scripts/checks/fixtures.sh](../scripts/checks/fixtures.sh). Fixture checks
exercise the shipped issue configuration helper, the shipped daily-learning
configuration sample against
[config-and-sources.md](../skills/daily-learning/references/config-and-sources.md),
and the shipped personal-chief-of-staff source-map sample
against the version 3 shape in
[source-bindings.md](../skills/personal-chief-of-staff/references/source-bindings.md).
The [Reviewing PRs checks](reviewing-prs/README.md) exercise the synthetic
GitHub stand-in and fixtures that its Skill Eval runs against.
The repository-integrity tests also exercise malformed packages and unsafe
paths. The routing checks run the shipped
[routing evidence script](../scripts/routing/evidence.py) against synthetic
benchmark data.

Repository text checks also require the "Rank by leverage" section in
`GLOBAL-AGENTS.md` and in the `managing-issues` skill to match the one in
[PRIORITIZATION.md](../PRIORITIZATION.md).

Repository text checks reject concrete local home-directory paths. Generic
placeholders and exact, file-scoped portable setup examples remain allowed;
context-dependent privacy review is still necessary.

Tests never call a model; evals always do. Skill Evals live in
`evals/<skill>/` at the repository root, not here, and the gate never runs
them. See [Skill Evals](../SKILLS.md#skill-evals) for when they run and what
each Eval Record holds.

Each fixture runner creates disposable state and requires no model calls.
Retain synthetic fixture inputs that these tests consume. Add a runner to the
explicit roster when adding a deterministic helper test; discovery checks that
the roster is complete. Fixtures in this public repository must be synthetic
and safe to publish. Keep real-use traces, private session logs, and generated
review pages outside the repository.
