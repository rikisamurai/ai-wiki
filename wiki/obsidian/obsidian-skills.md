---
title: Obsidian Skills（kepano）
tags: [obsidian, agent-skills, claude]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
last-ingested: 2026-04-22
status: stable
---

Obsidian Skills 是 Obsidian CEO Kepano 维护的官方 [[wiki/aigc/agent-skills|Agent Skills]] 集合（github.com/kepano/obsidian-skills），让任何兼容 Skills 规范的 Agent（[[wiki/obsidian/claudian|Claudian]]、Claude Code、Codex CLI、OpenCode）都能正确处理 Obsidian 特有的文件格式。

> [!example] 包含 5 个 skill
> | Skill | 作用 |
> | --- | --- |
> | **obsidian-markdown** | 处理 Obsidian Flavored Markdown：wikilinks、callouts、properties、embeds |
> | **[[wiki/obsidian/obsidian-bases\|obsidian-bases]]** | 生成 `.base` 文件（视图、过滤器、公式、汇总） |
> | **[[wiki/obsidian/json-canvas\|json-canvas]]** | 编辑 `.canvas` 文件（节点、边、分组） |
> | **[[wiki/obsidian/obsidian-cli\|obsidian-cli]]** | 通过 Obsidian CLI 操作 vault |
> | **[[wiki/obsidian/defuddle\|defuddle]]** | 用 Defuddle CLI 抓干净 Markdown 进 vault |

> [!tip] 安装路径与 Agent 绑定
> | Agent | 路径 |
> | --- | --- |
> | Claude Code / Claudian | `{vault}/.claude/skills/` |
> | Codex CLI | `~/.codex/skills/` |
> | OpenCode | `~/.opencode/skills/obsidian-skills/` |
>
> 也可以用 `/plugin marketplace add kepano/obsidian-skills` 走 marketplace 一键装。

> [!note] 为什么需要这套
> 不装的话 LLM 经常生成"语法上是 Markdown 但 Obsidian 不认"的内容——用 `[link](file.md)` 而不是 `[[wikilink]]`，YAML frontmatter 字段写错位，Bases 公式语法出错。Skills 把这些约束以官方文档形式喂给 Agent，等效于给 Agent 装了"Obsidian 母语模式"。
