---
title: AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比
tags:
  - browser-use
  - ai-agent
date: 2026-03-24
---

# AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比

> [!abstract] 概要
> 随着 AI Coding Agent（Claude Code、Cursor、Codex 等）的兴起，"让 AI 控制浏览器"成为刚需。本文深度对比三款代表性工具——[OpenCLI](https://github.com/jackwener/opencli)、[agent-browser](https://github.com/vercel-labs/agent-browser)、[browser-use CLI](https://docs.browser-use.com/open-source/browser-use-cli)，从架构、技术原理、适用场景等维度展开分析。

---

## 一、一句话定位

| 工具 | 定位 |
|---|---|
| **OpenCLI** | 万能遥控器 — 把网站、Electron 应用、本地 CLI 统一为命令行 |
| **agent-browser** | 通用机械臂 — 为 AI Agent 设计的高性能浏览器自动化原语 |
| **browser-use CLI** | 机械臂 + 云平台 — 浏览器自动化 CLI + Browser Use Cloud 管理 |

---

## 二、项目概况

| 维度 | OpenCLI | agent-browser | browser-use CLI |
|---|---|---|---|
| **作者** | jackwener（个人） | Vercel Labs | Browser Use 团队 |
| **语言** | TypeScript (Node.js) | Rust（原生二进制） | Python |
| **Stars** | 5.4k | — | 83.8k（与 Python 库共享仓库） |
| **License** | Apache-2.0 | Apache-2.0 | MIT |
| **安装** | `npm install -g @jackwener/opencli` | `npm install -g agent-browser` | `curl -fsSL https://browser-use.com/cli/install.sh \| bash` |

---

## 三、架构深度对比

### 3.1 OpenCLI：Browser Bridge + Dual-Engine

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

**Browser Bridge** 是其连接浏览器的核心，由两部分组成：

1. **Chrome Extension** — 安装在 Chrome 中，能在网页上下文中执行 JavaScript，访问已登录的 session
2. **Micro-daemon** — 自动启动，监听 `localhost:19825`，管理 CLI 与 Extension 之间的 WebSocket 连接

```
opencli (Node.js) ←WebSocket→ micro-daemon ←Chrome API→ Chrome Browser
```

**Dual-Engine（双引擎）** 是 OpenCLI 的适配器编写机制：

- **YAML Pipeline**（声明式）：适合简单 API 抓取。Pipeline steps 为 `fetch → map → filter → limit → download`，支持模板表达式（`${{ args.limit }}`）
- **TypeScript Adapter**（编程式）：适合复杂浏览器交互。通过 `page` 对象提供 `goto()`、`evaluate()`、`waitForSelector()`、`click()` 等方法

> [!tip] Dynamic Loader
> 只需把 `.yaml` 或 `.ts` 文件丢到 `clis/` 目录即可自动注册，无需手动配置。

### 3.2 agent-browser：Rust Daemon + Accessibility Tree

agent-browser 采用 **Client-Daemon 架构**：

```
Rust CLI（客户端）←→ Native Daemon（纯 Rust）←CDP WebSocket→ Chrome for Testing
```

- Daemon 在首次命令时**自动启动**，多次命令之间**持久存活**
- 无需 Node.js 或 Playwright 运行时，直接通过 CDP 与 Chrome 通信
- Chrome 通过 `agent-browser install` 从 Google 的 [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) 下载

**核心创新：Accessibility Tree Snapshot**

`agent-browser snapshot` 返回页面的**无障碍树**而非 DOM：

```
- heading "Example Domain" [ref=e1]
- paragraph "This domain is for use in illustrative examples." [ref=e2]
- link "More information..." [ref=e3]
```

后续用 ref 操作元素：

```bash
agent-browser click @e3          # 点击链接
agent-browser fill @e5 "hello"   # 填写表单
```

> [!important] 为什么 Accessibility Tree 比 DOM 更适合 AI？
>
> | 维度 | Accessibility Tree | 完整 DOM |
> |---|---|---|
> | Token 消耗 | ~200-400 tokens | ~3000-5000 tokens |
> | 元素定位 | 确定性 ref（`@e1`） | 需要 CSS selector / XPath |
> | AI 友好性 | 纯文本，LLM 天然擅长解析 | HTML 结构复杂，噪声多 |

还支持 **diff snapshot**，对比两次 snapshot 差异来检测页面变化：

```bash
agent-browser diff snapshot                        # 当前 vs 上一次
agent-browser diff snapshot --baseline before.txt  # 当前 vs 保存的文件
```

### 3.3 browser-use CLI：Multi-Session Daemon + Element Index

browser-use CLI 采用 **多会话 Daemon 架构**：

```
CLI 命令 ←Unix socket→ Background Daemon（Python）←CDP→ Chromium / Chrome / Cloud Browser
```

- 第一条命令启动后台 daemon，浏览器保持打开
- 后续命令通过 Unix socket 通信，延迟约 **~50ms**
- 每个 `--session` 有独立的 daemon、socket、PID 文件

**Element Index 系统：**

`browser-use state` 返回页面所有可交互元素的编号列表：

```
[0] input "Name"
[1] input "Email"
[2] button "Submit"
```

通过索引操作：

```bash
browser-use input 0 "John Doe"
browser-use input 1 "john@example.com"
browser-use click 2
```

---

## 四、核心差异化能力

### 4.1 OpenCLI 独有：Electron 应用 CLI 化

这是 OpenCLI 最大的差异化优势。技术原理：

> Electron 应用本质是本地 Chromium 实例 → 启动时暴露 CDP 调试端口 → 通过 CDP 注入控制 UI

```bash
# 启动 Cursor IDE 并暴露 CDP
/Applications/Cursor.app/Contents/MacOS/Cursor --remote-debugging-port=9226
```

每个 Electron adapter 遵循 **5-Command Pattern**：

| 命令 | 作用 | 技术要点 |
|---|---|---|
| `status` | 连接测试 | 确认 CDP 通路 |
| `dump` | 逆向工程 | dump DOM + Accessibility Snapshot，提取 CSS selector |
| `send` | 文本注入 | 用 `document.execCommand('insertText')` 穿透 React 状态管理 |
| `read` | 内容提取 | 找语义化 selector，格式化为 Markdown |
| `new` | 新建操作 | 通过原生键盘快捷键（`Meta+N`）触发 |

已支持 8 个桌面应用：Cursor、Codex、Antigravity、ChatGPT、ChatWise、Notion、Discord、Doubao（豆包）。

> [!note] 非 Electron 应用的降级方案
> 对于微信、飞书等原生应用，使用 **AppleScript + 剪贴板**：`Cmd+A → Cmd+C → pbpaste`。精度较低但可用。

### 4.2 OpenCLI 独有：External CLI Hub

OpenCLI 还充当外部 CLI 的统一入口：

```bash
opencli gh pr list --limit 5     # GitHub CLI
opencli docker ps                # Docker
opencli kubectl get pods         # Kubernetes
opencli obsidian search query="AI"  # Obsidian CLI
```

纯 passthrough，自动发现、自动安装（如 `gh` 未安装则自动 `brew install gh`），并通过 `opencli register mycli` 注册自定义 CLI。

### 4.3 OpenCLI 独有：AI 驱动的 Adapter 生成

```bash
opencli explore https://example.com --site mysite  # 探索站点 API/能力
opencli synthesize mysite                           # 从探索结果生成 YAML adapter
opencli cascade https://api.example.com/data        # 自动降级探测认证策略
opencli generate https://example.com --goal "hot"   # 一键完成 explore → synthesize → register
```

认证策略级联：`PUBLIC → COOKIE → HEADER → BROWSER → CDP`

### 4.4 agent-browser 独有：安全防护体系

agent-browser 为 AI Agent 场景设计了完整的安全机制（全部 opt-in）：

| 特性 | 说明 |
|---|---|
| **Authentication Vault** | 加密存储凭证，LLM 永远看不到密码 |
| **Content Boundary Markers** | 随机 nonce 标记包裹内容，防 Prompt Injection |
| **Domain Allowlist** | 限制导航到受信域名，阻止数据泄露 |
| **Action Policy** | 静态策略文件控制允许/禁止的操作类别 |
| **Action Confirmation** | 敏感操作需要显式批准 |
| **Output Length Limits** | 防止上下文溢出 |

### 4.5 agent-browser 独有：多 Provider 支持

除了本地 Chrome，还支持多个云浏览器后端：

```bash
agent-browser -p browserless open example.com   # Browserless
agent-browser -p browserbase open example.com   # Browserbase
agent-browser -p browser-use open example.com   # Browser Use Cloud
agent-browser -p kernel open example.com        # Kernel（隐身+持久 Profile）
```

甚至支持通过 Xcode Simulator + Appium 控制 **iOS Safari**。

### 4.6 browser-use CLI 独有：三种浏览器模式

```bash
# 默认：Headless Chromium
browser-use open https://example.com

# 真实 Chrome Profile（复用登录态）
browser-use --profile "Default" open https://gmail.com

# Cloud 浏览器（反指纹 + CAPTCHA 解决 + 代理）
browser-use cloud connect --proxy-country US
```

### 4.7 browser-use CLI 独有：Cloud 平台深度集成

CLI 内置了 Browser Use Cloud 的完整 REST passthrough：

```bash
browser-use cloud v2 POST /tasks '{"task":"Search for AI news"}'  # 创建云端 Agent 任务
browser-use cloud v2 poll <task-id>                                # 轮询任务状态
browser-use cloud v3 POST /sessions '{"model":"bu-max"}'          # v3 Session
```

**v3 API 特有能力**：Workspaces（跨 session 持久化存储）、结构化输出（Pydantic schema）、文件上传/下载、成本控制（`max_cost_usd`）。

此外还有 **Skill 系统**，将网站交互变成可复用的 API：

```python
# 创建 Skill（~30 秒）
skill = await client.skills.create(
    goal="Extract top X posts from HackerNews...",
    agent_prompt="Go to https://news.ycombinator.com..."
)
# 执行
result = await client.skills.execute(skill.id, parameters={"X": 10})
```

### 4.8 browser-use CLI 独有：Python 持久会话

```bash
browser-use python "x = 42"              # 设置变量
browser-use python "print(x)"            # 跨命令访问（输出 42）
browser-use python "print(browser.url)"  # 访问内置 browser 对象
```

---

## 五、技术决策全景对比

| 维度 | OpenCLI | agent-browser | browser-use CLI |
|---|---|---|---|
| **抽象层次** | 高层（语义化命令） | 底层（DOM 原语） | 中层（元素索引） |
| **页面理解** | 预置 adapter，不需要理解 DOM | Accessibility Tree snapshot | Element index 列表 |
| **AI 角色** | 开发时（生成 adapter） | 运行时（理解+操作页面） | 运行时（理解+操作页面） |
| **性能** | Node.js | Rust 原生，最快 | Python + Daemon（~50ms） |
| **Batch 能力** | 无（顺序执行） | JSON 数组批量命令 | 无 |
| **通用性** | 仅预置平台（50+ 站点） | 任意网页 | 任意网页 |
| **桌面应用** | 核心能力（8 个 Electron 应用） | 不支持 | 不支持 |
| **外部 CLI** | Hub 模式（gh/docker/kubectl 等） | 不支持 | 不支持 |
| **Cloud** | 无 | 多 Provider（Browserless 等） | Browser Use Cloud 深度集成 |
| **安全机制** | 基础（复用 Chrome 登录态） | 完整体系（Vault/域名白名单/策略） | Cloud 级别（反指纹/CAPTCHA） |
| **登录处理** | Chrome 原生 session 复用 | 手动处理 / Auth Vault | Profile 复用 / Cloud Session |
| **输出格式** | table/json/yaml/csv/markdown | 文本（token 高效） | 文本 / JSON |
| **MCP 支持** | 无 | 无（CLI-first 设计） | `--mcp` 作为 MCP Server |

---

## 六、适用场景推荐

### 选 OpenCLI 的场景

- 需要操作**已知平台**（Bilibili、Twitter、小红书等），追求开箱即用
- 需要 CLI 化 **Electron 桌面应用**（Cursor、Notion、Discord 等）
- 想把各种 CLI 工具**统一入口**，让 AI Agent 通过 `opencli list` 自动发现
- 对可靠性要求高——预置 adapter 的稳定性远高于 LLM 实时决策

### 选 agent-browser 的场景

- 需要操作**任意未知网页**，没有预置 adapter 可用
- 对**性能**有极致要求（Rust 原生 + Batch 模式）
- 在乎 **AI Agent 安全**（Prompt Injection 防护、域名白名单等）
- 使用 Claude Code / Cursor 等 **AI Coding Agent**，需要一个 CLI 形式的浏览器工具
- 需要 **多云浏览器 Provider** 支持

### 选 browser-use CLI 的场景

- 已在使用 **browser-use Python 库**，需要 CLI 补充
- 需要 **Browser Use Cloud** 的能力（反指纹、CAPTCHA 解决、住宅代理）
- 需要在浏览器上下文中执行 **Python 脚本**
- 需要 **Skill 系统**，将浏览器操作封装为可复用 API

---

## 七、总结：三种流派的哲学

> [!quote] 三种哲学
> - **OpenCLI** 信奉 **"预先适配"** — 为每个平台做好 adapter，AI 只需调用语义化命令
> - **agent-browser** 信奉 **"通用原语"** — 提供最底层的操控能力，让 AI 自己理解和操作
> - **browser-use CLI** 信奉 **"平台化"** — 本地 CLI + Cloud 平台，覆盖从开发到生产的全链路

这三者并非完全互斥。一个理想的 AI Agent 工具链可能是：用 **OpenCLI** 操作已知平台和桌面应用（快速稳定），用 **agent-browser** 或 **browser-use CLI** 操作未知网页（灵活通用），再用 **Browser Use Cloud** 处理需要反爬能力的场景。

---

> [!info] 参考链接
> - [OpenCLI GitHub](https://github.com/jackwener/opencli)
> - [agent-browser GitHub](https://github.com/vercel-labs/agent-browser) | [官网](https://agent-browser.dev/)
> - [Browser Use CLI 文档](https://docs.browser-use.com/open-source/browser-use-cli) | [GitHub](https://github.com/browser-use/browser-use)
