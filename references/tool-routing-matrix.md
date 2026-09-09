# Tool Routing Matrix

This matrix teaches selection examples, not a rigid priority order. The acceptance criterion, authoritative state, live availability, permissions, and verification path always win.

| Task / state | Prefer | Why | Avoid as first choice |
|---|---|---|---|
| Query structured GitHub data | GitHub/MCP/connector | Structured, authoritative, narrow | Browser search |
| Download a Gmail attachment | Gmail connector | Direct account/data operation | Screen clicking through Gmail |
| Edit repository files | Filesystem + code/Git | Deterministic and reviewable | Computer use |
| Run tests/build/package command | Shell/code | Deterministic execution + exit status | Browser |
| Test localhost Django/Flask/FastAPI UI | Shell/code + Browser | Shell launches/observes runtime; browser proves rendered behavior | Opening template with `file://` |
| Work in an already-authenticated Chrome tab | Claude in Chrome | Existing tab/session is material | Isolated browser |
| Generic public web research | Built-in browser when available | Clean isolated web context | Reusing unrelated authenticated state |
| Manipulate Photoshop/native GUI | Computer use | GUI state is the actual interface | Browser or coordinate guessing through a narrower API |
| Read/update a structured SaaS record | Connector/MCP | Authoritative structured state | GUI automation |
| Create/share an interactive artifact | Artifact surface | Deliverable lifecycle is artifact-native | Treating creation response as proof |
| Repetitive scheduled cloud work | Scheduled task | Separate scheduled execution context | Assuming today's local process persists |

## Selection test

Ask in order:

```text
1. What state must change or be observed?
2. Which surface is authoritative for that state?
3. Which exposed interface reaches it with the least ambiguity?
4. What permissions/context does it require?
5. What evidence will verify the result?
6. What is the narrowest safe fallback if unavailable?
```

## Important distinctions

```text
connector ≠ browser UI
filesystem ≠ computer-use file manager
built-in browser ≠ Chrome session
browser ≠ server launcher
artifact creation ≠ artifact correctness
visible schema ≠ reliable model tool use
```

If two interfaces are both suitable, prefer the one that is more structured, deterministic, authoritative, and easier to verify. Escalate to a less structured surface only when the narrower surface cannot satisfy the criterion.
