---
id: mcp-connectors
title: MCP servers, connectors, and external integrations
summary: Use connected integrations from their live schemas and returned identifiers, and distinguish not-exposed from not-configured, not-running, and not-permitted.
task_families:
  - integration
  - external-data
signals:
  - mcp
  - connector
  - integration
  - api
  - jira
  - linear
  - github
  - slack
  - notion
  - database
  - crm
  - ticket
  - issue
  - sync
conceptual_capabilities:
  - list integration tools
  - read external record
  - write external record
  - trigger external action
related_references:
  - references/mcp-and-connectors.md
  - references/mcp-deep-dive.md
  - references/tool-schema-literacy.md
essentials:
  - Only the exposed tool list proves an integration is present; a product name proves nothing.
  - Use identifiers returned by a lookup call; never construct an id from a title or a guess.
  - Separate read, write, and externally visible actions; confirm writes by reading back.
---

# MCP servers, connectors, and external integrations

## Purpose

Get real data out of, and real changes into, external systems through the
integrations this session actually has - without inventing servers, tools, or
identifiers.

## Use when

- The task names an external system, service, or dataset.
- The task needs records, tickets, messages, or documents from elsewhere.
- A change must be made in an external system.

## Do not use when

- The data is already in the conversation or on disk.
- No matching integration is exposed: report the gap and classify it. Do not
  substitute a plausible-sounding tool.
- The task is public web lookup with no account scope involved.

## Required evidence

1. The integration's tools appear in this session's exposed tool list.
2. The specific tool's live schema has been read (`SCHEMA_SEEN`).
3. For writes: the operation is authorized, and the target identifier came from
   a lookup result.
4. Whether the operation is externally visible (posts a message, emails
   someone, changes shared state). Those need explicit intent.

## Live tool-contract source

The exposed tool list plus each tool's own input schema. Documentation for the
underlying product is background knowledge, not a contract: the integration may
expose a narrower surface, different names, or fewer scopes than the product's
public API.

## Minimal workflow

1. Enumerate what is actually exposed for that system. Note the exact tool
   names.
2. Read the schema of the one tool you need. Note required fields, id formats,
   and enum values.
3. Look up the target with a read call. Capture the returned identifier
   verbatim.
4. Perform the smallest write, using the captured identifier.
5. Read back the changed record, or capture the write response as evidence when
   read-back is impossible.
6. Report what changed, in which system, with which identifier.

**Anti-pattern:** guessing an id from a human-readable title, or copying an
argument shape from a similarly named tool on another server. Both produce
confident calls that either fail or hit the wrong record.

## Verification

Done means:

- for a read: the returned data answers the question, and its scope is stated
  (which project, which account, which time range);
- for a write: the new state was confirmed by a read-back or by an explicit
  server acknowledgement that names the affected record;
- for an externally visible action: the user asked for it, and the report says
  exactly what became visible to whom.

## Common failures

- The integration is absent entirely - no such tool in the list.
- Present but not configured: no workspace, project, or credential bound.
- Present and configured but the server is down or unreachable.
- Present but the required scope was never granted (`PERMISSION_BLOCKED`).
- Schema mismatch: wrong field name, wrong enum, missing required parameter.
- Ambiguous lookup returning many candidates, and one is picked arbitrarily.
- Pagination ignored, so a partial result is reported as complete.

## Recovery

- Not connected: report which of the four states it is (not exposed, not
  configured, not running, not permitted). "Not connected" alone is not a
  diagnosis.
- Schema error: re-read the live schema and send the minimal valid call. Do not
  brute-force field names.
- Permission error: report the missing scope. Never try a different tool to
  accomplish the denied operation.
- Ambiguous target: stop and ask, or list candidates. Do not pick silently.
- Repeated failure: escalate to a clear report instead of retrying.

## Related deep references

- `references/mcp-and-connectors.md`
- `references/mcp-deep-dive.md`
- `references/tool-schema-literacy.md`
- `references/security-and-permissions.md`
