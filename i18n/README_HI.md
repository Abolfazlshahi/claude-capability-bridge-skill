# Claude Capability Bridge Skill

> यह Agent Skill third-party और custom-provider models को Claude Desktop / Cowork / Claude Code जैसे runtimes में उपलब्ध tools को सही तरीके से खोजने, चुनने, चलाने, verify करने और failures से recover करने में मदद करता है।

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · **🇮🇳 हिन्दी** · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## उद्देश्य

Runtime files, shell, browser, Chrome, Computer Use, MCP, Connectors, Projects, Skills, Plugins, Artifacts और Subagents जैसी capabilities दे सकता है। लेकिन tool उपलब्ध होना और model का यह जानना कि उसे कब, क्यों और किस क्रम में इस्तेमाल करना है—एक ही बात नहीं है।

यह Skill reusable workflow सिखाता है:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

यह कोई नया tool, permission या runtime capability नहीं बनाता।

## पहले vs बाद में

| Skill के बिना | Skill के साथ |
|---|---|
| उपलब्ध tools का पता न चल पाए | वास्तविक capabilities discover करता है |
| गलत tool या गलत order | task के अनुसार उचित surface और sequence |
| शुरुआती success पर रुकना | acceptance criteria के अनुसार final verification |
| एक ही error बार-बार retry करना | failure classify करके material variable बदलना |
| gateway और model capability को मिलाना | transport, runtime और model को अलग रखना |

ये engineering expectations हैं, measured benchmark percentages नहीं।

## Custom Provider Architecture

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

## Web App Verification

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

Process चलना, port listen करना, HTTP response देना, UI render होना और feature का सही काम करना अलग-अलग states हैं। `file://` से कोई server-side template खोलना वास्तविक application चलाने के बराबर नहीं है।

## Covered Capabilities

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

## Claude Code Adaptive Delivery

Skill किसी host को सार्वभौमिक रूप से अपने invocation के लिए मजबूर नहीं कर सकता। Claude Code के लिए repository में optional hook engine है जो हर turn पर reminder दोहराने के बजाय तभी context जोड़ता है जब वह उपयोगी हो।

| Event | व्यवहार |
|---|---|
| `SessionStart` | session में compact kernel और card catalogue एक बार देता है |
| `SessionStart` after compact | minimum protocol फिर देता है और पुराने observations को stale mark करता है |
| `UserPromptSubmit` | सामान्यतः कुछ नहीं; अधिकतम एक matching capability card inject करता है |
| `PostToolUseFailure` | failure classify करके bounded next-step guidance देता है |

Modes: `adaptive` (default), `session-only`, `legacy-every-turn`, `off`।

Hook delivery best-effort है; hook यह साबित नहीं कर सकता कि host ने text को model context में डाल दिया।

## Evaluation और Benchmarking

Skill को हर model के लिए बेहतर होने का दावा नहीं किया जाता। Controlled runs से प्रभाव मापना चाहिए:

```text
A  control                    बिना Skill और बिना hooks
B  skill only                 Skill installed, hooks registered नहीं
C  skill + adaptive           default configuration
D  skill + legacy-every-turn  comparison के लिए हर-turn reminder
```

Model, host, tools, provider, workspace, task wording और success criteria स्थिर रखें। cold और warm sessions अलग experiments हैं। Tool Selection, Schema Validity, Sequencing, Verification, Recovery, False Success, Efficiency और Safety मापें।

> **Fake percentages नहीं:** paired live runs के बिना improvement सिर्फ engineering hypothesis है।

## Installation

### Agent Skill

```bash
python3 scripts/package_skill.py
```

`dist/claude-capability-bridge/` बनता है। इसे host के Agent Skills mechanism से install करें।

### Claude Code Plugin

```bash
python3 scripts/package_claude_code_plugin.py
```

`dist/claude-capability-bridge-plugin/` बनता है जिसमें वही Skill और optional hook runtime होता है।

### Manual hook registration

[`bootstrap/settings.json.example`](../bootstrap/settings.json.example) की entries host settings में copy करें और `CLAUDE_CAPABILITY_BRIDGE_MODE` चुनें। Plugin अपने hooks खुद register करता है।

## Project Structure

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

Progressive disclosure:

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

ये checks structure, references, packaging, content contracts, hooks, state lifecycle और synthetic trace analysis को cover करते हैं। ये live model behavior, real Claude Code execution, full Windows support या provider cache behavior साबित नहीं करते।

## समर्थन / Donations

Donation addresses [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant) repository से लिए गए हैं।

| Network | Address |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## Telegram

[@pythash](https://t.me/pythash)

## License

यह project [MIT License](../LICENSE) के अंतर्गत है।

## Links

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
