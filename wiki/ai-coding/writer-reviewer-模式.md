---
title: Writer/Reviewer 模式
tags: [multi-session, claude-code, workflow]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
last-ingested: 2026-04-22
status: draft
---

Writer/Reviewer 模式是**多会话并行**的一种典型用法：一个 Claude 会话负责实现，另一个负责审查，二者通过你（或 Agent Teams 自动协调）来回传递。它不只是"两个会话"，而是利用**[[wiki/ai-coding/subagent-上下文隔离|独立上下文]]**避免"自己审自己"的盲点。

> [!example] 标准节奏
> | 会话 A（Writer） | 会话 B（Reviewer） |
> |---|---|
> | "实现 API 限流中间件" | |
> | | "审查 rateLimiter.ts，检查边界情况、竞态条件" |
> | "根据审查反馈修改：[贴会话 B 输出]" | |
> | | "再审一遍，确认问题已修复" |

**为什么必须两个会话**：让同一个会话既写又审，相当于让模型审查"自己刚说服自己是对的代码"——它会下意识为已写代码辩护，[[ai-code-review|AI Code Review]] 的"扁鹊大哥效应"完全失效。两个独立会话各自从干净上下文出发，Reviewer 没看过 Writer 的"思路演化史"，更容易发现 [[plausible-code|似是而非的代码]]。

**与 [[wiki/ai-coding/subagent-上下文隔离|Subagent]] 的区别**

| 维度 | Subagent | Writer/Reviewer |
|---|---|---|
| **谁主谁副** | 主线程是主，subagent 是工具 | 平级，互为输入 |
| **数据流向** | 主→子，子返回结论 | 双向多轮 |
| **典型时长** | 一次性任务 | 持续多轮迭代 |
| **协调成本** | 主线程自动 | 你或 Agent Teams 协调 |

**多会话工具栈**

- **桌面应用**：可视化管理多会话，每个会话独立 [[wiki/superpowers/using-git-worktrees|worktree]]
- **Web 版**：Anthropic 云基础设施的隔离 VM
- **Agent Teams**：多会话自动协调，共享任务和消息队列

> [!tip] 文件级分发是更轻的并行
> Writer/Reviewer 适合**质量门控**；如果只是想批量处理一批独立文件，用 `claude -p` + Bash for 循环更合适：
> ```bash
> for file in src/*.py; do
>   claude -p "重构 $file" --allowedTools Edit,Read &
> done
> ```
> `--allowedTools` 限定权限，避免并行任务踩坑。
