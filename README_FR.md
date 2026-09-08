# Claude Capability Bridge Skill

> Un Agent Skill qui aide les modèles tiers et Custom Provider à découvrir, sélectionner, exécuter, vérifier et récupérer correctement les workflows d’outils dans Claude Desktop / Cowork / Claude Code.

[🇬🇧 English](./README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · **🇫🇷 Français** · [🇮🇷 فارسی](./README_FA.md)

## 🎯 Objectif

Un runtime peut exposer des fichiers, Shell, navigateur, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts et Subagents. La présence de ces outils ne signifie pas que le modèle sait quand les utiliser, dans quel ordre, ni quelles preuves suffisent pour déclarer la tâche terminée.

Le Skill fournit une procédure réutilisable :

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

Il ne crée ni outil, ni permission, ni accès réseau supplémentaire.

## 🧠 Avant / Après

| Sans le Skill | Avec le Skill |
|---|---|
| Peut ignorer des capacités disponibles | Découvre les capacités réelles du runtime |
| Peut choisir le mauvais outil ou ordre | Sélectionne la surface et la séquence adaptées |
| Peut s’arrêter après un succès partiel | Vérifie le résultat final selon les critères d’acceptation |
| Peut répéter le même échec | Classe l’échec et change une variable pertinente |
| Peut confondre gateway, runtime et modèle | Sépare transport, fournisseur et capacités du modèle |

Ce sont des attentes d’ingénierie, pas des résultats de benchmark déjà mesurés.

## 🔌 Architecture Custom Provider

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

## 🌐 Vérification des Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Processus actif, port en écoute, réponse HTTP, rendu de l’interface et fonctionnement des fonctionnalités sont des états différents.

## 🧩 Capacités couvertes

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

## 📊 Évaluation

Comparez avec le même modèle, provider, host, outils et tâche :

```text
Bridge OFF  ↔  Bridge ON
```

Mesurez Tool Selection, Schema Validity, Sequencing, Verification, Recovery, False Success, Efficiency et Safety.

## 📦 Installation

```bash
python3 scripts/package_skill.py
```

Le dossier `dist/claude-capability-bridge/` est généré. Installez-le via le mécanisme Agent Skills de l’hôte ; lorsque Slash Commands est disponible :

```text
/claude-capability-bridge
```

## 💖 Soutenir le projet

Les adresses de donation proviennent du dépôt [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant).

| Réseau | Adresse |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## 📣 Telegram

Suivez [@pythash](https://t.me/pythash).

## 📄 Licence

Le projet est distribué sous [MIT License](./LICENSE).

## 🔗 Liens

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](./SKILL.md) · [Benchmarks](./benchmarks/README.md) · [References](./references/README.md) · [License](./LICENSE) · [Telegram](https://t.me/pythash)
