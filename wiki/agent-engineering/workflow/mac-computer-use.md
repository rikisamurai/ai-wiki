---
title: Mac Computer Use 架构（视觉 + AX + 事件 + 权限）
tags: [computer-use, macos, gui-agent]
date: 2026-05-09
sources:
  - "[[sources/clippings/mac-computer-use-axmanualaccessibility]]"
last-ingested: 2026-05-09
status: draft
---

Mac Computer Use 不是"截图 + 坐标点击"——它是 **screen capture（视觉理解）+ macOS Accessibility Tree（结构理解）+ CGEvent / AXPress（事件注入）+ TCC 权限审批** 四层组合。任何"agent 操作 Mac GUI"的方案都至少踩到这四层中的一层；漏掉其中一层就会在某类场景翻车。这是理解 [[wiki/agent-engineering/workflow/computer-use-agent-eval|Computer Use Agent Eval]] 评测对象的前置背景。

> [!important] 为什么纯截图点击不够
> "看图猜按钮、点 (430, 680)"在三类场景下不可靠：窗口被遮挡（截图不全）、多显示器/多 Space（坐标变换）、缩放/布局变化（坐标漂移）、Electron WebUI（控件无原生语义）。AX Tree 把"猜哪是按钮"换成"查 `role=AXButton, title=播放` 的元素"，稳定性差一个量级。

## 四层架构

> [!example] 链路图
> ```
> 视觉层    截图 / OCR / 视觉模型           ← 屏幕录制权限
>    ↓
> 结构层    macOS AX Tree / AXUIElement     ← Accessibility 权限
>    ↓
> 动作层    CGEvent.postToPid / AXPress / 键盘事件
>    ↓
> 安全层    app allowlist / 敏感操作审批 / TCC 弹窗
> ```

**视觉层** 解决"看到什么"，**结构层** 解决"哪个元素是什么 role"，**动作层** 解决"怎么按下去"，**安全层** 解决"用户允不允许"。四层缺一不可：

> [!compare] 缺一层会怎么样
> | 缺哪层 | 翻车场景 |
> |---|---|
> | 视觉层 | 命令行 GUI、Canvas 渲染（无 AX 节点） → 看不见就点不到 |
> | 结构层 | Electron / 复杂自定义控件 → 坐标漂移、按错钮 |
> | 动作层 | 纯输出报告 → 不能闭环 |
> | 安全层 | 敏感操作（删文件、转账）裸跑 → 真出事 |

## 结构层是稳定性的关键

AX Tree 类似一棵给系统辅助功能用的"语义化 DOM"，能给 agent 提供：当前窗口列表、控件 role/label/value/state、bounds、可执行 action（AXPress/AXIncrement 等）。这是 [[ax-manual-accessibility|AXManualAccessibility]] 这个 attribute 重要的根本原因——**没有 AX，Electron 应用对系统就是一个黑盒 WebArea**，整棵子树看不见，结构层退化成空洞，agent 必须回退到纯视觉。

> [!example] 与浏览器/前端的类比
> | 桌面 GUI | 前端等价物 |
> |---|---|
> | 截图 + 视觉模型 | 截图 + OCR |
> | macOS AX Tree | 语义化 DOM / [ARIA Tree](https://www.w3.org/TR/wai-aria-1.2/) |
> | AXManualAccessibility | 强制 Chromium 暴露内部 ARIA Tree |
> | AXPress / CGEvent click | Playwright `getByRole('button',{name:'播放'}).click()` |

把 Computer Use 类比 [[wiki/retrieval/browser/cdp|CDP]] 的浏览器自动化是有道理的：CDP 给 agent 一棵 DOM 树，AX 给 agent 一棵 OS 级 UI 树。**控制 web 用 CDP，控制原生 / Electron 用 AX**——两者解决的是同一个问题（结构化感知）在不同 surface 上的实例。

## 完整运行序列

> [!example] 一次操作的 8 个步骤
> 1. 获取用户授权（屏幕录制 + Accessibility 两个独立 TCC 弹窗）
> 2. 枚举窗口和目标 App（pid / window bounds / Space / display）
> 3. 对 Electron 做增强：`AXUIElementCreateApplication(pid)` 后设 [[ax-manual-accessibility|AXManualAccessibility]] = true（必要时 + AXEnhancedUserInterface）
> 4. 读取 UI 结构：AXChildren / AXRole / AXTitle / AXValue / AXFrame / AXActions
> 5. 视觉层补足：截图 + OCR + 图像识别 + 坐标转换（用于 AX 看不到的元素）
> 6. 规划操作：找按钮 / 找输入框 / 找菜单项，判断是否需要审批
> 7. 执行：AXPress / CGEvent 点击 / 键盘输入 / 粘贴 / 菜单
> 8. 反馈校验：再截图 + 再读 AX，判断是否成功

第 7 步的"后台点击不抢焦点"是另一类硬技术——见 [[wiki/skills/bgclick-rev-skill|bgclick-rev]] 对 `CGEvent.postToPid` + `kCGMouseEventWindowUnderMousePointer` 这条 path 的逆向分析；那是动作层在"Computer Use 不打断用户"这个约束下的具体实现。

## 关联

- 评测视角：[[wiki/agent-engineering/workflow/computer-use-agent-eval|Computer Use Agent Eval]]（OSWorld / WebArena）
- 浏览器对应物：[[wiki/retrieval/browser/cdp|CDP]] / [[wiki/retrieval/browser/agent-browser|agent-browser]]
- AX 关键开关：[[ax-manual-accessibility|AXManualAccessibility]]
- 后台点击实现：[[wiki/skills/bgclick-rev-skill|bgclick-rev]]
