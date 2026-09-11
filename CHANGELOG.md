# Changelog

All notable changes to this project are documented here. Dates are omitted on
purpose: the fixed content of this repository stays byte-stable so that hosts
which reuse a cached prompt prefix are not disturbed by cosmetic churn.

## 0.9.0

Structural release. The Skill keeps its name, its purpose, and its behavioural
stance; the way that guidance reaches the model changed.

### Fixed
- CI: the `PowerShell wrapper syntax` step wrapped `[ref]` around an
  undeclared `$errors`, which PowerShell rejects at runtime, so the step
  failed on every runner that ships pwsh. Parsing now runs through
  `scripts/check_powershell_syntax.ps1`, which declares both out-parameters
  and reports file, line, and column. `tests/python/test_ci.py` checks the
  `[ref]` contract statically on any host and executes the checker wherever
  a PowerShell exists.

- The no-Python fallback tests no longer skip on Windows. Mirroring tools
  into a private directory needs the symlink privilege; dropping every
  `PATH` entry that holds a python executable does not, and it works
  because Windows keeps its interpreters in their own directories. The
  constructed `PATH` is probed before use, so an unusable one still skips
  rather than passing quietly.

- `scripts/run_tests.py --summary` reports a run in a few lines: the host
  facts, every failing test id with its assertion, the skip reasons grouped
  by count, and the totals. The verbose per-test log is the default, but it
  is not something a human can paste into a bug report.

- **A discoverable but broken Python silenced the hooks completely.** The
  wrappers selected the first `python3`/`python` on `PATH` and trusted it.
  A Windows Store alias resolves, runs nothing, and prints nothing, so the
  session opened with no protocol at all. The wrappers now check whether
  the engine actually produced output and fall back when it did not.
- **The test suite trusted `bash -c` as proof that wrappers can run.** On
  Windows, `bash` on `PATH` is often the WSL launcher, which starts fine but
  cannot open a drive-letter path and exits 127. The probe now executes a
  real script file, prefers the bash shipped with Git for Windows, honours
  `BRIDGE_TEST_BASH`, and the runner prints which shell it selected.
- **A Windows checkout silently disabled every shell wrapper.** With Git's
  default `core.autocrlf=true`, `*.sh` was checked out with CRLF and `bash`
  aborted on the carriage return with exit code 127 before the hook could
  emit anything. `.gitattributes` now pins those files to LF, and a test
  fails loudly with the repair command instead of the failure looking like
  a code bug.
- **The state-directory refusal used a POSIX path on Windows.** When an
  override pointed inside the package, the engine fell back to
  `~/.local/state`, which is not where Windows keeps per-user state. The
  fallback is now the platform default (`%LOCALAPPDATA%` on Windows).
- **Platform-dependent tests reported failures instead of skips.** Tests
  that must execute a POSIX wrapper, build a Python-less `PATH`, or read
  POSIX mode bits now skip with an explicit reason on hosts where those
  things do not exist. A skip states what was not verified; a false failure
  hides it.
- **Plugin packages shipped broken links.** The built Claude Code plugin
  contained six files and no `references/`, while the instructions pointed at
  ten reference documents. Every packaged build now carries its own reference
  closure, and packaging fails if any local link inside the package is dangling.
- **The plugin manifest advertised the wrong version.** It was hard-coded to
  `0.0.0` while the Skill declared `0.8.0`. Both packagers now read the version
  from `SKILL.md`, and a test plus a CI step compare the three values.
- **The validator could not fail.** It printed `PASS` and exited `0` even with a
  missing reference or an empty file. It was rewritten to fail loudly, and it
  now prints the scope of what it actually checked.
- **The hooks ignored their input.** The shipped scripts emitted a fixed block
  and never read stdin, so they could not react to the event, the prompt, or a
  failure. They were replaced by an engine that parses the hook payload.

### Added

- **Adaptive hook engine** (`bootstrap/bridge_hook.py`): classifies session
  starts, routes at most one capability card per prompt, classifies tool
  failures into nine causes with concrete guidance, deduplicates repeats, and
  escalates once before going silent. It always exits `0`, never blocks a turn,
  and treats hook input strictly as data.
- **Four modes** via `CLAUDE_CAPABILITY_BRIDGE_MODE`: `off`, `session-only`,
  `adaptive` (default), and `legacy-every-turn` for baseline comparisons.
- **Kernel, profiles, and cards.** One small always-on kernel, four runtime
  profiles, and ten task cards loaded on demand, with a generated
  `cards/index.json` and a `--check` mode that fails when it drifts.
- **Content budgets** (`config/content-budgets.json`) enforced by the validator,
  expressed in characters and explicitly not in tokens.
- **Offline trace analyser** (`scripts/analyze_trace.py`) with synthetic
  fixtures: compares captured request bodies, locates the first rewritten
  region, flags unstable injected text, and echoes usage fields when they exist.
- **Cache contract** (`docs/cache-contract.md`): which layer controls what, and
  which claims require a live deployment before anybody may make them.
- **Test suite**: packaging, content, hook behaviour, state lifecycle, safety,
  cache invariants, and the trace analyser, runnable offline with
  `python3 scripts/run_tests.py`.
- **Windows checklist** (`tests/windows-manual-checklist.md`), unfilled on
  purpose: Windows support stays UNKNOWN until somebody runs it.

### Changed

- **Default behaviour**: the previous build reminded the model on every turn.
  The default is now adaptive, so ordinary turns are silent and context is added
  only at session boundaries, on a routed task family, or after a real failure.
  Set `legacy-every-turn` to restore the old behaviour.
- **Where the rules live**: operating rules moved out of the long reference
  documents into the kernel, profiles, and cards. The reference documents remain
  as background reading, and `references/MIGRATION.md` maps the old locations to
  the new ones.
- **Honesty rules are now enforced by tests**, not by convention: emitted text
  may not claim that a permission is granted, that a tool is available, or that
  a cache behaviour is guaranteed.

### Not changed

- The Skill name (`claude-capability-bridge`), so existing installs and the
  eval definitions keep working.
- The root `SKILL.md` layout for the single-skill plugin, which is valid.
- Old reference paths still exist; nothing was deleted.

### Migration from 0.8.0

1. Reinstall from a fresh build: `python3 scripts/package_skill.py` for the
   Skill directory, or `python3 scripts/package_claude_code_plugin.py` for the
   Claude Code plugin.
2. Re-register hooks from `bootstrap/settings.json.example`. The old
   `scripts/*.sh` hook entries point at files that no longer emit useful text.
3. Expect fewer injections per session. If you were relying on the per-turn
   reminder, set `CLAUDE_CAPABILITY_BRIDGE_MODE=legacy-every-turn` and compare
   the two modes on your own workload before choosing.
4. Delete stale state if you want a clean start: remove the
   `claude-capability-bridge` directory under your user state path.

### Cache note

The fixed content is designed to be compatible with prefix caching, and the
invariant tests keep it byte-stable across runs. That is a property of this
repository, not a measurement of any provider. Whether a deployment actually
reuses a cached prefix requires verification on that deployment, using the
usage fields returned by the provider.

## 0.8.0 and earlier

See the repository history. Those releases predate the changelog.
