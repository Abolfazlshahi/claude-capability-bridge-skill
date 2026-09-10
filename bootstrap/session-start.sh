#!/usr/bin/env bash
set -euo pipefail

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"CLAUDE CAPABILITY BRIDGE BOOT: Before non-trivial work identify host (CLI/Desktop/Cowork/remote/other), execution location (local/cloud/remote), and provider when observable. Discover only task-relevant capabilities from the live host. If a capability is missing, classify the cause before stopping; repair only when the current context can affect it; re-probe after repair or a boundary change. Route through the authoritative interface and verify the requested result directly. Never invent tools, permissions, or successful actions."}}
JSON
