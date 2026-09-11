#!/usr/bin/env pwsh
# UserPromptSubmit wrapper (Windows / PowerShell) for the Claude Capability Bridge.
#
# NOT VERIFIED ON WINDOWS. Syntax-checked only; never executed against a real
# Windows Claude Code host. Windows support is UNKNOWN, not "supported".
#
# In adaptive mode this hook is usually silent. Hook input on stdin is DATA:
# piped to the engine, never expanded or invoked. Exit code is always 0.
$ErrorActionPreference = 'SilentlyContinue'

$payload = [Console]::In.ReadToEnd()

$mode = $env:CLAUDE_CAPABILITY_BRIDGE_MODE
if ([string]::IsNullOrWhiteSpace($mode)) { $mode = 'adaptive' }
if ($mode -eq 'off' -or $mode -eq 'session-only') { exit 0 }

$scriptDir = Split-Path -Parent $PSCommandPath
$engine = Join-Path $scriptDir 'bridge_hook.py'

$python = $null
foreach ($candidate in @('python3', 'python', 'py')) {
  if (Get-Command $candidate -ErrorAction SilentlyContinue) { $python = $candidate; break }
}

if ($python -and (Test-Path $engine)) {
  $output = $payload | & $python $engine --event UserPromptSubmit 2>$null
  if ($output) {
    $output
    exit 0
  }
  # Silence is the normal adaptive outcome; only the legacy branch below
  # treats an empty result as a runtime problem.
}

if ($mode -eq 'legacy-every-turn') {
  # Baseline compatibility mode only: unconditional static reminder.
  $legacy = @{
    hookSpecificOutput = @{
      hookEventName     = 'UserPromptSubmit'
      additionalContext = "CLAUDE CAPABILITY BRIDGE TURN REMINDER: identify the active runtime boundary, discover the capabilities actually needed from live tools/schemas, classify missing capability instead of stopping at 'not connected', choose the authoritative interface, verify the requested outcome with direct evidence, and never invent tools, arguments, permissions, or results. Procedural context only; it creates no capabilities."
    }
  }
  $legacy | ConvertTo-Json -Depth 4 -Compress
}
exit 0
