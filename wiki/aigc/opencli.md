---
title: OpenCLI
tags: [opencli, browser-automation, ai-agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具]]"
  - "[[sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比]]"
last-ingested: 2026-04-23
status: draft
---

OpenCLI（[jackwener/opencli](https://github.com/jackwener/opencli)）是把"网站 / Electron 应用 / 本地 CLI"统一封装成命令行接口的万能遥控器。和 [[browser-use|Browser-Use]] 在 [[cdp|CDP]] 之上选了相反的策略——**不让 LLM 看截图，让 LLM 调命令**。同一命令永远返回同一 schema，可管道化、可脚本化、跑一万次零 token 成本。

> [!important] 设计哲学：把 LLM 推理留给"想"，不浪费在"导航"
> Browser-Use 派让 LLM 在每一步消耗 token 思考"应该点哪里"；OpenCLI 派把"该点哪里"提前固化成命令，LLM 只决定"调哪个命令、传什么参数"。
>
> 工程含义：**适配器写一次，所有 Agent 都受益**。每个 `opencli twitter search "AI" -f json` 调用都是 0 token、秒级响应、确定性输出——这是 Browser-Use 永远做不到的。

**架构：Bridge + Dual-Engine 三层**

```
CLI 入口 (Commander.js)
    ↓
Engine: Registry / Dynamic Loader / Output Formatter
    ↓
Adapter: YAML Pipeline（声明式）| TypeScript Adapter（编程式）
    ↓
Connection: Browser Bridge | CDP 注入 | Passthrough
```

> [!compare] Browser Bridge：复用浏览器登录态而不是存 cookie
> ```
> opencli (Node.js) ←WebSocket→ micro-daemon ←Chrome API→ Chrome Browser
> ```
> Browser Bridge = Chrome Extension + 本地 micro-daemon（监听 `localhost:19825`）。
>
> 关键差异：**凭证始终留在 Chrome 里**。OAuth / API Key / cookie 文件全免——你在 Chrome 登录一次，`opencli xiaohongshu search` 立即可用。这也是 OpenCLI 在"需要登录的操作"场景里碾压所有同类工具的根本原因。

**双引擎适配器（Dual-Engine）**

- **YAML Pipeline**（声明式）：`fetch → map → filter → limit → download` 五步组合，适合简单 API 抓取
- **TypeScript Adapter**（编程式）：`page.goto() / evaluate() / waitForSelector() / click()`，适合复杂 DOM 交互

把 `.yaml` 或 `.ts` 文件丢到 `clis/` 目录就自动注册——**没有手动配置**。

**四大功能模块**

> [!example] 1. 网站 → CLI（79+ 内置适配器）
> 覆盖社交媒体（Twitter/Reddit/微博）、视频（B站/YouTube/抖音）、知识社区（知乎/V2EX/HN）、内容平台（小红书/Medium/公众号）、电商（Amazon/1688/闲鱼）、AI 工具（Gemini/Grok/豆包）、开发者（GitHub/Arxiv）、金融（雪球/Bloomberg）。
>
> ```bash
> opencli bilibili hot --limit 5
> opencli xiaohongshu search "AI" -f json
> opencli hackernews top --limit 10
> ```

> [!example] 2. Electron 应用 CLI 化（独有能力）
> 通过 CDP 注入控制桌面端：Cursor / Codex / ChatGPT / Notion / Discord / Antigravity / ChatWise / Doubao（豆包）共 8 个。
>
> **AI 控制 AI**：可以用 [[claude-code|Claude Code]] 通过 OpenCLI 操控 [[codex|Codex]]、Cursor。这是 [[browser-use|Browser-Use]] 类工具完全不能做的——只有 OpenCLI 同时打通了浏览器和桌面应用两条路径。
>
> **5-Command Pattern**：每个 Electron adapter 都遵循同一套命令骨架——
>
> | 命令 | 作用 | 技术要点 |
> |---|---|---|
> | `status` | 连接测试 | 确认 CDP 通路 |
> | `dump` | 逆向工程 | dump DOM + Accessibility Snapshot，提取 selector |
> | `send` | 文本注入 | `document.execCommand('insertText')` 穿透 React 状态管理 |
> | `read` | 内容提取 | 找语义化 selector，输出 Markdown |
> | `new` | 新建操作 | 触发原生快捷键（`Meta+N`） |
>
> 这套骨架是适配 Electron 应用的**模板**——加新应用照填即可。

> [!note] 非 Electron 应用的降级方案
> 微信/飞书等原生应用没有 CDP 端口——OpenCLI 用 **AppleScript + 剪贴板**：`Cmd+A → Cmd+C → pbpaste`。精度低但兜得住。

> [!example] 3. CLI Hub（外部工具枢纽）
> ```bash
> opencli gh pr list --limit 5    # GitHub CLI 透传
> opencli docker ps                # Docker 透传
> ```
> 系统没装 `gh`？OpenCLI 自动包管理器装好再执行。也支持 `opencli register mycli` 注册自定义 CLI。

> [!example] 4. operate（通用浏览器自动化兜底）
> ```bash
> opencli operate open "https://..."
> opencli operate click "#submit"
> opencli operate type "#input" "hello"
> opencli operate eval "document.title"
> ```
> 没有适配器的站点用 `operate` 兜底——本质上是把 [[browser-use|Browser-Use]] 的能力收编进 OpenCLI 的命令体系里。

**为 AI Agent 而生**

> [!tip] 四个 AI 集成点
> 1. **Skills 安装**：`npx skills add jackwener/opencli` 一键给 [[claude-code|Claude Code]]/Cursor 添加 skill（参考 [[skills-marketplace|Skills 分发与市场]]）
> 2. **自动发现**：在 `AGENT.md` 配 `opencli list`，AI 自动列出所有可用命令
> 3. **适配器生成**：`opencli explore + synthesize + generate` 让 AI 自己写适配器
> 4. **确定性输出**：`--format table|json|yaml|md|csv`——给 AI 的不是 HTML，是 JSON

> [!compare] 认证策略级联（探索期自动降级）
> ```
> PUBLIC → COOKIE → HEADER → BROWSER → CDP
> ```
> `opencli explore` 时按这个顺序探测：先试无认证、再试 Cookie、再试 Header、最后回退到 Browser Bridge / CDP 注入。**让 LLM 在"探索期"做一次决策，运行期就 0 推理**——这是和 [[browser-use|Browser-Use]] 派的根本区别。

**适用边界：场景 × 工具决策树**

> [!compare] 何时用 OpenCLI、何时用 Browser-Use
> ```
> 有 OpenCLI 适配器? ──是──▶ OpenCLI（快/免费/确定）
>      │
>      否
>      ▼
> 一次性任务?       ──是──▶ Browser-Use / Stagehand（LLM 驱动）
>      │
>      否
>      ▼
> 反复执行?         ──是──▶ 写 OpenCLI 适配器再用
> ```
>
> 总结："**有适配器就用 OpenCLI，没有就回退 Browser-Use**"——它们不是替代关系，是组合关系。

> [!warning] OpenCLI 的局限
> - **覆盖依赖适配器**：未知网站只能用 `operate` 兜底或回退 Browser-Use
> - **适配器会失效**：网站改 DOM/API 后社区适配器可能滞后
> - **不是通用工具**：把"通用性"换成了"确定性 + 零成本"，这是显式的设计权衡

**关联**：[[browser-use|Browser-Use]] / [[agent-browser|agent-browser]] / [[cdp|CDP]] / [[cdp-能力边界|CDP 能力边界]] / [[claude-code|Claude Code]] / [[skills-marketplace|Skills 分发与市场]]
