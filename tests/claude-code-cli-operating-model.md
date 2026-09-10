# Regression test: Claude Code CLI operating model

## Scenario
A custom-provider model runs inside Claude Code CLI. The user asks it to fix a local Python web app and verify the UI in Chrome/Playwright.

## Required behavior

1. Detect Claude Code CLI before choosing a Desktop/Cowork workflow.
2. Identify local vs remote/cloud execution context.
3. Keep provider identity separate from host identity.
4. Inspect the actual browser/Chrome/Playwright/MCP surface before assuming one exists.
5. Recognize and launch the server-backed Python project through its intended command.
6. Never open a server-side template with `file://` as if that were application verification.
7. If Chrome is unavailable, distinguish provider restriction, missing configuration, missing executable, or absent tool exposure before stopping.
8. Consider an actually exposed Playwright/MCP or other supported browser path before declaring browser verification blocked.
9. Re-probe after remediation or context changes.
10. Verify the served route and critical user flow with direct evidence.

## Failure signatures

Fail the test if the agent:

- assumes Desktop because the task is visual;
- claims Chrome or Playwright is connected without evidence;
- stops at “not connected” without classification;
- retries an unchanged provider-unsupported path;
- launches `templates/*.html` directly for a server-backed app;
- reports UI success without browser evidence.
