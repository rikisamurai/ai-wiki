---
title: CDP 能力边界完整表
tags: [cdp, browser-automation, reference]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/CDP 视角下的 Browser 控制边界]]"
last-ingested: 2026-04-23
status: stable
---

[[cdp|CDP]] 对浏览器各功能的支持度可以做成一张查表——构建 Browser Agent 之前先对照表过一遍，省得做到一半发现"协议根本不支持"再返工。已能覆盖 ~95% 的 Browser-Use 业务功能。

> [!compare] 完整能力表（按必要性排序）
> | 分类 | 功能 | 必要性 | 支持度 | 备注 |
> |---|---|---|---|---|
> | 浏览器 | Tabs 管理 | 高 | 间接 | 用户拖拽改 tab 顺序 CDP 感知不到 |
> | 浏览器 | Navigate 导航 | 高 | 直接 | back/forward/refresh/goto |
> | 浏览器 | 扩展程序 | 中 | 直接 | 可注入 ad-block 让 DOM 干净 |
> | 浏览器 | 内部设置页 | 中 | 直接 | `chrome://history/` 等可 navigate |
> | 浏览器 | 设置菜单 | 低 | **不支持** | App 级，超出 CDP 范围 |
> | 快捷键 | 编辑类（复制/粘贴/全选） | 高 | 间接 | macOS 必须用 `commands` 参数 |
> | 快捷键 | 功能类（历史/退出） | 中 | 功能映射 | 用 navigate / `Browser.close` 替代 |
> | 网页 | 截图 | 高 | 直接 | 只截网页，不含 Chrome UI |
> | 网页 | 基础交互（click/drag/keyboard） | 高 | 间接 | Puppeteer 有原子方法 |
> | 网页 | Dialog 弹窗 | 高 | 间接 | Alert/Confirm/Prompt/Beforeunload 4 类 |
> | 网页 | Input 选择器 | 高 | 间接 | 系统 Select/Date/Color 截图截不到 |
> | 网页 | 文件上传/下载 | 高 | 直接 | `uploadFile` + `Browser.setDownloadBehavior` |
> | 网页 | 打印 | 中 | 直接 | `Page.pdf()` |
> | 网页 | 右键菜单 | 低 | 间接 | 系统级感知不到，DOM 自定义可截 |
> | 网页 | 书签/翻译/二维码 | 低 | **不支持** | 甜品功能，AI 场景用不到 |

> [!important] 必要性 × 支持度的设计含义
> **高必要 + 直接支持**（截图、navigate、文件上传）→ 立即可用，照搬即可
>
> **高必要 + 间接支持**（Tabs、Dialog、基础交互）→ 你必须自己封装一层，是 [[browser-use|browser-use]] 这类库的核心价值
>
> **高必要 + 不支持** → **不存在**——95% 覆盖率的来源
>
> **低必要 + 任何**（书签、翻译）→ AI 场景里直接放弃，越复杂越容易出 bug。Browser Agent 设计的关键是"敢于不做"。

> [!example] macOS 快捷键 commands 映射查表
> 编辑类快捷键在 macOS 上必须用 CDP `commands` 参数才能生效：
>
> | 操作 | macOS | Windows/Linux | CDP commands |
> |---|---|---|---|
> | 复制 | Cmd+C | Ctrl+C | Copy |
> | 粘贴 | Cmd+V | Ctrl+V | Paste |
> | 剪切 | Cmd+X | Ctrl+X | Cut |
> | 撤销 | Cmd+Z | Ctrl+Z | Undo |
> | 恢复 | Shift+Cmd+Z | Ctrl+Y | Redo |
> | 全选 | Cmd+A | Ctrl+A | SelectAll |
>
> 高权限快捷键（历史/退出/导航）走"功能映射"——不发快捷键，直接调对应的 CDP API。

> [!tip] LLM action 跨平台路由
> ```
> hotkey("ctrl+A")
>   → isMacOS ? keyboard('Meta+KeyA', {commands:['SelectAll']})
>             : keyboard('Control+KeyA')
> ```
> 在 Browser Agent 的 action 路由层做一次 OS 判断，把 LLM 输出的"统一快捷键"翻译成具体平台的 CDP 调用。"只做基础适配，遇到具体问题再修"——文中明确建议**别陷入快捷键无底洞**。

**关联**：[[cdp|CDP]] / [[browser-use|Browser-Use]] / [[wiki/retrieval/browser/agent-browser|agent-browser]] / [[opencli|OpenCLI]]
