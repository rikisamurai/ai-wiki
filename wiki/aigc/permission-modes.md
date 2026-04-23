---
title: 权限模式（YOLO / Safe / Plan）
tags: [claude-code, security, agent]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/💡claude-tips]]"
last-ingested: 2026-04-23
status: draft
---

Claude Code 的三档权限模式（[[wiki/obsidian/claudian|Claudian]] 也继承）控制 Agent 工具调用前是否需要用户确认，是 Agent 安全的第一道闸门。

> [!compare] 三档对比
> | 模式 | 工具调用 | 适用场景 |
> | --- | --- | --- |
> | **YOLO** | 全部直接执行，无需确认 | 信任度高、可回滚的环境（如 git worktree、沙箱） |
> | **Safe** | 每次工具调用都弹窗确认 | 重要 vault / 生产代码库 |
> | **Plan**（[[wiki/aigc/plan-mode\|Plan Mode]]） | 仅允许只读工具，写操作禁用 | 复杂任务的探索阶段 |

> [!warning] YOLO 不是"信任 LLM"
> YOLO 安全的前提是**环境本身可恢复**——git 干净、有 worktree 隔离、文件系统有快照。脱离这些前提的 YOLO 等于把方向盘丢给 Agent 上高速。

> [!tip] 命令黑名单与 [[wiki/aigc/mcp|MCP]] 搭配
> 三档之外还有两个细粒度旋钮：**Command blocklist**（正则拦截 `rm -rf` / `git push --force`）和 **Allowed export paths**（限制 vault 外可写目录，默认只放 `~/Desktop` `~/Downloads`）。结合 MCP server 的颗粒度，可以给"读 GitHub" YOLO，给"写数据库" Safe。

> [!example] CLI 临时覆盖
> 命令行参数会临时覆盖 [[settings-scopes|settings.json]] 的权限配置（优先级仅次于 Managed）：
> ```bash
> claude --dangerously-skip-permissions   # CI/脚本环境绕过所有确认
> claude --allowedTools "Edit,Write"      # 仅允许编辑/写入工具
> ```
> 持久化的策略写到 `.claude/settings.json`（项目共享）或 `~/.claude/settings.json`（个人全局）——CLI 参数适合一次性试验，不要让它成为常态。
