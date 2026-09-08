# Claude Capability Bridge Skill

> 一个面向第三方与自定义 Provider 模型的 Agent Skill，帮助它们在 Claude Desktop / Cowork / Claude Code 类运行时中发现、选择、执行、验证并恢复工具工作流。

[🇬🇧 English](./README.md) · **🇨🇳 简体中文** · [🇪🇸 Español](./README_ES.md) · [🇮🇳 हिन्दी](./README_HI.md) · [🇸🇦 العربية](./README_AR.md) · [🇫🇷 Français](./README_FR.md) · [🇮🇷 فارسی](./README_FA.md)

## 🎯 项目目标

运行时可能提供文件、Shell、浏览器、Chrome、Computer Use、MCP、Connectors、Projects、Skills、Plugins、Artifacts、Subagents 等能力，但“工具存在”不等于“模型知道什么时候、为什么以及按什么顺序使用它”。

本 Skill 提供可复用的程序性知识：

```text
Discover → Select → Execute → Observe → Verify → Recover → Report
```

它不会创建新工具、权限、浏览器会话或 MCP 服务，只指导模型正确使用运行时实际暴露的能力。

## 🧠 使用前 vs 使用后

| 未使用 Skill | 使用 Skill |
|---|---|
| 可能不知道有哪些工具 | 先发现真实 Capability |
| 可能选择错误工具或顺序 | 根据任务选择合适工具与顺序 |
| 执行成功第一步就结束 | 按验收标准验证最终结果 |
| 反复重试同一个错误 | 分类失败并改变关键变量 |
| 混淆 Gateway、Runtime 与 Model | 分离 Transport、Provider 与模型能力 |

这些是工程预期，不是已经测得的 benchmark 百分比。真实效果请运行 `benchmarks/`。

## 🔌 Custom Provider 架构

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

一个重要例子是 MCP Tool Search：当 endpoint 指向非 first-party host 时，其行为可能受 gateway 对相关协议能力的支持影响，因此“工具没有被发现”不能直接等同于“模型不会使用工具”。

## 🌐 Web App 端到端验证

```text
Inspect Repo
→ Baseline
→ Implement / Fix
→ Start Server
→ Confirm Listener + HTTP
→ Discover Real URL / Port
→ Choose Browser
→ Test Critical Flow
→ Inspect UI / Telemetry
→ Diagnose → Patch → Re-test
→ Deterministic Checks
→ Visual Verification
→ Evidence Report
```

进程运行、端口监听、HTTP 正常、UI 渲染以及核心功能工作是不同层级，不能互相替代。

## 🧩 覆盖能力

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

## 📊 Evaluation

使用相同的模型、Provider、Host、工具、任务进行 A/B：

```text
Bridge OFF  ↔  Bridge ON
```

关注 Tool Selection、Schema Validity、Sequencing、Verification、Recovery、False Success、Efficiency 和 Safety，而不是文档数量。

## 📦 安装

```bash
python3 scripts/package_skill.py
```

生成：

```text
dist/claude-capability-bridge/
```

然后通过宿主的 Agent Skills 机制安装；支持 Slash Command 的环境中可使用：

```text
/claude-capability-bridge
```

## 💖 支持项目

捐赠地址来源于 [Chat-management-bot-and-AI-assistant](https://github.com/Abolfazlshahi/Chat-management-bot-and-AI-assistant)：

| 网络 | 地址 |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT TRC20 | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT BEP20 | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

<a href="https://nowpayments.io/donation?api_key=724be14f-9bdf-4318-99d0-0a837b5493b6" target="_blank" rel="noreferrer noopener"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Cryptocurrency & Bitcoin donation button by NOWPayments"></a>

## 📣 Telegram

关注 [@pythash](https://t.me/pythash) 获取项目与技术更新。

## 📄 许可证

本项目采用 [MIT License](./LICENSE)。

## 🔗 链接

[Repository](https://github.com/Abolfazlshahi/claude-capability-bridge-skill) · [SKILL.md](./SKILL.md) · [Benchmarks](./benchmarks/README.md) · [References](./references/README.md) · [License](./LICENSE) · [Telegram](https://t.me/pythash)
