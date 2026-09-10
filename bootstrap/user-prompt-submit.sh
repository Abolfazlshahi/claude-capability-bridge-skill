#!/usr/bin/env bash
# UserPromptSubmit wrapper for the Claude Capability Bridge.
#
# In adaptive mode this hook is usually SILENT. It only speaks when the context
# epoch changed (fresh session, compact, clear, fork, resume) or when the prompt
# clearly matches one capability card that has not been pointed at yet.
#
# Hook input is DATA: it is piped to the engine and never expanded or eval'd.
# Exit code is always 0; user work is never blocked.
# If no Python runtime exists this hook stays silent (no static per-turn text,
# because unconditional per-turn reminders are exactly what we are removing).
set -u

PAYLOAD="$(cat 2>/dev/null || true)"

MODE="${CLAUDE_CAPABILITY_BRIDGE_MODE:-adaptive}"
if [ "$MODE" = "off" ] || [ "$MODE" = "session-only" ]; then
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
ENGINE="$SCRIPT_DIR/bridge_hook.py"

PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done

if [ -n "$PYTHON" ] && [ -f "$ENGINE" ]; then
  printf '%s' "$PAYLOAD" | "$PYTHON" "$ENGINE" --event UserPromptSubmit 2>/dev/null
  exit 0
fi

if [ "$MODE" = "legacy-every-turn" ]; then
  # Baseline compatibility mode only: unconditional static reminder.
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"CLAUDE CAPABILITY BRIDGE TURN REMINDER: identify the active runtime boundary, discover the capabilities actually needed from live tools/schemas, classify missing capability instead of stopping at 'not connected', choose the authoritative interface, verify the requested outcome with direct evidence, and never invent tools, arguments, permissions, or results. Procedural context only; it creates no capabilities."}}
JSON
fi
exit 0
