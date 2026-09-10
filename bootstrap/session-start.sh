#!/usr/bin/env bash
# SessionStart wrapper for the Claude Capability Bridge.
#
# Contract:
#   * hook input arrives on stdin as JSON and is treated as DATA only;
#   * it is piped to the engine, never expanded, sourced, or eval'd;
#   * exit code is always 0 so a hook problem cannot block the user;
#   * if no Python runtime exists, a small static fallback is printed instead.
#     Nothing is auto-installed.
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
  OUTPUT="$(printf '%s' "$PAYLOAD" | "$PYTHON" "$ENGINE" --event SessionStart 2>/dev/null || true)"
  if [ -n "$OUTPUT" ]; then
    printf '%s\n' "$OUTPUT"
    exit 0
  fi
  # An interpreter can be discoverable and still useless: a Windows Store
  # "python3" alias resolves, runs nothing, and prints nothing. Empty output
  # at session start is a malfunction, so fall through to the static
  # fallback below rather than open a session with no protocol at all.
fi

# Fallback: no Python runtime available. Static, minimal, session-scoped only.
cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"CAPABILITY BRIDGE (static fallback: no Python runtime found, so adaptive routing and state tracking are disabled).\n1. Simple self-contained request -> answer directly, no discovery ceremony.\n2. Tool work -> verify from the live host what is exposed and permitted before acting.\n3. Never invent a tool, argument, permission, or result.\n4. Tool success != task success; verify the outcome.\n5. After a context reset, re-observe instead of trusting earlier observations.\nProcedural context only: it creates no tools and no permissions."}}
JSON
exit 0
