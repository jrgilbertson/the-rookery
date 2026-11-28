#!/usr/bin/env bash
# Keep bootstrap commands out of workflow run blocks: actionlint 1.7.12
# can deadlock feeding large scripts to ShellCheck (rhysd/actionlint#651).
set -euo pipefail
tool_dir="$RUNNER_TEMP/rookery-tools"
mkdir -p "$tool_dir"
curl_args=(-fsSL --retry 2 --retry-all-errors --connect-timeout 10 --max-time 60)

download_release_asset() {
  local repo="$1"
  local tag="$2"
  local asset="$3"
  local dest="$4"

  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    if command -v gh >/dev/null 2>&1; then
      local gh_cmd=(
        gh release download "$tag"
        --repo "github.com/$repo"
        --pattern "$asset"
        --output "$dest"
        --clobber
      )
      if command -v timeout >/dev/null 2>&1; then
        gh_cmd=(timeout 60 "${gh_cmd[@]}")
      fi

      local attempt
      for attempt in 1 2 3; do
        if GH_TOKEN="$GITHUB_TOKEN" GH_HOST="github.com" "${gh_cmd[@]}"; then
          return 0
        fi
        if (( attempt < 3 )); then
          sleep $(( attempt * 2 ))
        fi
      done
      return 1
    fi
    echo "install-verification-tools: gh not found; falling back to unauthenticated curl" >&2
  fi

  curl "${curl_args[@]}" -o "$dest" "https://github.com/$repo/releases/download/$tag/$asset"
}

download_release_asset evilmartians/lefthook v2.1.10 lefthook_2.1.10_Linux_x86_64.gz "$RUNNER_TEMP/lefthook.gz"
echo "0b14162a0bb2f0c64ae0759f6102f6e19c4d00981666a8ac73d4f5a6878ada4f  $RUNNER_TEMP/lefthook.gz" | sha256sum --check
gzip -dc "$RUNNER_TEMP/lefthook.gz" > "$tool_dir/lefthook"

download_release_asset rhysd/actionlint v1.7.12 actionlint_1.7.12_linux_amd64.tar.gz "$RUNNER_TEMP/actionlint.tar.gz"
echo "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8  $RUNNER_TEMP/actionlint.tar.gz" | sha256sum --check
tar -xzf "$RUNNER_TEMP/actionlint.tar.gz" -C "$tool_dir" actionlint

download_release_asset koalaman/shellcheck v0.11.0 shellcheck-v0.11.0.linux.x86_64.tar.xz "$RUNNER_TEMP/shellcheck.tar.xz"
echo "8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198  $RUNNER_TEMP/shellcheck.tar.xz" | sha256sum --check
tar -xJf "$RUNNER_TEMP/shellcheck.tar.xz" -C "$RUNNER_TEMP"
cp "$RUNNER_TEMP/shellcheck-v0.11.0/shellcheck" "$tool_dir/shellcheck"

download_release_asset gitleaks/gitleaks v8.30.1 gitleaks_8.30.1_linux_x64.tar.gz "$RUNNER_TEMP/gitleaks.tar.gz"
echo "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb  $RUNNER_TEMP/gitleaks.tar.gz" | sha256sum --check
tar -xzf "$RUNNER_TEMP/gitleaks.tar.gz" -C "$tool_dir" gitleaks

chmod +x "$tool_dir/lefthook" "$tool_dir/actionlint" "$tool_dir/shellcheck" "$tool_dir/gitleaks"
echo "$tool_dir" >> "$GITHUB_PATH"
