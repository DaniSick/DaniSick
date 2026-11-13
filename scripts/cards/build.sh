#!/usr/bin/env bash
# Regenerate every README card. Pass --fetch to refresh stats.json first (needs GITHUB_TOKEN or GH_TOKEN).
set -euo pipefail
cd "$(dirname "$0")"
[[ "${1:-}" == "--fetch" ]] && python3 stats.py
python3 about.py
python3 focus.py
python3 stack.py
