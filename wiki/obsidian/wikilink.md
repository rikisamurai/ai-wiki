---
title: Wikilink
tags: [obsidian, linking, syntax]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 内部链接（Internal Links）]]"
last-ingested: 2026-04-22
status: draft
---

Wikilink 是 Obsidian 默认的内部链接语法 `[[文件名]]`，比标准 Markdown 链接 `[文本](path)` 更短、不必 URL 编码、自动跟随重命名。它是 [[wiki/obsidian/zettelkasten|Zettelkasten]] 网络化思维在 Obsidian 里能跑起来的语法基础。

> [!example] 4 种常见形态
> | 目标 | 语法 |
> | --- | --- |
> | 文件 | `[[三大运动定律]]` 或 `[[三大运动定律.md]]` |
> | 自定义显示 | `[[三大运动定律\|定律]]` |
> | 当前笔记内标题 | `[[#预览链接]]` |
> | 跨笔记标题 | `[[About#Links]]` `[[帮助#问题#报告 Bug]]`（多级） |
> | 块引用 | `[[file#^id]]` —— 详见 [[wiki/obsidian/block-reference\|块引用]] |
> | 跨库搜索 | `[[##team]]`（标题）/ `[[^^block]]`（块） |

> [!compare] Wikilink vs Markdown Link
> | | Wikilink | Markdown |
> | --- | --- | --- |
> | 语法 | `[[file]]` | `[file](file.md)` |
> | URL 编码 | 不需要 | 空格要写 `%20` |
> | 重命名 | Obsidian 自动更新所有引用 | 同样自动更新（设置开启时） |
> | 互操作 | Obsidian / Roam / Logseq | 任何 Markdown 工具 |
> | 默认 | 是 | 否，需在设置中切换 |

> [!warning] 链接里不能出现的字符
> `# | ^ : %% [[ ]]` 都是 wikilink 的元字符或保留符号，会被误解析。中文虽可用，但跨工具兼容性差——本仓库 wiki 文件名采用 kebab-case 就是这个考虑。

> [!tip] 嵌入与跳转的区别
> 链接前加 `!` 就是嵌入（transclusion）：`[[file]]` 跳转，`![[file]]` 在当前位置渲染目标内容。详见 [[wiki/obsidian/embed-files|嵌入文件]]。
