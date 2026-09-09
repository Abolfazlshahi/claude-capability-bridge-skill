# Task Recipes

These are compact procedural recipes. Adapt tool names and arguments to the runtime rather than copying fictional tool syntax.

## Recipe: build a web app and prove it works

```text
inspect repo
→ identify project type + framework + runtime
→ read project instructions / metadata / scripts
→ construct launch contract
→ baseline checks
→ implement
→ start the intended server/runtime
→ confirm listener + HTTP readiness
→ discover real URL/port
→ choose appropriate browser surface
→ inspect rendered app
→ execute critical journey
→ inspect failures
→ patch
→ repeat failed journey
→ deterministic checks
→ visual review
→ cleanup
→ evidence report
```

**Hard gate:** do not open a template or arbitrary HTML file directly in the browser until the project has been classified as intentionally static. For Python/server-rendered projects, test the served application through its actual runtime.

## Recipe: recognize a project before launching it

```text
inspect root files
→ README / explicit instructions
→ package / dependency metadata
→ framework markers
→ entry points
→ declared scripts / task files
→ classify STATIC / SERVER-BACKED / FULL-STACK / UNKNOWN
→ construct launch contract
→ only then choose launch + browser path
```

Never replace a project-declared launch method with a remembered framework command without evidence.

## Recipe: fix a bug reported from a screenshot

```text
inspect screenshot evidence
→ locate likely UI/component
→ inspect source
→ reproduce if possible
→ make minimal patch
→ run deterministic check
→ launch according to project execution model
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
→ execute smallest safe example
→ observe result
→ classify model vs runtime vs provider issue
→ continue only after the capability boundary is understood
```

If the tool itself is absent or the endpoint does not preserve the required protocol, this is an integration problem rather than a Skill-knowledge problem.
