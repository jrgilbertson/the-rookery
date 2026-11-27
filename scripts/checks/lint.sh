#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

for tool in actionlint shellcheck ruby python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "lint: required tool '$tool' is not installed" >&2
    exit 1
  fi
done

check_tmp_dir=$(mktemp -d)
trap 'rm -rf "$check_tmp_dir"' EXIT
safe_files="$check_tmp_dir/safe-files"
if ! git ls-files --cached --others --exclude-standard -z |
  python3 -c '
import os
import sys
from pathlib import Path

# Mirrors scripts/checks/repository.py; lint validates the tree before running it.
ALLOWED_ROOT_SYMLINKS = {
    "CONCEPTS.md": "GLOSSARY.md",
}


def allowed_root_symlink(root: Path, candidate: Path, relative: Path) -> bool:
    if len(relative.parts) != 1:
        return False
    expected_target = ALLOWED_ROOT_SYMLINKS.get(relative.name)
    if expected_target is None:
        return False
    try:
        if os.readlink(candidate) != expected_target:
            return False
        target = root / expected_target
        if target.is_symlink():
            return False
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
        return resolved == target.resolve(strict=True) and resolved.is_file()
    except (FileNotFoundError, OSError, ValueError):
        return False


root = Path(sys.argv[1]).resolve(strict=True)
for raw_path in sys.stdin.buffer.read().split(b"\0"):
    if not raw_path:
        continue
    relative = Path(os.fsdecode(raw_path))
    candidate = root / relative
    try:
        candidate.relative_to(root)
    except ValueError:
        print(f"lint: repository path escapes the repository: {os.fsdecode(raw_path)!r}", file=sys.stderr)
        raise SystemExit(1)
    current = root
    skip_allowed_symlink = False
    for component in relative.parts:
        current /= component
        if current.is_symlink():
            if current == candidate and allowed_root_symlink(root, candidate, relative):
                skip_allowed_symlink = True
                break
            print(f"lint: symbolic link is not allowed: {os.fsdecode(raw_path)!r}", file=sys.stderr)
            raise SystemExit(1)
    if skip_allowed_symlink:
        continue
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except FileNotFoundError:
        continue
    except (OSError, ValueError):
        print(f"lint: resolved path leaves the repository or cannot be verified: {os.fsdecode(raw_path)!r}", file=sys.stderr)
        raise SystemExit(1)
    if resolved.is_file():
        sys.stdout.buffer.write(raw_path + b"\0")
' "$repo_root" >"$safe_files"; then
  exit 1
fi

python3 scripts/checks/repository.py

shell_files=()
python_files=()
ruby_files=()
yaml_files=()
while IFS= read -r -d '' task_file; do
  case "$task_file" in
    *.sh) shell_files+=("$task_file") ;;
    *.py) python_files+=("$task_file") ;;
    *)
      if [[ -x "$task_file" && -f "$task_file" && ! -L "$task_file" ]]; then
        first_line=''
        IFS= read -r first_line < "$task_file" || true
        case "$first_line" in
          '#!'*bash|'#!'*/sh) shell_files+=("$task_file") ;;
          '#!'*python*) python_files+=("$task_file") ;;
        esac
      fi
      ;;
  esac
  case "$task_file" in
    *.rb) ruby_files+=("$task_file") ;;
  esac
  case "$task_file" in
    *.yml|*.yaml) yaml_files+=("$task_file") ;;
  esac
done <"$safe_files"

if ((${#shell_files[@]})); then
  shellcheck "${shell_files[@]}"
  for task_file in "${shell_files[@]}"; do
    bash -n "$task_file"
  done
fi

if ((${#python_files[@]})); then
  pycache_dir="$check_tmp_dir/pycache"
  mkdir "$pycache_dir"
  PYTHONPYCACHEPREFIX="$pycache_dir" python3 -m py_compile "${python_files[@]}"
fi

for task_file in "${ruby_files[@]}"; do
  ruby -c "$task_file"
done

if ((${#yaml_files[@]})); then
  ruby -e 'require "yaml"; ARGV.each { |path| YAML.parse_file(path) }' -- "${yaml_files[@]}"
fi

actionlint
echo "lint: repository integrity checks passed"
