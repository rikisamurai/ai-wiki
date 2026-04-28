---
title: Codex Sandbox + Approval（双维度权限）
tags: [codex, security, permissions]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/codex/Codex Best Practices]]"
last-ingested: 2026-04-23
status: draft
---

Codex 把 Agent 权限拆成**两个正交维度**——比 Claude Code 的[[permission-modes|YOLO/Safe/Plan 三档]]更细，但也更需要理解后才能配对。

> [!compare] 两个独立维度
> | 维度 | 控制什么 | 类比 |
> |---|---|---|
> | **Sandbox Mode** | Codex 能读写哪些目录/文件 | 文件系统的"地理边界" |
> | **Approval Mode** | Codex 何时需要你点确认才能执行命令 | 触发器的"时间边界" |
>
> 两者独立配置——你可以给最大沙箱（read/write 整个仓库）但每条命令都要确认；也可以给最小沙箱（只读）但完全不打断。Claude Code 的"YOLO" ≈ Sandbox=full + Approval=never；"Safe" ≈ Sandbox=full + Approval=always。

> [!important] 拆开两个维度有什么用
> 现实场景里，"能不能改文件" 和 "要不要打断我" 经常需要分开决定：
> - **大重构 + 我盯着**：full sandbox，high approval（每步看一眼）
> - **后台跑长任务**：full sandbox，never approval（别打断我开会）
> - **改不熟悉的代码**：minimal sandbox，high approval（双保险）
> - **只想要 review，不要改**：read-only sandbox，never approval（自动跑完拿报告）
>
> Claude Code 把这两个维度合在 YOLO/Safe/Plan 里，简洁但少一些灵活度——所以 Plan Mode 之外要细配权限，得编辑 settings.json。

**Sandbox Mode 的典型档位**（Codex 文档语境）：

- **Read-only**：只能读，不能写——适合 review/分析
- **Workspace write**：可改当前工作区，不能跨出仓库根目录
- **Full access**：完全自由——慎用

**Approval Mode 的典型档位**：

- **Always**：每条 shell 命令都问
- **On-failure**：失败了才问（自动重试/调整）
- **Never**：完全静默——配 sandbox 限制使用

> [!warning] 默认是收紧的，明确需要再放
> Codex Best Practices 的原文："**Start with the defaults and loosen permissions only when needed.**" 因为很多"质量问题"本质是"权限问题"——错误的工作目录、缺写权限、模型默认值不对。先收紧、看哪里卡了再针对性放，比一上来全开然后到处踩坑安全得多。

> [!example] 配置层级
> | 位置 | 用途 |
> |---|---|
> | `~/.codex/config.toml` | 个人默认偏好 |
> | `.codex/config.toml`（仓库根） | 仓库共享行为 |
> | 命令行参数 | 一次性覆盖 |
>
> 与 [[settings-scopes|Claude Code Settings Scopes]] 同构——更具体的覆盖更宽泛的。

**关联**：[[permission-modes|Claude Code 权限模式]]（同一问题的不同设计） / [[wiki/claude-code/codex|Codex]] / [[wiki/claude-code/fail-closed-tool-defaults|Fail-Closed 默认]]（"默认收紧"在工具层的实现）
