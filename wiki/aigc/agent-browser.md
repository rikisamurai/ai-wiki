---
title: agent-browser
tags: [agent-browser, browser-automation, ai-agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具]]"
  - "[[sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比]]"
  - "[[sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/OpenCLI、Agent-Browser 与 Browser-Use 深度横向评测]]"
last-ingested: 2026-04-23
status: draft
---

agent-browser（[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)）是 Vercel Labs 开源的"为 AI Agent 设计的浏览器自动化原语"——不像 [[browser-use|Browser-Use]] 把原始截图喂给 LLM，也不像 [[opencli|OpenCLI]] 把每个网站封成专用命令，而是**在浏览器层做针对 Agent 的优化**：纯 Rust 守护进程、Accessibility Tree 抽象、Token 高效的元素引用机制。

> [!compare] 三流派定位
> | 流派 | 代表 | LLM 输入抽象层级 |
> |---|---|---|
> | Browser-Use 派 | [[browser-use\|browser-use]] | 最原始（截图 + DOM） |
> | **专用 Agent 派** | **agent-browser** | **中等（Accessibility Tree + Refs）** |
> | CLI 派 | [[opencli\|OpenCLI]] | 最抽象（结构化命令） |
>
> 选型：通用 + 控制力 → agent-browser；通用 + 灵活 → Browser-Use；高频 + 确定 → OpenCLI。

**架构：Rust Client + Daemon + Chrome for Testing**

```
Rust CLI（客户端）←→ Native Daemon（纯 Rust）←CDP WebSocket→ Chrome for Testing
```

- **Daemon 持久化**：首次命令自动启动，多命令之间持续存活；命令延迟 ~50ms
- **无 Node.js 依赖**：守护进程纯 Rust 直连 [[cdp|CDP]]，无 Playwright 运行时
- **Chrome for Testing**：通过 `agent-browser install` 从 Google 官方下载干净的测试用 Chrome——不污染用户日常浏览器

> [!important] 核心创新：Accessibility Tree Snapshot + 确定性 Refs
> `agent-browser snapshot` 返回的不是 DOM 而是**无障碍树**，每个交互元素分配确定 ID（`@e1`、`@e2`）：
>
> ```
> - heading "Example Domain" [ref=e1]
> - paragraph "..." [ref=e2]
> - link "More information..." [ref=e3]
> ```
>
> 后续操作直接引用：
> ```bash
> agent-browser click @e3
> agent-browser fill @e5 "hello"
> ```
>
> | 维度 | Accessibility Tree | 完整 DOM |
> |---|---|---|
> | Token 消耗 | ~200-400 | ~3000-5000 |
> | 元素定位 | 确定性 ref（`@e1`） | CSS selector / XPath（易错） |
> | AI 友好性 | 纯文本，LLM 天然擅长 | HTML 噪声多 |
>
> 这是它在 [[wiki/ai-coding/context-window|上下文]]经济学上的杀手锏——把无关节点全过滤掉，只留可交互元素 + 稳定 ID。

> [!example] 量化基准：93% Token 锐减 + 95% 首次成功率
> 同一组 6 个测试循环：
>
> | 工具 | 字符消耗 | 估算 Token | 相对值 |
> |---|---|---|---|
> | Playwright MCP（基准） | ~31,000 | ~7,800 | 100% |
> | **agent-browser** | **~5,500** | **~1,400** | **18%（-82% Token）** |
>
> 同样的上下文预算，agent-browser 能多跑 **5.7 倍**测试流。
>
> 任务可靠性：agent-browser **首次尝试成功率 95%**（Playwright MCP / Chrome DevTools MCP 仅 75%-80%）——这 15-20pp 的提升直接来自"不让 LLM 编 selector"。

> [!tip] Diff Snapshot：检测页面变化
> ```bash
> agent-browser diff snapshot                       # 当前 vs 上一次
> agent-browser diff snapshot --baseline before.txt # 当前 vs 保存基线
> ```
> 用于 Agent 在多步操作中**确认上一步真的生效**——比"截图 + LLM 比较"高效几个数量级。

**安全防护体系（Opt-in）**

> [!warning] 为 AI Agent 量身定制的安全机制
> | 特性 | 说明 |
> |---|---|
> | **Authentication Vault** | 凭证本地加密（`~/.agent-browser/.encryption`），LLM 永远看不到密码 |
> | **Content Boundary Markers** | `--content-boundaries` 用随机 nonce 包裹页面内容，防 [[wiki/aigc/fail-closed-tool-defaults\|Prompt Injection]] |
> | **Domain Allowlist** | 限制导航到受信域名，阻止数据外泄 |
> | **Action Policy** | 静态策略文件控制允许/禁止的操作类别 |
> | **Action Confirmation** | 敏感操作显式批准 |
> | **Output Length Limits** | 防上下文溢出 |
>
> 对比之下 [[browser-use|Browser-Use]] / [[opencli|OpenCLI]] 几乎不内置这些——agent-browser 是少数把"AI Agent 专用安全"作为一等公民的工具。

> [!warning] 软肋：反爬虫能力弱
> agent-browser 的浏览器指纹是"标准自动化"的——遇到 Cloudflare Turnstile / 严苛 Bot Fight Mode 容易直接被拦。即便强制有头模式仍然容易触发 Google CAPTCHA。
>
> 对策：用 `-p browserless / browserbase / kernel` 接外部云浏览器供应商。这意味着**生产数据采集场景下 agent-browser 必须叠加付费基础设施**——这是它和 [[browser-use|Browser-Use]] + Bright Data 这类组合的关键差距。

**多 Provider 支持**

```bash
agent-browser -p browserless open example.com   # Browserless
agent-browser -p browserbase open example.com   # Browserbase
agent-browser -p browser-use open example.com   # Browser Use Cloud
agent-browser -p kernel open example.com        # Kernel（隐身+持久 Profile）
```

甚至支持通过 Xcode Simulator + Appium 控制 **iOS Safari**——这是其他两家都没有的能力。

**Electron 应用控制**

通过 `agent-browser connect <port>` 接入暴露 CDP 的 Electron 应用（VS Code / Slack / Discord / Figma / Notion / Spotify），**复用同一套 Snapshot + Refs 工作流**——网页和桌面应用在 Agent 视角下完全统一。

```bash
agent-browser --session slack connect 9222
agent-browser --session vscode connect 9223
```

支持**命名会话**——一个 Agent 同时控制多个独立终端窗口。

> [!tip] 反 MCP 设计：Skill 而非 Server
> agent-browser 代表了"轻量级 CLI 替代 [[mcp|MCP]]"的思潮——通过 `npx skills add` 等工具直接把 `SKILL.md` 下发到 `~/.claude/skills/`（参考 [[skills-marketplace|Skills 分发]]）。
>
> 比 MCP 优越的地方：JSON Schema 不占常驻 token；人类开发者可以在终端直接 `agent-browser click @e3` 介入诊断——这是 MCP server 做不到的。

**关联**：[[browser-use|Browser-Use]] / [[opencli|OpenCLI]] / [[cdp|CDP]] / [[cdp-能力边界|CDP 能力边界]] / [[claude-code|Claude Code]] / [[skills-marketplace|Skills 分发与市场]] / [[mcp|MCP]]
