- Minimal `changelog.d/` fragment workflow and stdlib Python rollup script
  (`scripts/changelog-rollup.py`) so concurrent pull requests no longer collide
  on `CHANGELOG.md`. Pull requests add `<pr-or-slug>.<section>.md` fragments
  preserving human-written Keep a Changelog prose verbatim, offline fixture
  checks validate fragments and rollup behavior in `lefthook pre-push`, and
  `WORKFLOWS.md`, `RELEASING.md`, `CHANGELOG.md`, and `repo-captain` now align
  on the fragment workflow.
