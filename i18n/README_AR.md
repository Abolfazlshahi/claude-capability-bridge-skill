# Claude Capability Bridge Skill

> مهارة Agent Skill تساعد نماذج الطرف الثالث وCustom Provider على اكتشاف الأدوات المتاحة داخل Claude Desktop / Cowork / Claude Code، واختيارها وتشغيلها والتحقق من نتائجها والتعافي من الأخطاء.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · **🇸🇦 العربية** · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## الفكرة

قد يوفّر الـRuntime أدوات للملفات وShell والمتصفح وChrome وComputer Use وMCP وConnectors وProjects وSkills وPlugins وArtifacts وSubagents. لكن وجود الأداة لا يعني أن النموذج يعرف متى يستخدمها، أو بأي ترتيب، أو كيف يثبت أن المهمة اكتملت فعلاً.

تعلّم المهارة نموذجاً عملياً واضحاً:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

المهارة لا تنشئ صلاحيات أو أدوات جديدة؛ بل تعلّم النموذج استخدام ما يتيحه الـRuntime فعلياً.

## قبل وبعد

| بدون Skill | مع Skill |
|---|---|
| قد لا يكتشف الأدوات المتاحة | يبدأ باكتشاف القدرات الفعلية |
| قد يختار أداة أو ترتيباً خاطئاً | يختار السطح والأداة المناسبين |
| قد يتوقف عند نجاح جزئي | يتحقق من معيار القبول النهائي |
| قد يكرر نفس الخطأ | يصنّف الخطأ ويغيّر المتغير المؤثر |
| قد يخلط بين Gateway وRuntime وModel | يفصل النقل والمزوّد وقدرات النموذج |

هذه توقعات هندسية وليست نسب Benchmark مقاسة مسبقاً.

## بنية Custom Provider

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

## التحقق من Web Apps

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

تشغيل العملية، الاستماع على المنفذ، استجابة HTTP، ظهور الواجهة وعمل الميزة هي حالات مختلفة. فتح قالب خادم عبر `file://` لا يعادل تشغيل التطبيق الحقيقي.

## القدرات المشمولة

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

## التسليم التكيفي في Claude Code

لا يستطيع الـSkill إجبار كل Host على استدعائه. لذلك يتضمن المستودع لـClaude Code محرك hooks اختيارياً يضيف السياق فقط عندما يكون مفيداً بدلاً من تكرار التذكير في كل دورة.

| الحدث | السلوك |
|---|---|
| `SessionStart` | إصدار kernel المختصر وكتالوج البطاقات مرة واحدة لكل session |
| `SessionStart` بعد compact | إعادة الحد الأدنى من البروتوكول ووضع الملاحظات السابقة كـstale |
| `UserPromptSubmit` | غالباً لا يخرج شيئاً، وبحد أقصى يحقن capability card واحدة مطابقة |
| `PostToolUseFailure` | تصنيف الفشل وتقديم إرشاد محدود للخطوة التالية |

الأنماط: `adaptive` (الافتراضي)، `session-only`، `legacy-every-turn`، `off`.

تسليم hook هو best-effort ولا يستطيع الـhook إثبات أن الـHost أدخل النص فعلاً في سياق النموذج.

## التقييم وBenchmarking

لا يدّعي المشروع أن الـSkill يحسن كل نموذج. يجب إثبات ذلك بتشغيلات مضبوطة:

```text
A  control                    بدون Skill وبدون hooks
B  skill only                 تثبيت Skill بدون تسجيل hooks
C  skill + adaptive           الإعداد الافتراضي
D  skill + legacy-every-turn  تذكير كل دورة للمقارنة
```

يجب تثبيت النموذج والـHost والأدوات والـprovider والـworkspace ونص المهمة ومعايير النجاح. افصل بين جلسات cold وwarm. قس Tool Selection وSchema Validity وSequencing وVerification وRecovery وFalse Success وEfficiency وSafety.

> **بدون نسب مختلقة:** قبل وجود paired live runs، أي تحسن مجرد فرضية هندسية وليس نتيجة تجريبية.

## التثبيت

### Agent Skill

```bash
python3 scripts/package_skill.py
```

ينتج `dist/claude-capability-bridge/` ليتم تثبيته عبر آلية Agent Skills الخاصة بالـHost.

### Claude Code Plugin

```bash
python3 scripts/package_claude_code_plugin.py
```

ينتج `dist/claude-capability-bridge-plugin/` ويضم الـSkill نفسه مع runtime اختياري للـhooks.

### التسجيل اليدوي للـhooks

انسخ الإدخالات من [`bootstrap/settings.json.example`](../bootstrap/settings.json.example) إلى إعدادات الـHost واختر `CLAUDE_CAPABILITY_BRIDGE_MODE`. الـPlugin يسجل hooks الخاصة به تلقائياً.

## هيكل المشروع

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

مسار الكشف التدريجي:

```text
kernel → runtime profile → task card → reference → execution → verification
```

## التحقق

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 scripts/run_tests.py
python3 bootstrap/bridge_hook.py --selftest
python3 scripts/analyze_trace.py --selftest
```

هذه الفحوصات تغطي البنية والمراجع والحزم وعقود المحتوى والـhooks ودورة حياة الحالة وتحليل trace الاصطناعي. لكنها لا تثبت سلوك النموذج الحي أو التنفيذ الحقيقي داخل Claude Code أو دعم Windows الكامل أو سلوك cache لدى provider.

## دعم المشروع

عناوين التبرع مأخوذة من مستودع [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant).

| الشبكة | العنوان |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## Telegram

تابع [@pythash](https://t.me/pythash).

## الترخيص

المشروع منشور بموجب [MIT License](../LICENSE).

## روابط

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
