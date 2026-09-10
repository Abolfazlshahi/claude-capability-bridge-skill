#!/usr/bin/env bash
set -euo pipefail

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"CLAUDE CAPABILITY BRIDGE TURN REMINDER: Before non-trivial execution, identify the active runtime/execution/provider boundary; discover the capabilities actually needed from live tools/schemas; classify missing capability instead of stopping at 'not connected'; attempt only authorized remediation; choose the authoritative interface; verify the requested outcome with direct evidence; never invent tools, arguments, permissions, or results. This reminder is procedural context only and does not create missing capabilities."}}
JSON
