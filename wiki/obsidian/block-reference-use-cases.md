---
title: 块引用使用场景
tags: [obsidian, linking, workflow]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 block reference use cases]]"
last-ingested: 2026-04-22
status: draft
---

[[wiki/obsidian/block-reference|块引用]] 真正发挥威力是在跨笔记复用一段固定内容时——金句、决策、API 规范、任务等"想被多处嵌入又只想维护一处"的内容。下面 5 个场景覆盖 80% 的日常用法。

> [!example] 场景 1：日记 → 项目笔记
> 决策记在每日笔记里：
> ```markdown
> 今天讨论后决定用 PostgreSQL 而非 MongoDB。 ^db-decision
> ```
> 项目笔记里嵌入：
> ```markdown
> ![[2026-03-12#^db-decision]]
> ```

> [!example] 场景 2：读书金句 → 个人成长 [[wiki/obsidian/moc-索引笔记|MOC]]
> 在《原则》读书笔记标注：
> ```markdown
> 痛苦 + 反思 = 进步。 ^dalio-pain
> ```
> 在 MOC 嵌入跨笔记建立联系。

> [!example] 场景 3：单点维护
> 把 API 版本说明写在 `技术规范.md`：
> ```markdown
> 当前 API v3，请求需 `X-API-Version: 3` header。 ^api-version
> ```
> 多个相关笔记 `![[技术规范#^api-version]]`，改一处全更新。

> [!example] 场景 4：MOC 聚合碎片
> 在"AI 学习 MOC"里把不同笔记的关键段聚合：
> ```markdown
> ## 核心概念速览
> ### Transformer
> ![[深度学习笔记#^transformer-core]]
> ### Prompt 工程
> ![[Prompt 技巧#^prompt-tips]]
> ```

> [!example] 场景 5：跨文件任务追踪
> 项目计划里：
> ```markdown
> - [ ] 完成认证模块重构 ^task-auth
> ```
> 每日笔记 `![[项目计划#^task-auth]]`，在日记里勾选自动同步源文件状态。

> [!tip] 与 [[wiki/obsidian/dataview|Dataview]] / [[wiki/obsidian/obsidian-bases|Bases]] 配合
> Dataview/Bases 适合"按规则**动态聚合**整篇笔记"；块引用适合"按手动**点位嵌入**段落"。两者互补——MOC 的骨架靠 Dataview 自动列表，但里面的"金句精选区"靠块引用手挑。
