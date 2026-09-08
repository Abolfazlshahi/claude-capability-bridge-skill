# Custom Provider Adaptation

## Problem statement

A third-party model can receive tool definitions from a host and still underperform because it lacks the procedural habits that Anthropic's own models have learned or that the host expects from them.

This Skill addresses the knowledge side of that gap.

## Three independent dimensions

### Runtime capability
Can the host actually execute the tool?

### Model awareness
Does the model know that the tool exists and what class of problem it solves?

### Procedural competence
Does the model know the right sequence, arguments, state checks, and verification steps?

These dimensions must not be conflated.

## Diagnostic patterns

### Sees tools but ignores them
Likely awareness/routing issue. Make capability discovery and trigger conditions explicit.

### Calls browser too early
Likely routing issue. Reinforce connector/API → code/files → browser → computer-use escalation.

### Starts server but never opens it
Likely workflow issue. Use the web-app verification reference.

### Opens app but declares success immediately
Likely verification issue. Require explicit acceptance assertions.

### Repeats broken tool calls
Likely recovery issue. Require classification and a changed variable between retries.

### Requests impossible tool
Likely runtime mismatch. Report unavailable capability instead of simulating it.

## Prompt-independent workflow encoding

The strongest bridge is not a giant list of tool descriptions. Encode reusable state machines:

```text
condition
→ capability check
→ tool selection
→ tool call
→ result inspection
→ assertion
→ next state / recovery
```

This is easier for a wide variety of models to follow and reduces reliance on memorized provider-specific behavior.

## Model variability

Expect differences among models in:

- tool-call syntax discipline;
- ability to infer argument values;
- tendency to overuse GUI actions;
- willingness to verify;
- handling of long-running processes;
- error diagnosis;
- visual grounding;
- persistence across multi-step loops.

The bridge should compensate with explicit checkpoints rather than assuming one model's behavior is universal.

## Runtime variability

Different hosts may expose different names or schemas for conceptually similar capabilities. Never hard-code an invented tool name. Map the reference workflow to the tools actually provided by the current host.

## Compatibility principle

The bridge should be host-neutral in wording but runtime-aware in action:

```text
WHAT capability is needed?
→ Which actual exposed tool provides it?
→ What schema does that tool require?
→ What evidence will confirm success?
```

## Non-goals

This project does not attempt to reproduce proprietary hidden prompts, model weights, internal safety classifiers, private APIs, or undocumented internal orchestration.
