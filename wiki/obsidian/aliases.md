---
title: Aliases（别名）
tags: [obsidian, linking, frontmatter]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 内部链接（Internal Links）]]"
last-ingested: 2026-04-22
status: draft
---

Aliases 是在笔记 frontmatter 里声明的"备用名"，让 [[wiki/obsidian/wikilink|wikilink]] 自动补全和反向链接识别多个名字。声明一次全库通用，不必每次都写 `[[file|显示文本]]`。

> [!example] 声明与命中
> ```yaml
> ---
> aliases: [QUIC 协议, Quick UDP Internet]
> ---
> ```
> 之后 `[[QUIC 协议]]` 或 `[[Quick UDP Internet]]` 都会指向这篇笔记，反向链接面板也都能识别。

> [!compare] Aliases vs `[[file|显示文本]]` 显示文本覆盖
> | | Aliases | `[[file\|显示文本]]` |
> | --- | --- | --- |
> | 范围 | 全库通用 | 单次链接 |
> | 反向链接 | 别名出现就能识别 | 不影响 |
> | 设置位置 | 目标笔记 frontmatter | 引用方笔记内 |
> | 适合 | 中英对照、缩写、旧名 | 上下文里的临时改写 |

> [!tip] 与"未链接提及"配合
> Obsidian 反向链接面板有"未链接提及"区，列出全文里出现别名但还没创建链接的位置。日常清理 [[wiki/obsidian/inbox-工作流|inbox]] 时扫一眼就能补上漏掉的链接，是维持 [[wiki/obsidian/knowledge-graph|知识图谱]] 完整性的低成本动作。

> [!example] 本仓库的潜在用法
> 给 [[wiki/aigc/mcp|MCP]] 页面加 `aliases: [Model Context Protocol]`，给 [[wiki/aigc/plan-mode|Plan Mode]] 加 `aliases: [规划模式]`——后续中英文混写都能被自动识别为同一概念。
