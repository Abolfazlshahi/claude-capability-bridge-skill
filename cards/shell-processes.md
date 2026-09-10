---
id: shell-processes
title: Commands, builds, tests, and long-running processes
summary: Run commands and services so control returns, failures are diagnosed from real output, and readiness is proven instead of assumed.
task_families:
  - execution
  - build-test
signals:
  - run
  - command
  - shell
  - terminal
  - install
  - build
  - compile
  - test
  - tests
  - script
  - process
  - server
  - port
  - background
  - lint
  - dependency
conceptual_capabilities:
  - execute command
  - run tests
  - start process
  - inspect process
related_references:
  - references/code-and-shell.md
  - references/failure-recovery.md
  - references/verification.md
essentials:
  - Anything unbounded runs in the background with output to a log; never block the turn on a server.
  - Read the actual error text before changing anything; do not retry an unchanged command.
  - Exit code 0 is not task success. Check the artifact or endpoint the command was supposed to affect.
---

# Commands, builds, tests, and long-running processes

## Purpose

Execute real commands and services, keep the session responsive, and diagnose
failures from actual output rather than from assumptions about the toolchain.

## Use when

- The task needs a build, test run, install, migration, script, or CLI call.
- The task needs a service running so something else can be exercised.
- A previous step failed and the real error text is the only way forward.

## Do not use when

- A file edit alone achieves the goal - see `cards/filesystem-git.md`.
- The goal is verifying a web app through a user path - start here to launch,
  then continue in `cards/browser-webapp.md`.
- The environment does not expose command execution at all. Report the boundary
  instead of simulating output.

## Required evidence

1. An execution capability is exposed in this session.
2. The real working directory, not an assumed project root.
3. The relevant toolchain actually exists here (`node`, `python3`, package
   manager, etc.). Absence is common and expected.
4. Whether network egress is available, **before** planning an install.
5. Whether the operation is destructive or side-effecting, and whether that is
   authorized.

## Live tool-contract source

The exposed execution tool and its schema: timeout behaviour, working-directory
handling, output truncation, and whether background execution is supported. Two
hosts with similar-looking shell tools can differ on every one of those.

## Minimal workflow

1. Establish the working directory and confirm the entry point exists.
2. Run the smallest command that produces evidence (`--version`, a single test
   file, a dry run) before running the expensive one.
3. For anything that can run unbounded - servers, watchers, log tails, dev
   builds - start it detached with stdout and stderr redirected to a log file,
   record the process id, then poll with a **finite** command.
4. Poll readiness with a bounded loop that has a hard attempt limit, and treat
   "no readiness signal" as failure, not as success-after-waiting.
5. Read the log on failure. Quote the real error, not a paraphrase.

**Anti-pattern:** launching a dev server in the foreground and waiting. The
turn never returns, no verification happens, and the run looks hung.

## Verification

Done means:

- the command's exit status is known **and** the intended effect is confirmed
  (file produced, endpoint answering, migration applied, tests reported);
- for a service: a readiness probe succeeded against the real host and port,
  not the port you hoped for;
- for tests: the reported counts are read from output, never inferred.

A zero exit code with no artifact check is not verification.

## Common failures

- `command not found` - the toolchain is absent, not broken.
- Wrong directory, so a correct command operates on the wrong project.
- `EADDRINUSE` - something already holds the port; discover it instead of
  killing blindly.
- `ECONNREFUSED` - the process is not up or not listening where you expect.
- Install failure because egress is blocked. That is an environment boundary.
- Output truncated by the tool, hiding the real error further up.

## Recovery

- Missing dependency: report it and ask before installing anything global.
- Port conflict: identify the holder, then either reuse it or pick another port
  deliberately.
- Timeout: move to background execution plus finite polling. Do not simply
  re-run and hope.
- Repeated identical failure: stop. Change one material variable, or report the
  concrete block with the real error text.
- Never auto-retry a side-effecting command (publish, deploy, delete, payment)
  after an ambiguous error. Verify current state first.

## Related deep references

- `references/code-and-shell.md`
- `references/failure-recovery.md`
- `references/project-recognition-and-launch.md`
- `references/verification.md`
