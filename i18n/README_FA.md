# Claude Capability Bridge Skill

> یک Agent Skill برای اینکه مدل‌های Third‑Party و Custom Provider بتوانند در محیط‌هایی مثل Claude Desktop / Cowork / Claude Code قابلیت‌های موجود را بهتر کشف، انتخاب، اجرا، بررسی و بازیابی کنند.

[🇬🇧 English](../README.md) · [🇨🇳 中文](./README_ZH.md) · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · **🇮🇷 فارسی**

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

مقایسه روی چهار حالت انجام می‌شود، با ثابت نگه داشتن مدل، میزبان، provider، ابزارها، ورک‌اسپیس و متن دقیق تسک:

```text
A  control                    بدون Skill و بدون hook
B  skill only                 فقط Skill نصب است
C  skill + adaptive           حالت پیش‌فرض 0.9.0
D  skill + legacy-every-turn  رفتار قدیمی، یادآوری در هر نوبت
```

معیار اصلی «هزینه به ازای هر موفقیت تأییدشده» است: مجموع توکن ورودی و خروجی تقسیم بر تعداد موفقیت‌هایی که با شواهد تأیید شده‌اند. معیارهای دیگر: Tool Selection، Schema Validity، Sequencing، Verification، Recovery، False Success، Efficiency و Safety.

جلسه‌های cold و warm دو آزمایش جدا هستند و نباید با هم میانگین گرفته شوند. اگر provider فیلد usage را برنگرداند، مقدار unknown ثبت می‌شود، نه صفر.

## 📦 نصب

**به صورت Agent Skill:**

```bash
python3 scripts/package_skill.py                 # -> dist/claude-capability-bridge/
```

پوشه ساخته‌شده را با مکانیزم Agent Skills میزبان نصب کنید. در محیطی که Slash Command دارد:

```text
/claude-capability-bridge
```

**به صورت پلاگین Claude Code** (همان محتوا به علاوه hookها):

```bash
python3 scripts/package_claude_code_plugin.py    # -> dist/claude-capability-bridge-plugin/
```

هر دو بسته فایل‌های reference، profile و card خودشان را همراه دارند، بنابراین هیچ لینک داخلی به بیرون بسته اشاره نمی‌کند و اگر چنین چیزی پیش بیاید build شکست می‌خورد.

**ثبت hook** (فقط برای نصب Skill ساده لازم است؛ پلاگین خودش ثبت می‌کند): ورودی‌های `bootstrap/settings.json.example` را در تنظیمات کپی کنید و حالت را انتخاب کنید:

```bash
export CLAUDE_CAPABILITY_BRIDGE_MODE=adaptive           # پیش‌فرض
export CLAUDE_CAPABILITY_BRIDGE_MODE=session-only       # فقط شروع جلسه
export CLAUDE_CAPABILITY_BRIDGE_MODE=legacy-every-turn  # رفتار قدیمی برای مقایسه
export CLAUDE_CAPABILITY_BRIDGE_MODE=off                # هیچ خروجی‌ای تولید نمی‌شود
```

**بازگشت به عقب:** حالت را روی `off` بگذارید، یا ورودی‌های hook را حذف کنید و Skill را نگه دارید، یا کل بسته را پاک کنید. چیزی خارج از پوشه بسته و یک پوشه state کاربر نوشته نمی‌شود؛ پاک کردن آن پوشه، وضعیت همه جلسه‌ها را ریست می‌کند.

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
├── SKILL.md          # هسته همیشه‌فعال، کوچک و پایدار
├── profiles/         # یک پروفایل برای هر runtime میزبان
├── cards/            # کارت‌های خانواده تسک + index.json تولیدشده
├── references/       # مطالعه پس‌زمینه مفصل
├── bootstrap/        # موتور hook، wrapperهای shell و PowerShell
├── config/           # بودجه محتوا که validator اعمال می‌کند
├── docs/             # قرارداد کش و ممیزی پایه
├── scripts/          # packager، validator، تحلیل trace، اجراکننده تست
├── tests/python/     # مجموعه تست آفلاین
├── benchmarks/       # سناریوها، variantها، متریک‌ها
├── evals/
├── CHANGELOG.md
└── LICENSE
```

## 🛡️ مرزهای طراحی

این Skill **نمی‌تواند** Browser، MCP Server، Permission، Network Access، Filesystem Mount یا provider protocol compatibility ایجاد کند. همچنین ادعا نمی‌کند که یک مدل third-party را به مدل Anthropic تبدیل می‌کند.

## ✅ چه چیزی واقعاً تست شده است

بررسی‌های محلی:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py            # ساختار، بودجه، گراف مرجع، بسته‌های ساخته‌شده
python3 scripts/run_tests.py                 # کل مجموعه تست آفلاین
python3 bootstrap/bridge_hook.py --selftest  # موتور hook
python3 scripts/analyze_trace.py --selftest  # تحلیل trace روی fixture مصنوعی
```

**پوشش داده می‌شود:** بسته‌بندی و بسته بودن گراف مرجع، قراردادهای محتوا، رفتار hook با payload واقعی، چرخه عمر state و بازیابی از خرابی، ثابت‌های امنیتی (ورودی hook فقط داده است، نشت نداشتن secret، ادعا نکردن permission) و پایداری بایت‌به‌بایت متن ثابت.

**پوشش داده نمی‌شود:** رفتار زنده مدل، اجرای واقعی در Claude Code، ویندوز (به `tests/windows-manual-checklist.md` مراجعه کنید که عمداً پر نشده است) و رفتار کش هیچ provider ای. مورد آخر فقط از روی فیلدهای usage زنده قابل خواندن است؛ توضیح در `docs/cache-contract.md`.

## 📄 مجوز

این پروژه تحت [MIT License](../LICENSE) منتشر شده است. متن کامل مجوز در فایل [`LICENSE`](../LICENSE) قرار دارد.

## 🔗 لینک‌های سریع

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [Skill](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
