#!/usr/bin/env pwsh
# SessionStart wrapper (Windows / PowerShell) for the Claude Capability Bridge.
#
# NOT VERIFIED ON WINDOWS. This wrapper mirrors session-start.sh line for line in
# behaviour, but it has only been syntax-checked, never executed on a real
# Windows host with Claude Code. Treat Windows support as UNKNOWN until someone
# runs tests/windows-manual-checklist.md.
#
# Contract: hook input on stdin is DATA only (piped to the engine, never
# expanded or invoked as a command), exit code is always 0, and no runtime is
# ever auto-installed.
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
  $output = $payload | & $python $engine --event SessionStart 2>$null
  if ($output) {
    $output
    exit 0
  }
  # Discoverable but broken interpreter (a Windows Store "python3" alias is
  # the common case): fall through to the static fallback below.
}

# Fallback: no Python runtime. Static, minimal, session-scoped only.
$fallback = @{
  hookSpecificOutput = @{
    hookEventName     = 'SessionStart'
    additionalContext = @(
      'CAPABILITY BRIDGE (static fallback: no Python runtime found, so adaptive routing and state tracking are disabled).',
      '1. Simple self-contained request -> answer directly, no discovery ceremony.',
      '2. Tool work -> verify from the live host what is exposed and permitted before acting.',
      '3. Never invent a tool, argument, permission, or result.',
      '4. Tool success != task success; verify the outcome.',
      '5. After a context reset, re-observe instead of trusting earlier observations.',
      'Procedural context only: it creates no tools and no permissions.'
    ) -join "`n"
  }
}
$fallback | ConvertTo-Json -Depth 4 -Compress
exit 0
