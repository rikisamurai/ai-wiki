---
title: Browser-Use
tags: [browser-use, browser-automation, agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/CDP 视角下的 Browser 控制边界]]"
  - "[[sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具]]"
last-ingested: 2026-04-23
status: draft
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

**关联**：[[cdp|CDP]] / [[cdp-能力边界|CDP 能力边界]] / [[opencli|OpenCLI]] / [[wiki/aigc/agent-browser|agent-browser]]
