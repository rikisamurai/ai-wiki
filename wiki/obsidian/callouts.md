---
title: Obsidian Callouts
tags: [obsidian, markdown, formatting]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-tips/obsidian-callouts]]"
last-ingested: 2026-04-22
status: draft
---

Callouts 是 Obsidian 在标准 Markdown blockquote 上扩展的高亮信息块，语法 `> [!type] 标题`。它们自带颜色、图标和折叠态，是组织笔记结构最轻量的视觉边界——本仓库 wiki 页面规范要求"用 Callouts 区分定义/示例/对比"就基于此。

> [!example] 基本语法
> ```markdown
> > [!tip] 自定义标题
> > 正文
> 
> > [!faq]- 默认折叠（` -` 后缀）
> > > [!note] 嵌套 Callout
> > > 继续缩进即可
> ```

> [!note] 13 种内置类型 + 别名
> | 类别 | 类型 | 别名 |
> | --- | --- | --- |
> | 中性 | `note` `info` `todo` `quote` | `cite` |
> | 摘要 | `abstract` | `summary` `tldr` |
> | 提示 | `tip` | `hint` `important` |
> | 成功 | `success` | `check` `done` |
> | 疑问 | `question` | `help` `faq` |
> | 警示 | `warning` | `caution` `attention` |
> | 失败/危险 | `failure` `danger` `bug` | `fail` `missing` `error` |
> | 例子 | `example` | — |
>
> 别名和原类型完全等价，写起来选语义最贴切的即可。

> [!tip] 自定义类型（CSS Snippet）
> 设置 → 外观 → CSS 代码片段，新建 `.css` 文件：
> ```css
> .callout[data-callout="custom"] {
>   --callout-color: 255, 0, 0;     /* RGB，无 rgb() */
>   --callout-icon: lucide-alert-circle;  /* Lucide 图标名 */
> }
> ```
> 然后 `> [!custom]` 就能用。

> [!compare] Callouts vs Header
> 本仓库 [[index|index]] 和 [[wiki/obsidian/inbox-工作流|inbox 工作流]] 都强调"克制使用 header"——短内容用 Callout 自带的视觉边界更好，外层不要再套 `##`。Header 适合多分支且每段较长的内容；Callout 适合"一段定义/一段示例/一段对比"的并列。

**与 [[wiki/obsidian/obsidian-skills|obsidian-markdown skill]] 的关系**：让 LLM 写 Obsidian 笔记时正确使用 Callouts 类型，是 obsidian-markdown skill 的核心约束之一——LLM 默认会写成 `**Note:**` 或 emoji 块，装上 skill 才会生成 `> [!note]` 这种原生语法。
