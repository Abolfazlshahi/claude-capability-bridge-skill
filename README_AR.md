# Claude Capability Bridge Skill

> مهارة Agent Skill تساعد نماذج الطرف الثالث وCustom Provider على اكتشاف الأدوات المتاحة داخل Claude Desktop / Cowork / Claude Code، واختيارها وتشغيلها والتحقق من نتائجها والتعافي من الأخطاء.

[🇬🇧 English](./README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · **🇸🇦 العربية** · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## 🎯 الفكرة

قد يوفّر الـRuntime أدوات للملفات وShell والمتصفح وChrome وComputer Use وMCP وConnectors وProjects وSkills وPlugins وArtifacts وSubagents. لكن وجود الأداة لا يعني أن النموذج يعرف متى يستخدمها، أو بأي ترتيب، أو كيف يثبت أن المهمة اكتملت فعلاً.

تعلّم المهارة نموذجاً عملياً واضحاً:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

المهارة لا تنشئ صلاحيات أو أدوات جديدة؛ بل تعلّم النموذج استخدام ما يتيحه الـRuntime فعلياً.

## 🧠 قبل وبعد

| بدون Skill | مع Skill |
|---|---|
| قد لا يكتشف الأدوات المتاحة | يبدأ باكتشاف القدرات الفعلية |
| قد يختار أداة أو ترتيباً خاطئاً | يختار السطح والأداة المناسبين |
| قد يتوقف عند نجاح جزئي | يتحقق من معيار القبول النهائي |
| قد يكرر نفس الخطأ | يصنّف الخطأ ويغيّر المتغير المؤثر |
| قد يخلط بين Gateway وRuntime وModel | يفصل النقل والمزوّد وقدرات النموذج |

هذه توقعات هندسية وليست نسب Benchmark مقاسة مسبقاً.

## 🔌 بنية Custom Provider

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

إعدادات مثل `ANTHROPIC_BASE_URL` تغيّر endpoint أو مسار النقل، لكنها لا تجعل النموذج الخارجي مطابقاً تلقائياً لنموذج Anthropic. يجب التحقق بشكل مستقل من Tool Calling وVision وContext وReasoning وتوافق البروتوكول.

## 🌐 التحقق من Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

تشغيل العملية، الاستماع على المنفذ، استجابة HTTP، ظهور الواجهة وعمل الميزة هي حالات مختلفة.

## 🧩 القدرات المشمولة

- Browser / Claude in Chrome
- Computer Use
- MCP / Remote Connectors
- Local MCP / Desktop Extensions
- Projects / Files / Git
- Skills / Plugins
- Artifacts / Interactive Apps
- Subagents / Scheduled Work
- حدود Local / Cloud / Remote
- Permissions / Security / Prompt Injection
- Recovery والتحقق القائم على الأدلة
- Custom Provider / Gateway behavior

## 📊 التقييم

قارن باستخدام نفس النموذج والمزوّد والـHost والأدوات والمهمة:

```text
Bridge OFF  ↔  Bridge ON
```

قس Tool Selection وSchema Validity وSequencing وVerification وRecovery وFalse Success وEfficiency وSafety.

## 📦 التثبيت

```bash
python3 scripts/package_skill.py
```

سيتم إنشاء `dist/claude-capability-bridge/`. ثبّت المجلد عبر آلية Agent Skills الخاصة بالـHost، ثم استخدم عند دعم Slash Commands:

```text
/claude-capability-bridge
```

## 💖 دعم المشروع

عناوين التبرع مأخوذة من مستودع [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant).

| الشبكة | العنوان |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## 📣 Telegram

تابع [@pythash](https://t.me/pythash).

## 📄 الترخيص

المشروع منشور بموجب [MIT License](./LICENSE).

## 🔗 روابط

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](./SKILL.md) · [Benchmarks](./benchmarks/README.md) · [References](./references/README.md) · [License](./LICENSE) · [Telegram](https://t.me/pythash)
