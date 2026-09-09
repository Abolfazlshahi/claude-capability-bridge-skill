# Project Recognition Regression Scenario

## Scenario

A workspace contains:

```text
app.py
requirements.txt
templates/reports.html
static/
README.md
```

The README explains that the application is a Python server-rendered web app and provides a command for starting the development server.

## Incorrect behavior

```text
see reports.html
→ open file directly in browser
→ conclude the page works
```

This bypasses server-side rendering and can produce misleading output such as raw template syntax, unresolved variables, missing routes, or broken server-dependent behavior.

## Required behavior

```text
inspect README + project metadata
→ classify server-backed Python project
→ identify declared environment and launch command
→ start the intended server
→ confirm process + listener + HTTP readiness
→ discover actual URL/port
→ open served reports route
→ verify rendered state and representative behavior
```

## Pass criteria

- The project execution model is identified before browser testing.
- `templates/reports.html` is not treated as the application entry point.
- The project's declared launch method is preferred over a remembered command.
- Browser verification targets the served route.
- A page load alone is not treated as proof of feature correctness.
