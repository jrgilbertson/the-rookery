# Changelog fragments

Add one fragment per pull request here instead of editing [CHANGELOG.md](../CHANGELOG.md) directly so concurrent branches do not collide.

## Filename

Name each file `<pr-or-slug>.<section>.md`, where `<section>` is a Keep a Changelog heading in lowercase:

- `added` -> `### Added`
- `changed` -> `### Changed`
- `deprecated` -> `### Deprecated`
- `removed` -> `### Removed`
- `fixed` -> `### Fixed`
- `security` -> `### Security`

Examples: `462-changelog-fragments.added.md`, `fix-overlap-guard.fixed.md`.

## Content

Write one or more Markdown bullet items (`- ...`). Keep prose verbatim; do not include a `##` or `###` section heading inside the fragment.

```markdown
- Concise, human-written description of the change, wrapped cleanly across
  lines if needed.
```

## Rolling up

Run [`scripts/changelog-rollup.py`](../scripts/changelog-rollup.py) during release prep (or whenever you want to fold fragments into `CHANGELOG.md`):

```bash
python3 scripts/changelog-rollup.py --check          # validate fragments without editing files
python3 scripts/changelog-rollup.py --dry-run        # preview the updated CHANGELOG.md
python3 scripts/changelog-rollup.py                  # merge into ## [Unreleased] and remove fragments
python3 scripts/changelog-rollup.py --release 0.4.0  # merge into a target release section
```
