# Project Recognition and Launch

## Why this exists

A coding workspace is not automatically a static website. Before opening an HTML file in a browser, determine what the project is, how it is intended to run, and which process actually serves the application.

A browser can render a standalone `.html` file, but that is not equivalent to running a Python, Node, Django, Flask, FastAPI, Rails, PHP, or other server-backed application. Server-side templates, routes, APIs, imports, asset pipelines, environment variables, cookies, sessions, and client-side build steps may all require the project's runtime.

## Recognition phase

Before launching a project, inspect the workspace for authoritative signals:

```text
repository root
→ README / project docs
→ package / build metadata
→ framework markers
→ dependency / lock files
→ declared run scripts
→ application entry points
→ environment/config files
→ existing dev-server or task configuration
```

Do not infer the framework from a single filename when stronger evidence is available.

## Useful recognition signals

| Signal | Likely implication |
|---|---|
| `pyproject.toml`, `requirements.txt`, `Pipfile` | Python project; inspect scripts/entry points and framework dependencies |
| `manage.py`, `django` dependency | Django application; use the project's Django run/config conventions |
| `flask` dependency, `app.py`, `wsgi.py` | Flask-style server application; inspect the declared entry point |
| `fastapi`, `uvicorn` | FastAPI/ASGI application; inspect the project's launch configuration |
| `package.json` | Node/JavaScript project; inspect `scripts` before choosing a command |
| `vite`, `next`, `astro`, `react`, `vue` | frontend/framework dev server or build pipeline; follow project scripts |
| `Cargo.toml` | Rust project; inspect Cargo targets/scripts |
| `go.mod` | Go project; inspect documented run/build commands |
| `pom.xml`, `build.gradle` | JVM project; inspect the declared build/run task |
| `composer.json` | PHP project; inspect framework and server instructions |
| `Gemfile` | Ruby project; inspect Bundler/Rails or other app commands |
| static-only `index.html` with no runtime markers | standalone/static site may be directly previewable |

These are recognition hints, not commands. Project documentation and declared scripts take precedence.

## Launch contract

Before browser verification, construct a small launch contract:

```text
PROJECT TYPE
FRAMEWORK
PACKAGE / ENVIRONMENT MANAGER
ENTRY POINT
INTENDED DEV / PREVIEW COMMAND
BIND ADDRESS
PORT / URL
REQUIRED ENVIRONMENT
READINESS SIGNAL
SHUTDOWN / OWNERSHIP METHOD
```

A missing field is a reason to inspect further, not to invent a conventional value.

## Static vs served application

Use this distinction explicitly:

```text
STATIC DOCUMENT
→ direct file preview may be sufficient

SERVER APPLICATION
→ start the intended application runtime
→ verify listener / HTTP readiness
→ open the served URL

FULL-STACK APPLICATION
→ start required services
→ verify service dependencies
→ open the actual frontend URL
→ exercise a real data/auth/user flow
```

When server-rendered templates are present, opening the template source as a `file://` URL is not application testing.

## Python-specific workflow

For Python projects:

1. Inspect `pyproject.toml`, `requirements*.txt`, `manage.py`, `app.py`, `wsgi.py`, `asgi.py`, README instructions, and project scripts.
2. Identify the intended environment (`venv`, Poetry, uv, Pipenv, Conda, or documented alternative).
3. Prefer the project's documented or scripted launch command.
4. Start the server from the correct project root and environment.
5. Wait for a real readiness signal.
6. Discover the actual URL/port from output or configuration.
7. Browse the served application, not a template file directly.

Do not blindly assume `python app.py`, `flask run`, `uvicorn main:app`, port `8000`, or port `5000` unless project evidence supports it.

## Django-specific workflow

For Django projects:

```text
identify manage.py/settings module
→ inspect documented environment requirements
→ install/use declared dependencies
→ run project's development command
→ confirm HTTP readiness
→ browse the actual route
→ exercise a representative request/form/auth flow
```

Templates under `templates/` are source artifacts, not normally the browser entry point.

## Node/frontend workflow

For Node projects:

```text
inspect package.json
→ choose declared script
→ install only required dependencies
→ start dev/preview server
→ capture actual URL/port
→ inspect rendered app
```

A static HTML file inside a Vite/Next/Astro/React/Vue project does not automatically represent the running application.

## Multi-service projects

When a frontend depends on an API/database/worker:

```text
map service dependencies
→ determine which services are required for the target flow
→ start only owned/needed services
→ verify each required readiness signal
→ test through the real integration boundary
```

Do not report a frontend-only page load as full-stack success when the requested feature requires the backend.

## When direct file preview is valid

Direct browser opening can be appropriate when the project is intentionally static and the acceptance criteria are limited to static rendering. Even then, verify relative assets, client-side behavior, and any constraints imposed by `file://` access.

## Failure diagnosis

If the browser shows a raw template, source text, missing variables, broken imports, or a route that should be server-rendered:

```text
STOP browser iteration
→ reclassify project
→ inspect launch contract
→ start intended runtime
→ verify HTTP readiness
→ open served URL
→ retest
```

Do not patch the browser URL repeatedly while the wrong execution model is still in use.

## Evidence

A credible project-launch claim records evidence for:

```text
project recognized
→ intended command identified
→ owned process started
→ listener confirmed
→ HTTP response confirmed
→ browser opened actual served URL
→ critical behavior exercised
```

"The HTML opened" is not sufficient evidence for a server-backed application's correctness.
