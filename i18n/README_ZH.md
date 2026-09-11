# Claude Capability Bridge Skill

> 一个面向第三方与自定义 Provider 模型的 Agent Skill，帮助它们在 Claude Desktop / Cowork / Claude Code 类运行时中发现、选择、执行、验证并恢复工具工作流。

[🇬🇧 English](../README.md) · **🇨🇳 简体中文** · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## 项目目标

运行时可能提供文件、Shell、浏览器、Chrome、Computer Use、MCP、Connectors、Projects、Skills、Plugins、Artifacts、Subagents 等能力，但“工具存在”不等于“模型知道什么时候、为什么以及按什么顺序使用它”。

本 Skill 提供可复用的程序性知识：

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

它不会创建新工具、权限、浏览器会话或 MCP 服务，只指导模型正确使用运行时实际暴露的能力。

## 使用前 vs 使用后

| 未使用 Skill | 使用 Skill |
|---|---|
| 可能不知道有哪些工具 | 先发现真实 Capability |
| 可能选择错误工具或顺序 | 根据任务选择合适工具与顺序 |
| 执行成功第一步就结束 | 按验收标准验证最终结果 |
| 反复重试同一个错误 | 分类失败并改变关键变量 |
| 混淆 Gateway、Runtime 与 Model | 分离 Transport、Provider 与模型能力 |

这些是工程预期，不是已经测得的 benchmark 百分比。

## Custom Provider 架构

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

`ANTHROPIC_BASE_URL` 等配置可以改变 endpoint 或传输路径，但不会自动把第三方模型变成 Anthropic 模型。Tool Calling、Vision、Context、Reasoning 以及协议功能都必须单独验证。

## Web App 端到端验证

```text
Inspect Repo → Baseline → Implement / Fix
→ Start Server → Confirm Listener + HTTP
→ Discover Real URL / Port → Choose Browser
→ Test Critical Flow → Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks → Visual Verification → Evidence Report
```

进程运行、端口监听、HTTP 正常、UI 渲染以及核心功能工作是不同层级。一份通过 `file://` 打开的服务端模板并不等同于真正运行的应用。

## 覆盖能力

- Browser / Claude in Chrome
- Computer Use
- MCP / Remote Connectors
- Local MCP / Desktop Extensions
- Projects / Files / Git
- Skills / Plugins
- Artifacts / Interactive Apps
- Subagents / Scheduled Work
- Local / Cloud / Remote boundaries
- Permissions / Safety / Prompt Injection
- Recovery / Evidence-based Verification
- Custom Provider / Gateway behavior

## Claude Code 自适应交付

Skill 无法在所有宿主中强制自身被调用。对于 Claude Code，本仓库提供可选的 hook engine，只在有用时增加上下文，而不是每轮重复提醒。

| 事件 | 行为 |
|---|---|
| `SessionStart` | 每个 session 一次输出精简 kernel 和 card catalogue |
| `SessionStart` after compact | 恢复最小协议并把之前的观察标记为 stale |
| `UserPromptSubmit` | 通常不输出；最多注入一个匹配任务的 capability card |
| `PostToolUseFailure` | 分类失败并给出有界的下一步建议 |

模式：`adaptive`（默认）、`session-only`、`legacy-every-turn`、`off`。

Hook delivery 是 best-effort：hook 无法证明宿主真的把文本传给了模型。

## Evaluation 与 benchmarking

项目不会声称 Skill 对所有模型都有提升；效果必须通过受控运行验证：

```text
A  control                    无 Skill、无 hooks
B  skill only                 安装 Skill，不注册 hooks
C  skill + adaptive           默认配置
D  skill + legacy-every-turn  每轮提醒，用于历史行为比较
```

保持 model、host、tools、provider、workspace、task wording 和成功标准一致。cold 与 warm session 分开实验。关注 Tool Selection、Schema Validity、Sequencing、Verification、Recovery、False Success、Efficiency 和 Safety。

> **不编造百分比：** 在获得成对的 live runs 之前，任何提升都只是工程假设，而不是实验结果。

## 安装

### Agent Skill

```bash
python3 scripts/package_skill.py
```

生成 `dist/claude-capability-bridge/`，通过宿主的 Agent Skills 机制安装。

### Claude Code Plugin

```bash
python3 scripts/package_claude_code_plugin.py
```

生成 `dist/claude-capability-bridge-plugin/`，包含相同的 Skill 和可选 hook runtime。

### 手动注册 hooks

把 [`bootstrap/settings.json.example`](../bootstrap/settings.json.example) 中的条目加入宿主配置，并设置 `CLAUDE_CAPABILITY_BRIDGE_MODE`。Plugin 会自动注册自己的 hooks。

## 项目结构

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

渐进式披露路径：

```text
kernel → runtime profile → task card → reference → execution → verification
```

## 验证

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 scripts/run_tests.py
python3 bootstrap/bridge_hook.py --selftest
python3 scripts/analyze_trace.py --selftest
```

这些检查覆盖结构、引用闭包、packaging、内容契约、hooks、state lifecycle 以及 synthetic trace 分析。它们不证明 live model behavior、真实 Claude Code 执行、完整 Windows 支持或 provider cache 行为。

## 支持项目

捐赠地址来源于 [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant)：

| 网络 | 地址 |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## Telegram

关注 [@pythash](https://t.me/pythash) 获取项目与技术更新。

## 许可证

本项目采用 [MIT License](../LICENSE)。

## 链接

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](../SKILL.md) · [Benchmarks](../benchmarks/README.md) · [References](../references/README.md) · [License](../LICENSE) · [Telegram](https://t.me/pythash)
