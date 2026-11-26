#!/usr/bin/env python3
"""Stage a repo-captain Eval Case run directory, or move a staged run to a later turn.

    stage.py <case> <run-dir>     build a fresh run directory for one case
    stage.py turn <run-dir> <n>   before sending operator turn n

Staging builds the case's git history for real, so the Captain's `git
merge-base` and `git range-diff` run on real commits. It then writes the
world file with the SHAs of the commits it just made, so the gh stand-in and
git agree. Tokens in the fixture's world and captain state are replaced:
`<<sha:ID>>` and `<<short:ID>>` with a commit's full and seven-character
SHA, `<<diff:ID>>` with that commit's diff against the default branch, and
`<<workspace>>` with the Captain's checkout.

The run directory gets:
  bin/          the gh and orca stand-ins
  remote/       a bare repository that plays GitHub's copy; it refuses pushes
                to branches that already exist, since the world file, not
                git, says where a pull request's head is
  workspace/    the Captain's checkout, cloned from remote/
  world.json    the staged world both stand-ins read
  gh-state/ orca-state/   the stand-ins' private state directories
  xdg-state/    XDG_STATE_HOME for the run, holding the case's captain state

`stage.py turn` writes the turn number for both stand-ins and moves the
remote's branch and refs/pull/<number>/head refs to the heads that turn lists.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAND_INS = {"gh": HERE.parents[1] / "reviewing-prs/stand-ins/gh", "orca": HERE.parent / "stand-ins/orca"}
EMPTY = "0" * 40
HOOK = """#!/bin/sh
while read old new ref; do
  if [ "$old" != "%s" ]; then
    echo "stand-in remote: $ref already exists. A pull request's head comes from the eval's world file, so this remote accepts only new branches." >&2
    exit 1
  fi
done
""" % EMPTY


def fail(message: str) -> None:
    print(f"stage: {message}", file=sys.stderr)
    raise SystemExit(1)


def git(*args: str, cwd: Path | None = None, date: str | None = None) -> str:
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Fixture Author",
                       GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_NAME="Fixture Author",
                       GIT_COMMITTER_EMAIL="fixture@example.invalid")
    if date:
        environment.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    result = subprocess.run(["git", *args], cwd=cwd, env=environment, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def outside_work_trees(path: Path) -> None:
    if any((parent / ".git").exists() for parent in (path, *path.parents)):
        fail(f"{path} is inside a git work tree; stage runs outside every repository")


def build_history(spec: dict, build: Path) -> dict[str, str]:
    git("init", "-q", "-b", "fixture-build", cwd=build)
    shas: dict[str, str] = {}
    for position, commit in enumerate(spec["commits"]):
        if position and not commit.get("parent"):
            fail(f"commit {commit['id']}: every commit after the first names its parent")
        if commit.get("parent"):
            git("checkout", "-q", "--detach", shas[commit["parent"]], cwd=build)
        for path, content in commit.get("files", {}).items():
            target = (build / path).resolve()
            if path.startswith("/") or ".." in Path(path).parts or build.resolve() not in target.parents:
                fail(f"commit {commit['id']}: unsafe path {path!r}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for path in commit.get("delete", []):
            git("rm", "-q", "--", path, cwd=build)
        git("add", "-A", cwd=build)
        git("commit", "-q", "--allow-empty", "--no-verify", "-m", commit["message"], cwd=build, date=f"2026-11-{commit.get('day', 18)}T{9 + position // 60:02d}:{position % 60:02d}:00Z")
        shas[commit["id"]] = git("rev-parse", "HEAD", cwd=build).strip()
        git("update-ref", f"refs/fixture/{commit['id']}", shas[commit["id"]], cwd=build)
    return shas


def replace(value: object, tokens: dict[str, str]) -> object:
    if isinstance(value, str):
        for token, text in tokens.items():
            value = value.replace(token, text)
        return value
    if isinstance(value, list):
        return [replace(item, tokens) for item in value]
    if isinstance(value, dict):
        return {key: replace(item, tokens) for key, item in value.items()}
    return value


def stage(case: str, run: Path) -> None:
    fixture = HERE / case
    if not (fixture / "world.json").is_file():
        fail(f"no fixture {case!r}")
    if run.exists() and any(run.iterdir()):
        fail(f"{run} is not empty")
    run.mkdir(parents=True, exist_ok=True)
    run = run.resolve()
    outside_work_trees(run)
    world = json.loads((fixture / "world.json").read_text(encoding="utf-8"))
    spec = world.pop("git")
    slug, name = spec["repo"], spec["repo"].split("/")[1]
    default = world["repos"][slug]["defaultBranch"]
    for folder in ("bin", "remote", "gh-state", "orca-state", "xdg-state", "build"):
        (run / folder).mkdir()
    for command, source in STAND_INS.items():
        shutil.copy2(source, run / "bin" / command)
        (run / "bin" / command).chmod(0o755)

    build, remote = run / "build", run / "remote" / f"{name}.git"
    shas = build_history(spec, build)
    git("init", "-q", "--bare", "-b", default, str(remote))
    git("push", "-q", str(remote), "refs/fixture/*:refs/fixture/*", cwd=build)
    for branch, commit in spec["branches"].items():
        git("update-ref", f"refs/heads/{branch}", shas[commit], cwd=remote)
    for commit in shas:
        git("update-ref", "-d", f"refs/fixture/{commit}", cwd=remote)
    # GitHub serves any commit it has by SHA, including a pull request's earlier heads.
    git("config", "uploadpack.allowAnySHA1InWant", "true", cwd=remote)
    hook = remote / "hooks" / "pre-receive"
    hook.write_text(HOOK, encoding="utf-8")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    main = shas[spec["branches"][default]]
    tokens = {"<<workspace>>": str(run / "workspace")}
    for commit, sha in shas.items():
        tokens[f"<<sha:{commit}>>"] = sha
        tokens[f"<<short:{commit}>>"] = sha[:7]
        tokens[f"<<diff:{commit}>>"] = git("diff", "--no-color", "--no-ext-diff", f"{main}...{sha}", cwd=build)
    world = replace(world, tokens)
    contents = {}
    for path in git("ls-tree", "-r", "--name-only", main, cwd=build).splitlines():
        contents[path] = git("show", f"{main}:{path}", cwd=build)
    world["repos"][slug]["contents"] = {default: contents}
    world["repos"][slug]["gitRemote"] = str(remote)
    # GitHub keeps refs/pull/<number>/head for every pull request, forks included.
    for number, pull in world["repos"][slug]["pulls"].items():
        if pull["headRefOid"] in shas.values():
            git("update-ref", f"refs/pull/{number}/head", pull["headRefOid"], cwd=remote)
    (run / "world.json").write_text(json.dumps(world, indent=2) + "\n", encoding="utf-8")

    git("clone", "-q", str(remote), str(run / "workspace"))
    git("config", "user.name", "Dana Acme", cwd=run / "workspace")
    git("config", "user.email", "dana-acme@example.invalid", cwd=run / "workspace")
    seed = fixture / "captain-state"
    if seed.is_dir():
        target = run / "xdg-state" / f"{name}-captain"
        for source in sorted(path for path in seed.rglob("*") if path.is_file()):
            copy = target / source.relative_to(seed)
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_text(replace(source.read_text(encoding="utf-8"), tokens), encoding="utf-8")
    shutil.rmtree(build)
    print(f"stage: {case} staged in {run}")


def move_to_turn(run: Path, turn: int) -> None:
    world = json.loads((run / "world.json").read_text(encoding="utf-8"))
    for slug, repo in world["repos"].items():
        remote = repo.get("gitRemote")
        for step in range(2, turn + 1):
            for change in world.get("turns", {}).get(str(step), []):
                if remote and change["pull"].startswith(f"{slug}#") and "headRefOid" in change.get("set", {}):
                    number = change["pull"].split("#")[1]
                    branch = change["set"].get("headRefName", repo["pulls"][number]["headRefName"])
                    git("update-ref", f"refs/heads/{branch}", change["set"]["headRefOid"], cwd=Path(remote))
                    git("update-ref", f"refs/pull/{number}/head", change["set"]["headRefOid"], cwd=Path(remote))
    for folder in ("gh-state", "orca-state"):
        (run / folder / "turn").write_text(f"{turn}\n", encoding="utf-8")
    print(f"stage: {run} is at turn {turn}")


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 3 and args[0] == "turn" and args[2].isdigit() and int(args[2]) >= 2:
        move_to_turn(Path(args[1]).resolve(), int(args[2]))
    elif len(args) == 2 and args[0] != "turn":
        stage(args[0], Path(args[1]))
    else:
        fail("usage: stage.py <case> <run-dir> | stage.py turn <run-dir> <n>")


if __name__ == "__main__":
    main()
