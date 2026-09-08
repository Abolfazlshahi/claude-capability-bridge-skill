# Projects and Files

## State model

Keep these scopes separate:

```text
conversation context
project knowledge/context
live filesystem/worktree
external connector state
browser state
desktop application state
```

A fact appearing in one scope does not prove it exists in another.

## Project knowledge

Project workspaces can provide persistent instructions and uploaded/reference material. Use them for context and rules, but still inspect the live worktree before editing files.

## Filesystem

Before editing:

1. identify repository/workspace root;
2. inspect relevant files;
3. understand neighboring conventions;
4. preserve user changes;
5. edit the smallest necessary surface.

Never overwrite user work merely to make a workflow easier.

## Generated artifacts

Distinguish:

- tracked source files;
- generated build output;
- temporary files;
- test artifacts;
- user-provided assets.

Keep generated artifacts out of source edits unless the user requests them.

## Context budgeting

Large files and logs should be inspected selectively. Prefer targeted search, line ranges, or summaries when sufficient. Load full files only when the complete structure matters.

For repetitive debugging output:

```text
collect
→ filter relevant lines
→ preserve context around errors
→ diagnose
```

## Environment variables and secrets

Environment configuration can exist in `.env`, shell variables, secret stores, or host settings. Never dump the whole environment to chat. Inspect variable names and only the minimum value needed to diagnose a problem; redact secrets in reports.

## Repository integrity

Before destructive repository operations, check status/diff when available. Do not reset, clean, force-push, or overwrite user changes without explicit authorization.

## Project/file mismatch

If the project knowledge says a file exists but the live worktree does not:

```text
trust live filesystem for filesystem operations
trust project knowledge for its documented context
report the discrepancy when material
```

## Browser/worktree mismatch

A browser showing a web app does not prove the source on disk is the version being viewed. Verify the server process, working directory, build mode, and URL before attributing browser behavior to a source change.