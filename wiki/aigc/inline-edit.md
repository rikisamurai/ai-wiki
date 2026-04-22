---
title: Inline Edit
tags: [claude-code, editor, workflow]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
last-ingested: 2026-04-22
status: draft
---

Inline Edit 是 [[wiki/obsidian/claudian|Claudian]]（同时也是 Cursor、VS Code Copilot 等工具）的一种局部编辑模式：选中文本 + 快捷键 + 自然语言指令，Agent 在原地改写并以 word-level diff 预览结果，确认后才落盘。它是聊天面板之外的一条"轻量旁路"。

> [!compare] Inline Edit vs 聊天面板
> | | Inline Edit | 聊天面板 |
> | --- | --- | --- |
> | 触发 | 选中 + 快捷键 | 切换面板 |
> | 上下文 | 选区为主，可读其他文件 | 全 vault / 整个项目 |
> | 写权限 | **只能改选区** | 全开 |
> | 适用 | 翻译、改语气、修小 bug | 多文件改动、设计决策 |
> | 反馈 | word-level diff 预览 | 自由对话 |

> [!tip] 写权限被收紧到选区是关键
> 这是 [[wiki/aigc/permission-modes|权限模式]] 思路的延伸——Inline Edit 等价于一个"作用域 = 当前选区"的临时 Safe Mode。Agent 即使"想"改其他文件也做不到，可以放心 YOLO。

> [!example] 高频用法
> - 选中一段中文 → "翻译成英文"
> - 选中函数 → "加 TypeScript 类型"
> - 选中段落 → "压成 3 句"
> - 光标处不选中 → "插入一个 React 组件壳子"
