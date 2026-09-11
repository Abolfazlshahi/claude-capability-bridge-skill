---
id: computer-use
title: Screen and GUI control
summary: Drive a graphical desktop only when such a capability is exposed, with bounded steps and visual verification after every action.
task_families:
  - gui
  - desktop-automation
signals:
  - screen
  - desktop
  - gui
  - mouse
  - keyboard
  - click on the screen
  - window
  - application
  - native app
  - screen recording
  - drag
conceptual_capabilities:
  - capture screen
  - move pointer
  - send keystrokes
  - control application window
related_references:
  - references/computer-use.md
  - references/interactive-surfaces.md
  - references/security-and-permissions.md
essentials:
  - GUI control is a rare, explicitly provisioned capability; absence is the normal case.
  - Never act blind: capture, act once, capture again, compare.
  - Prefer a CLI, API, or browser path when one exists; GUI control is the most fragile option.
---

# Screen and GUI control

## Purpose

Operate a graphical environment - windows, pointer, keyboard - when no
programmatic path exists, while keeping every action observable and reversible.

## Use when

- The target only exists as a desktop application with no CLI or API.
- The user explicitly asks for on-screen interaction or a visual walkthrough.
- A workflow genuinely requires seeing and manipulating the desktop.

## Do not use when

- A CLI, API, connector, or browser path exists. Those are cheaper, faster, and
  verifiable. See `cards/shell-processes.md`, `cards/mcp-connectors.md`,
  `cards/browser-webapp.md`.
- No screen-control capability is exposed. Report `UNAVAILABLE`; never narrate
  clicks that did not happen.
- The task involves credentials on screen - see
  `cards/authenticated-browser.md` and hand off instead.

## Required evidence

1. A screen-control capability is exposed in this session, with an actual
   screenshot/pointer/keyboard contract.
2. A display exists. Headless environments have no screen to control.
3. The current screen state, captured **before** the first action.
4. Explicit user intent for anything destructive or account-affecting.

## Live tool-contract source

The exposed tool's own schema: screen dimensions, coordinate origin, supported
actions, key naming, and whether it returns an image you can actually inspect.
Coordinate conventions differ between hosts; never carry them over.

## Minimal workflow

1. Capture the current screen and identify the target element from that image.
2. Perform exactly one action.
3. Capture again and compare against the expected new state.
4. Repeat, one action at a time, with a hard step budget.
5. Stop and report when the screen does not match the expectation twice in a
   row.

**Anti-pattern:** issuing a scripted sequence of clicks at remembered
coordinates without re-capturing between steps. One layout shift turns the rest
of the sequence into random input on someone's machine.

## Verification

Done means:

- the final screenshot shows the intended end state;
- side effects that are not visible on screen were confirmed some other way
  (a saved file, an updated record);
- the report distinguishes what was seen from what was inferred.

## Common failures

- No display available, so capture fails or returns a blank image.
- Coordinate mismatch from scaling or a different resolution than assumed.
- Focus stolen by another window, sending keystrokes to the wrong place.
- Timing: acting before the UI finished rendering.
- Modal dialog or permission prompt intercepting input.
- Irreversible click (delete, purchase, submit) performed while exploring.

## Recovery

- Blank or failed capture: report `UNAVAILABLE` rather than continuing blind.
- Unexpected screen: stop, capture, describe what is actually there, and ask.
- Focus problems: re-capture, re-identify the window, act once.
- Irreversible action taken by mistake: report it immediately and precisely.
  Do not attempt silent cleanup.
- Two consecutive mismatches: abandon the GUI path and report the block.

## Related deep references

- `references/computer-use.md`
- `references/interactive-surfaces.md`
- `references/security-and-permissions.md`
