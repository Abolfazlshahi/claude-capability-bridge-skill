# Claude Capability Bridge Skill

> यह Agent Skill third-party और custom-provider models को Claude Desktop / Cowork / Claude Code जैसे runtimes में उपलब्ध tools को सही तरीके से खोजने, चुनने, चलाने, verify करने और failures से recover करने में मदद करता है।

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · **🇮🇳 हिन्दी** · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## 🎯 उद्देश्य

Runtime files, shell, browser, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts और Subagents जैसी capabilities दे सकता है। लेकिन tool उपलब्ध होना और model का यह जानना कि उसे कब, क्यों और किस क्रम में इस्तेमाल करना है—एक ही बात नहीं है।

यह Skill reusable workflow सिखाता है:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

यह कोई नया tool, permission या runtime capability नहीं बनाता।

## 🧠 पहले vs बाद में

| Skill के बिना | Skill के साथ |
|---|---|
| उपलब्ध tools का पता न चल पाए | वास्तविक capabilities discover करता है |
| गलत tool या गलत order | task के अनुसार उचित surface और sequence |
| शुरुआती success पर रुकना | acceptance criteria के अनुसार final verification |
| एक ही error बार-बार retry करना | failure classify करके material variable बदलना |
| gateway और model capability को मिलाना | transport, runtime और model को अलग रखना |

ये engineering expectations हैं, measured benchmark percentages नहीं।

## 🔌 Custom Provider Architecture

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

`ANTHROPIC_BASE_URL` जैसे configuration endpoint/transport बदल सकते हैं, लेकिन third-party model को अपने-आप Anthropic model नहीं बनाते। Tool Calling, Vision, Context, Reasoning और protocol compatibility अलग-अलग verify करनी चाहिए।

## 🌐 Web App Verification

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Process चलना, port listen करना, HTTP response देना, UI render होना और feature का सही काम करना अलग-अलग states हैं।

## 🧩 Covered Capabilities

- Browser / Claude in Chrome
- Computer Use
- MCP / Remote Connectors
- Local MCP / Desktop Extensions
- Projects / Files / Git
- Skills / Plugins
- Artifacts / Interactive Apps
- Subagents / Scheduled Work
- Local / Cloud / Remote boundaries
- Permissions / Security / Prompt Injection
- Recovery और evidence-based verification
- Custom Provider / Gateway behavior

## 📊 Evaluation

एक ही model, provider, host, tools और task पर तुलना करें:

```text
Bridge OFF  ↔  Bridge ON
```

Tool selection, schema validity, sequencing, verification, recovery, false-success, efficiency और safety मापें।

## 📦 Installation

```bash
python3 scripts/package_skill.py
```

यह `dist/claude-capability-bridge/` बनाता है। Host के Agent Skills mechanism से install करें और supported environment में:

```text
/claude-capability-bridge
```

## 💖 समर्थन / Donations

Donation addresses [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant) repository से लिए गए हैं।

| Network | Address |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

## 📣 Telegram

[@pythash](https://t.me/pythash)

## 📄 License

यह project [MIT License](../LICENSE) के अंतर्गत है।

## 🔗 Links

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
