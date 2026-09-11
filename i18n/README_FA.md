# Claude Capability Bridge Skill

> یک Agent Skill برای مدل‌های Third‑Party و Custom Provider تا در Runtimeهایی مثل Claude Desktop / Cowork / Claude Code قابلیت‌های واقعاً موجود را بهتر کشف، انتخاب، اجرا، راستی‌آزمایی و بازیابی کنند.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · **🇮🇷 فارسی**

## ایده پروژه

Runtime ممکن است فایل، Shell، Browser، Chrome، Computer Use، MCP، Connectors، Projects، Skills، Plugins، Artifacts و Subagents را در اختیار مدل بگذارد؛ اما وجود capability با بلد بودنِ زمان استفاده، ترتیب استفاده و روش اثبات نتیجه یکسان نیست.

این Skill یک لایه‌ی دانش اجرایی و رویه‌ای ارائه می‌کند:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

> این Skill ابزار یا Permission جدیدی ایجاد نمی‌کند و محدودیت‌های Provider یا Runtime را دور نمی‌زند.

## قبل و بعد

| بدون Skill | با Skill |
|---|---|
| ممکن است Runtime یا اجرای واقعی را اشتباه تشخیص دهد | ابتدا host و execution boundary مرتبط با task را از شواهد زنده مشخص می‌کند |
| ممکن است capability موجود را با capability قابل‌استفاده اشتباه بگیرد | capability موردنیاز را کشف و وضعیت آن را طبقه‌بندی می‌کند |
| ممکن است ابزار یا ترتیب اشتباه را انتخاب کند | از سطح authoritative و ترتیب مناسب استفاده می‌کند |
| ممکن است با اجرای یک دستور موفق متوقف شود | نتیجه‌ی واقعی و معیار پذیرش را بررسی می‌کند |
| ممکن است همان خطا را چند بار تکرار کند | failure را طبقه‌بندی و فقط با تغییر متغیر مؤثر retry می‌کند |
| ممکن است محدودیت Custom Provider را با نقص procedural قاطی کند | Model، Runtime، Provider و Environment را از هم جدا می‌کند |

این‌ها انتظارهای مهندسی هستند، نه نتیجه‌ی benchmark اندازه‌گیری‌شده.

## معماری Custom Provider

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

تنظیماتی مثل `ANTHROPIC_BASE_URL` می‌توانند endpoint یا مسیر transport را تغییر دهند، اما مدل third-party را به‌طور جادویی معادل مدل Anthropic نمی‌کنند. Tool Calling، Vision، Context، Reasoning و protocol compatibility باید جداگانه بررسی شوند.

## Web App و راستی‌آزمایی

```text
Inspect Repo
   ↓
Baseline
   ↓
Implement / Fix
   ↓
Start Server
   ↓
Confirm Listener + HTTP
   ↓
Discover Real URL / Port
   ↓
Open Appropriate Browser
   ↓
Test Critical User Flow
   ↓
Inspect UI / Telemetry
   ↓
Diagnose → Patch → Re-test
   ↓
Deterministic Checks
   ↓
Visual Verification
   ↓
Evidence Report
```

اجرای process، listening بودن port، پاسخ HTTP، render شدن UI و کارکرد feature مراحل متفاوتی هستند. باز کردن یک template سمت‌سرور با `file://` معادل اجرای واقعی application نیست.

## قابلیت‌های پوشش‌داده‌شده

- Browser و Claude in Chrome
- Computer Use
- MCP و Remote Connectors
- Local MCP و Desktop Extensions
- Projects و Files و Git
- Skills و Plugins
- Artifacts و Interactive Apps
- Subagents و Scheduled Work
- مرزهای Local / Cloud / Remote
- Permission، Safety و Prompt Injection
- Failure Recovery و Evidence-based Verification
- Custom Provider و Gateway behavior

## Adaptive delivery در Claude Code

Skill قابل‌حمل نمی‌تواند به‌طور جهانی invocation خودش را اجبار کند. این repository برای Claude Code یک hook engine اختیاری دارد که به‌جای تکرار reminder در هر نوبت، فقط در جاهای لازم context وارد می‌کند.

| رویداد | رفتار |
|---|---|
| `SessionStart` | kernel فشرده و catalogue کارت‌ها یک‌بار در session ارائه می‌شود |
| `SessionStart` بعد از compact | پروتکل حداقلی دوباره برقرار و مشاهدات قبلی stale علامت‌گذاری می‌شوند |
| `UserPromptSubmit` | معمولاً خروجی ندارد و حداکثر یک capability card مرتبط تزریق می‌شود |
| `PostToolUseFailure` | failure طبقه‌بندی و راهنمای مرحله‌ی بعدی به‌صورت محدود ارائه می‌شود |

حالت‌ها:

```text
adaptive (پیش‌فرض) | session-only | legacy-every-turn | off
```

Hook delivery best-effort است و hook نمی‌تواند ثابت کند که host متن را واقعاً به model رسانده است.

## ارزیابی و benchmark

اثرگذاری این Skill روی همه‌ی مدل‌ها ادعا نمی‌شود و باید با اجرای کنترل‌شده اندازه‌گیری شود:

```text
A  control                    بدون Skill و بدون hook
B  skill only                 Skill نصب است ولی hook ثبت نشده
C  skill + adaptive           حالت پیش‌فرض 0.9.0
D  skill + legacy-every-turn  یادآوری در هر نوبت برای مقایسه با رفتار قبلی
```

مدل، host، ابزارها، provider config، workspace، متن task و معیار موفقیت باید ثابت بمانند. cold و warm session آزمایش‌های جدا هستند و معیار «هزینه به ازای هر موفقیت تأییدشده» باید کنار شمارش خام گزارش شود.

معیارهای مفید شامل Tool Selection، Schema Validity، Sequencing، Verification، Recovery، False Success، Efficiency و Safety هستند.

> **بدون درصد جعلی:** تا وقتی paired live runs وجود نداشته باشد، بهبود فقط یک فرضیه‌ی مهندسی است.

## نصب

### Agent Skill

```bash
python3 scripts/package_skill.py
```

این دستور `dist/claude-capability-bridge/` را می‌سازد. پوشه‌ی ساخته‌شده را با مکانیزم Agent Skills میزبان نصب کنید.

### Claude Code plugin

```bash
python3 scripts/package_claude_code_plugin.py
```

این دستور `dist/claude-capability-bridge-plugin/` را می‌سازد و همان Skill را همراه runtime اختیاری hook بسته‌بندی می‌کند.

### ثبت hook برای نصب ساده Skill

ورودی‌های [`bootstrap/settings.json.example`](../bootstrap/settings.json.example) را در settings کپی کنید و `CLAUDE_CAPABILITY_BRIDGE_MODE` را انتخاب کنید. plugin hookهای خودش را ثبت می‌کند.

برای rollback می‌توانید mode را روی `off` بگذارید، hookها را حذف کنید یا package را پاک کنید.

## حمایت از پروژه

حمایت مالی اختیاری است. آدرس‌های donation از مخزن [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant) گرفته شده‌اند.

| شبکه | آدرس |
|---|---|
| **TON** | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| **USDT TRC20** | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| **USDT BEP20** | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## کانال

آخرین پروژه‌ها و مطالب را در [@pythash](https://t.me/pythash) دنبال کنید.

## ساختار پروژه

```text
├── SKILL.md                   # kernel پایدار
├── profiles/                  # قراردادهای نسبتاً پایدار host
├── cards/                     # رویه‌های خانواده‌ی task + index تولیدشده
├── references/                # مطالب عمیق و troubleshooting
├── bootstrap/                 # hook engine و registration examples
├── config/                    # بودجه‌ی محتوا
├── docs/                      # cache contract و migration notes
├── scripts/                   # packager، validator، card index و trace tools
├── tests/python/              # مجموعه تست آفلاین
├── benchmarks/                # سناریوها، variantها و متریک‌ها
├── evals/
├── CHANGELOG.md
└── LICENSE
```

مسیر کلی پروژه:

```text
kernel → runtime profile → task card → reference → execution → verification
```

## مرزهای طراحی

این Skill نمی‌تواند Browser runtime، Computer-use runtime، MCP Server، Filesystem Mount، Network Access، Permission، provider protocol compatibility یا capabilityهای گمشده‌ی model را ایجاد کند.

## چه چیزی واقعاً تست شده است

بررسی‌های آفلاین با این فرمان‌ها انجام می‌شوند:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 scripts/run_tests.py
python3 bootstrap/bridge_hook.py --selftest
python3 scripts/analyze_trace.py --selftest
```

CI نیز همین offline suite را اجرا می‌کند و علاوه بر آن packaging، Agent Skills validation، card index، JSON و benchmark schema را بررسی می‌کند.

**پوشش داده نمی‌شود:** live model behavior، اجرای واقعی در Claude Code برای هر host، رفتار cache در provider و بخش‌های ویندوزی که هنوز به‌صورت دستی ثبت نشده‌اند. این موارد تا زمان مشاهده‌ی واقعی `UNKNOWN` می‌مانند.

## مجوز

این پروژه تحت [MIT License](../LICENSE) منتشر شده است.

## لینک‌های سریع

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
