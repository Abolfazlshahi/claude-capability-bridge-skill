# Claude Capability Bridge Skill

> Un Agent Skill para que modelos de terceros y Custom Providers aprendan a descubrir, seleccionar, ejecutar, verificar y recuperar flujos de trabajo dentro de Claude Desktop / Cowork / Claude Code.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · **🇪🇸 Español** · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## Objetivo

Un runtime puede exponer archivos, Shell, navegador, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts y Subagents. Tener esas herramientas disponibles no significa que el modelo sepa cuándo usarlas, cómo encadenarlas ni qué evidencia demuestra que el trabajo terminó correctamente.

El Skill enseña un protocolo reutilizable:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

No crea herramientas ni permisos; enseña a usar correctamente las capacidades que el runtime realmente expone.

## Antes vs Después

| Sin el Skill | Con el Skill |
|---|---|
| Puede no descubrir herramientas disponibles | Descubre y clasifica las capacidades reales |
| Puede elegir la herramienta o el orden incorrecto | Selecciona una superficie adecuada y una secuencia válida |
| Puede detenerse tras una señal parcial de éxito | Comprueba los criterios de aceptación finales |
| Puede repetir el mismo error | Clasifica el fallo y cambia una variable material |
| Puede confundir gateway, runtime y modelo | Separa transporte, proveedor y capacidades del modelo |

Estas son expectativas de ingeniería, no porcentajes de benchmark ya medidos.

## Arquitectura de Custom Provider

```text
Claude Desktop / Claude Code
            ↓
     Agent Runtime + Tools
            ↓
      Anthropic API Contract
            ↓
      Gateway / Proxy / Adapter
            ↓
       Third‑Party Model
```

Configuraciones como `ANTHROPIC_BASE_URL` cambian el endpoint o transporte, pero no hacen que un modelo de terceros sea equivalente a un modelo Anthropic. Tool Calling, Vision, Context, Reasoning y compatibilidad con funciones de protocolo deben verificarse por separado.

## Verificación de Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Un proceso en ejecución, un puerto escuchando, una respuesta HTTP, una UI renderizada y una funcionalidad correcta son estados diferentes. Una plantilla abierta con `file://` no equivale a ejecutar la aplicación real.

## Capacidades cubiertas

- Browser / Claude in Chrome
- Computer Use
- MCP / Remote Connectors
- Local MCP / Desktop Extensions
- Projects / Files / Git
- Skills / Plugins
- Artifacts / Interactive Apps
- Subagents / Scheduled Work
- Límites Local / Cloud / Remote
- Permisos / Seguridad / Prompt Injection
- Recuperación de errores y verificación basada en evidencias
- Comportamiento de Custom Providers y gateways

## Entrega adaptativa en Claude Code

El Skill no puede obligar universalmente a un host a invocarlo. Para Claude Code, el repositorio incluye un motor de hooks opcional que añade contexto solo cuando resulta útil, en lugar de repetir un recordatorio en cada turno.

| Evento | Comportamiento |
|---|---|
| `SessionStart` | Emite una vez el kernel compacto y el catálogo de cards |
| `SessionStart` tras compact | Rehidrata el protocolo mínimo y marca observaciones anteriores como obsoletas |
| `UserPromptSubmit` | Normalmente no emite nada; como máximo inyecta una card relevante |
| `PostToolUseFailure` | Clasifica el fallo y proporciona orientación limitada para el siguiente paso |

Modos: `adaptive` (predeterminado), `session-only`, `legacy-every-turn` y `off`.

La entrega del hook es best-effort: el hook no puede demostrar que el host realmente insertó su texto en el contexto del modelo.

## Evaluación y benchmarking

La eficacia no se afirma de forma universal. Debe demostrarse con ejecuciones controladas:

```text
A  control                    sin Skill y sin hooks
B  skill only                 Skill instalado, hooks no registrados
C  skill + adaptive           configuración predeterminada
D  skill + legacy-every-turn  recordatorio de cada turno para comparación
```

Mantén constantes el modelo, host, herramientas, provider, workspace, texto de tarea y criterio de éxito. Separa sesiones cold y warm. Mide Tool Selection, Schema Validity, Sequencing, Verification, Recovery, False Success, Efficiency y Safety.

> **Sin porcentajes inventados:** hasta que existan ejecuciones live emparejadas, cualquier mejora es una hipótesis de ingeniería, no un resultado experimental.

## Instalación

### Agent Skill

```bash
python3 scripts/package_skill.py
```

Genera `dist/claude-capability-bridge/`. Instálalo mediante el mecanismo Agent Skills del host.

### Plugin de Claude Code

```bash
python3 scripts/package_claude_code_plugin.py
```

Genera `dist/claude-capability-bridge-plugin/`, con el mismo Skill y el runtime opcional de hooks.

### Registro manual de hooks

Copia las entradas de [`bootstrap/settings.json.example`](../bootstrap/settings.json.example) en la configuración del host y selecciona `CLAUDE_CAPABILITY_BRIDGE_MODE`. El plugin registra sus propios hooks.

## Estructura del proyecto

```text
claude-capability-bridge-skill/
├── SKILL.md
├── profiles/
├── cards/
├── references/
├── bootstrap/
├── config/
├── docs/
├── scripts/
├── tests/python/
├── benchmarks/
├── evals/
├── assets/
├── i18n/
├── CHANGELOG.md
└── LICENSE
```

El proyecto usa divulgación progresiva:

```text
kernel → runtime profile → task card → reference → execution → verification
```

## Validación

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 scripts/run_tests.py
python3 bootstrap/bridge_hook.py --selftest
python3 scripts/analyze_trace.py --selftest
```

Estas comprobaciones cubren estructura, referencias, packaging, contratos de contenido, hooks, ciclo de vida del estado y análisis de traces sintéticos. No demuestran el comportamiento live del modelo, una ejecución real dentro de Claude Code, Windows completo ni el comportamiento de caché de un provider.

## Apoyar el proyecto

Las direcciones de donación proceden del repositorio [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant).

| Red | Dirección |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## Telegram

[@pythash](https://t.me/pythash)

## Licencia

Publicado bajo [MIT License](../LICENSE).

## Enlaces

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
