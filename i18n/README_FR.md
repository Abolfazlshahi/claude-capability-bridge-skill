# Claude Capability Bridge Skill

> Un Agent Skill qui aide les modèles tiers et Custom Provider à découvrir, sélectionner, exécuter, vérifier et récupérer correctement les workflows d’outils dans Claude Desktop / Cowork / Claude Code.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · **🇫🇷 Français** · [🇮🇷 فارسی](./README_FA.md)

## Objectif

Un runtime peut exposer des fichiers, Shell, navigateur, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts et Subagents. La présence de ces outils ne signifie pas que le modèle sait quand les utiliser, dans quel ordre, ni quelles preuves suffisent pour déclarer la tâche terminée.

Le Skill fournit une procédure réutilisable :

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

Il ne crée ni outil, ni permission, ni accès réseau supplémentaire.

## Avant / Après

| Sans le Skill | Avec le Skill |
|---|---|
| Peut ignorer des capacités disponibles | Découvre les capacités réelles du runtime |
| Peut choisir le mauvais outil ou ordre | Sélectionne la surface et la séquence adaptées |
| Peut s’arrêter après un succès partiel | Vérifie le résultat final selon les critères d’acceptation |
| Peut répéter le même échec | Classe l’échec et change une variable pertinente |
| Peut confondre gateway, runtime et modèle | Sépare transport, fournisseur et capacités du modèle |

Ce sont des attentes d’ingénierie, pas des résultats de benchmark déjà mesurés.

## Architecture Custom Provider

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

`ANTHROPIC_BASE_URL` peut modifier l’endpoint ou le transport, mais ne rend pas automatiquement un modèle tiers équivalent à un modèle Anthropic. Tool Calling, Vision, Context, Reasoning et compatibilité des protocoles doivent être vérifiés séparément.

## Vérification des Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Processus actif, port en écoute, réponse HTTP, rendu de l’interface et fonctionnement des fonctionnalités sont des états différents. Ouvrir un template serveur via `file://` ne revient pas à exécuter l’application réelle.

## Capacités couvertes

- Browser / Claude in Chrome
- Computer Use
- MCP / Remote Connectors
- Local MCP / Desktop Extensions
- Projects / Files / Git
- Skills / Plugins
- Artifacts / Interactive Apps
- Subagents / Scheduled Work
- Limites Local / Cloud / Remote
- Permissions / Security / Prompt Injection
- Recovery et vérification fondée sur des preuves
- Comportement Custom Provider / Gateway

## Livraison adaptative dans Claude Code

Le Skill ne peut pas forcer universellement un host à l’invoquer. Pour Claude Code, le dépôt fournit un moteur de hooks optionnel qui ajoute du contexte seulement lorsqu’il est utile au lieu de répéter un rappel à chaque tour.

| Événement | Comportement |
|---|---|
| `SessionStart` | Émet une fois le kernel compact et le catalogue des cards |
| `SessionStart` après compact | Réhydrate le protocole minimal et marque les observations précédentes comme obsolètes |
| `UserPromptSubmit` | En général aucun output ; au plus une card de capacité correspondante |
| `PostToolUseFailure` | Classe l’échec et fournit une orientation limitée pour l’étape suivante |

Modes : `adaptive` (par défaut), `session-only`, `legacy-every-turn`, `off`.

La livraison du hook est best-effort : le hook ne peut pas prouver que le host a réellement inséré son texte dans le contexte du modèle.

## Évaluation et benchmarking

Le projet ne prétend pas améliorer tous les modèles. L’effet doit être démontré par des exécutions contrôlées :

```text
A  control                    sans Skill et sans hooks
B  skill only                 Skill installé, hooks non enregistrés
C  skill + adaptive           configuration par défaut
D  skill + legacy-every-turn  rappel à chaque tour pour comparaison
```

Gardez constants le modèle, le host, les outils, le provider, le workspace, le texte de tâche et les critères de succès. Séparez les sessions cold et warm. Mesurez Tool Selection, Schema Validity, Sequencing, Verification, Recovery, False Success, Efficiency et Safety.

> **Pas de pourcentages inventés :** tant qu’il n’existe pas de paired live runs, toute amélioration reste une hypothèse d’ingénierie.

## Installation

### Agent Skill

```bash
python3 scripts/package_skill.py
```

Génère `dist/claude-capability-bridge/`, à installer via le mécanisme Agent Skills de l’host.

### Plugin Claude Code

```bash
python3 scripts/package_claude_code_plugin.py
```

Génère `dist/claude-capability-bridge-plugin/` avec le même Skill et le runtime optionnel des hooks.

### Enregistrement manuel des hooks

Copiez les entrées de [`bootstrap/settings.json.example`](../bootstrap/settings.json.example) dans les réglages du host et choisissez `CLAUDE_CAPABILITY_BRIDGE_MODE`. Le plugin enregistre ses propres hooks.

## Structure du projet

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

Divulgation progressive :

```text
kernel → runtime profile → task card → reference → execution → verification
```

## Validation

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 scripts/run_tests.py
python3 bootstrap/bridge_hook.py --selftest
python3 scripts/analyze_trace.py --selftest
```

Ces vérifications couvrent la structure, les références, le packaging, les contrats de contenu, les hooks, le cycle de vie de l’état et l’analyse de traces synthétiques. Elles ne prouvent pas le comportement live du modèle, une exécution réelle dans Claude Code, le support Windows complet ou le comportement du cache d’un provider.

## Soutenir le projet

Les adresses de donation proviennent du dépôt [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant).

| Réseau | Adresse |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## Telegram

Suivez [@pythash](https://t.me/pythash).

## Licence

Le projet est distribué sous [MIT License](../LICENSE).

## Liens

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
