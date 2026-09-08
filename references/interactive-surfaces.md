# Interactive Surfaces: Connectors, Apps, and Artifacts

Claude's environment is not limited to text-returning tools. Some connected services can render interactive applications inside the conversation, and Cowork can create interactive Artifacts. These surfaces require state-oriented verification.

## Interactive connector / MCP app

When a connector renders an interactive UI:

```text
request
→ connector selects/opens app
→ observe rendered state
→ interact if needed
→ verify resulting state
```

Do not treat the connector's textual acknowledgement as proof that the UI operation succeeded.

Use the interactive surface when the connected service already provides the relevant interface. Do not rebuild an equivalent UI through browser automation unless required.

## Artifact workflow

For generated artifacts, distinguish:

```text
source/generated content
→ artifact created
→ artifact renders
→ artifact behavior works
→ artifact saved/versioned/shared state is correct
```

When the user's acceptance criterion is an interactive dashboard, tracker, comparison tool, or similar deliverable, verify the artifact itself.

## Artifact verification checklist

- artifact exists in the expected artifact surface;
- content is complete;
- interactive controls behave as intended;
- data/state shown to the user is correct;
- links and external integrations behave as intended where relevant;
- the saved/versioned artifact can be reopened when that matters;
- sharing/access scope is not broader than intended.

## Cross-application context

Some connector/app integrations can pass context between applications. Treat the handoff as a trust boundary:

```text
source application
→ transferred context
→ destination application
→ resulting state
```

Verify that the right data crossed the boundary and that unrelated private data did not.

## Key rule

A richer interface does not lower the verification bar. It raises the importance of observing the actual user-facing state.
