---
title: Context Window
tags: [context-window, llm-fundamentals]
date: 2026-04-22
sources:
  - "[[sources/inbox/使用 Claude Code：会话管理与 100 万 上下文【译】]]"
last-ingested: 2026-04-22
status: stable
---

# Context Window

> [!note] TL;DR
> Context Window 是模型生成下一次回答时眼前能"同时看到"的所有信息：系统提示词、聊天记录、工具调用及其输出、读过的文件，全部加在一起。Claude Code 现在的上限是 **100 万 token**。窗口越大不等于越好用——一切关键决策都归结为：**怎么管理这个窗口**。

## 包含什么

```
[ 系统提示词（含 CLAUDE.md / 工具定义 / 行为规则） ]
[ 历史对话（user / assistant 轮次） ]
[ 每次工具调用 + 工具输出 ]
[ 模型读过的每一个文件全文 ]
————————————————————————
                      合计 ≤ window 上限
```

不在窗口里的东西，模型**就是看不见**——不管它跟当前任务多相关。所以"塞进窗口"和"留在窗口里"是两个不同的工程问题。

## 为什么 100 万 token 不能解决一切问题

> [!warning] 大窗口 ≠ 高质量
> Window 大 → 能塞更多东西 → 反而容易触发 [[context-rot|Context Rot]]：注意力被分散到更多 token 上，早期遗留的无关内容开始干扰当前任务。模型表现随上下文长度变长而**下降**。

100 万 token 的真正用处不是"塞满它"，而是**给上下文管理留出充裕的腾挪空间**：可以提前 [[compact-vs-clear|/compact]] 而不必等到窗口爆满（爆满时模型已经"智商不在线"），可以保留更长的历史让 [[rewind-胜过纠正|/rewind]] 找到合适的回退点。

## 与上下文管理的关系

Context Window 是物理容器，[[会话管理动作|/continue、/rewind、/clear、/compact、subagent]] 是操作工具。物理上限给定后，差距就出在操作姿势上：

- 不会用工具 → 撞窗口上限 → 自动 compact → 翻车
- 用得熟 → 主动管理窗口 → 长会话也能保持质量

## 与 Prefix Cache 的关系

每次请求发出去的"窗口里的全部内容"决定了 [[prefix-cache|Prefix Cache]] 命中情况。窗口前段稳定 → 缓存命中 → 便宜+快；窗口前段一变 → 缓存全废 → 贵+慢。所以"管理上下文窗口"和"管理缓存"在工程上是同一件事的两面。

## 关联

- 窗口拉满后的代价：[[context-rot]]
- 操作工具：[[会话管理动作]] / [[compact-vs-clear]] / [[rewind-胜过纠正]] / [[subagent-上下文隔离]]
- 缓存层关系：[[prefix-cache]] / [[稳定前缀-动态后缀]]
