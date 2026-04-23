---
title: Dataview
tags: [obsidian, plugin, query]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/🚀obsidian-quick-start]]"
last-ingested: 2026-04-22
status: stable
---

Dataview 是把 Obsidian 库变成可查询数据库的插件——以 frontmatter、tag、文件元数据为字段，用类 SQL 的 DQL 写出 LIST / TABLE / TASK / CALENDAR 视图。是动态聚合笔记最常用的工具。

> [!example] 三种典型查询
> **未完成任务按文件夹分组**：
> ```
> TASK
> WHERE !completed
> GROUP BY file.folder
> ```
>
> **最近 7 天修改的笔记**：
> ```
> TABLE file.mtime as "修改时间"
> WHERE file.mtime >= date(today) - dur(7 days)
> SORT file.mtime DESC
> ```
>
> **按 tag 过滤进行中的项目**：
> ```
> LIST
> FROM #项目
> WHERE status = "进行中"
> ```

> [!compare] Dataview vs Obsidian Bases
> | | Dataview | [[wiki/obsidian/obsidian-web-clipper\|Bases]] |
> | --- | --- | --- |
> | 实现 | 第三方插件 | Obsidian 1.7+ 核心 |
> | 查询语法 | DQL（自创） | YAML + 公式 |
> | 视图 | 表格/列表/任务/日历 | 表格/卡片 |
> | 性能 | 大库慢 | 原生，更快 |
> | 状态 | 仍主流但社区担心未来 | 官方推动方向 |

> [!tip] 与其他插件协作
> 配合 [[wiki/obsidian/templater|Templater]] 写入结构化 frontmatter，Dataview 才能查得到。和 [[wiki/obsidian/moc-索引笔记|MOC]] 是天作之合——MOC 页面里嵌一段 Dataview 就能自动维护索引。
