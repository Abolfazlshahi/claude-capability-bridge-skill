# Custom Provider Adaptation

## What this Skill can and cannot fix

A third-party model can receive the same runtime tools as an Anthropic model and still behave differently because tool schemas do not automatically provide the workflow knowledge needed to choose, sequence, verify, and recover from those tools. Anthropic describes Skills as a mechanism for reusable procedural knowledge and workflows. citeturn384783search0turn688364search4

The bridge therefore targets the **knowledge/procedure side** of the gap. It cannot create a missing runtime capability, repair a broken tool adapter, or upgrade a model's fundamental ability to emit valid tool calls.

## Five independent dimensions

### 1. Runtime capability
Can the host actually execute the operation?

### 2. Model awareness
Does the model recognize that an exposed capability exists and what class of problem it solves?

### 3. Schema competence
Can it map current live tool schemas to valid arguments and interpret returned data correctly?

### 4. Procedural competence
Can it sequence tools, maintain state, handle dependencies, and verify the intended outcome?

### 5. Verification competence
Does it know what evidence is sufficient for the user's actual acceptance criterion?

Keep these dimensions separate. A Skill can directly influence 2–5, but only indirectly and probabilistically affects behavior.

## Failure attribution

Use the following diagnosis before changing prompts or references:

```text
Tool is absent from runtime
  → integration/runtime problem

Tool is present but model never considers it
  → awareness/routing problem

Tool is selected but arguments are malformed
  → schema/tool-call problem

Tool call succeeds but sequence is wrong
  → procedural problem

Sequence reaches target but agent stops too early
  → verification problem

Model cannot reliably emit/parse tool calls at all
  → model/provider compatibility ceiling
```

The final category is especially important: a larger Skill may not fix a model whose tool-calling interface, structured-output reliability, context handling, or visual grounding is fundamentally inadequate.

## Attribution protocol

To determine whether this Skill actually helps a model, use paired evaluations with the same runtime surface and task:

```text
             SAME HOST + SAME TOOLS
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
     BASELINE MODEL            + BRIDGE SKILL
          │                         │
          └────────────┬────────────┘
                       ▼
             compare behavior
```

Hold constant:

- user prompt;
- tool schemas;
- project/files;
- permissions;
- browser state;
- network conditions;
- temperature/decoding settings where possible;
- task order and seed where supported.

Measure more than completion:

```text
tool-choice accuracy
schema-valid call rate
unnecessary-call rate
state-tracking accuracy
verification completion
false-success rate
recovery success
critical safety failures
```

Run multiple trials per scenario. One successful run is not evidence of a robust improvement.

## High-value symptoms the bridge should improve

### Tool exists but model ignores it
Load the relevant capability reference and make the trigger/selection condition explicit.

### Model opens browser before using a direct connector
Reinforce the narrowest-capability policy and require it to compare candidates by task fit, observability, determinism, reversibility, and privilege.

### Model starts a server but never tests it
Use the web-app state machine: process → listener → HTTP/app readiness → browser → critical path.

### Model opens the page and declares success
Require an acceptance assertion and, for UI tasks, user-facing evidence.

### Model repeats identical failed calls
Require error classification and a changed variable or tool path before retry.

### Model claims use of unavailable tools
Treat as a capability-state failure; the Skill should force runtime evidence before claims.

## High-value non-fixes

Do **not** respond to a runtime problem by adding prose such as:

```text
"Use browser X"
"There is definitely a tool Y"
"Port is always 3000"
```

Do not hard-code private tool names or infer undocumented host behavior into the Skill.

## Design implication

The strongest bridge is not a huge encyclopedia. It is a compact set of reusable protocols:

```text
condition
→ discover capability
→ inspect live contract
→ select narrowest reliable surface
→ execute
→ observe
→ assert
→ recover if needed
→ verify
→ report evidence
```

Deep references should only be loaded when the task crosses into their capability family. This follows the progressive-disclosure model of Agent Skills. citeturn688364search1

## Runtime variability

Current Claude Desktop/Cowork behavior itself varies by execution surface and availability state. Cloud sessions, local desktop resources, browser surfaces, local MCP/Desktop Extensions, scheduled runs, and connected services do not imply the same resource access. Anthropic explicitly documents these boundaries. citeturn688364search0turn384783search1

Therefore the Skill must remain **runtime-aware, not product-assumption-driven**.

## Success criterion

The bridge is useful only if controlled evaluation shows a repeatable improvement in agent behavior. Documentation size, number of reference files, or perceived completeness are not evidence of effectiveness.

## Non-goals

This project does not attempt to reproduce private system prompts, model weights, proprietary internal safety classifiers, hidden orchestration, or undocumented tool contracts.