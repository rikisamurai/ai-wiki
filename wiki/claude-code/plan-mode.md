---
title: Plan Mode
tags: [claude-code, agent, workflow]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
last-ingested: 2026-04-22
status: stable
---

Plan Mode 是 Claude Code 的一种工作模式：Agent 先用只读工具探索代码库、设计实施方案，把计划呈给用户审批后再动手执行。在 Claude Code CLI 和 [[wiki/obsidian/claudian|Claudian]] 里通过 `Shift+Tab` 切换。

> [!note] 为什么要有这个模式
> 复杂多步骤任务里，Agent 经常"边想边做"——做了三步发现方向不对，回退成本高。Plan Mode 强制把"思考"和"执行"分两个阶段：第一阶段只读，确保 Agent 充分理解上下文；第二阶段才允许写。

> [!compare] Plan Mode vs 直接动手
> | 维度 | 直接执行 | Plan Mode |
> | --- | --- | --- |
> | 适用任务 | 单步、目标明确 | 多步、跨文件、有架构决策 |
> | 用户介入 | 中途看到错走再叫停 | 计划阶段一次审批 |
> | 工具权限 | 全开 | 只读探索，写操作禁用 |
> | 失败成本 | 已写入需回滚 | 仅丢弃计划 |

> [!tip] 与 [[wiki/claude-code/permission-modes|权限模式]] 的关系
> Plan Mode 本身就是 YOLO/Safe/Plan 三档权限里的一档——核心机制是"工具白名单收紧到只读"。Safe Mode 是逐次确认每个工具调用，Plan Mode 是直接禁掉一类工具，思路不同但都是降低 [[wiki/agent-engineering/philosophy/plausible-code|似是而非代码]] 的产生。
