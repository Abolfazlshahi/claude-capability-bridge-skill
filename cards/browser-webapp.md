---
id: browser-webapp
title: Web apps - launch, browse, and exercise the real user path
summary: Run a web project for real, reach it through an available browser path, and test what a user would actually do.
task_families:
  - web
  - browser
signals:
  - browser
  - website
  - web app
  - webapp
  - frontend
  - localhost
  - url
  - page
  - click
  - form
  - screenshot
  - navigate
  - dev server
  - react
  - next.js
  - html page
conceptual_capabilities:
  - navigate page
  - inspect dom
  - capture screenshot
  - run dev server
related_references:
  - references/browser-workflows.md
  - references/webapp-verification.md
  - references/project-recognition-and-launch.md
essentials:
  - Opening a built file with file:// is not running a server-backed app.
  - Prove readiness against the real host and port before interacting.
  - Verify the user path (load, interact, result), not just that a page returned HTML.
---

# Web apps - launch, browse, and exercise the real user path

## Purpose

Take a web project from "code exists" to "a real user path was exercised and
the result was observed", without pretending a browser exists when it does not.

## Use when

- The task involves a site, page, front-end project, or a URL to visit.
- The task asks whether something works in the browser, or asks for a
  screenshot or a UI behaviour check.
- A local web project must be started and then exercised.

## Do not use when

- No browser path exists in this run. Report the limitation; do not narrate an
  imaginary browsing session.
- The task needs a logged-in session or credentials - see
  `cards/authenticated-browser.md` first.
- The work is OS-level clicking outside a browser - see
  `cards/computer-use.md`.
- Only static analysis of source is needed - see `cards/filesystem-git.md`.

## Required evidence

1. A browser/navigation capability is exposed here. This is **optional** in most
   hosts; absence is a normal outcome, not a defect.
2. For a local project: the framework and its real start command, from project
   config - not from a guess.
3. The actual bound host and port, read from process output, not assumed to be
   the framework default.
4. Whether the target requires authentication.
5. Whether outbound network access exists, when the target is remote.

## Live tool-contract source

The exposed navigation/inspection tool and its schema: what it returns
(rendered text, DOM, screenshot), whether it can click and type, whether it
shares a persistent session, and whether it can reach `localhost` at all. Some
fetch-style tools retrieve HTML but cannot execute JavaScript; that is not
browsing.

## Minimal workflow

1. Recognize the project: read the manifest/config to find the dev or preview
   command. See `references/project-recognition-and-launch.md`.
2. Install only if dependencies are missing and installing is permitted.
3. Start the server detached, log its output, and read the log to learn the
   **actual** URL.
4. Poll readiness with a bounded retry limit until the endpoint answers.
5. Choose the available browser path. If several exist, prefer the one that
   renders and can interact; if only a fetch-style tool exists, say that UI
   interaction was not possible.
6. Exercise the real user path: load the entry page, perform the key
   interaction, and read the resulting state.
7. Capture the evidence the user asked for (result text, screenshot, console or
   network errors).

**Anti-pattern:** opening `file:///.../index.html` and reporting the app works.
Routing, API calls, environment variables, and server rendering are all absent
on that path.

## Verification

Done means:

- the page loaded from the real served URL, not from a filesystem path;
- the interaction the user cares about was performed and its effect observed;
- errors were checked, not just absence of a crash;
- if any step was impossible, the report names which step and why.

## Common failures

- Assumed port; the framework chose another one.
- Readiness assumed after a fixed sleep, so the first interaction hits a dead
  socket.
- Client-side routes that only work through the server, returning 404 directly.
- A fetch-only tool returning an empty shell for a JavaScript-rendered app.
- Sandboxed browser cannot reach the user's `localhost` at all.
- Screenshot captured before render completed.

## Recovery

- Connection refused: re-read the server log; confirm the process is alive and
  which address it bound.
- Blank or shell-only page: check whether the tool executes JavaScript; if not,
  report the limitation instead of concluding the app is broken.
- No browser capability: report `UNAVAILABLE` for the browser step, and offer
  what can be verified without it (build success, server response, tests).
- Repeated identical failure: stop and report the concrete block with the real
  error output.

## Related deep references

- `references/browser-workflows.md`
- `references/webapp-verification.md`
- `references/project-recognition-and-launch.md`
- `references/interactive-surfaces.md`
