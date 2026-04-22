---
title: Templater
tags: [obsidian, plugin, template]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/🚀obsidian-quick-start]]"
last-ingested: 2026-04-22
status: draft
---

Templater 是 Obsidian 的高级模板插件，相比核心"模板"插件多了 JavaScript 表达式、动态变量、条件逻辑和循环。它是把模板从"占位符替换"提升到"小型脚本引擎"的关键插件。

> [!compare] 核心模板 vs Templater
> | | 核心模板 | Templater |
> | --- | --- | --- |
> | 变量 | `{{title}}` `{{date}}` `{{time}}` | 上述 + 任意 JS 表达式 |
> | 逻辑 | 无 | `<%* if/for %>` 完整 JS |
> | 用户输入 | 无 | `tp.system.prompt()` 弹窗 |
> | 文件操作 | 仅插入 | 创建/移动/重命名文件 |
> | 触发时机 | 手动插入 | 手动 / 文件创建 / 命令 |

> [!example] 一个 Templater 用例
> ```
> ---
> title: <% tp.file.title %>
> date: <% tp.date.now("YYYY-MM-DD") %>
> tags: [<% await tp.system.prompt("tags?") %>]
> ---
> ```
> 创建笔记时弹窗输入 tag，自动填到 frontmatter。

**和其他插件配合**：常和 [[wiki/obsidian/dataview|Dataview]] 联动——Templater 写入 frontmatter，Dataview 查询；和 QuickAdd 联动，做"快速捕获 → 自动归类"的批处理。配合 [[wiki/obsidian/inbox-工作流|inbox 工作流]] 可以让新建笔记直接落入 inbox 并打好 status。
