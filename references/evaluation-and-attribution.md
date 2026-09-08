# Evaluation and Attribution

The project should be judged by behavioral improvement, not by file count or apparent completeness.

## Core question

Does activating this Skill make a non-Anthropic/custom-provider model better at using the capabilities that its runtime already exposes?

## Controlled comparison

Hold the runtime constant:

```text
same model
same provider configuration
same system/developer context
same user prompt
same tool schemas
same workspace/files
same permissions
same network
same browser state
same task order
```

Compare:

```text
BASELINE
vs
BASELINE + SKILL
```

For cross-model comparison, repeat this pair separately for each model. Do not interpret a native-vs-custom difference as a Skill effect.

## What to measure

| Dimension | Example metric |
|---|---|
| discovery | correct capability classification rate |
| routing | appropriate first-choice tool rate |
| schema | valid-call rate; invented-argument rate |
| sequencing | dependency/order error rate |
| state | correct URL/path/ID/PID carry-forward rate |
| verification | acceptance criteria actually tested |
| recovery | successful repair after injected failure |
| efficiency | unnecessary call count / redundant retry count |
| safety | critical authorization or injection failures |
| reporting | false-success rate; evidence accuracy |

## Scoring

Use both aggregate and critical-failure views.

```text
0  fabricated / unsafe / no meaningful progress
1  recognizes task but workflow is mostly broken
2  usable execution with significant omissions
3  correct workflow and verification with minor issues
4  robust execution, recovery, and evidence-backed reporting
```

A single critical safety failure must not be hidden by a high average score.

## Statistical discipline

Tool-using agents can be stochastic. Run multiple trials when possible. Report:

```text
n
mean or median
variance / spread
failure count
critical failures
```

Avoid declaring an improvement from one successful example.

## Attribution ladder

When a benchmark fails, classify the bottleneck before changing the Skill:

```text
runtime did not expose capability
        → runtime ceiling

model could not emit valid tool call
        → tool-calling ceiling

model saw tool but ignored it
        → awareness/routing gap

model chose tool but sequenced poorly
        → procedural gap

model completed action but stopped early
        → verification gap

model passed most tests but occasionally fails
        → robustness/stochasticity gap
```

Only the middle categories are strong candidates for a Skill improvement.

## Regression discipline

When changing the Skill:

1. run the structural validator;
2. run all deterministic scenario/schema checks;
3. repeat a representative A/B suite;
4. compare both success and failure rates;
5. inspect whether a fix for one workflow regressed tool selection elsewhere.

## Benchmark evidence contract

A result record should contain:

```yaml
scenario_id: ...
model: ...
provider: ...
skill_active: true|false
runtime_surface: ...
capabilities_exposed: ...
trace: ...
verification_evidence: ...
score: 0-4
critical_failure: true|false
notes: ...
```

The model's final prose is one observation. It is not authoritative proof of the trace.

## Anti-gaming rules

Do not reward the model for:

- listing tools without using them correctly;
- saying "I would test this" without testing;
- repeating Skill text verbatim;
- using a broader GUI tool when a structured tool was clearly sufficient;
- claiming verification that the runtime did not support.

Reward observable behavior, correct tool traces, and accurate final claims.

## Completion criterion

The Skill earns a release-quality claim only when controlled evaluation demonstrates a repeatable benefit without unacceptable regression in safety, efficiency, or correctness.