# Claude Capability Bridge Skill

> یک Agent Skill برای اینکه مدل‌های Third‑Party و Custom Provider بتوانند در محیط‌هایی مثل Claude Desktop / Cowork / Claude Code قابلیت‌های موجود را بهتر کشف، انتخاب، اجرا، بررسی و بازیابی کنند.

[🇬🇧 English](./README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · **🇮🇷 فارسی**

## 🎯 ایده پروژه

ممکن است Runtime ابزارهای زیادی مثل فایل، Shell، Browser، Chrome، Computer Use، MCP، Connectors، Projects، Skills، Plugins، Artifacts و Subagents را در اختیار مدل بگذارد؛ اما داشتن ابزار با بلد بودنِ زمان استفاده، ترتیب استفاده، روش بررسی نتیجه و بازیابی از خطا یکسان نیست.

این Skill یک لایه دانش اجرایی و رویه‌ای اضافه می‌کند:

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

> این Skill ابزار یا Permission جدیدی ایجاد نمی‌کند؛ فقط نحوه استفاده از قابلیت‌های واقعاً موجود را آموزش می‌دهد.

## 🧠 قبل و بعد

| بدون Skill | با Skill |
|---|---|
| ممکن است ابزار موجود را کشف نکند | ابتدا Capabilityهای واقعی Runtime را بررسی می‌کند |
| ممکن است ابزار یا ترتیب اشتباه را انتخاب کند | ابزار مناسب و ترتیب وابستگی‌ها را انتخاب می‌کند |
| ممکن است با دیدن اجرای یک دستور موفق متوقف شود | نتیجه نهایی و معیار پذیرش را بررسی می‌کند |
| ممکن است خطا را با retry تکراری پاسخ دهد | خطا را طبقه‌بندی و متغیر مؤثر را تغییر می‌دهد |
| ممکن است محدودیت Custom Provider را نشناسد | Runtime، Gateway و Model capability را جدا می‌کند |

**نکته:** موارد بالا انتظارهای مهندسی هستند، نه نتایج benchmark اندازه‌گیری‌شده. برای اندازه‌گیری واقعی از `benchmarks/` استفاده کنید.

## 🔌 معماری Custom Provider

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

تنظیماتی مثل `ANTHROPIC_BASE_URL` حمل‌ونقل یا endpoint را تغییر می‌دهند؛ آن‌ها مدل را به‌طور جادویی معادل یک مدل Anthropic نمی‌کنند. موضوعاتی مثل Tool Calling، Vision، Context، Reasoning و پشتیبانی از protocol features باید جداگانه بررسی شوند.

یکی از نمونه‌های مهم، MCP Tool Search است: در endpointهای non-first-party، رفتار Tool Search می‌تواند به تنظیمات و سازگاری gateway وابسته باشد؛ بنابراین «ابزار کشف نشده» را نباید فوراً به «مدل ابزار را بلد نیست» نسبت داد.

## 🌐 جریان اصلی: تست Web App

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

اجرای process، listening بودن port، پاسخ HTTP، render شدن UI و کارکرد feature مراحل متفاوتی هستند.

## 🧩 قابلیت‌های پوشش‌داده‌شده

- Browser و Claude in Chrome
- Computer Use
- MCP و Remote Connectors
- Local MCP و Desktop Extensions
- Projects و Files و Git
- Skills و Plugins
- Artifacts و Interactive Apps
- Subagents و Scheduled Work
- Local / Cloud / Remote execution boundaries
- Permission، Safety، Prompt Injection
- Failure Recovery و Evidence-based Verification
- Custom Provider / Gateway behavior

## 📊 ارزیابی

پروژه شامل evaluation و benchmark است و برای مقایسه پیشنهاد می‌کند:

```text
SAME MODEL
SAME PROVIDER
SAME HOST
SAME TOOLS
SAME TASK

Bridge OFF  ↔  Bridge ON
```

معیارهای مهم شامل Tool Selection، Schema Validity، Sequencing، Verification، Recovery، False Success، Efficiency و Safety هستند.

## 📦 نصب

```bash
python3 scripts/package_skill.py
```

خروجی:

```text
dist/claude-capability-bridge/
```

سپس پوشه ساخته‌شده را با مکانیزم Agent Skills میزبان نصب کنید و در محیطی که Slash Command ارائه می‌دهد:

```text
/claude-capability-bridge
```

## 💖 حمایت از پروژه

حمایت مالی کاملاً اختیاری است. آدرس‌های donation این پروژه از مخزن [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant) گرفته شده‌اند.

| شبکه | آدرس |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## 📣 کانال

آخرین پروژه‌ها و مطالب را در [@pythash](https://t.me/pythash) دنبال کنید.

## 📚 ساختار پروژه

```text
├── SKILL.md
├── references/
├── benchmarks/
├── evals/
├── scripts/
├── tests/
└── LICENSE
```

## 🛡️ مرزهای طراحی

این Skill **نمی‌تواند** Browser، MCP Server، Permission، Network Access، Filesystem Mount یا provider protocol compatibility ایجاد کند. همچنین ادعا نمی‌کند که یک مدل third-party را به مدل Anthropic تبدیل می‌کند.

## 📄 مجوز

این پروژه تحت [MIT License](./LICENSE) منتشر شده است. متن کامل مجوز در فایل [`LICENSE`](./LICENSE) قرار دارد.

## 🔗 لینک‌های سریع

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [Skill](./SKILL.md) · [Benchmarks](./benchmarks/README.md) · [References](./references/README.md) · [License](./LICENSE) · [Telegram](https://t.me/pythash)
