#!/usr/bin/env pwsh
# PostToolUseFailure wrapper (Windows / PowerShell) for the Claude Capability Bridge.
#
# NOT VERIFIED ON WINDOWS. Syntax-checked only; never executed against a real
# Windows Claude Code host. Windows support is UNKNOWN, not "supported".
#
# Coverage limit, documented on purpose: this event fires for tool calls that
# ran and failed. Pre-execution rejections (unknown tool name, schema validation
# failure, permission refusal before execution) are NOT guaranteed to reach it.
#
# Hook input on stdin is DATA: piped to the engine, never expanded or invoked.
# Exit code is always 0. No automatic retry of side-effecting operations.
$ErrorActionPreference = 'SilentlyContinue'

$payload = [Console]::In.ReadToEnd()

$mode = $env:CLAUDE_CAPABILITY_BRIDGE_MODE
if ([string]::IsNullOrWhiteSpace($mode)) { $mode = 'adaptive' }
if ($mode -eq 'off') { exit 0 }

$scriptDir = Split-Path -Parent $PSCommandPath
$engine = Join-Path $scriptDir 'bridge_hook.py'

$python = $null
foreach ($candidate in @('python3', 'python', 'py')) {
  if (Get-Command $candidate -ErrorAction SilentlyContinue) { $python = $candidate; break }
}

if ($python -and (Test-Path $engine)) {
  $output = $payload | & $python $engine --event PostToolUseFailure 2>$null
  if ($output) { $output }
  exit 0
}

# No Python runtime: stay silent rather than emit a generic reminder that
# cannot be matched to the actual failure.
exit 0
