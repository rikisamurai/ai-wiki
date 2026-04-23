---
title: Claudian
tags: [obsidian, plugin, claude-code]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
last-ingested: 2026-04-22
status: stable
---

Claudian 是把 Claude Code 嵌入 Obsidian 的第三方插件，让整个 vault 成为 Claude 的工作目录。它复用了 Claude Code CLI 的全部 agentic 能力——文件读写、Bash、搜索、多步骤工作流——同时把 Obsidian 的 wikilink、frontmatter、笔记选区作为上下文喂给模型。

> [!note] 与"在 Obsidian 里调 ChatGPT"的根本区别
> 普通 AI 插件是"输入框 + API 调用"。Claudian 是把 Obsidian 当 Claude Code 的工作目录——`@filename` 引用文件、Inline Edit 原地改写、[[wiki/aigc/plan-mode|Plan Mode]] 先设计后执行、[[wiki/aigc/permission-modes|YOLO/Safe/Plan 权限分级]] 都直接继承自 CLI。

> [!example] 上下文管理是核心卖点
> | 操作 | 效果 |
> | --- | --- |
> | 自动附加当前笔记 | 打开笔记直接聊，无需复制粘贴 |
> | `@filename` | 引用 vault 内任意文件 |
> | `@Agents/` | 调用自定义子 agent |
> | `@mcp-server` | 激活 [[wiki/aigc/mcp\|MCP]] 工具 |
> | Excluded tags | 防 `#sensitive` 笔记被自动加载 |

> [!tip] 复用 Claude Code 生态
> Skills 放在 `~/.claude/skills/` 或 `{vault}/.claude/skills/`，Agents 同理放 `agents/` 目录——格式与 Claude Code 原生兼容，可在 CLI 与 Claudian 之间无缝迁移。

> [!warning] 常见安装坑
> - 必须先安装 Claude Code CLI（推荐原生安装，避开 nvm/fnm/volta 路径问题）
> - GUI 应用找不到 CLI 时报 `spawn claude ENOENT`，去 Settings → Advanced → Claude CLI path 手动填 `which claude` 的输出
> - 仅桌面端，移动端不支持

支持通过 `ANTHROPIC_BASE_URL` 切换到 Openrouter / Kimi / GLM / DeepSeek 等兼容 Anthropic API 的后端。
