---
title: Obsidian Bases
tags: [obsidian, view, query]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
last-ingested: 2026-04-22
status: draft
---

Obsidian Bases 是 Obsidian 1.7+ 内置的"数据库视图"功能，把 vault 里所有有 frontmatter 的笔记当数据行，用 YAML 配置定义视图、过滤器、公式、汇总。`.base` 文件可以用 `![[xxx.base#view-id]]` 嵌入到任意笔记。

> [!compare] Bases vs [[wiki/obsidian/dataview|Dataview]]
> | | Bases | Dataview |
> | --- | --- | --- |
> | 实现 | Obsidian 核心（1.7+） | 第三方插件 |
> | 配置 | YAML | DQL 类 SQL |
> | 视图 | 表格 / 卡片 | 列表/表格/任务/日历 |
> | 公式 | 表达式（类 Excel） | 函数 + 操作符 |
> | 性能 | 原生，更快 | 大库慢 |
> | 嵌入 | `![[file.base#view]]` | code block |

> [!example] 本仓库的用法
> 仓库根目录的 `index.base` 和 `log.base` 就是 Bases 文件——`index.md` 嵌入 `recent-wiki` 视图自动列最近 7 天更新；[[wiki/obsidian/inbox-工作流|inbox 工作流]] 用 Bases 视图过滤 `status: pending` 当待办列表。

> [!tip] 与 [[wiki/obsidian/obsidian-skills|obsidian-bases skill]] 的关系
> Bases 的 YAML 语法对人类好写，对 LLM 反而容易写错（视图 ID、公式、过滤器嵌套）。装 obsidian-bases skill 后 Agent 才能稳定生成正确的 `.base` 文件。
