# Claude Capability Bridge Skill

> Un Agent Skill para que modelos de terceros y Custom Providers aprendan a descubrir, seleccionar, ejecutar, verificar y recuperar flujos de trabajo dentro de Claude Desktop / Cowork / Claude Code.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · **🇪🇸 Español** · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## 🎯 Objetivo

Un runtime puede exponer archivos, Shell, navegador, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts y Subagents. Tener esas herramientas disponibles no significa que el modelo sepa cuándo usarlas, cómo encadenarlas ni qué evidencia demuestra que el trabajo terminó correctamente.

El Skill enseña un protocolo reutilizable:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

No crea herramientas ni permisos; enseña a usar correctamente las capacidades que el runtime realmente expone.

## 🧠 Antes vs Después

| Sin el Skill | Con el Skill |
|---|---|
| Puede no descubrir herramientas disponibles | Descubre y clasifica las capacidades reales |
| Puede elegir la herramienta o el orden incorrecto | Selecciona una superficie adecuada y una secuencia válida |
| Puede detenerse tras una señal parcial de éxito | Comprueba los criterios de aceptación finales |
| Puede repetir el mismo error | Clasifica el fallo y cambia una variable material |
| Puede confundir gateway, runtime y modelo | Separa transporte, proveedor y capacidades del modelo |

Estas son expectativas de ingeniería, no porcentajes de benchmark ya medidos.

## 🔌 Arquitectura de Custom Provider

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

## 🌐 Verificación de Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Un proceso en ejecución, un puerto escuchando, una respuesta HTTP, una UI renderizada y una funcionalidad correcta son estados diferentes.

## 🧩 Capacidades cubiertas

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

## 📊 Evaluación

Usa el mismo modelo, provider, host, herramientas y tarea:

```text
Bridge OFF  ↔  Bridge ON
```

Mide selección de herramientas, validez del schema, secuenciación, profundidad de verificación, recuperación, falsos positivos de éxito, eficiencia y seguridad.

## 📦 Instalación

```bash
python3 scripts/package_skill.py
```

Genera `dist/claude-capability-bridge/`. Instálalo mediante el mecanismo Agent Skills del host y, cuando exista Slash Command:

```text
/claude-capability-bridge
```

## 📄 Licencia

Publicado bajo [MIT License](../LICENSE).

## 🔗 Enlaces

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
