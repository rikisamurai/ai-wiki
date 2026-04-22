---
title: 块引用（Block Reference）
tags: [obsidian, linking, transclusion]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/block-link-demo]]"
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 block reference use cases]]"
last-ingested: 2026-04-22
status: draft
---

块引用是 Obsidian wikilink 的细粒度变种：在任意"块"（段落、列表项、引用、表格行等）末尾加 `^id` 创建块 ID，然后通过 `[[file#^id]]` 跳转或 `![[file#^id]]` 嵌入。它把"链接到笔记"细化到"链接到笔记里的某一段"。

> [!example] 创建与引用
> ```markdown
> 这是一段值得被引用的话。 ^my-decision
>
> 跳转：[[file#^my-decision]]
> 嵌入：![[file#^my-decision]]
> ```
> 输入 `[[^^` 可弹搜索框选目标块，自动生成随机 ID（如 `^a3f9c2`）。

> [!note] "块"的定义
> 块是任何独立内容单元——一个段落、一个列表项、一个标题段落、一张表格、一条 callout、一个数学公式块。`^id` 必须放在该块的末尾。

> [!warning] 限制
> - 块 ID 只允许字母、数字、连字符 `-`，不支持中文或空格
> - 嵌入是实时同步的：源块变了，嵌入处自动更新
> - 源块删除 → 所有引用变断链，[[wiki/obsidian/knowledge-graph|图谱]] 里也会显示为断链关系

> [!compare] 块引用 vs 章节引用 vs 整页引用
> | 形式 | 语法 | 适合 |
> | --- | --- | --- |
> | 整页 | `[[file]]` / `![[file]]` | 整篇笔记 |
> | 章节 | `[[file#标题]]` / `![[file#标题]]` | 笔记内某个 header 下的所有内容 |
> | 块 | `[[file#^id]]` / `![[file#^id]]` | 段落级最细粒度 |

**典型用法**：跨笔记嵌入金句、决策、API 规范等"想被多处复用又只想维护一处"的内容。详见 [[wiki/obsidian/block-reference-use-cases|块引用使用场景]]。
