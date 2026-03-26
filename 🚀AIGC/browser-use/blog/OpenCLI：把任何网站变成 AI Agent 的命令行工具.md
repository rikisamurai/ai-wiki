---
title: OpenCLI：把任何网站变成 AI Agent 的命令行工具
tags:
  - browser-use
  - ai-agent
date: 2026-04-07
---

# OpenCLI：把任何网站变成 AI Agent 的命令行工具

> [!info] 项目信息
> - GitHub：[jackwener/opencli](https://github.com/jackwener/opencli)
> - License：Apache-2.0
> - 语言：TypeScript (Node.js)
> - 安装：`npm install -g @jackwener/opencli`

## 一句话定位

**OpenCLI 是一个万能遥控器** — 把任何网站、Electron 应用、本地 CLI 工具统一为命令行接口，让 AI Agent 能够通过 CLI 控制一切。

核心理念：**零 LLM 成本、确定性执行、复用浏览器登录态**。同一命令永远返回同一结构，可管道化、可脚本化、CI 友好，跑一万次不花一分钱 token。

---

## 核心架构

### Browser Bridge + Dual-Engine

OpenCLI 的架构分为三层：

```
CLI 入口 (Commander.js)
    ↓
Engine Layer: Registry / Dynamic Loader / Output Formatter
    ↓
Adapter Layer: YAML Pipeline（声明式）| TypeScript Adapter（编程式）
    ↓
Connection Layer: Browser Bridge（网站）| CDP 注入（Electron）| Passthrough（外部 CLI）
```

#### Browser Bridge

Browser Bridge 是 OpenCLI 连接浏览器的核心机制，由两部分组成：

1. **Chrome Extension** — 安装在 Chrome/Chromium 中，能在网页上下文中执行 JavaScript，访问已登录的 session
2. **Micro-daemon** — 自动启动，监听 `localhost:19825`，管理 CLI 与 Extension 之间的 WebSocket 连接

```
opencli (Node.js) ←WebSocket→ micro-daemon ←Chrome API→ Chrome Browser
```

> [!tip] 账号安全
> OpenCLI 复用 Chrome/Chromium 的登录态，凭证始终留在浏览器中，不会被存储或外泄。同时内置了反指纹和反风控措施。

#### Dual-Engine（双引擎适配器）

- **YAML Pipeline**（声明式）：适合简单 API 抓取，pipeline steps 为 `fetch → map → filter → limit → download`，支持模板表达式
- **TypeScript Adapter**（编程式）：适合复杂浏览器交互，通过 `page` 对象提供 `goto()`、`evaluate()`、`waitForSelector()`、`click()` 等方法

只需把 `.yaml` 或 `.ts` 文件丢到 `clis/` 目录即可自动注册，无需手动配置。

---

## 四大功能模块

### 1. 网站 → CLI

将任意网站变成确定性 CLI 命令。目前已内置 **79+ 适配器**，覆盖全球和中国主流平台：

| 类别 | 代表站点 |
|---|---|
| 社交媒体 | Twitter/X、Reddit、Instagram、Facebook、TikTok、微博、即刻 |
| 视频 | Bilibili、YouTube、抖音、Douyin |
| 知识社区 | 知乎、V2EX、StackOverflow、HackerNews、Linux.do |
| 内容平台 | 小红书、Medium、Substack、豆瓣、微信公众号 |
| 电商 | Amazon、1688、闲鱼、JD、Coupang |
| AI 工具 | Gemini、Grok、元宝、豆包、NotebookLM |
| 开发者 | GitHub（via gh）、Product Hunt、Dev.to、Arxiv |
| 金融 | 雪球、Yahoo Finance、Bloomberg、Barchart |

```bash
opencli bilibili hot --limit 5         # B站热门
opencli xiaohongshu search "AI" -f json # 小红书搜索
opencli twitter trending               # Twitter 趋势
opencli hackernews top --limit 10       # HN 热帖
```

### 2. Electron 应用 CLI 化

通过 CDP 注入，把桌面 Electron 应用变成可脚本化的 CLI 工具：

| 应用 | 能力 |
|---|---|
| **Cursor** | Composer 对话、代码提取、模型切换 |
| **Codex** | 无头驱动 OpenAI Codex CLI Agent |
| **Antigravity** | 终端控制 Antigravity Ultra |
| **ChatGPT** | 自动化 ChatGPT macOS 桌面端 |
| **Notion** | 搜索、读写 Notion 页面 |
| **Discord** | 消息、频道、服务器管理 |

> [!abstract] AI 控制 AI
> OpenCLI 能让 AI Agent 通过 CLI 控制其他 AI 应用（如用 Claude Code 操控 Cursor），实现 **AI 自己控制自己** 的能力。

### 3. CLI Hub（外部工具枢纽）

OpenCLI 可以作为所有本地 CLI 的统一入口，支持自动发现、自动安装和纯透传执行：

```bash
opencli gh pr list --limit 5       # GitHub CLI
opencli docker ps                  # Docker
opencli obsidian search query="AI" # Obsidian CLI
```

如果系统中还没有对应工具（如 `gh`），OpenCLI 会自动通过包管理器安装后重新执行。也可以注册自定义 CLI：

```bash
opencli register mycli
```

### 4. 浏览器自动化（operate）

`operate` 命令赋予 AI Agent 直接操控浏览器的能力：

```bash
opencli operate open "https://example.com"   # 打开页面
opencli operate click "#submit"              # 点击元素
opencli operate type "#input" "hello"        # 输入文本
opencli operate screenshot                   # 截图
opencli operate eval "document.title"        # 执行 JS
```

支持的操作包括：`open`、`state`、`click`、`type`、`select`、`keys`、`wait`、`get`、`screenshot`、`scroll`、`back`、`eval`、`network` 等。

---

## 为 AI Agent 而生

OpenCLI 专门为 AI Agent 设计了完整的集成方案：

1. **Skills 安装** — 为 Claude Code、Cursor 等提供开箱即用的 skill：
   ```bash
   npx skills add jackwener/opencli
   ```

2. **自动发现** — 在 `AGENT.md` 或 `.cursorrules` 中配置 `opencli list`，AI 即可自动发现所有可用命令

3. **适配器生成** — AI 可以自动探索网站并生成新适配器：
   ```bash
   opencli explore https://example.com --site mysite   # 发现 API
   opencli synthesize mysite                            # 生成适配器
   opencli generate https://example.com --goal "hot"    # 一键完成
   ```

4. **确定性输出** — 所有命令支持 `--format` 参数（`table`、`json`、`yaml`、`md`、`csv`），方便 AI 解析

---

## 快速上手

```bash
# 1. 安装 Browser Bridge 扩展
# 从 GitHub Releases 下载 opencli-extension.zip，加载到 Chrome

# 2. 安装 OpenCLI
npm install -g @jackwener/opencli

# 3. 验证连通性
opencli doctor
opencli daemon status

# 4. 试一试
opencli list                        # 查看所有命令
opencli hackernews top --limit 5    # 公共 API，无需浏览器
opencli bilibili hot --limit 5      # 需要 Browser Bridge
```

> [!warning] 前置要求
> - Node.js >= 20.0.0
> - Chrome/Chromium 运行中且已登录目标网站
> - Browser Bridge 扩展已安装并启用

---

## 与同类工具的对比

> [!info] 延伸阅读
> 更详细的三方对比见 [[AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比]]

### 工具定位一览

| 工具 | 方式 | 最适合场景 |
|---|---|---|
| **OpenCLI** | 预制适配器（YAML/TS） | 确定性站点命令、广泛平台覆盖、桌面应用控制 |
| **Browser-Use** | LLM 驱动浏览器 | 通用 AI 浏览器自动化 |
| **Crawl4AI** | 异步爬虫 | 大规模数据抓取 |
| **Firecrawl** | 抓取 API / 自托管 | 干净的 Markdown 提取 |
| **agent-browser** | 浏览器原语 CLI | Token 高效的 AI Agent 浏览 |
| **Stagehand** | AI 浏览器框架 | 开发者友好的浏览器自动化 |
| **Skyvern** | 视觉 AI 自动化 | 跨站点通用工作流 |

### 场景对比

#### 定时批量数据抓取

> 场景："每小时从 Bilibili/Reddit/HackerNews 拉取热门帖子到数据管线"

OpenCLI 是最佳选择。`opencli bilibili hot -f json` 每次返回相同结构化 schema，零成本，秒级完成。Crawl4AI 也不错但需要为每个站点编写提取逻辑；Browser-Use / Stagehand 每次运行都要消耗 LLM 推理，既慢又贵且不确定。

#### AI Agent 站点操作

> 场景："AI Agent 需要搜索 Twitter、阅读 Reddit 帖子或发布小红书笔记"

OpenCLI 提供结构化 JSON 输出、秒级确定性执行、数百个现成命令。当 Agent 需要 `twitter search "AI news" -f json` 时，确定性命令严格优于让 LLM 逐步点击网页 — Agent 把 token 省下来用于推理，而不是导航。

#### 需要登录的操作

> 场景："访问我的书签、发布内容、操作需要登录的站点"

OpenCLI 通过 Browser Bridge 实时复用 Chrome 登录态，无需存储或传输凭证。你在 Chrome 中登录一次，所有命令立即生效 — 不需要 OAuth、不需要 API Key、不需要凭证文件。其他工具在这方面要么需要手动管理 cookie，要么完全无法访问已认证的 session。

#### 通用网页浏览与探索

> 场景："探索未知网站、填写表单、处理复杂多步流程"

**OpenCLI 不适合这个场景。** 它只能操作有预制适配器的站点。如果需要处理未知网站或一次性任务，应该使用 Browser-Use、Stagehand 等 LLM 驱动的工具。OpenCLI 用确定性和零成本换取了通用性。

#### 桌面应用控制

> 场景："从终端脚本化控制 Cursor、ChatGPT、Notion 等 Electron 应用"

**这是 OpenCLI 独有的能力。** 其他浏览器自动化工具都无法控制桌面应用。OpenCLI 通过 CDP + AppleScript 提供了 8 个桌面适配器，是唯一能做到这一点的 CLI 工具。

### 最佳实践：组合使用

OpenCLI 适合与通用浏览器工具搭配使用，而非互相替代：

```
有适配器?  ──是──▶  OpenCLI（快速、免费、确定性）
     │
     否
     │
     ▼
一次性任务?  ──是──▶  Browser-Use / Stagehand（LLM 驱动）
     │
     否
     │
     ▼
反复执行?   ──是──▶  编写 OpenCLI 适配器，然后用 OpenCLI
```

### OpenCLI 的局限

- **覆盖范围依赖适配器** — 只能操作有预制适配器的站点，新增站点需要编写 YAML 或 TypeScript 适配器
- **适配器维护** — 网站更新 DOM 或 API 后，对应适配器可能需要更新，虽然社区在维护但仍可能出现失效
- **非通用工具** — 无法处理任意网站，对于未知站点需要搭配通用浏览器工具作为兜底
