# Releasing The Rookery

This is the maintainer checklist for a Release Snapshot. `main` remains the
rolling install source; a release records one validated historical state.

## Prepare the candidate

- Use one release branch and identify its exact commit and tree.
- Update public documentation and move the finished changelog entry from
  `Unreleased` to the target version.
- From a clean checkout at the exact candidate commit, run the complete
  Lefthook check group documented in [tests/README.md](tests/README.md).
  Determine any behavioral evaluation the candidate needs through the
  [SKILLS.md evaluation workflow](SKILLS.md#evaluation-workflow), and report
  its actual coverage and unresolved revalidation.
- Audit the public tree, history, hosted GitHub surfaces, licenses, attribution,
  and shipped skill behavior. Resolve every material privacy, licensing,
  security, install, or documentation blocker.

Keep raw scan output and other potentially private evidence outside the
repository. Put only concise, sanitized results and exact candidate identities
in the release pull request.

## Freeze and publish

- Obtain the owner's final documentation and repository review.
- Merge only after required checks pass, then verify the merged tree still
  matches the qualified candidate and freeze that green `main` commit.
- Confirm `main` still points at the frozen commit, then install the catalog
  from `main` through the documented public `npx skills add` path. Confirm
  every catalog skill is listed and every helper under a skill's `scripts/`
  directory is still executable in the installed copy. Run the
  [Install Probe](CONCEPTS.md#install-probe) activation check for each
  supported harness, or record it as Unmeasured for a harness that is not
  available. This is a maintainer step; agents do not install skills locally.
- Read back the public repository protections, security-reporting path, and
  the install result above before creating a release.
- Enable release immutability and read back the enabled state before the target
  tag or GitHub Release exists.
- Create an annotated semantic-version tag at the frozen commit, then publish
  the GitHub Release from the matching changelog entry. For `v0.2.0`, the notes
  must also identify it as the first public OSS Release Snapshot, state that
  ordinary installs follow rolling `main`, explain the pre-`1.0.0` stability
  boundary, and identify `v0.1.0` as a historical private-era snapshot.
- Verify the peeled tag, release target, frozen `main` commit, and published
  release's immutable state all agree.

Visibility changes, ruleset changes, merges, tags, release publication, and
announcements are owner actions. If a published snapshot needs correction,
publish a new semantic version; never move or reuse the old tag.
