---
title: Agent Skills 规范
tags: [agent, claude-code, spec]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
  - "[[sources/posts/aigc/ai-coding/blog/🛠️ 构建 Claude Code 的经验：如何使用 Skills]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-22
status: draft
---

Agent Skills 是一种跨 Agent 通用的能力包格式（规范见 agentskills.io），让 Claude Code、Codex CLI、OpenCode 等不同客户端都能消费同一份"技能"。它把 prompt、工具描述、调用约束打包成一个 `skill.md` 文件，按上下文自动触发，不需要写在 system prompt 里也能让 Agent 用上。

> [!compare] Agent Skills vs Slash Command vs Subagent
> | | Skill | Slash Command | [[wiki/ai-coding/subagent-上下文隔离\|Subagent]] |
> | --- | --- | --- | --- |
> | 触发 | Agent 根据上下文自动调用 | 用户显式 `/cmd` | 用户/Agent 显式分派 |
> | 上下文 | 注入到主对话 | 注入到主对话 | 独立隔离上下文 |
> | 适合 | 领域知识 + 操作约束 | 高频固定动作 | 大块独立任务 |

> [!example] 一个 skill 的最小结构
> ```yaml
> ---
> name: obsidian-markdown
> description: 创建和编辑 Obsidian Flavored Markdown
> when_to_use: 用户在 vault 内编辑 .md 文件时
> ---
>
> （正文 prompt + 示例 + 反例）
> ```
> Agent 在每次决策前会扫一遍可用 skills 的 description，符合就把正文加载进上下文。

> [!tip] 跨 Agent 复用
> 同一份 skill 仓库（如 [[wiki/obsidian/obsidian-skills|obsidian-skills]]）能服务多种 Agent —— Claude Code 装到 `.claude/skills/`，Codex CLI 装到 `~/.codex/skills`，[[wiki/obsidian/claudian|Claudian]] 装到 `{vault}/.claude/skills/`。这是 [[wiki/aigc/mcp|MCP]] 之外另一条"标准化 Agent 生态"的路径。

## 深入

- [[skills-9-分类]]：Anthropic 内部几百个 Skills 归纳出的 9 大类别，写新 Skill 前先判定属于哪类
- [[skill-编写实践]]：踩坑点章节、`description` 是 if-then、不要说显而易见的事等钢律
- [[渐进式披露]]：把 SKILL.md 当索引，细节下沉到 `references/` 和 `assets/`
