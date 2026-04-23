---
title: Inbox 工作流
tags: [obsidian, inbox, workflow]
date: 2026-04-22
sources:
  - "[[sources/inbox/告别复制粘贴：浏览器一键剪藏到 Obsidian]]"
last-ingested: 2026-04-22
status: stable
---

# Inbox 工作流

> [!note] TL;DR
> "**收件箱 = 中转站，不是仓库**"——把所有原料先无脑塞进 `inbox/`，由后续 AI 流程（或手动）分类、提炼、归档。这套模式抄自 GTD（Getting Things Done），结合 Obsidian 的 frontmatter properties 和 LLM 工作流，能让"收"和"理"完全解耦。

## 核心原则

```
收（即时、无脑、零成本）
   ↓
inbox/ ── pending 状态在这里堆着
   ↓
理（批量、慢思考、AI 辅助）
   ↓
分类归档到 wiki/ / projects/ / archive/
```

> [!quote] 一句话总结
> 剪藏负责收，AI 负责理。

## 为什么要这套架构

直接"看到 → 整理"的失败模式：

- **整理成本太高 → 直接放弃收**：纠结分类，最后什么都没存
- **整理打断信息流**：刷 Twitter 看到好东西，停下整理 5 分钟，回来已经断片
- **当下判断不准**：刚看到时觉得"很重要"，一周后才知道是哪类

inbox 的本质是 **延迟决策**：先存住，等后续 batch 处理时一次性判断。

## 5 个 properties 是关键

来自 [[obsidian-web-clipper|Web Clipper]] 模板的标准 frontmatter：

```yaml
type: inbox
status: pending      # ← 关键字段
source: web-clipper  # 或 manual / readwise / ...
url: {{url}}
created: {{date}}
```

**`status` 字段是工作流的引擎**：

| status 值 | 含义 |
|---|---|
| `pending` | 等待处理（默认） |
| `processing` | 正在被 AI 或人提炼 |
| `done` | 已沉淀到 wiki/，可归档 |
| `discard` | 看完没价值，待删 |

用 Bases 视图过滤 `status: pending` 就是你的"待办列表"。

## AI 介入的两种姿势

> [!example] 让 LLM 处理 inbox
> - **`/research <inbox-file>`**：把单篇文章拆成多个知识笔记（这就是本仓库 [/ingest](../../.claude/commands/ingest.md) 命令做的事）
> - **`/kickoff <想法>`**：把"想法型" inbox 转成可执行的项目计划

LLM 的优势是**批量+不挑剔**——一次处理 20 篇，不会嫌烦不会漏。

## 与本仓库的对应关系

ai-wiki 的 `sources/inbox/` 就是 inbox 工作流的物理实现：

- `sources/inbox/` ← Web Clipper / 手动写入的草稿堆
- `wiki/**/*.md` ← 沉淀产物（status 等价于 done）
- 根目录 `migration-backlog.md` ← 显式追踪 pending 队列（按需创建；2026-04 首批已归档至 [[wiki/_orphans/migration-2026-04|_orphans/migration-2026-04.md]]）

`/migrate-next` 命令就是把 inbox `pending` 一个个变成 `done` 的驱动器。

## 失败模式

> [!warning] inbox 也会"过期"
> 如果 inbox 越堆越多但从来不"理"，它就退化成另一个收藏夹墓地。
> 
> **应对**：
> - 设上限（比如 inbox 超过 50 条就强制开个清理 session）
> - 用 Bases 把"超过 30 天还 pending 的"标红
> - 接受"删除"也是一种处理——不是每篇都值得沉淀

## 关联

- 入口工具：[[obsidian-web-clipper]]
- 处理引擎（本仓库实现）：[/ingest](../../.claude/commands/ingest.md) / [/migrate-next](../../.claude/commands/migrate-next.md)
- 类似理念：GTD 的 Inbox / Tiago Forte 的 PARA Capture / Zettelkasten 的 Fleeting Notes
