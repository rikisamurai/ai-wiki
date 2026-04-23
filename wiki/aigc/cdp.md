---
title: CDP（Chrome DevTools Protocol）
tags: [cdp, browser-automation, agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/CDP 视角下的 Browser 控制边界]]"
last-ingested: 2026-04-23
status: draft
---

CDP（Chrome DevTools Protocol）是 Chromium 提供的远程调试协议——本意是给 DevTools 用，但被 Puppeteer / Playwright / Browser Agent 拿来当**浏览器控制 API**。AI Agent 操作浏览器（[[browser-use|browser-use]]、[[opencli|OpenCLI]]、agent-browser）几乎都跑在 CDP 上。理解它的能力边界，决定了你的 Agent 能做什么、不能做什么。

> [!important] 它不是"能控制浏览器"，是"能调试浏览器"
> CDP 设计初衷是 debug，**所有不属于调试范畴的功能都不在协议里**——书签、历史记录里的联想、设置菜单、扩展 UI、Chrome 账号弹窗。这就是为什么 Browser Agent 经常"看不到"用户视角下显眼的东西——不是 bug，是协议本身就没暴露这层。

> [!compare] 能力同心圆
> ```
> Computer ⊃ Browser ⊃ CDP ⊃ Puppeteer
> ```
> | 层 | 范围 | 限制 |
> |---|---|---|
> | Computer | 全集 | 没有限制 |
> | Browser | App 层权限 | 不能直接操作本地文件等 |
> | **CDP** | 调试能力 | 收藏/历史联想等非调试信息无权限 |
> | Puppeteer | CDP 子集 | 没用全部 CDP API |
>
> 选库的影响：用 Puppeteer 时遇到"做不到"，先看是 Puppeteer 没封装、还是 CDP 真做不到。前者你可以直接调 raw CDP API；后者只能换思路。

**[[cdp-能力边界|3 档能力边界]]**

CDP 对每个浏览器功能可分为：

- **直接支持**：Puppeteer 有现成 API（截图、navigate、文件上传）
- **间接支持**：组合多个 CDP API（Tabs、Dialog、基础交互）
- **不能支持**：CDP 协议没暴露（设置菜单、书签、翻译）

详细能力清单见 [[cdp-能力边界|CDP 能力边界完整表]]——里面把 15 个浏览器功能按必要性 × 支持度做了二维分类，是设计 Browser Agent 时的查表。

> [!warning] macOS 上的快捷键陷阱
> CDP 在 macOS 发送 `Meta+KeyA` **不会真的全选**——这个 bug 从 2017 年就存在。原因：CDP 发送的不是真系统键盘事件，作用域被限制在 Chrome/Page 内部。绕开方法是用 `Input.dispatchKeyEvent` 的 `commands` 参数：
>
> ```javascript
> await page.keyboard.down("KeyA", { commands: ["SelectAll"] });
> await page.keyboard.up("KeyA");
> ```
>
> 这是 Browser Agent 在 macOS 上"为什么 Cmd+A 不工作"的**唯一**正确解释。

> [!tip] 截图坐标的隐性坑
> CDP 的 `Page.captureScreenshot` 只截**网页本身**——不包含 Chrome 浏览器外部 UI（地址栏、tab bar）。但**部分 VLM 模型训练时用的是完整 Chrome 截图**——直接把 CDP 截图喂给这些 VLM 会导致 action 坐标系统错位。要么换 VLM、要么自己合成完整截图。

**关联**：[[cdp-能力边界|CDP 能力边界]] / [[browser-use|Browser-Use]] / [[opencli|OpenCLI]] / [[wiki/aigc/agent-browser|agent-browser]]
