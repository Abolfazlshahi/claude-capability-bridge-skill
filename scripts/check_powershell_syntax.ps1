#!/usr/bin/env pwsh
# Parses the PowerShell wrappers and reports syntax errors.
#
# Parsing is not execution. A clean parse means the file is syntactically
# valid; it says nothing about whether the wrapper behaves correctly on a real
# Windows Claude Code host. That stays UNKNOWN until
# tests/windows-manual-checklist.md is filled in.
#
# Usage: pwsh -NoProfile -File scripts/check_powershell_syntax.ps1 [path ...]
# Paths may be files or directories; directories are searched for *.ps1.
# Exit codes: 0 = everything parsed, 1 = at least one parse error, 2 = bad usage.

$ErrorActionPreference = 'Stop'

$paths = @($args)
if ($paths.Count -eq 0) { $paths = @('bootstrap') }

$files = @()
foreach ($path in $paths) {
    if (Test-Path -LiteralPath $path -PathType Container) {
        foreach ($item in Get-ChildItem -LiteralPath $path -Filter '*.ps1' -File -Recurse) {
            $files += $item.FullName
        }
    }
    elseif (Test-Path -LiteralPath $path -PathType Leaf) {
        $files += (Resolve-Path -LiteralPath $path).Path
    }
    else {
        Write-Host "usage error: no such file or directory: $path"
        exit 2
    }
}

if ($files.Count -eq 0) {
    Write-Host "usage error: no .ps1 files found in: $($paths -join ', ')"
    exit 2
}

$broken = 0
foreach ($file in $files) {
    # Both out-parameters must exist before [ref] can wrap them. Wrapping an
    # undeclared variable is what broke this check before: PowerShell answers
    # "[ref] cannot be applied to a variable that does not exist".
    $tokens = $null
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($file, [ref]$tokens, [ref]$errors) | Out-Null
    if ($errors -and $errors.Count -gt 0) {
        $broken += 1
        foreach ($parseError in $errors) {
            $line = $parseError.Extent.StartLineNumber
            $column = $parseError.Extent.StartColumnNumber
            Write-Host "parse error: ${file}:${line}:${column}: $($parseError.Message)"
        }
    }
    else {
        Write-Host "parse ok: $file"
    }
}

if ($broken -gt 0) {
    Write-Host "$broken file(s) failed to parse"
    exit 1
}

Write-Host "$($files.Count) PowerShell file(s) parsed"
Write-Host 'NOTE: parsing is not execution. Windows behaviour stays UNKNOWN until tests/windows-manual-checklist.md is filled in.'
exit 0
