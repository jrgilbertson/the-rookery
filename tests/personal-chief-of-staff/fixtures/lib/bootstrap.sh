#!/usr/bin/env bash

fixture_bootstrap() {
  local caller_bin_dir=$1 required trace_parent trace_name

  for required in PCOS_FIXTURE_ROOT PCOS_FIXTURE_SPECIMEN PCOS_FIXTURE_TRACE; do
    [[ -n "${!required:-}" ]] || die "missing required fixture variable: ${required}"
  done

  [[ "$PCOS_FIXTURE_SPECIMEN" =~ ^[a-z][a-z0-9]{3}$ ]] ||
    die "invalid fixture specimen token"
  [[ -d "$PCOS_FIXTURE_ROOT" ]] || die "fixture root must already exist"

  fixture_root=$(cd "$PCOS_FIXTURE_ROOT" && pwd -P)
  fixture_dir=$(cd "$caller_bin_dir/.." && pwd -P)
  repo_root=$(cd "$fixture_dir/../../.." && pwd -P)

  [[ "$fixture_root" != / ]] || die "fixture root must not be the filesystem root"

  case "$fixture_root/" in
    "$repo_root/"*) die "fixture root must be outside the repository" ;;
  esac
  case "$repo_root/" in
    "$fixture_root/"*) die "fixture root must not contain the repository" ;;
  esac

  trace_parent=$(cd "$(dirname "$PCOS_FIXTURE_TRACE")" 2>/dev/null && pwd -P) ||
    die "fixture trace parent must already exist"
  trace_name=$(basename "$PCOS_FIXTURE_TRACE")
  [[ "$trace_parent" == "$fixture_root" && "$trace_name" == trace.jsonl ]] ||
    die "fixture trace must be the trace.jsonl leaf inside the fixture root"
  trace_path="$fixture_root/trace.jsonl"
  [[ ! -L "$PCOS_FIXTURE_TRACE" && ! -L "$trace_path" ]] ||
    die "fixture trace must not be a symlink"
  [[ ! -e "$trace_path" || -f "$trace_path" ]] ||
    die "fixture trace must be a regular file"
}

fixture_prepare_state_dir() {
  local state_dir=$1 state_path
  shift

  case "$state_dir/" in
    "$fixture_root/"*) ;;
    *) die "fixture state must stay inside the fixture root" ;;
  esac
  [[ ! -L "$state_dir" ]] || die "fixture state directory must not be a symlink"
  mkdir -p "$state_dir"
  [[ -d "$state_dir" && ! -L "$state_dir" ]] ||
    die "fixture state directory is invalid"

  for state_path in "$@"; do
    [[ "${state_path%/*}" == "$state_dir" ]] ||
      die "fixture state file must stay inside its state directory"
    [[ ! -L "$state_path" ]] || die "fixture state file must not be a symlink"
    [[ ! -e "$state_path" || -f "$state_path" ]] ||
      die "fixture state path must be a regular file"
  done
}
