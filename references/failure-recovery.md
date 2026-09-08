# Failure Recovery

## Recovery contract

Never respond to uncertainty with blind repetition. Every recovery step must add information or change the execution path.

```text
OBSERVE
→ CLASSIFY
→ MINIMIZE
→ RECOVER/ESCALATE
→ REPRODUCE
→ VERIFY
```

## Failure taxonomy

### Tool unavailable
The required tool is not exposed or disabled.

Action: inspect available capabilities, choose a documented fallback, or report a hard block.

### Permission/approval blocked
The host requires user approval or denies access.

Action: honor the boundary. Do not bypass it. Ask only for the specific authorization needed when the task warrants it.

### Setup/environment failure
Missing runtime, dependency, executable, environment variable, port, or OS support.

Action: inspect concrete evidence, fix setup only when within task scope, then re-run the smallest failing check.

### Process/readiness failure
A server/process starts incorrectly, exits, hangs, or does not become reachable.

Action: inspect stdout/stderr, process state, port ownership, and binding; then correct one cause at a time.

### Navigation/selector failure
Browser or GUI target cannot be found.

Action: re-observe current state, identify the target again, then retry using fresh semantic/visual evidence.

### Application/runtime failure
The program starts but behavior is wrong.

Action: reproduce on the failing path, gather browser/network/log/source evidence, patch the localized cause, and repeat the assertion.

### Data/authentication failure
Credentials, account state, authorization, external data, or server state prevents completion.

Action: never request secrets in chat just to unblock a tool. Use the runtime's authorization mechanism or report the exact block.

### Model/tool-use misunderstanding
The model repeatedly misuses an available tool.

Action: consult the appropriate workflow reference; make tool choice and post-call assertions explicit.

### Safety/authorization boundary
The requested action is sensitive, irreversible, or prohibited.

Action: stop or seek the required explicit authorization. Never weaken safety controls to complete a task.

## Retry policy

Retry only when at least one is true:

- transient failure is plausible;
- fresh state has been observed;
- a meaningful input has changed;
- the service is still becoming ready.

Do not repeat an identical failing action more than once without new evidence.

## Fallback ladder

For technical tasks:

```text
structured API/connector
→ filesystem/code
→ browser
→ computer use
→ manual handoff/report block
```

Escalation should make the task more observable or capable, not merely more complex.

## Stop conditions

Stop automation when:

- the requested criterion is verified;
- the environment becomes ambiguous;
- a safety boundary is reached;
- the remaining work requires unavailable capability;
- repeated attempts are not adding information.

## Reporting a block

A good block report identifies:

```text
WHAT is blocked
WHY it is blocked
WHAT was attempted
WHAT evidence was observed
WHICH capability is missing
WHAT would unblock it
```
