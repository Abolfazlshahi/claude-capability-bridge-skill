#!/usr/bin/env bash
# PostToolUseFailure wrapper for the Claude Capability Bridge.
#
# Coverage limit, documented on purpose: this event fires for tool calls that
# ran and failed. Pre-execution rejections (unknown tool name, schema validation
# failure, permission refusal before execution) are NOT guaranteed to reach it.
# Those cases are reported as UNKNOWN/UNOBSERVABLE rather than invented.
#
# Hook input is DATA: piped to the engine, never expanded or eval'd.
# The engine classifies from documented structured fields only, never retries a
# side-effecting call, and never echoes raw error text back into context.
# Exit code is always 0.
set -u

PAYLOAD="$(cat 2>/dev/null || true)"

MODE="${CLAUDE_CAPABILITY_BRIDGE_MODE:-adaptive}"
if [ "$MODE" = "off" ]; then
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
  OUTPUT="$(printf '%s' "$PAYLOAD" | "$PYTHON" "$ENGINE" --event PostToolUseFailure 2>/dev/null || true)"
  if [ -n "$OUTPUT" ]; then
    printf '%s\n' "$OUTPUT"
  fi
  exit 0
fi

# No Python runtime: stay silent rather than emit a generic reminder that
# cannot be matched to the actual failure.
exit 0
