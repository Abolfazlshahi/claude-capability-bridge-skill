#!/usr/bin/env bash
set -euo pipefail

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PostToolUseFailure","additionalContext":"CLAUDE CAPABILITY BRIDGE FAILURE REMINDER: A tool call just failed. Do not repeat the same call blindly. Inspect the actual error and classify the cause (tool/schema, permission/approval, environment/dependency, process/readiness, navigation/target, protocol/gateway, network/auth, provider support, or model/procedural). Change one material variable, re-probe when appropriate, then retry only when justified; otherwise report a concrete block. Never convert 'not connected' into a final diagnosis without evidence, and never claim success without verification."}}
JSON
