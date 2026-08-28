#!/usr/bin/env bash
set -euo pipefail

# Tiny wrapper to make capturing easier.
# Usage:
#   ./capture.sh URL OUTPUT_PATH

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 URL OUTPUT_PATH" >&2
    exit 1
fi

URL="$1"
OUTPUT_PATH="$2"

uv run --python 3.12 \
    capture-page.py \
    --screenshot \
    "$URL" \
    "$OUTPUT_PATH"