---
title: Obsidian Web Clipper
tags: [obsidian, web-clipper, ingest]
date: 2026-04-22
sources:
  - "[[sources/inbox/告别复制粘贴：浏览器一键剪藏到 Obsidian]]"
last-ingested: 2026-04-22
status: stable
---

# Obsidian Web Clipper

> [!note] TL;DR
> Obsidian 官方出的浏览器插件，一键把网页正文转成 Markdown 存进 vault，**省掉"复制 → 新建 → 粘贴 → 调格式 → 存图"的全套手活**。它是 [[inbox-工作流|inbox 工作流]] 的入口环节——负责"收"，剪藏进来后由 AI 负责"理"。

## 这玩意做什么

```
浏览器看到好文章
   │ 点工具栏 Obsidian 图标
   ↓
[ Web Clipper 抓取正文 + 元数据 ]
   │ 选模板 → 预览 → 添加到 Obsidian
   ↓
你的 vault 收件箱里多了一篇 .md
   - 标题 ✅
   - 原文链接 ✅
   - 正文（已转 Markdown）✅
   - frontmatter properties ✅
```

## 配模板的关键：5 个属性

模板能塞 frontmatter 进每一篇剪藏，方便后续筛选/归档：

| 属性 | 值 | 用途 |
|---|---|---|
| `type` | `inbox` | 标记这是收件箱物料 |
| `status` | `pending` | 等待处理 |
| `source` | `web-clipper` | 区分人工写 vs 剪藏 |
| `url` | `{{url}}` | 反查原文 |
| `created` | `{{date}}` | 时间线排序 |

这套 metadata 是配合 [[inbox-工作流|inbox 工作流]] 设计的——`status: pending` 让 AI 一眼能找到"哪些还没处理"。

## 为什么不直接复制粘贴

> [!compare] 三种存网页内容的姿势
> | 方式 | 时间成本 | 元数据 | 图片 |
> |---|---|---|---|
> | 复制 → 粘贴 → 调 | ~3 min/篇 | 手敲 | 一张张右键存 |
> | 浏览器收藏夹 | 5 秒 | 只有 URL | 没有 |
> | **Web Clipper** | **2 秒** | **frontmatter 全自动** | **正文图自动包含** |

收藏夹的问题是"链接腐烂"——原文删了你的笔记也死了。Web Clipper 把全文存到本地，**离线可用、可被 AI 索引**。

## 与 ai-wiki 三层架构的关系

剪藏进来的内容直接落进 [[../../sources/inbox/]]——也就是本仓库的 `sources/inbox/`，是 [[ai-wiki-架构|三层架构]] 中的"原料层"。LLM 只读不改，由 [[../../.claude/commands/ingest|/ingest]] 命令负责把它沉淀进 `wiki/`。

> [!tip] 不必追求剪藏当下的整理
> 收件箱是中转站，东西不能一直放那儿——但**进的时候越无脑越好**。整理交给后续工作流。

## 关联

- 后续处理：[[inbox-工作流]]
- 类似流派：手抄笔记、自动 RSS 导入、Readwise → Obsidian 同步
- 如果用 Cursor/Claude Code 维护 vault，剪藏文件就是它们的 input
