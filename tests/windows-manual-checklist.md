# Windows manual verification checklist

**Status: NOT VERIFIED.** No step below has been executed on Windows by this
project. The PowerShell wrappers are syntax-checked only. Until somebody runs
this checklist on a real machine and records the results, Windows support is
UNKNOWN, and no README, release note, or issue reply may claim otherwise.

Record results by editing the Result column: `PASS`, `FAIL`, or `UNKNOWN`.
Leave `UNKNOWN` when a step could not be run. Do not infer one row from another.

## Environment to record first

| Field | Value |
| --- | --- |
| Windows build | |
| PowerShell version (`$PSVersionTable.PSVersion`) | |
| Shell used by the host (PowerShell 5.1 / 7 / cmd) | |
| Python launcher present (`py -3 --version`, `python --version`) | |
| Claude Code version | |
| Install path (contains a space? OneDrive-synced?) | |

## 1. Runtime discovery

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 1.1 | Run `python -V` and `python3 -V` in the host shell | At least one resolves, or both fail cleanly | |
| 1.2 | Run `powershell -File bootstrap\session-start.ps1 < NUL` | Exit code 0, no red error text | |
| 1.3 | Repeat 1.2 with PowerShell 7 (`pwsh`) | Exit code 0 | |
| 1.4 | Rename Python off PATH, rerun 1.2 | Static fallback text is printed, exit code still 0 | |

## 2. Hook wiring

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 2.1 | Install the Skill and register hooks from `bootstrap/settings.json.example` with Windows paths | Claude Code starts with no hook errors | |
| 2.2 | Start a session | SessionStart context appears once | |
| 2.3 | Send several ordinary prompts | No per-turn reminder in `adaptive` mode | |
| 2.4 | Send a browser/automation prompt | At most one capability card is injected | |
| 2.5 | Trigger a failing tool call (e.g. a missing binary) | A failure class line appears once | |
| 2.6 | Repeat the same failing call three times | Escalation once, then silence | |
| 2.7 | `/compact`, then send a prompt | The protocol is reissued once with a stale-state warning | |

## 3. Modes

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 3.1 | `$env:CLAUDE_CAPABILITY_BRIDGE_MODE="off"` | No hook output at all, exit code 0 | |
| 3.2 | `session-only` | SessionStart only; no prompt-time output | |
| 3.3 | `legacy-every-turn` | A reminder on every prompt (baseline comparison mode) | |
| 3.4 | Unset the variable | Behaves as `adaptive` | |

## 4. State directory

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 4.1 | Run a session, then inspect `%LOCALAPPDATA%\claude-capability-bridge` | `session-*.json` exists, valid JSON | |
| 4.2 | Set `CLAUDE_CAPABILITY_BRIDGE_STATE_DIR` to a custom path | State is written there instead | |
| 4.3 | Point the state dir inside the installed package | Engine refuses and falls back to the user state dir; package files unchanged | |
| 4.4 | Corrupt a state file, start a new turn | Engine recovers silently, turn is never blocked | |
| 4.5 | Make the state directory unwritable (deny write ACL) | Turn still completes, no crash, no error text | |
| 4.6 | Inspect state-file ACLs | **Known gap:** POSIX `0600` is not applied on NTFS. Record the effective ACL. | |

## 5. Path and encoding hazards

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 5.1 | Install under a path containing a space | Hooks still run | |
| 5.2 | Install under a path containing a non-ASCII character | Hooks still run, output is not mojibake | |
| 5.3 | Check the wrappers are not corrupted by CRLF conversion | Scripts still parse | |
| 5.4 | Send a prompt containing `$(...)`, backticks, and `;` | Text is treated as data, nothing executes | |
| 5.5 | Run with an execution policy of `Restricted` | Documented failure, exit code still 0, session not blocked | |

## 6. Engine parity

| # | Step | Expected | Result |
| --- | --- | --- | --- |
| 6.1 | `python bootstrap\bridge_hook.py --selftest` | Prints OK | |
| 6.2 | `python bootstrap\bridge_hook.py --diagnose` | Reports mode, state dir, budget, card count | |
| 6.3 | `python scripts\run_tests.py` | Same pass count as on Linux, or the differences are recorded here | |
| 6.4 | `python scripts\validate_skill.py` | PASS | |
| 6.5 | `python scripts\package_skill.py` and the plugin packager | Both build, file counts match the Linux build | |

## Reporting

Attach the filled table to the pull request or issue. A partially filled table
is more useful than a claim of support: rows left `UNKNOWN` stay UNKNOWN in the
README too.
