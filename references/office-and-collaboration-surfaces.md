# Office and Collaboration Surfaces

These are host surfaces distinct from a generic Cowork/Claude Desktop chat session or a Claude Code terminal session. Each has its own capability model, verification path, permissions, and failure modes. Confirm which surface is active before choosing a workflow.

## Microsoft 365 add-ins: Excel, Word, PowerPoint, Outlook

Claude can operate inside Microsoft 365 add-in surfaces as well as create standalone Office files through code execution. These are not interchangeable mechanisms.

```text
Native Office add-in
→ acts in the active Microsoft 365 application and document
→ may preserve native document structures and application state

File-creation workflow
→ runs through workspace/code execution
→ creates or edits a standalone .docx/.xlsx/.pptx/.pdf
→ does not require the native Office application to be open
```

Skills enabled in Claude can also be available in the Microsoft 365 add-ins. Do not assume that an installed Skill therefore has identical behavior on every surface; adapt the workflow to the active application.

### Per-application verification

"The file changed" is not sufficient evidence of a correct Office task.

```text
Word       → verify the intended text/format and review tracked changes/comments
Excel      → verify formulas, affected cells/ranges, and representative computed output
PowerPoint → verify slide master/layout/theme integrity plus editable chart/diagram state
Outlook    → distinguish draft creation from actual send; verify the final mail state
```

For Excel, formula presence is not equivalent to formula correctness. For PowerPoint, a linked chart can change when its source data changes, so re-check the slide after relevant source updates.

## Outlook write boundaries

Draft, send, calendar, and file operations are distinct capabilities. A visible compose surface does not prove that sending is authorized or exposed.

```text
CREATE DRAFT ≠ SEND MESSAGE
READ MAIL ≠ MODIFY MAILBOX
```

Treat write scopes, admin configuration, client support, and beta/rollout state as time-sensitive. Never promise send/modify behavior from the mere presence of Outlook integration.

## Do not confuse Office add-ins with file-creation Skills

A workspace may contain a document-generation Skill while the user is actually working in an open native Office file.

```text
Need live in-place Office state
→ prefer the native Office surface when exposed and authorized

Need a standalone deliverable
→ use file creation/code/Skill

Need both
→ define which artifact is authoritative and verify each separately
```

See `skills-and-plugins.md`, `artifact-lifecycle.md`, and `verification.md`.

## Claude Tag in Slack

Claude Tag is a Slack-native shared Claude identity, distinct from a plain connector used by another Claude surface to read or search Slack.

```text
Slack connector
→ tool access for a Claude session
→ task remains attached to that session/user context

Claude Tag
→ Claude participates as a shared identity in configured Slack channels
→ people in the channel can steer the same work
→ organization/channel permissions and memory boundaries matter
```

Claude Tag is release-sensitive and currently beta. Channel work, direct messages, and organization-configured access are distinct contexts. Do not assume that the permissions or memory of a private Claude chat carry into a tagged channel.

Proactive follow-up or channel posting is a higher-impact action than passive lookup:

```text
shared-channel output
→ minimize sensitive data
→ respect channel scope
→ verify the destination before posting
```

See `security-and-permissions.md`.

## Voice mode

Voice is a spoken interaction surface, not merely text chat with audio output. Tool access and verification affordances can differ by surface and rollout.

```text
spoken turn
≠
visible transcript + diff + screenshot
```

Before claiming a tool-mediated action is verified, identify what evidence the active voice surface actually exposes. Do not assume every text-chat tool or UI affordance is available during voice interaction.

## Cross-conversation memory vs Skill session state

Do not collapse account-level memory into the Skill's current-session state.

```text
Claude account memory / past-chat retrieval
→ may provide context from other conversations when enabled

Skill session-memory
→ tracks capability and execution state for the current runtime/session

Project files / CLAUDE.md / auto memory
→ persistent project or Code-specific context
```

A model should only claim to remember a past conversation when the current surface actually exposes that memory or retrieval result. Never fabricate history from the existence of a memory feature.

Cross-conversation memory, project-local memory, and runtime state can also have different privacy, scope, and persistence boundaries. Treat each as its own capability.

## Verification discipline

Every surface here is release-, plan-, client-, and permission-sensitive. Follow `source-notes.md`: record the mechanism you actually observed and avoid hardcoding old availability claims.

Use this invariant:

```text
INTEGRATION EXISTS
≠
WRITE CAPABILITY ENABLED
≠
ACTION AUTHORIZED
≠
CONTENT CORRECT
≠
DELIVERY/PERSISTENCE VERIFIED
```

Related references: `security-and-permissions.md`, `skills-and-plugins.md`, `artifact-lifecycle.md`, `session-memory.md`, `runtime-boundary-matrix.md`, `source-notes.md`.
