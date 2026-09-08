# Skills and Plugins

## Skills

A Skill is a directory containing a required `SKILL.md` plus optional references, scripts, and assets. It is a packaging mechanism for procedural knowledge.

The bridge should use Skills to teach workflows that a raw model may not reliably infer from tool schemas alone.

## Progressive disclosure

Keep the main Skill file focused on:

- identity/purpose;
- trigger conditions;
- core invariants;
- routing rules;
- links to deeper references.

Move large workflow manuals, examples, checklists, and background material into `references/`. Keep deterministic helper code in `scripts/`.

Do not load every reference for every request. Consult only the capability family relevant to the current task.

## Triggering

The description should clearly state:

- what capability gap the Skill addresses;
- task families where it applies;
- major tools/workflows it teaches;
- that it is useful for custom/third-party models.

Avoid a vague description such as "helps with Claude". Triggering should be tied to observable task intent.

## Skill vs runtime capability

A Skill can teach:

- tool selection;
- argument patterns;
- workflow ordering;
- verification;
- recovery;
- safety boundaries;
- reusable scripts.

A Skill cannot itself create an unavailable browser, computer-use endpoint, MCP server, connector, filesystem mount, or code-execution runtime.

## Installing specialized Skills

Before performing a specialized task, inspect whether a more specific installed Skill already owns it. The bridge is an orchestration layer and should yield to specialized instructions where they are more precise.

Examples:

```text
PDF task
→ use PDF-specific Skill if present

Spreadsheet task
→ use spreadsheet-specific Skill if present

Web app verification
→ use this bridge + webapp verification references
```

## Plugins

Plugins package broader functionality, commonly including Skills and integrations. When a plugin exposes a direct connector or specialized workflow, prefer its supported path over rebuilding the same operation through GUI automation.

Treat locally installed plugin/MCP code as executable software. Only use trusted sources and respect organization controls.

## Reference hygiene

A reference should answer a concrete question. Good examples:

- How do I choose browser vs Chrome?
- How do I test a localhost web app?
- How do I recover from a failed tool call?
- How do I validate an MCP mutation?

Avoid repeating the same general instructions in many references; keep one canonical source and link to it from the bridge.

## Model adaptation

For a weaker or unfamiliar third-party model, make critical sequences explicit. Prefer structured mini-protocols:

```text
WHEN condition
→ CHECK capability
→ CALL tool
→ OBSERVE result
→ ASSERT invariant
→ CONTINUE or RECOVER
```

This converts hidden procedural knowledge into explicit, reusable behavior without pretending the model has Anthropic-native tool habits.