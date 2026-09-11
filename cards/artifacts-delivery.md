---
id: artifacts-delivery
title: Producing and actually delivering artifacts
summary: Creating a file is not delivering it; use a delivery path the host really provides and confirm the user can open the result.
task_families:
  - delivery
  - documents
signals:
  - download
  - deliver
  - send me
  - give me the file
  - export
  - attach
  - zip
  - pdf
  - csv
  - docx
  - pptx
  - slides
  - report
  - artifact
  - link to the file
conceptual_capabilities:
  - create file
  - expose file to user
  - render artifact
  - attach file to destination
related_references:
  - references/artifact-lifecycle.md
  - references/projects-and-files.md
  - references/interactive-surfaces.md
essentials:
  - Producing a file inside your execution environment is not delivery.
  - A sandbox or local filesystem path is not a download URL; never present it as a link.
  - Delivery is verified when the artifact is reachable through the host's own surface, with the expected name and type.
---

# Producing and actually delivering artifacts

## Purpose

Turn work into something the user can actually open, in the place they expect,
without confusing "the bytes exist somewhere" with "the user received it".

## Use when

- The user asks for a file, document, deck, sheet, archive, image, or report.
- The user asks for a download, an export, or an attachment.
- A result must be handed to a person or placed into a destination surface.

## Do not use when

- The answer belongs in the conversation as text. Do not manufacture a file the
  user never asked for.
- The file is an internal intermediate step only.

## Required evidence

1. A creation capability exists (write file, generate document, render).
2. A **delivery** capability exists and is distinct from creation: download,
   attach, upload, or embed. This is the part most often missing.
3. The destination and audience are known when delivery means placing the file
   somewhere shared.
4. Format constraints of the delivery surface (allowed types, size limits, and
   whether it renders or only stores).

If creation exists but delivery does not, say so before building anything
heavy.

## Live tool-contract source

The exposed creation and delivery tools with their own schemas. What counts as
"delivered" is defined by the host: a returned file reference, an attachment
block, an upload result, or a rendered artifact. Never assume a path string is
enough.

## Minimal workflow

1. Confirm both halves exist: produce **and** deliver.
2. Produce the artifact in the execution environment, in the requested format.
3. Sanity-check it there: non-zero size, correct extension, opens/parses.
4. Invoke the delivery path explicitly and capture what it returns (file
   reference, attachment id, embed handle).
5. Reference the artifact in the reply using the host's own mechanism. Do not
   fabricate a URL.
6. State the file name, format, and where it now lives.

**Anti-pattern:** writing `/tmp/report.pdf` and replying with a markdown link
to that path. The user gets a dead link and no file.

## Verification

Done means:

- the delivery call succeeded and returned a usable reference;
- the artifact's name, type, and size are as intended;
- for a shared destination: it landed in the intended place with the intended
  audience, confirmed by reading back;
- if delivery was impossible, the reply says exactly that and offers the
  content inline instead.

## Common failures

- Format produced by extension only - a `.xlsx` that is really CSV text.
- Delivery surface rejects the type or size, silently or with a vague error.
- Multi-file output delivered as loose files when a single archive was needed.
- Broken relative asset paths, so a rendered artifact loads nothing.
- Placing a file in a broader-audience destination than the source content
  allows, without asking.
- Reporting success from the creation step while the delivery step never ran.

## Recovery

- No delivery capability: report it plainly, then provide the content inline or
  in the smallest supported form.
- Rejected type/size: convert or split deliberately, and say what changed.
- Corrupt artifact: regenerate with a real library for that format instead of
  hand-writing bytes.
- Audience mismatch: stop and ask before publishing narrower content to a
  broader destination.

## Related deep references

- `references/artifact-lifecycle.md`
- `references/projects-and-files.md`
- `references/office-and-collaboration-surfaces.md`
- `references/interactive-surfaces.md`
