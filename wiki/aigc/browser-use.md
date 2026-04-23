---
title: Browser-Use
tags: [browser-use, browser-automation, agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/CDP 视角下的 Browser 控制边界]]"
  - "[[sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具]]"
  - "[[sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/AI Agent 的三种浏览器控制流派：OpenCLI、agent-browser、browser-use CLI 深度对比]]"
  - "[[sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/OpenCLI、Agent-Browser 与 Browser-Use 深度横向评测]]"
last-ingested: 2026-04-23
status: stable
---

Browser-Use 是 AI Agent 操作真实浏览器的总称——既指开源库 [browser-use](https://github.com/browser-use/browser-use)（Python），也指更广义的"让 LLM 看着截图点按钮"的范式。它和 [[opencli|OpenCLI]]、[[wiki/aigc/agent-browser|agent-browser]] 同属 [[cdp|CDP]] 之上的应用层。

> [!important] 三大流派
> 浏览器自动化在 Agent 时代分化出三种思路：
> | 流派 | 代表 | 思路 |
> |---|---|---|
> | **Browser-Use 派** | browser-use Python 库 | LLM 看截图 + DOM，输出 click/type 坐标 |
> | **CLI 派** | [[opencli\|OpenCLI]] | 把网站包成命令行工具，agent 调命令 |
> | **专用 Agent 派** | [[wiki/aigc/agent-browser\|agent-browser]] | 浏览器层针对 agent 优化（无 UI 干扰、专用 selectors） |
>
> 三者都跑在 CDP 之上——区别在**让 LLM 处理多原始的输入**。Browser-Use 给最原始（截图），CLI 给最抽象（命令），agent-browser 介于两者。

**架构核心：CDP + LLM 的视觉环路**

```
LLM "我看到登录按钮，应该点它"
    ↓ 输出 action: click(x=520, y=340)
CDP `Input.dispatchMouseEvent(...)`
    ↓
浏览器执行点击
    ↓
等待 DOM 变化 / 截新图
    ↓
回到 LLM 决策
```

每一轮"看图 → 想 → 点"是一个 perception-action loop。Browser-Use 的核心工作其实是**把这套循环工程化**：截图压缩、DOM 抽象、错误恢复、坐标系对齐。

> [!warning] 截图坐标的 VLM 陷阱
> 部分视觉模型用**完整 Chrome 截图**训练（含地址栏 + tab bar），但 [[cdp|CDP]] 的 `Page.captureScreenshot` 只截网页本身。直接喂给这类 VLM 会产生**坐标系错位**——LLM 以为按钮在屏幕 (520, 340)，实际网页里在 (520, 280)。这是 Browser Agent 最难调的问题之一，详见 [[cdp|CDP § 截图]]。

**95% 业务功能覆盖率**

[[cdp-能力边界|CDP 能力表]]列了 15 个功能——除了"设置菜单"和"书签/翻译"这两类**低必要**功能，其余都至少能间接支持。也就是说**业务上能想到的浏览器操作 95% 能做**，剩下 5% 基本是甜品功能。这是 Browser-Use 范式可行的根本原因。

> [!compare] 直接支持 vs 间接支持
> "直接支持"的 API（截图、navigate、文件上传）是 Puppeteer 已封装的；**"间接支持"才是各家 Browser-Use 库的核心价值**——Tabs 管理、Dialog 处理、Input 选择器适配，每家都得自己封一层。如果你在挑库，看的不是"支不支持"，是**"间接支持那部分封装得是否地道"**。

> [!tip] 跨平台快捷键
> 跨 macOS / Windows / Linux 的快捷键差异是 Browser Agent 的隐性坑——LLM 不知道 OS。在 action 路由层做一次 OS 判断翻译（详见 [[cdp-能力边界|CDP 能力表 § 快捷键]]），别让 LLM 自己处理这层差异。

**反模式：让 Agent 处理"低必要"功能**

> [!warning] 别让 Agent 操作设置菜单 / 翻译 / 书签
> 这些功能 [[cdp|CDP]] **不支持**，靠组合 hack 能勉强做到，但极脆弱：
> - 设置菜单 UI 改一次，所有 hack 失效
> - 浏览器版本升级可能突然不工作
> - LLM 误识别概率比常规网页高得多
>
> AI 场景的设计原则：**敢于不做**。把这些功能从 Agent 的 action 集合里拿掉，整体可靠性反而上升。

**browser-use CLI：Element Index + 多模态**

[browser-use CLI](https://docs.browser-use.com/open-source/browser-use-cli)（Python，多会话 Daemon，~50ms 命令延迟）是 browser-use 派最成熟的实现：

```
[0] input "Name"
[1] input "Email"
[2] button "Submit"
```

```bash
browser-use input 0 "John Doe"
browser-use click 2
```

> [!compare] Element Index vs Refs vs 适配器
> | 工具 | 状态表征 | LLM 角色 |
> |---|---|---|
> | browser-use | DOM + 数字索引 + 视觉 Bounding Box | 运行时理解+操作 |
> | [[agent-browser\|agent-browser]] | Accessibility Tree + `@e1` Refs | 运行时理解+操作（Token 更省） |
> | [[opencli\|OpenCLI]] | 完全隐藏 DOM | 仅在"探索期"理解，运行期 0 推理 |
>
> browser-use 独有：**视觉边界框**——把数字索引以 BBox 形式叠在截图上，配合 GPT-4o / Claude Sonnet 4 这类 VLM 能解决"DOM 存在但被遮挡"的问题。代价是更高的 Token 与延迟。

**三种浏览器模式**

```bash
browser-use open https://example.com                          # Headless Chromium（默认）
browser-use --profile "Default" open https://gmail.com         # 真实 Chrome Profile（复用登录态）
browser-use cloud connect --proxy-country US                   # Cloud（反指纹 + CAPTCHA + 代理）
```

**Cloud 平台深度集成**

CLI 内置 Browser Use Cloud 完整 REST passthrough：

```bash
browser-use cloud v2 POST /tasks '{"task":"Search for AI news"}'
browser-use cloud v3 POST /sessions '{"model":"bu-max"}'
```

**v3 API 特有**：Workspaces（跨 session 持久化）、结构化输出（Pydantic schema）、文件上传/下载、`max_cost_usd` 成本控制。

> [!example] Skill 系统：把网站交互变成可复用 API
> ```python
> skill = await client.skills.create(
>     goal="Extract top X posts from HackerNews...",
>     agent_prompt="Go to https://news.ycombinator.com..."
> )
> result = await client.skills.execute(skill.id, parameters={"X": 10})
> ```
> 探索期 ~30 秒生成 Skill，之后调用就走结构化参数——和 [[opencli|OpenCLI]] 的"适配器"思路殊途同归，区别在 Skill 是 LLM 自动生成、OpenCLI 适配器需要人写或半人工。

> [!tip] `--mcp`：作为 MCP Server 的入口
> `browser-use --mcp` 直接把整个 CLI 暴露为 [[mcp|MCP]] Server，是三家里唯一原生支持 MCP 的——agent-browser 和 OpenCLI 都倾向"反 MCP，走轻量 CLI / Skill"路线。

> [!example] 量化基准：稳健换延迟
> 标准化 Web Agent 基准（最多 20 步 / 6 分钟内完成"找特定食谱"等任务）：
>
> | 工具 | 自报告完成 | LLM 评估实际 | 整体可靠性 | 平均耗时 |
> |---|---|---|---|---|
> | Notte（高度定制） | — | 79.0% | 96.6% | 47s |
> | **browser-use** | **77.3%** | **60.2%** | **83.3%** | **113s** |
> | Convergence | — | 31.4% | 50.0% | 83s |
>
> 113 秒 vs 47 秒——这是"为了在动态网站上不失败"必须付出的深度解析 + 视觉校验代价。
>
> **配 Bright Data 等住宅代理时**：7 个防御最严域名平均 **98.44% 成功率**（Zillow / Indeed 等达 100%）——这是其他两家拍马都赶不上的"反爬天花板"，归功于 1.5 亿动态住宅 IP + 网络级 CAPTCHA 解决。

> [!warning] AI 安全：间接 Prompt Injection 80% ASR
> Browser-Use 类工具把抓到的网页文本注入 LLM 上下文——CIA triad 评估发现 **5 种主流 Web Agent（含 browser-use）面对恶意网页时攻击成功率高达 80%**。已有 CVE 记录与 PoC：
>
> - 激活摄像头 / 窃取本地文件 / 用户身份伪造
> - 诱导 Agent 死循环刷新页面（DoS）
>
> 缓解：[[agent-browser|agent-browser]] 的 `--content-boundaries` 用 nonce 包裹外部内容；browser-use 本身**没有内置等价机制**——这是用 browser-use 跑生产 Agent 时必须自己加一层的安全空白点。参考 [[wiki/aigc/fail-closed-tool-defaults|Fail-Closed 工具默认]]。

**关联**：[[cdp|CDP]] / [[cdp-能力边界|CDP 能力边界]] / [[opencli|OpenCLI]] / [[agent-browser|agent-browser]] / [[mcp|MCP]] / [[claude-code|Claude Code]]
