# Task Recipes

These are compact procedural recipes. Adapt tool names and arguments to the runtime rather than copying fictional tool syntax.

## Recipe: build a web app and prove it works

```text
inspect repo
→ detect framework/package manager
→ read scripts
→ baseline checks
→ implement
→ start dev server
→ confirm readiness
→ open real URL
→ inspect UI
→ execute critical journey
→ inspect failures
→ patch
→ repeat failed journey
→ deterministic checks
→ visual review
→ cleanup
→ evidence report
```

## Recipe: fix a bug reported from a screenshot

```text
inspect screenshot evidence
→ locate likely UI/component
→ inspect source
→ reproduce if possible
→ make minimal patch
→ run deterministic check
→ open affected route
→ reproduce original symptom
→ verify corrected state
```

Do not treat a screenshot as proof of the underlying cause; it is evidence of observed appearance.

## Recipe: investigate an API failure

```text
reproduce request
→ capture URL/method/status
→ inspect request/response shape
→ inspect server logs
→ locate client/server boundary
→ patch smallest relevant side
→ re-run request
→ verify user-visible result
```

## Recipe: perform a repository change safely

```text
inspect status
→ identify relevant files
→ read local conventions
→ edit narrowly
→ inspect diff
→ run targeted checks
→ run broader checks when cheap
→ report changed files and verification
```

## Recipe: browser account-context task

```text
determine whether existing authenticated context is required
→ select appropriate browser surface
→ confirm current account/page without exposing sensitive details
→ perform minimum necessary action
→ verify resulting state
→ stop
```

Never move credentials or session tokens between browser surfaces.

## Recipe: GUI-only workflow

```text
discover computer-use capability
→ identify application
→ observe screen
→ perform one short action
→ observe
→ perform next action
→ verify final state
```

Prefer application APIs, connectors, filesystem, shell, or browser interfaces whenever they satisfy the request.

## Recipe: missing capability

```text
required capability
→ is it exposed?
  ├─ yes → use it
  └─ no → is there a narrower fallback?
             ├─ yes → use fallback + disclose scope
             └─ no → stop and report limitation
```

Never fill a capability gap by pretending the action happened.

## Recipe: custom-provider failure

```text
tool exists but model fails to use it
→ inspect tool description/schema
→ identify missing procedural step
→ consult relevant reference
→ execute smallest safe example
→ observe result
→ continue task
```

If the tool itself is absent, this is an integration problem rather than a Skill-knowledge problem.
