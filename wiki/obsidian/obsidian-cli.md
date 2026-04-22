---
title: Obsidian CLI
tags: [obsidian, cli, automation]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
last-ingested: 2026-04-22
status: draft
---

Obsidian CLI 是官方提供的命令行工具（help.obsidian.md/cli），让脚本和 Agent 不打开 GUI 就能操作 vault：读写笔记、搜索、触发命令面板的命令、调试插件和主题。

> [!example] 典型操作
> | 命令 | 用途 |
> | --- | --- |
> | `obsidian note read <path>` | 读笔记内容 |
> | `obsidian note write` | 创建/更新笔记 |
> | `obsidian search "<query>"` | 全文搜索 |
> | `obsidian command run <id>` | 触发命令面板里的任意命令 |
> | `obsidian plugin reload <id>` | 插件热重载（开发调试） |

> [!compare] CLI vs [[wiki/aigc/mcp|MCP server]] vs URI
> | | CLI | MCP server | obsidian:// URI |
> | --- | --- | --- | --- |
> | 形态 | shell 命令 | LLM 工具 | URL 链接 |
> | 适合 | 脚本、Agent Bash 调用 | LLM 直接调 | 跨应用跳转 |
> | 需 GUI | 否 | 否 | 是 |

> [!tip] Agent 用法
> 配 [[wiki/obsidian/obsidian-skills|obsidian-cli skill]] 后，Claude Code / [[wiki/obsidian/claudian|Claudian]] 在 vault 内做"批量重命名"、"批量改 frontmatter"、"插件开发热重载"时能直接调 CLI 而不是跑 GUI 操作录制——比 Bash 操作 `.md` 文件更安全（CLI 会校验 vault 索引）。
