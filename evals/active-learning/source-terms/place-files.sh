#!/usr/bin/env bash
set -eu
python3 -I "$(dirname "$0")/../fixture.py" . source-terms
