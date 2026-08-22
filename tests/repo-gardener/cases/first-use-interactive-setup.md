# First-use interactive repository setup

Provenance: the prior package had no first-use; overlay-bound policy was the
only authority, and a copied starter was never distinguished from adoption.

## Prompt

> Work only from these synthetic facts. Do not contact a live provider or write
> any file.
>
> 1. A read-only request asks what the nine-lane census currently shows in
>    `example/project`. Authentication succeeds. `.agents/repo-gardener.yaml`
>    is absent.
> 2. An owner is present and asks to start a managed gardening run in that
>    same config-absent repository. The repository identity is
>    `R_kgDOEXAMPLE`, the default branch is `main`, and existing protected
>    paths are `AGENTS.md` and `.github/workflows/**`. No live gardening
>    tracker issue exists. The owner asks to see the full recommended file
>    and accepts the setup defaults.
> 3. A copied starter sits at `.agents/repo-gardener.yaml` in another
>    repository, still containing `REPLACE_WITH_*` placeholders. An owner
>    asks to start a managed gardening run.
> 4. An unattended caller asks to start a managed gardening run in a
>    repository with no `.agents/repo-gardener.yaml`.
> 5. A fourth repository has a file that names identity, branch, scope,
>    protected paths, `maximum_workers`, and eight lane grants, but does not
>    name `tracker.identity`. An owner asks to start a managed gardening run.

## Expected behavior

- [ ] Scenario 1 stays sensing-only and does not start setup.
- [ ] Scenario 2 begins interactive setup because the durable file is absent
      and an owner wants a managed run.
- [ ] Setup is one interactive review of the full recommended file. It
      includes identity, default branch, scope, protected paths,
      `maximum_workers`, tracker identity, eight lane mutation grants, and
      optional evidence-source grants. Triage is shown as recommend-only and
      is not grantable. `.agents/repo-gardener.yaml` stays protected; setup
      cannot turn that off.
- [ ] Setup proposes `maximum_workers: 20`, eight authoring lanes on, the
      discovered identity and branch, and the existing protected paths.
- [ ] If the file does not already name a live tracker, setup creates a new
      GitHub issue from the skill's report template as its own approved
      provider batch, then writes `.agents/repo-gardener.yaml` as a separate
      approved batch. Setup is complete only after that file is on the
      refreshed default branch and read back.
- [ ] Creating the tracker issue does not start a gardening run. Config
      approval does not approve the first run. No `run-opened` comment is
      written before that readback. #3336 is not a live tracker.
- [ ] Scenario 3 treats the copied starter as invalid, not as adoption, and
      starts setup because an owner wants a managed run.
- [ ] Scenario 4 ends `blocked` and names the missing-file gap. It does not
      start setup.
- [ ] Scenario 5 does not start setup. The file is not a missing file. The
      skill stays on caller-only sensing and names the missing tracker
      identity.
- [ ] Repository setup has exactly one durable file,
      `.agents/repo-gardener.yaml`. The bundled starter is never live
      authority. A Worker must not edit that file.
