---
title: OpenClaw Memory（原生混合检索 + 一次性 dump 写）
tags: [openclaw, memory, claude-code]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

OpenClaw 是 9 大 harness 里**唯一原生支持语义检索**的：markdown 落盘 + 每 agent SQLite 索引 + 70/30 向量/BM25 [[hybrid-retrieval|混合检索]]。但写路径上有个奇怪的设计——窗口满时打一个 "silent internal turn" 让模型在一回合内决定要写什么，长期记忆因此**选择性且不稳定**。这条短板直接催生了 Mem0 的 OpenClaw 集成（247k stars 的相当一部分增长被归因到这里）。

## 内建检索：原生混合

> [!note] 9 家里唯一原生 semantic
> - 文件：`~/.openclaw/workspace/MEMORY.md`（人 curate） + 日期日志 `YYYY-MM-DD.md`
> - 索引：每 agent 一个 SQLite，带 embedding
> - 检索：**70% 向量相似度 + 30% BM25**（典型 [[hybrid-retrieval|混合检索]]）
>
> 对比同期 [[auto-memory|Claude Code]] 按文件名选、[[codex-memory|Codex]] grep、[[hermes-agent|Hermes]] FTS5——OpenClaw 是唯一能匹配 paraphrase 的内建实现。

## 写路径：silent internal turn

> [!warning] 一回合决定一切
> 当上下文窗口快满时：
> 1. OpenClaw 触发一个"silent internal turn"——**对用户不可见**的一回合
> 2. 这回合内让模型自己决定"哪些重要、写到 MEMORY.md"
> 3. 写完清空窗口
>
> 问题：**长期记忆完全取决于这一回合里模型怎么挑**。一次挑漏了就永远丢；不同 session 的标准还会漂移——所以长期 memory 看起来"选择性且不一致"。这与 [[compact-vs-clear|compact vs clear]] 选择 compact 但只给一次机会是同一个失败模式。

## Mem0 的 OpenClaw 插件如何补

`@mem0/openclaw-mem0` 把这件事拆成两个连续动作而不是一次性 dump：

> [!compare] 内建 vs Mem0 接管
> | 阶段 | 内建 OpenClaw | + Mem0 |
> |---|---|---|
> | **每轮开始** | — | **Auto-Recall**：注入相关历史 memory |
> | **每轮结束** | — | **Auto-Capture**：写入新事实、更新 stale、合并重复 |
> | **窗口满时** | silent internal turn 决定写什么 | 已经持续在写，窗口满不影响长期 memory |
> | **scoping** | workspace 本地 | `run_id` (session) + `userId` (长期) |

源故事提到 Mem0 的 247k stars **相当一部分增长**被归因到 OpenClaw 集成填的这个空——说明 silent-turn 模式的痛在生产里被广泛感知。

## 为什么"原生 semantic + 写路径有 bug"会发生

> [!important] 设计取舍
> 把检索做得好（混合）让"找到对的记忆"是强项；但写路径选了"窗口满才 batch dump"，省了**每轮**做写决策的 token 开销。这个权衡在窗口够大的场景成立，但**长会话**会把所有写决策挤到一个无法预知的临界点上——决定记什么的负担在那一刻爆炸。
>
> Mem0 的方案是反向：**每轮都做小决策**，分摊 token 开销，但每轮都付。两者是不同的工作量分布选择。

## 与 hosted memory 路线的关系

OpenClaw 本质上还是本地 markdown + 本地 SQLite。它的"语义检索"优势在 [[managed-agents-memory|hosted memory]] 路线里被默认拿到（AgentCore / Managed Agents 都有内建结构化检索），但 OpenClaw 的优势是**不依赖云**。这条路径对在意数据本地化的团队仍然成立。

## 相关页面

- [[hybrid-retrieval|混合检索（Hybrid Retrieval）]] — 70/30 是其典型配比
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — OpenClaw 是"检索 keyword"短板的唯一例外，但写路径有 bug
- [[mem0|Mem0]] — 接管 OpenClaw 写路径的具体方案
- [[compact-vs-clear|Compact vs Clear]] — silent internal turn = 一次性 compact 的失败模式
- [[auto-memory|Claude Code Auto Memory]] · [[codex-memory|Codex Memories]] · [[hermes-agent|Hermes Agent]] — 同类对比
