---
title: Claude HUD（Statusline 仪表盘）
tags: [claude-code, observability, plugin]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/🛠️claude-code-tools]]"
last-ingested: 2026-04-23
status: draft
---

Claude HUD 是 Claude Code 的 statusline 插件，把 [[wiki/agent-engineering/context/context-window|上下文窗口]] 健康度、speed limit 消耗、subagent 状态、tool 活动**实时显示在终端输入区下方**。它解决的核心问题：Claude Code 的"context 还剩多少、被谁占了"在原生 UI 里几乎不可见，等到 [[wiki/agent-engineering/context/compact-vs-clear|自动 compact]] 触发时已经晚了。

> [!example] 显示效果
> ```
> [Opus] │ my-project git:(main*)
> Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
> ```
>
> 进度条颜色绿→黄→红，**红的时候就该主动 [[compact-vs-clear|/compact]] 或 [[handoff-md|HANDOFF]]** 而不是继续硬塞。

> [!important] 为什么 statusline 比"事后查 cost"重要
> `/cost` 是回顾性的——它告诉你已经花了多少。HUD 是预警性的——它让你**在窗口被填满之前**做决策。这与 [[wiki/agent-engineering/context/context-rot|Context Rot]] 的核心命题一致：模型在窗口接近上限时智商最不在线，主动管理必须**提前**。

**安装与配置**（前置：Claude Code v1.0.80+，Node 18+）

```bash
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```

三档预设：**Full**（全开）/ **Essential**（活动 + git）/ **Minimal**（只 model + context 进度条）。日常推荐 Essential——Full 信息量大但屏幕拥挤，Minimal 又少了 subagent 状态这种关键信号。

> [!tip] 与 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]]搭配
> 当主线程派出多个 subagent 并行时，HUD 的"Agent 追踪"区会显示每个 worker 的运行状态和耗时——这是少数能看到 [[wiki/agent-engineering/workflow/subagent-上下文隔离|subagent]] 内部进度的方式。否则你只能等它返回最终报告才知道发生了什么。

**关联**：HUD 是 Claude Code 提供的 [statusline API](https://docs.anthropic.com/en/docs/claude-code/settings#statusline) 的应用——你也可以用 `/statusline` skill（项目内的 `statusline-setup` agent）配置自己的极简版本，不必完整安装 HUD。
