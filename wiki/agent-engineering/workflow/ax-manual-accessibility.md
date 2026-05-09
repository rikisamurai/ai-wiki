---
title: AXManualAccessibility（Electron 的 AX Tree 开关）
tags: [computer-use, electron, accessibility]
date: 2026-05-09
sources:
  - "[[sources/clippings/mac-computer-use-axmanualaccessibility]]"
last-ingested: 2026-05-09
status: draft
---

`AXManualAccessibility` 是 macOS Accessibility API 里的一个布尔 attribute——**外部 agent 把它对一个 Electron / Chromium 进程设为 `true`，就能让该 app 暴露内部完整的 Accessibility Tree**。这是 [[mac-computer-use|Mac Computer Use 架构]]里"结构层"在 Electron 应用上能不能跑通的开关。Electron 默认不暴露 AX Tree，外部工具看到的只是单个 `WebArea` 黑盒；翻开这个 bit 之后，按钮、输入框、列表等 HTML/CSS 渲染出的控件才能被 agent 读到。

> [!important] 它不是二进制 magic bit
> 名字里的"特殊比特位"容易让人以为是 Mach-O 文件里某个 flag。其实是**给目标进程动态设置的一个 AX 属性**——通过 `AXUIElementSetAttributeValue` 写入运行时的 AXUIElement，重启就丢。

## 怎么打开它

> [!example] Objective-C 形态
> ```objc
> CFStringRef kAXManualAccessibility = CFSTR("AXManualAccessibility");
> AXUIElementRef appRef = AXUIElementCreateApplication(app.processIdentifier);
> AXUIElementSetAttributeValue(appRef, kAXManualAccessibility, kCFBooleanTrue);
> ```

> [!example] Swift 形态
> ```swift
> let axApp = AXUIElementCreateApplication(pid)
> AXUIElementSetAttributeValue(
>   axApp,
>   "AXManualAccessibility" as CFString,
>   true as CFTypeRef
> )
> ```

调用方需要持有 macOS Accessibility 权限（系统设置 → 隐私与安全 → 辅助功能里勾选 agent 自身）。否则 `AXUIElementCreateApplication` 返回的 ref 写不进去。

## 为什么 Electron 需要这个

Electron app = Chromium + Node.js + Native Shell。按钮 / 输入框 / 菜单基本是 HTML/CSS/JS 渲染。macOS 默认不会去问 Chromium "请把内部 ARIA Tree 暴露给我"，所以系统辅助功能看到的就是：

> [!compare] 翻 bit 前后
> ```
> // 翻 bit 之前
> Window
> └── WebArea           ← 整个内容区只有这一个节点
>
> // 翻 bit 之后（Chromium 接到信号，开始把 ARIA Tree 投射到 AX）
> Window
> └── WebArea
>     ├── Button: 播放
>     ├── Input: 搜索
>     ├── ListItem: 歌曲 A
>     └── Button: 下载
> ```

Electron 官方文档明确说：第三方辅助技术可以通过设这个 attribute 手动开启 accessibility features。**它是一种"按需启用"——平时不开是为了省内存和 CPU**（维护 AX Tree 投射有持续开销）。

## 与 AXEnhancedUserInterface 的关系

> [!compare] 两个相关 attribute
> | 属性 | 作用 | 适用对象 |
> |---|---|---|
> | `AXManualAccessibility` | 让 Electron / Chromium 手动开启 AX Tree | Electron / Chromium 系 |
> | `AXEnhancedUserInterface` | 通用信号："当前有增强辅助交互需求" | 部分原生 app（取决于实现） |

实战经验：**两个属性都试一遍**。不同 Chromium / Electron 版本、不同 native app 对这两个 bit 的响应不一样，单试一个可能漏掉。开源 Computer Use 工具（Hammerspoon / Alma 等）的标准做法都是顺序设置两个。

## 翻不翻这个 bit 的稳定性差距

> [!example] 操作 Electron app 的两种姿势
> ```text
> 没翻 bit：  截图 → 视觉模型猜"屏幕 (430,680) 像是播放按钮" → 坐标点击
>             ↑ 窗口缩放 / 暗色模式 / 控件状态变 → 全套塌
>
> 翻了 bit：  AXChildren 找 role=AXButton, title=播放
>             → 拿元素 frame
>             → 调 AXPress（或对其 frame 中心点 CGEvent.postToPid）
>             ↑ 跨缩放 / 跨主题 / 跨语言（label 不变）都稳
> ```

[[wiki/agent-engineering/workflow/computer-use-agent-eval|Computer Use Agent Eval]] 评测里 Electron app 的成功率差距多半来自这一步——评测不会标注"你翻了 bit 没"，但底层调用栈翻没翻直接决定 task pass/fail。

## 与本 wiki 其他概念的连接

> [!note] 三个 macOS GUI agent 关键技术
> | 技术 | 解决什么 | 在哪 |
> |---|---|---|
> | [[mac-computer-use\|四层架构]] | 整体框架 | 本 workflow |
> | **AXManualAccessibility（本页）** | Electron 结构层退化问题 | 本 workflow |
> | [[wiki/skills/bgclick-rev-skill\|bgclick-rev]] | 后台点击不抢焦点的动作层 | wiki/skills |
>
> 三者组合 = 一个能稳定操作 Electron app（Slack / Notion / VS Code / 网易云 / 飞书）的 GUI agent。
