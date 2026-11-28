#!/usr/bin/env python3
"""Exercise failure paths in the dependency-free repository checker."""

from __future__ import annotations

import gzip
import io
import json
import os
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/checks/repository.py"
LINT = ROOT / "scripts/checks/lint.sh"
FIXTURES = ROOT / "scripts/checks/fixtures.sh"
SYNC = ROOT / "scripts/sync-global-agents.sh"
INSTALLER = ROOT / "scripts/checks/install-verification-tools.sh"

FIXTURE_RUNNERS = (
    "tests/changelog/fixtures/run-changelog-checks.py",
    "tests/evals/fixtures/run-eval-checks.py",
    "tests/managing-issues/fixtures/run-config-checks.py",
    "tests/personal-chief-of-staff/fixtures/run-sample-checks.py",
    "tests/repository-integrity/check_catalog.py",
    "tests/repository-integrity/check_repository.py",
    "tests/reviewing-prs/fixtures/run-template-checks.py",
    "tests/routing/fixtures/run-routing-checks.py",
)


def run_checker(repository: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/checks/repository.py"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_home_paths(repository: Path) -> None:
    document = repository / "home-path.txt"
    # Construct synthetic paths so the detector's own test source needs no bypass.
    macos = "/Users/" + "fixture-account/project"
    linux = "/home/" + "fixture-account/project"
    windows = "C:" + "\\Users\\fixture-account\\project"
    home_relative = "~" + "/fixture-project"
    approved = "~" + "/.codex/AGENTS.md"
    document.write_text(
        "/usr/local/bin\n/opt/homebrew/bin\nrelative/home/project\n"
        "https://example.invalid/home/project\n"
        "http://localhost/home/project\nhttps://localhost/Users/project\n"
        "/Users/" + "<user>/project\n/home/" + "{user}/project\n"
        "/Users/" + "$USER/project\n/home/" + "${USER}/project\n"
        "C:" + "\\Users\\%USERNAME%\\project\n"
        "C:" + "\\Users\\<user>\\project\n"
        "c:" + "/uSeRs/<user>/project\n"
        "file:///Users/" + "<user>/project\n"
        "file:///home/" + "${USER}/project\n"
        "~" + "/<project>\n~" + "/$PROJECT\n",
        encoding="utf-8",
    )
    generic = run_checker(repository)
    require(generic.returncode == 0, f"generic path examples failed: {generic.stderr}")

    for contents in (
        macos, linux, windows, home_relative,
        "/Users/" + "example", "/home/" + "example",
        "c:" + "\\uSeRs\\fixture-account\\project",
        "C:" + "\\\\Users\\\\fixture-account\\\\project",
        "file://" + macos, "file://" + linux,
        "file://localhost" + macos, "file://localhost" + linux,
        "C:" + "/users/fixture-account/project",
        "c:" + "/uSeRs/fixture-account/project",
        approved,
    ):
        document.write_text("ordinary text\n" + contents + "\n", encoding="utf-8")
        result = run_checker(repository)
        require(
            result.returncode == 1
            and "home-path.txt:2: local home-directory path is not allowed" in result.stderr,
            f"repository checker accepted local home path {contents!r}: {result.stderr}",
        )
    document.unlink()

    claude_path = "~" + "/.claude/CLAUDE.md"
    workflow = repository / "WORKFLOWS.md"
    workflow.write_text(f"Shared instructions: `{approved}`.\n", encoding="utf-8")
    reviewed = run_checker(repository)
    require(reviewed.returncode == 0, f"reviewed setup example failed: {reviewed.stderr}")
    for unreviewed in (home_relative, approved + ".private", claude_path):
        workflow.write_text(f"`{approved}` and `{unreviewed}`\n", encoding="utf-8")
        result = run_checker(repository)
        require(
            result.returncode == 1
            and "WORKFLOWS.md:1: local home-directory path is not allowed" in result.stderr,
            f"reviewed example exempted another path: {result.stderr}",
        )
    workflow.unlink()

    machine_setup = repository / "MACHINE-SETUP.md"
    codex_config_path = "~" + "/.codex/config.toml"
    claude_marketplace_path = "~" + "/.claude/plugins/marketplaces/compound-engineering-plugin"
    antigravity_path = "~" + "/.gemini/config/AGENTS.md"
    antigravity_plugins_dir = "~" + "/.gemini/config/plugins"
    antigravity_ce_path = "~" + "/.gemini/config/plugins/compound-engineering"
    grok_path = "~" + "/.grok/AGENTS.md"
    cursor_path = "~" + "/.cursor/rules/global-agents.mdc"
    machine_setup_paths = (
        approved,
        codex_config_path,
        claude_path,
        claude_marketplace_path,
        antigravity_path,
        antigravity_plugins_dir,
        antigravity_ce_path,
        grok_path,
        cursor_path,
    )
    machine_setup.write_text(
        "\n".join(f"- `{path}`" for path in machine_setup_paths)
        + f"\n- `@{approved}`\n",
        encoding="utf-8",
    )
    reviewed_setup = run_checker(repository)
    require(
        reviewed_setup.returncode == 0,
        f"reviewed MACHINE-SETUP.md examples failed: {reviewed_setup.stderr}",
    )
    for unreviewed in (
        home_relative,
        f"@{home_relative}",
        approved + ".private",
        "~" + "/.codex/other.toml",
        "~" + "/.cursor/rules/other.mdc",
        "~" + "/.gemini/config/plugins/other-plugin",
        "~" + "/.claude/plugins/marketplaces/other-plugin",
    ):
        machine_setup.write_text(f"`{approved}` and `{unreviewed}`\n", encoding="utf-8")
        rejected_setup = run_checker(repository)
        require(
            rejected_setup.returncode == 1
            and "MACHINE-SETUP.md:1: local home-directory path is not allowed" in rejected_setup.stderr,
            f"MACHINE-SETUP.md allowlist exempted {unreviewed!r}: {rejected_setup.stderr}",
        )
    machine_setup.unlink()

    outside = repository / "outside-setup.md"
    for scoped_path in (
        codex_config_path,
        claude_marketplace_path,
        antigravity_path,
        antigravity_plugins_dir,
        antigravity_ce_path,
        grok_path,
        cursor_path,
    ):
        outside.write_text(f"Path: `{scoped_path}`\n", encoding="utf-8")
        rejected_outside = run_checker(repository)
        require(
            rejected_outside.returncode == 1
            and "outside-setup.md:1: local home-directory path is not allowed" in rejected_outside.stderr,
            f"MACHINE-SETUP.md path was accepted outside its file ({scoped_path!r}): {rejected_outside.stderr}",
        )
    outside.unlink()

    test_source = repository / "tests/repository-integrity/check_repository.py"
    test_source.parent.mkdir(parents=True)
    test_source.write_text(f'path = "{macos}"\n', encoding="utf-8")
    result = run_checker(repository)
    require(
        result.returncode == 1
        and "tests/repository-integrity/check_repository.py:1: local home-directory path is not allowed"
        in result.stderr,
        f"detector test source was exempted from home-path checking: {result.stderr}",
    )
    test_source.unlink()


def check_link_scanning(repository: Path) -> None:
    document = repository / "syntax.markdown"
    document.write_text(
        '![image](target.md)\n[outer[inner](target.md)\n[](target.md)\n'
        '[empty]()\n[multiline\nlabel](target.md)\n'
        '[titled](<target.md> "title")\n[root](/target.md#anchor)\n'
        '[encoded](%74arget.md?query#anchor)\n'
        '[reference]: target.md\n', encoding="utf-8",
    )
    valid = run_checker(repository)
    require(valid.returncode == 0, f"link syntax changed: {valid.stderr}")
    document.write_text("[empty]()\n![outer[inner](missing.md)\n", encoding="utf-8")
    broken = run_checker(repository)
    require(broken.returncode == 1 and "syntax.markdown:2: broken relative link: missing.md" in broken.stderr,
            f"link offset or nested-label behavior changed: {broken.stderr}")
    document.unlink()

    malformed = repository / "malformed.md"
    for text in ("[" * 500_000, "[x](" * 125_000):
        malformed.write_text(text + "\n", encoding="utf-8")
        try:
            result = run_checker(repository)
        except subprocess.TimeoutExpired as exc:
            raise AssertionError("malformed Markdown link scanning exceeded 10 seconds") from exc
        require(result.returncode == 0, f"malformed Markdown failed: {result.stderr}")
    malformed.write_text("[" * 500_000 + "\n[valid](target.md)\n", encoding="utf-8")
    require(run_checker(repository).returncode == 0, "malformed prefix hid a valid link")
    malformed.unlink()


def check_rule_copies(repository: Path) -> None:
    heading = "## Rank by leverage"
    rule = f"{heading}\n\nOrder work by leverage, highest first.\n\n- Impact: 1 to 3.\n"
    source = repository / "PRIORITIZATION.md"
    global_copy = repository / "GLOBAL-AGENTS.md"
    skill_copy = repository / "skills/managing-issues/references/prioritization.md"
    skill_copy.parent.mkdir(parents=True)

    def write(source_rule: str = rule, global_rule: str = rule, skill_rule: str | None = rule) -> None:
        source.write_text(f"# How I prioritize\n\nWhy.\n\n## Breaking ties\n\nTies.\n\n{source_rule}", encoding="utf-8")
        global_copy.write_text(f"# Guidance\n\n## Work clearly\n\nBe clear.\n\n{global_rule}\n## Write plainly\n\nPlainly.\n", encoding="utf-8")
        if skill_rule is None:
            skill_copy.unlink(missing_ok=True)
        else:
            skill_copy.write_text(f"# Prioritization\n\nMaintainers: a copy.\n\n{skill_rule}\n## Derived values\n\n| a | b |\n|---|---|\n| 1 | 1 |\n", encoding="utf-8")

    write()
    clean = run_checker(repository)
    require(clean.returncode == 0, f"matching rule copies failed: {clean.stderr}")
    changed = rule.replace("highest first", "lowest first")
    for arguments, diagnostic in (
        ({"global_rule": changed}, "GLOBAL-AGENTS.md: '## Rank by leverage' section differs"),
        ({"skill_rule": changed},
         "skills/managing-issues/references/prioritization.md: '## Rank by leverage' section differs"),
        ({"source_rule": rule.replace(heading, "## Rank by value")},
         "PRIORITIZATION.md: expected exactly one '## Rank by leverage' section"),
        ({"skill_rule": None}, "skills/managing-issues/references/prioritization.md: missing"),
    ):
        write(**arguments)
        result = run_checker(repository)
        require(result.returncode == 1 and diagnostic in result.stderr,
                f"rule copy check did not report {diagnostic!r}: {result.stderr}")
    shutil.rmtree(repository / "skills")
    source.unlink()
    global_copy.unlink()
    require(run_checker(repository).returncode == 0, "repository without the rule failed")


def check_contract_copies(repository: Path) -> None:
    contract = "# Review contract\n\nA verdict names the reviewed head.\n"
    first = repository / "skills/reviewing-prs/references/review-contract.md"
    second = repository / "skills/repo-captain/references/review-contract.md"
    for path in (first, second):
        path.parent.mkdir(parents=True)

    def write(first_text: str | None = contract, second_text: str | None = contract) -> None:
        for path, text in ((first, first_text), (second, second_text)):
            if text is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(text, encoding="utf-8")

    write()
    clean = run_checker(repository)
    require(clean.returncode == 0, f"matching contract copies failed: {clean.stderr}")
    for arguments, diagnostic in (
        ({"second_text": contract.replace("reviewed", "current")},
         "skills/repo-captain/references/review-contract.md: differs from "
         "skills/reviewing-prs/references/review-contract.md"),
        ({"second_text": contract + "\n"},
         "skills/repo-captain/references/review-contract.md: differs from "
         "skills/reviewing-prs/references/review-contract.md"),
        ({"second_text": None}, "skills/repo-captain/references/review-contract.md: missing"),
        ({"first_text": None}, "skills/reviewing-prs/references/review-contract.md: missing"),
    ):
        write(**arguments)
        result = run_checker(repository)
        require(result.returncode == 1 and diagnostic in result.stderr,
                f"contract copy check did not report {diagnostic!r}: {result.stderr}")
    shutil.rmtree(repository / "skills")
    require(run_checker(repository).returncode == 0, "repository without the contract failed")


def check_contract_factor_lines(repository: Path) -> None:
    factor = "- Impact, how much better it makes things: 1 to 3."
    section = f"## Rank by leverage\n\nOrder work by leverage.\n\n{factor}\n"
    source = repository / "PRIORITIZATION.md"
    global_copy = repository / "GLOBAL-AGENTS.md"
    skill_copy = repository / "skills/managing-issues/references/prioritization.md"
    contracts = [repository / "skills/reviewing-prs/references/review-contract.md",
                 repository / "skills/repo-captain/references/review-contract.md"]
    for path in (skill_copy, *contracts):
        path.parent.mkdir(parents=True)
    for path in (source, global_copy, skill_copy):
        path.write_text(f"# Rule\n\n{section}", encoding="utf-8")

    def write(line: str) -> None:
        for path in contracts:
            path.write_text(f"# Review contract\n\n## Scores\n\n{line}\n", encoding="utf-8")

    write(factor)
    clean = run_checker(repository)
    require(clean.returncode == 0, f"contract with the rule's factor lines failed: {clean.stderr}")
    write(factor.replace("better", "worse"))
    result = run_checker(repository)
    diagnostic = ("skills/reviewing-prs/references/review-contract.md: its factor lines differ from the "
                  "'## Rank by leverage' section of PRIORITIZATION.md")
    require(result.returncode == 1 and diagnostic in result.stderr,
            f"contract factor check did not report {diagnostic!r}: {result.stderr}")
    shutil.rmtree(repository / "skills")
    source.unlink()
    global_copy.unlink()


def check_yaml_arguments(repository: Path, temporary_root: Path) -> None:
    # Only workflow discovery is unrelated to this disposable YAML fixture.
    tools = temporary_root / "lint-tools"
    tools.mkdir()
    actionlint = tools / "actionlint"
    actionlint.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    actionlint.chmod(0o755)
    environment = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ["PATH"])
    ruby_fixture = repository / "ordinary.rb"
    ruby_fixture.write_text("# Syntax fixture\n", encoding="utf-8")
    marker = repository / "yaml-executed"
    payload = repository / "-eFile.write('yaml-executed','ran');#.yaml"
    payload.write_text("key: value\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", payload.name], cwd=repository, check=True)

    def lint() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "scripts/checks/lint.sh"], cwd=repository,
            env=environment, capture_output=True, text=True, check=False,
        )

    valid = lint()
    require(not marker.exists(), "lint executed a YAML filename as Ruby source")
    require(valid.returncode == 0, f"valid leading-dash YAML failed: {valid.stderr}")
    payload.write_text("key: [\n", encoding="utf-8")
    invalid = lint()
    require(invalid.returncode != 0, "invalid leading-dash YAML was not parsed")
    subprocess.run(["git", "rm", "--cached", "--force", "--", payload.name],
                   cwd=repository, check=True, capture_output=True)
    payload.unlink()
    ordinary = repository / "ordinary.yaml"
    ordinary.write_text("key: value\n", encoding="utf-8")
    require(lint().returncode == 0, "ordinary YAML failed")
    ordinary.unlink()
    ruby_fixture.unlink()


def check_root_symlinks(repository: Path, temporary_root: Path) -> None:
    tools = temporary_root / "symlink-lint-tools"
    tools.mkdir()
    actionlint = tools / "actionlint"
    actionlint.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    actionlint.chmod(0o755)
    environment = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ["PATH"])

    def lint() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "scripts/checks/lint.sh"],
            cwd=repository,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def require_rejected(expected_path: str, description: str) -> None:
        for label, result in (("repository", run_checker(repository)), ("lint", lint())):
            require(
                result.returncode != 0
                and expected_path in result.stderr
                and "symbolic link is not allowed" in result.stderr,
                f"{label} check accepted {description}: {result.stderr}",
            )

    glossary = repository / "GLOSSARY.md"
    concepts = repository / "CONCEPTS.md"
    outside = temporary_root / "outside-glossary.md"
    outside.write_text("# Outside\n", encoding="utf-8")

    # Allowed root compatibility symlink pointing to a regular GLOSSARY.md.
    glossary.write_text("# Glossary\n", encoding="utf-8")
    concepts.symlink_to("GLOSSARY.md")
    allowed = run_checker(repository)
    require(allowed.returncode == 0, f"allowed root symlink failed repository check: {allowed.stderr}")
    allowed_lint = lint()
    require(allowed_lint.returncode == 0, f"allowed root symlink failed lint check: {allowed_lint.stderr}")

    # GLOSSARY.md itself is still checked as a regular file, once (not duplicated through CONCEPTS.md).
    glossary.write_text("# Glossary \n", encoding="utf-8")
    target_defect = run_checker(repository)
    require(
        target_defect.returncode == 1
        and "GLOSSARY.md:1: trailing whitespace" in target_defect.stderr
        and "CONCEPTS.md:" not in target_defect.stderr,
        f"GLOSSARY.md defect check via symlink behaved unexpectedly: {target_defect.stderr}",
    )
    glossary.write_text("# Glossary\n", encoding="utf-8")

    # Dangling CONCEPTS.md -> GLOSSARY.md must fail.
    glossary.unlink()
    require_rejected("CONCEPTS.md", "dangling allowed symlink")

    # CONCEPTS.md -> GLOSSARY.md when GLOSSARY.md is a directory must fail.
    glossary.mkdir()
    require_rejected("CONCEPTS.md", "directory target for allowed symlink")
    glossary.rmdir()

    # Chained symlink (CONCEPTS.md -> GLOSSARY.md -> outside or target.md) must fail on CONCEPTS.md itself.
    for chain_target in (outside, repository / "target.md"):
        glossary.symlink_to(chain_target)
        require_rejected("CONCEPTS.md", f"chained symlink target {chain_target!r}")
        glossary.unlink()

    glossary.write_text("# Glossary\n", encoding="utf-8")

    # Wrong targets for CONCEPTS.md (wrong file, escaping repo, absolute path, non-canonical path).
    for bad_target in (
        "target.md",
        "../outside-glossary.md",
        str(glossary.resolve()),
        "./GLOSSARY.md",
    ):
        concepts.unlink()
        concepts.symlink_to(bad_target)
        require_rejected("CONCEPTS.md", f"CONCEPTS.md -> {bad_target!r}")
    concepts.unlink()

    # Non-allowlisted root symlink pointing to GLOSSARY.md must fail.
    alias = repository / "ALIAS.md"
    alias.symlink_to("GLOSSARY.md")
    require_rejected("ALIAS.md", "non-allowlisted root symlink")
    alias.unlink()

    # Nested CONCEPTS.md symlink (including inside skills/) must fail.
    skill_dir = repository / "skills/example-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "GLOSSARY.md").write_text("# Nested\n", encoding="utf-8")
    (skill_dir / "CONCEPTS.md").symlink_to("GLOSSARY.md")
    require_rejected("skills/example-skill/CONCEPTS.md", "nested skills/ CONCEPTS.md symlink")
    shutil.rmtree(repository / "skills")

    docs_dir = repository / "docs"
    docs_dir.mkdir(exist_ok=True)
    nested_docs = docs_dir / "CONCEPTS.md"
    nested_docs.symlink_to("../GLOSSARY.md")
    require_rejected("docs/CONCEPTS.md", "nested docs/ CONCEPTS.md symlink")
    nested_docs.unlink()

    # Symlinked ancestor directory must fail.
    real_dir = repository / "real-dir"
    real_dir.mkdir()
    (real_dir / "note.md").write_text("# Note\n", encoding="utf-8")
    linked_dir = repository / "linked-dir"
    linked_dir.symlink_to(real_dir, target_is_directory=True)
    require_rejected("linked-dir", "symlinked ancestor directory")
    linked_dir.unlink()
    shutil.rmtree(real_dir)

    glossary.unlink()


def check_guidance_copy(temporary_root: Path) -> None:
    repository = temporary_root / "guidance-repository"
    script = repository / "scripts/sync-global-agents.sh"
    script.parent.mkdir(parents=True)
    shutil.copy2(SYNC, script)
    subprocess.run(["git", "init", "-q", repository], check=True)

    def sync(*arguments, env=None):
        return subprocess.run(["bash", "scripts/sync-global-agents.sh", *arguments],
                              cwd=repository, env=env, capture_output=True, text=True, timeout=10)

    require(sync("--check").returncode == 0, "unconfigured freshness check failed")
    source = temporary_root / "guidance-source.md"
    source.write_text("# Synthetic guidance\n", encoding="utf-8")
    subprocess.run(["git", "config", "rookery.globalAgentsSource", str(source)],
                   cwd=repository, check=True)
    outside = temporary_root / "guidance-outside.md"
    outside.write_text("outside sentinel\n", encoding="utf-8")
    destination = repository / "GLOBAL-AGENTS.md"
    destination.symlink_to(outside)
    copied = sync()
    require(outside.read_text() == "outside sentinel\n", "guidance copy overwrote a symlink target")
    require(copied.returncode == 0 and not destination.is_symlink(),
            f"guidance copy did not replace symlink entry: {copied.stderr}")
    for target in (temporary_root / "missing-guidance.md", temporary_root):
        destination.unlink()
        destination.symlink_to(target)
        require(sync().returncode == 0 and not destination.is_symlink(),
                "guidance copy did not replace dangling or directory symlink")
    require(not list(temporary_root.glob(".GLOBAL-AGENTS.*")), "copy wrote into outside directory")
    destination.unlink()
    destination.mkdir()
    require(sync().returncode != 0 and not list(destination.iterdir()),
            "guidance copy wrote into a destination directory")
    destination.rmdir()

    marker = repository / "module-executed"
    (repository / "tempfile.py").write_text(
        "from pathlib import Path\nPath('module-executed').touch()\nraise RuntimeError('planted module')\n",
        encoding="utf-8",
    )
    require(sync().returncode == 0 and not marker.exists(), "guidance copy imported checkout code")
    require(destination.read_bytes() == source.read_bytes(), "guidance bytes changed")
    require(destination.stat().st_mode & 0o777 == 0o644, "guidance mode is not 0644")
    destination.write_text("old guidance\n", encoding="utf-8")
    require(sync().returncode == 0 and destination.read_bytes() == source.read_bytes(),
            "regular destination was not replaced")

    tools = temporary_root / "sync-tools"
    tools.mkdir()
    wrapper = tools / "python3"
    wrapper.write_text(
        "#!/bin/sh\nmv " + shlex.quote(str(source)) + " " + shlex.quote(str(source) + ".saved") +
        "\nmkdir " + shlex.quote(str(source)) + "\nexec " + shlex.quote(sys.executable) + ' "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    environment = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ["PATH"])
    original = destination.read_bytes()
    require(sync(env=environment).returncode != 0 and destination.read_bytes() == original,
            "failed guidance copy changed destination")
    require(not list(repository.glob(".GLOBAL-AGENTS.*")), "failed copy left temporary file")
    source.rmdir()
    Path(str(source) + ".saved").replace(source)
    source.unlink()
    require(sync().returncode != 0 and destination.read_bytes() == original,
            "missing source changed destination")
    source.write_bytes(original)
    subprocess.run(["git", "add", "GLOBAL-AGENTS.md"], cwd=repository, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qm", "Synthetic guidance"], cwd=repository, check=True)
    require(sync("--check").returncode == 0, "fresh committed guidance was rejected")
    source.write_text("updated guidance\n", encoding="utf-8")
    require(sync("--check").returncode != 0, "stale committed guidance was accepted")

    def git(*arguments):
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        *arguments], cwd=repository, check=True, capture_output=True)

    # A branch that does not edit the copy is judged by the default branch.
    git("branch", "old-branch")
    destination.write_bytes(source.read_bytes())
    git("commit", "-qam", "Refresh guidance")
    git("update-ref", "refs/remotes/origin/main", "HEAD")
    git("checkout", "-q", "old-branch")
    require(sync("--check").returncode == 0,
            "branch that does not edit guidance was judged by its stale HEAD copy")
    source.write_text("newer guidance\n", encoding="utf-8")
    stale_default = sync("--check")
    require(stale_default.returncode != 0, "stale default-branch guidance was accepted")
    require(
        "do not copy" in stale_default.stderr.lower()
        and "run scripts/sync-global-agents.sh and commit" not in stale_default.stderr,
        f"unedited branch failure message did not warn against copying guidance in: {stale_default.stderr}",
    )

    # A branch that edits the copy is judged by what it pushes.
    destination.write_bytes(source.read_bytes())
    git("commit", "-qam", "Edit guidance on branch")
    require(sync("--check").returncode == 0, "branch with fresh edited guidance was rejected")
    source.write_text("newest guidance\n", encoding="utf-8")
    stale_edited = sync("--check")
    require(stale_edited.returncode != 0, "branch with stale edited guidance was accepted")
    require(
        "run scripts/sync-global-agents.sh and commit" in stale_edited.stderr,
        f"edited branch failure message did not tell it to sync and commit: {stale_edited.stderr}",
    )
    source.write_bytes(subprocess.run(["git", "show", "origin/main:GLOBAL-AGENTS.md"], cwd=repository,
                                      check=True, capture_output=True).stdout)
    require(sync("--check").returncode != 0,
            "branch with stale edited guidance was accepted because main matched")

    # Without a merge base, as in a shallow clone, the check cannot tell
    # whether the branch edits the copy, so it asks for the history.
    git("checkout", "-q", "--orphan", "unrelated")
    source.write_bytes(destination.read_bytes())
    git("commit", "-qm", "Unrelated history")
    unrelated = sync("--check")
    require(unrelated.returncode != 0 and "history" in unrelated.stderr,
            f"guidance check without a merge base did not ask for history: {unrelated.stderr}")


def check_install_verification_tools(temporary_root: Path) -> None:
    installer_root = temporary_root / "installer-check"
    fixtures = installer_root / "fixtures"
    stub_bin = installer_root / "stub-bin"
    fixtures.mkdir(parents=True)
    stub_bin.mkdir()

    def write_executable_archive(archive_path: Path, mode: str, member_name: str, tool_name: str) -> None:
        payload = f"#!/bin/sh\necho {tool_name}\n".encode("utf-8")
        with tarfile.open(archive_path, mode) as archive:
            info = tarfile.TarInfo(member_name)
            info.size = len(payload)
            info.mode = 0o755
            archive.addfile(info, io.BytesIO(payload))

    with gzip.open(fixtures / "lefthook_2.1.10_Linux_x86_64.gz", "wb") as handle:
        handle.write(b"#!/bin/sh\necho lefthook\n")
    write_executable_archive(
        fixtures / "actionlint_1.7.12_linux_amd64.tar.gz", "w:gz", "actionlint", "actionlint"
    )
    write_executable_archive(
        fixtures / "shellcheck-v0.11.0.linux.x86_64.tar.xz",
        "w:xz",
        "shellcheck-v0.11.0/shellcheck",
        "shellcheck",
    )
    write_executable_archive(
        fixtures / "gitleaks_8.30.1_linux_x64.tar.gz", "w:gz", "gitleaks", "gitleaks"
    )

    gh_stub = stub_bin / "gh"
    gh_stub.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, shutil, sys\n"
        "from pathlib import Path\n"
        "args = sys.argv[1:]\n"
        "with Path(os.environ['STUB_LOG']).open('a', encoding='utf-8') as log:\n"
        "    log.write(json.dumps({\n"
        "        'tool': 'gh',\n"
        "        'argv': args,\n"
        "        'gh_token': os.environ.get('GH_TOKEN', ''),\n"
        "        'gh_host': os.environ.get('GH_HOST', ''),\n"
        "    }) + '\\n')\n"
        "fail_once = os.environ.get('STUB_FAIL_ONCE_FILE', '')\n"
        "if fail_once and Path(fail_once).exists():\n"
        "    Path(fail_once).unlink()\n"
        "    raise SystemExit(1)\n"
        "pattern = args[args.index('--pattern') + 1]\n"
        "output = args[args.index('--output') + 1]\n"
        "shutil.copyfile(Path(os.environ['STUB_FIXTURES']) / pattern, output)\n",
        encoding="utf-8",
    )
    gh_stub.chmod(0o755)

    curl_stub = stub_bin / "curl"
    curl_stub.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, shutil, sys\n"
        "from pathlib import Path\n"
        "args = sys.argv[1:]\n"
        "with Path(os.environ['STUB_LOG']).open('a', encoding='utf-8') as log:\n"
        "    log.write(json.dumps({'tool': 'curl', 'argv': args}) + '\\n')\n"
        "output = args[args.index('-o') + 1]\n"
        "asset = args[-1].rsplit('/', 1)[-1]\n"
        "shutil.copyfile(Path(os.environ['STUB_FIXTURES']) / asset, output)\n",
        encoding="utf-8",
    )
    curl_stub.chmod(0o755)

    sha_stub = stub_bin / "sha256sum"
    sha_stub.write_text(
        "#!/usr/bin/env python3\n"
        "import os, sys\n"
        "from pathlib import Path\n"
        "lines = [line.strip() for line in sys.stdin if line.strip()]\n"
        "with Path(os.environ['STUB_SHA_LOG']).open('a', encoding='utf-8') as log:\n"
        "    for line in lines:\n"
        "        log.write(line + '\\n')\n"
        "if os.environ.get('STUB_FAIL_SHA') == '1':\n"
        "    raise SystemExit(1)\n"
        "for line in lines:\n"
        "    _, target = line.split(None, 1)\n"
        "    if not Path(target).is_file() or Path(target).stat().st_size == 0:\n"
        "        raise SystemExit(1)\n",
        encoding="utf-8",
    )
    sha_stub.chmod(0o755)

    sleep_stub = stub_bin / "sleep"
    sleep_stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    sleep_stub.chmod(0o755)

    def run_installer(name: str, extra_env: dict[str, str | None]):
        case_dir = installer_root / name
        runner_temp = case_dir / "runner-temp"
        runner_temp.mkdir(parents=True)
        github_path = case_dir / "github-path"
        github_path.write_text("", encoding="utf-8")
        stub_log = case_dir / "calls.jsonl"
        sha_log = case_dir / "sha.log"
        env = dict(os.environ)
        env.pop("GITHUB_TOKEN", None)
        env.pop("GH_TOKEN", None)
        env.pop("GH_HOST", None)
        env.update(
            {
                "PATH": str(stub_bin) + os.pathsep + os.environ["PATH"],
                "RUNNER_TEMP": str(runner_temp),
                "GITHUB_PATH": str(github_path),
                "STUB_FIXTURES": str(fixtures),
                "STUB_LOG": str(stub_log),
                "STUB_SHA_LOG": str(sha_log),
            }
        )
        for key, value in extra_env.items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        result = subprocess.run(
            ["bash", str(INSTALLER)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        calls = (
            [json.loads(line) for line in stub_log.read_text(encoding="utf-8").splitlines() if line]
            if stub_log.exists()
            else []
        )
        sha_lines = (
            [line for line in sha_log.read_text(encoding="utf-8").splitlines() if line]
            if sha_log.exists()
            else []
        )
        return result, runner_temp, github_path, calls, sha_lines

    def require_tools_installed(runner_temp: Path, github_path: Path) -> None:
        tool_dir = runner_temp / "rookery-tools"
        for tool_name in ("lefthook", "actionlint", "shellcheck", "gitleaks"):
            binary = tool_dir / tool_name
            require(binary.is_file(), f"installer did not place {tool_name} in {tool_dir}")
            require(bool(binary.stat().st_mode & stat.S_IXUSR), f"{tool_name} is not executable")
        require(
            str(tool_dir) in github_path.read_text(encoding="utf-8").splitlines(),
            f"installer did not append {tool_dir} to GITHUB_PATH",
        )

    # 1. Authenticated CI path: GITHUB_TOKEN set + gh available.
    token = "fixture-ci-token"
    auth_result, auth_temp, auth_path, auth_calls, auth_sha = run_installer(
        "authenticated", {"GITHUB_TOKEN": token}
    )
    require(auth_result.returncode == 0, f"authenticated install failed: {auth_result.stderr}")
    require_tools_installed(auth_temp, auth_path)
    require(len(auth_sha) == 4, f"expected 4 sha256sum checks, got {len(auth_sha)}")
    require(
        len(auth_calls) == 4 and all(call["tool"] == "gh" for call in auth_calls),
        f"authenticated install did not use gh for all 4 tools: {auth_calls}",
    )
    for call in auth_calls:
        require(call["gh_token"] == token, f"gh did not receive GITHUB_TOKEN via GH_TOKEN: {call}")
        require(call["gh_host"] == "github.com", f"gh was not scoped to github.com: {call}")
        repo_arg = call["argv"][call["argv"].index("--repo") + 1]
        require(repo_arg.startswith("github.com/"), f"gh --repo was not host-scoped: {repo_arg}")
        require(
            all(token not in arg for arg in call["argv"]),
            f"GITHUB_TOKEN leaked into gh argv: {call['argv']}",
        )

    # 2. Unauthenticated standalone fallback: GITHUB_TOKEN unset.
    unauth_result, unauth_temp, unauth_path, unauth_calls, unauth_sha = run_installer(
        "unauthenticated", {"GITHUB_TOKEN": None}
    )
    require(unauth_result.returncode == 0, f"unauthenticated install failed: {unauth_result.stderr}")
    require_tools_installed(unauth_temp, unauth_path)
    require(len(unauth_sha) == 4, f"expected 4 sha256sum checks on fallback, got {len(unauth_sha)}")
    require(
        len(unauth_calls) == 4 and all(call["tool"] == "curl" for call in unauth_calls),
        f"unauthenticated install did not fall back to curl: {unauth_calls}",
    )
    for call in unauth_calls:
        require(
            call["argv"][-1].startswith("https://github.com/"),
            f"unexpected curl download URL: {call['argv'][-1]}",
        )
        require(
            all("authorization" not in arg.lower() for arg in call["argv"]),
            f"unauthenticated curl sent an Authorization header: {call['argv']}",
        )

    # 3. Retry recovery on transient gh failure.
    fail_marker = installer_root / "fail-once"
    fail_marker.write_text("fail\n", encoding="utf-8")
    retry_result, retry_temp, retry_path, retry_calls, _ = run_installer(
        "retry", {"GITHUB_TOKEN": token, "STUB_FAIL_ONCE_FILE": str(fail_marker)}
    )
    require(retry_result.returncode == 0, f"retry install failed: {retry_result.stderr}")
    require_tools_installed(retry_temp, retry_path)
    require(
        len(retry_calls) == 5 and all(call["tool"] == "gh" for call in retry_calls),
        f"expected 5 gh calls with one transient retry, got {len(retry_calls)}",
    )

    # 4. Checksum mismatch fails closed without updating GITHUB_PATH.
    bad_sha_result, _, bad_sha_path, _, _ = run_installer(
        "bad-sha", {"GITHUB_TOKEN": token, "STUB_FAIL_SHA": "1"}
    )
    require(bad_sha_result.returncode != 0, "installer accepted a failing sha256sum check")
    require(
        bad_sha_path.read_text(encoding="utf-8") == "",
        "installer updated GITHUB_PATH despite sha256sum failure",
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rookery-repository-check-") as temporary:
        temporary_root = Path(temporary)
        check_guidance_copy(temporary_root)
        check_install_verification_tools(temporary_root)
        repository = temporary_root / "repository"
        checker = repository / "scripts/checks/repository.py"
        checker.parent.mkdir(parents=True)
        shutil.copy2(CHECKER, checker)
        subprocess.run(["git", "init", "-q", repository], check=True)

        (repository / "target.md").write_text("# Target\n", encoding="utf-8")
        (repository / "README.md").write_text(
            "[target](target.md)\n\n[target-reference]: target.md\n",
            encoding="utf-8",
        )
        (repository / "large.json").write_text(
            '{"large": ' + "9" * 5000 + "}\n",
            encoding="utf-8",
        )
        clean = run_checker(repository)
        require(clean.returncode == 0, f"clean repository failed: {clean.stderr}")
        check_home_paths(repository)
        check_link_scanning(repository)
        check_rule_copies(repository)
        check_contract_copies(repository)
        check_contract_factor_lines(repository)

        invalid_text = repository / "invalid-text.txt"
        for contents, diagnostic in (
            ("missing newline", "missing final newline"),
            ("trailing space \n", "trailing whitespace"),
            ("trailing tab\t\n", "trailing whitespace"),
        ):
            invalid_text.write_text(contents, encoding="utf-8")
            result = run_checker(repository)
            require(
                result.returncode == 1
                and "invalid-text.txt:" in result.stderr
                and diagnostic in result.stderr,
                f"text check did not reject {contents!r}: {result.stderr}",
            )
        invalid_text.unlink()

        for regular_name in (
            "plans",
            "docs/plans",
            "docs/brainstorms",
            "docs/ideation",
            "docs/dogfood-reports",
            "docs/reports",
            "docs/pulse-reports",
            "outputs",
            "tmp",
        ):
            regular_path = repository / regular_name
            regular_path.parent.mkdir(parents=True, exist_ok=True)
            regular_path.write_text("ordinary tracked file\n", encoding="utf-8")
            subprocess.run(["git", "add", regular_path], cwd=repository, check=True)
            regular_result = run_checker(repository)
            require(
                regular_result.returncode == 0,
                f"repository checker treated regular file {regular_name} as a transient directory",
            )
            subprocess.run(
                ["git", "rm", "--cached", "--force", regular_path],
                cwd=repository,
                check=True,
                capture_output=True,
            )
            regular_path.unlink()

        for transient_name in (
            "plans/force-added.md",
            "docs/plans/force-added.md",
            "docs/brainstorms/force-added.md",
            "docs/ideation/force-added.md",
            "docs/dogfood-reports/force-added.md",
            "docs/reports/force-added.md",
            "docs/pulse-reports/force-added.md",
            "outputs/force-added.md",
            "tmp/force-added.md",
        ):
            transient_path = repository / transient_name
            transient_path.parent.mkdir(parents=True, exist_ok=True)
            transient_path.write_text("# Force-added artifact\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "--force", transient_path],
                cwd=repository,
                check=True,
            )
            transient_result = run_checker(repository)
            require(
                transient_result.returncode == 1
                and "transient working artifact must not be tracked"
                in transient_result.stderr,
                f"repository checker accepted tracked transient path {transient_name}",
            )
            subprocess.run(
                ["git", "rm", "--cached", "--force", transient_path],
                cwd=repository,
                check=True,
                capture_output=True,
            )
            transient_path.unlink()

        invalid_json = repository / "invalid.json"
        invalid_json.write_text('{"broken": }\n', encoding="utf-8")
        invalid = run_checker(repository)
        require(
            invalid.returncode == 1 and "invalid.json" in invalid.stderr,
            "invalid JSON did not fail with its path",
        )
        invalid_json.unlink()

        invalid_utf8_json = repository / "invalid-utf8.json"
        invalid_utf8_json.write_bytes(b'{"broken": "\xff"}\n')
        invalid_utf8 = run_checker(repository)
        require(
            invalid_utf8.returncode == 1 and "invalid-utf8.json" in invalid_utf8.stderr,
            "invalid UTF-8 JSON did not fail with its path",
        )
        invalid_utf8_json.unlink()

        readme = repository / "README.md"
        readme_contents = readme.read_bytes()
        readme.write_bytes(b"# Invalid UTF-8\n\xff\n")
        invalid_utf8_markdown = run_checker(repository)
        require(
            invalid_utf8_markdown.returncode == 1
            and "README.md: invalid UTF-8" in invalid_utf8_markdown.stderr,
            "invalid UTF-8 Markdown did not fail with its path",
        )
        readme.write_bytes(readme_contents)

        for filename in ("LICENSE", ".gitignore", ".gitleaksignore"):
            public_text = repository / filename
            public_text.write_bytes(b"invalid UTF-8: \xff\n")
            invalid_utf8_public_text = run_checker(repository)
            require(
                invalid_utf8_public_text.returncode == 1
                and f"{filename}: invalid UTF-8" in invalid_utf8_public_text.stderr,
                f"invalid UTF-8 {filename} did not fail with its path",
            )
            public_text.unlink()

        extensionless_binary = repository / "opaque-binary"
        extensionless_binary.write_bytes(b"\x00\xff\x00")
        extensionless_binary_result = run_checker(repository)
        require(
            extensionless_binary_result.returncode == 0,
            "unrelated extensionless binary was treated as repository text: "
            f"{extensionless_binary_result.stderr}",
        )
        extensionless_binary.unlink()

        binary_asset = repository / "asset.webp"
        binary_asset.write_bytes(b"RIFF\xffWEBP")
        binary = run_checker(repository)
        require(
            binary.returncode == 0,
            f"binary asset was treated as repository text: {binary.stderr}",
        )
        binary_asset.unlink()

        nonstandard_paths = []
        for name, constant in (
            ("nan", "NaN"),
            ("infinity", "Infinity"),
            ("negative-infinity", "-Infinity"),
        ):
            nonstandard_json = repository / f"nonstandard-{name}.json"
            nonstandard_json.write_text(
                f'{{"value": {constant}}}\n',
                encoding="utf-8",
            )
            nonstandard_paths.append(nonstandard_json)
        nonstandard = run_checker(repository)
        for nonstandard_json in nonstandard_paths:
            require(
                nonstandard.returncode == 1
                and nonstandard_json.name in nonstandard.stderr,
                f"non-standard JSON file {nonstandard_json.name} was accepted",
            )
            nonstandard_json.unlink()

        broken_link = repository / "broken.md"
        broken_link.write_text("[missing](missing.md)\n", encoding="utf-8")
        broken = run_checker(repository)
        require(
            broken.returncode == 1 and "broken.md" in broken.stderr,
            "broken relative link did not fail with its path",
        )
        broken_link.unlink()

        broken_reference = repository / "broken-reference.md"
        broken_reference.write_text(
            "[missing][guide]\n\n[guide]: missing.md\n",
            encoding="utf-8",
        )
        broken_reference_result = run_checker(repository)
        require(
            broken_reference_result.returncode == 1
            and "broken-reference.md" in broken_reference_result.stderr,
            "broken reference-style relative link did not fail with its path",
        )
        broken_reference.unlink()

        (temporary_root / "outside.md").write_text("private sibling\n", encoding="utf-8")
        escaping_link = repository / "escaping.md"
        escaping_link.write_text("[outside](../outside.md)\n", encoding="utf-8")
        escaping = run_checker(repository)
        require(
            escaping.returncode == 1 and "relative link leaves repository" in escaping.stderr,
            "repository-escaping link was accepted",
        )
        escaping_link.unlink()

        outside_text = temporary_root / "outside.txt"
        outside_text.write_text("private sibling\n", encoding="utf-8")
        (repository / "linked.txt").symlink_to(outside_text)
        linked = run_checker(repository)
        require(
            linked.returncode == 1 and "symbolic link is not allowed" in linked.stderr,
            "repository checker followed a symbolic link",
        )
        (repository / "linked.txt").unlink()

        lint = repository / "scripts/checks/lint.sh"
        shutil.copy2(LINT, lint)
        check_yaml_arguments(repository, temporary_root)
        check_root_symlinks(repository, temporary_root)
        outside_shell = temporary_root / "outside.sh"
        outside_shell.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        (repository / "linked.sh").symlink_to(outside_shell)
        lint_result = subprocess.run(
            ["bash", "scripts/checks/lint.sh"],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            lint_result.returncode != 0 and "symbolic link is not allowed" in lint_result.stderr,
            "lint accepted a symbolic-link source file",
        )
        (repository / "linked.sh").unlink()

        checker.unlink()
        checker_marker = temporary_root / "checker-executed"
        outside_checker = temporary_root / "outside-checker.py"
        outside_checker.write_text(
            f"from pathlib import Path\nPath({str(checker_marker)!r}).touch()\n",
            encoding="utf-8",
        )
        checker.symlink_to(outside_checker)
        lint_checker_result = subprocess.run(
            ["bash", "scripts/checks/lint.sh"],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            lint_checker_result.returncode != 0 and not checker_marker.exists(),
            "lint executed a symlinked repository checker before validating it",
        )

        fixture_repository = temporary_root / "fixture-repository"
        fixture_repository.mkdir()
        subprocess.run(["git", "init", "-q", fixture_repository], check=True)
        fixture_script = fixture_repository / "scripts/checks/fixtures.sh"
        fixture_script.parent.mkdir(parents=True)
        shutil.copy2(FIXTURES, fixture_script)
        marker = temporary_root / "runner-executed"
        outside_runner = temporary_root / "outside-runner.sh"
        outside_runner.write_text(
            f"#!/usr/bin/env bash\nprintf ran >{marker}\n",
            encoding="utf-8",
        )
        for runner_name in FIXTURE_RUNNERS:
            runner = fixture_repository / runner_name
            runner.parent.mkdir(parents=True, exist_ok=True)
            if runner_name == FIXTURE_RUNNERS[0]:
                runner.symlink_to(outside_runner)
            elif runner.suffix == ".sh":
                runner.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            else:
                runner.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        fixture_result = subprocess.run(
            ["bash", "scripts/checks/fixtures.sh"],
            cwd=fixture_repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            fixture_result.returncode != 0
            and "fixtures: symbolic-link runner is not allowed:" in fixture_result.stderr
            and not marker.exists(),
            "fixture check did not reject the symbolic-link runner before execution: "
            f"{fixture_result.stderr}",
        )

        first_runner = fixture_repository / FIXTURE_RUNNERS[0]
        first_runner.unlink()
        first_runner.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        unlisted_runner = fixture_repository / "tests/unlisted/run-unlisted.sh"
        unlisted_runner.parent.mkdir(parents=True)
        unlisted_runner.write_text(f"#!/usr/bin/env bash\nprintf ran >{marker}\n", encoding="utf-8")
        unlisted_result = subprocess.run(
            ["bash", "scripts/checks/fixtures.sh"],
            cwd=fixture_repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            unlisted_result.returncode != 0
            and "fixtures: explicit roster does not match discovered runners" in unlisted_result.stderr
            and not marker.exists(),
            f"fixture check accepted a runner missing from its roster: {unlisted_result.stderr}",
        )

    print(
        "PASS: repository checks reject malformed content, tracked transient "
        "artifacts, unsafe links, and symlinked inputs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
