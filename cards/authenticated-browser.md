---
id: authenticated-browser
title: Authenticated and stateful browsing
summary: Work with logged-in sessions without handling credentials you should not have or assuming a session carries over.
task_families:
  - web
  - identity
signals:
  - login
  - log in
  - sign in
  - password
  - credentials
  - session
  - cookie
  - authenticated
  - dashboard
  - account
  - two-factor
  - captcha
  - paywall
conceptual_capabilities:
  - persistent browser session
  - reuse existing login
  - user-visible browser handoff
related_references:
  - references/browser-workflows.md
  - references/security-and-permissions.md
  - references/interactive-surfaces.md
essentials:
  - Never ask for, store, or type a password the user did not deliberately hand to a supported flow.
  - A logged-in session in one context does not exist in another context.
  - When a human step is required (2FA, CAPTCHA, consent), hand off; do not attempt to bypass it.
---

# Authenticated and stateful browsing

## Purpose

Reach content that requires an existing identity, while keeping credential
handling, consent, and session boundaries intact.

## Use when

- The target is behind a login, a paywall, or an account-scoped dashboard.
- The task depends on a session the user already has.
- A flow requires a human decision step: consent, 2FA, CAPTCHA, payment.

## Do not use when

- The target is public - use `cards/browser-webapp.md`.
- An API or connector with proper scopes exists - prefer it; see
  `cards/mcp-connectors.md`.
- No browser path exists at all: report `UNAVAILABLE`.

## Required evidence

1. A browser capability exists **and** its session model is known: fresh and
   isolated per call, or persistent and possibly the user's own profile.
2. Whether the host offers a user-visible handoff for manual steps.
3. Which identity is actually in use. Do not infer it from the URL.
4. Explicit user intent for anything that acts on their account.

## Live tool-contract source

The browser tool's own schema and documented session behaviour: profile reuse,
cookie persistence, whether the user can see and take over the window, and
whether storage survives between calls. Assume none of these unless the
contract says so.

## Minimal workflow

1. Try the least-privileged path first: public data, an authorized API, or an
   already-connected integration.
2. If browsing is required, check whether an authenticated session already
   exists by loading a known account-scoped page and reading the result.
3. If unauthenticated, stop and hand off. Ask the user to sign in through the
   supported surface, or ask them to complete the human step.
4. After a handoff, re-check state instead of assuming it succeeded.
5. Do the narrow task only. Read what was asked; do not wander into other
   account areas.
6. Report which identity and which surface produced the result.

**Anti-pattern:** asking the user to paste a password into chat, or storing a
cookie/token in a file "for later". Both are credential mishandling regardless
of intent.

## Verification

Done means:

- the content proves the session was authenticated (account-specific data
  visible), not just that a page returned 200;
- any action taken on the account is confirmed by reading back the resulting
  state;
- the report says which identity was used and which steps needed a human.

## Common failures

- Redirected to a login page while treating the HTML as the target content.
- Session expired mid-flow, so later steps operate as an anonymous visitor.
- CAPTCHA or bot protection blocking automation. This is a boundary, not a
  puzzle to defeat.
- Wrong account: multiple profiles, and the automation used the default.
- Isolated per-call browser losing state between steps.

## Recovery

- Login wall: hand off to the user. Never attempt credential entry on your own
  initiative or try alternate endpoints to skirt the wall.
- Expired session: re-authenticate through the supported surface, then re-verify
  before continuing.
- Bot protection: report the block explicitly; do not rotate identifiers,
  spoof, or retry in a loop.
- Ambiguous identity: stop and ask which account is intended.

## Related deep references

- `references/browser-workflows.md`
- `references/security-and-permissions.md`
- `references/interactive-surfaces.md`
