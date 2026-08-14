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

python3 scripts/checks/repository.py

shell_files=()
python_files=()
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
done < <(git ls-files --cached --others --exclude-standard -z)

if ((${#shell_files[@]})); then
  shellcheck "${shell_files[@]}"
  for task_file in "${shell_files[@]}"; do
    bash -n "$task_file"
  done
fi

if ((${#python_files[@]})); then
  pycache_dir=$(mktemp -d)
  trap 'rm -rf "$pycache_dir"' EXIT
  PYTHONPYCACHEPREFIX="$pycache_dir" python3 -m py_compile "${python_files[@]}"
fi

ruby_files=()
while IFS= read -r -d '' task_file; do
  ruby_files+=("$task_file")
done < <(git ls-files --cached --others --exclude-standard -z -- '*.rb')
for task_file in "${ruby_files[@]}"; do
  ruby -c "$task_file"
done

yaml_files=()
while IFS= read -r -d '' task_file; do
  yaml_files+=("$task_file")
done < <(git ls-files --cached --others --exclude-standard -z -- '*.yml' '*.yaml')
if ((${#yaml_files[@]})); then
  ruby -e 'require "yaml"; ARGV.each { |path| YAML.parse_file(path) }' "${yaml_files[@]}"
fi

actionlint
echo "lint: repository integrity checks passed"
