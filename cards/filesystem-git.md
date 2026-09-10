---
id: filesystem-git
title: Files, repositories, and version control
summary: Read, edit, and commit real files without guessing paths, overwriting work, or claiming a change landed.
task_families:
  - files
  - repository
signals:
  - file
  - files
  - folder
  - directory
  - path
  - repo
  - repository
  - git
  - commit
  - branch
  - diff
  - patch
  - refactor
  - rename
  - codebase
conceptual_capabilities:
  - read file
  - write file
  - edit file
  - list directory
  - search code
  - version control
related_references:
  - references/projects-and-files.md
  - references/code-and-shell.md
  - references/security-and-permissions.md
essentials:
  - Read the real path before editing; never edit from memory of a filename.
  - Targeted edits beat full-file rewrites; a rewrite silently deletes work you did not read.
  - Re-read after writing. A successful write tool is not proof the intended change exists.
---

# Files, repositories, and version control

## Purpose

Work on real files and repositories so the change the user asked for actually
exists on disk, is scoped to what they asked for, and is reviewable.

## Use when

- The task names a file, folder, path, repository, or code symbol.
- The task is to inspect, modify, create, move, or delete project content.
- The task needs history: what changed, who changed it, what is staged.

## Do not use when

- The answer is knowledge-only and touches nothing on disk. Answer directly.
- The user wants a **deliverable** they can open or download: producing a file
  is not delivery - see `cards/artifacts-delivery.md`.
- The work is really process execution (build, test, server) - see
  `cards/shell-processes.md`.

## Required evidence

Before the first write:

1. A file/edit capability is exposed in this session (`SCHEMA_SEEN` at least).
2. The working directory is known from live evidence, not assumed.
3. The target path exists and its current content has been read - or you know
   it does not exist and creation is intended.
4. For repository operations: this is actually a checkout, and you know whether
   the working tree is clean.

If any of these is `UNKNOWN`, resolve that one thing first. Do not sweep the
whole environment.

## Live tool-contract source

The host's exposed tool list and each tool's own schema. Nothing else. Tool
names differ per host: a read/edit/search tool here may not exist there, and a
capability name in this card is conceptual, not callable.

## Minimal workflow

1. Locate: list or search to resolve the real path. One targeted search beats a
   recursive dump of the tree.
2. Read the region you intend to change, plus enough surrounding context to
   keep the edit unambiguous.
3. Edit with the narrowest operation available: replace the specific text, not
   the whole file.
4. Re-read the changed region to confirm the new state.
5. If the repository is version controlled, inspect the diff before committing,
   and keep commits topical.

**Anti-pattern:** rewriting an entire file from a mental model of its contents.
It destroys code you never saw, and the tool still reports success.

## Verification

Done means all of these:

- the edited region reads back with the intended content;
- nothing unrelated was modified (check the diff, not your intention);
- for a commit: the commit exists, contains only the intended files, and the
  working tree state afterwards is what you say it is.

A green tool result is not verification. Verification is reading the artifact.

## Common failures

- Editing a path that looks right but is not the file the host actually uses.
- Ambiguous match: the edit anchor appears more than once, so the wrong site
  changes.
- Trailing-whitespace, encoding, or line-ending mismatch making an anchor fail.
- Assuming a git identity, remote, or branch that does not exist here.
- Treating a permission refusal as a transient error and retrying unchanged.

## Recovery

- Anchor not found: re-read the file, do not loosen the anchor until it matches
  something unintended.
- Wrong site edited: restore from what you read earlier or from version
  control, then redo with a unique anchor.
- Permission denied: report the exact blocked operation and path. Do not seek a
  different tool to perform the denied write.
- Unclear repository state: report the state you can prove and ask before
  history-rewriting operations.

## Related deep references

- `references/projects-and-files.md`
- `references/code-and-shell.md`
- `references/security-and-permissions.md`
- `references/verification.md`
