---
title: Codex Memories（两阶段写入 + grep 检索）
tags: [codex, memory, claude-code]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

OpenAI Codex 的 memory 路线和 [[auto-memory|Claude Code Auto Memory]] 显著不同：默认关闭、两阶段写入（per-rollout 提取 + global 合并）、读路径是 grep + 5,000 token 硬截断。没有 SQLite、没有 embedding。这条选择给了 Codex 比 Claude Code 更强的"写入审慎"、但比之更弱的"读出召回"。

## 文件布局

> [!note] 一个目录的 markdown
> `~/.codex/memories/`
> - `memory_summary.md` — 启动时先读，**5,000 token 硬截断（silent truncation）**
> - `MEMORY.md` — 按需被 grep 命中（substring 匹配）
> - `raw_memories.md` — 未合并的原始片段
> - `skills/` — 程序性记忆（类比 [[skill-编写实践|Skill]]）
> - `rollout_summaries/` — 历史 rollout 摘要
>
> 默认 off，要 `features.memories` flag 打开。**纯 local，state 不离机**。

## 写路径：两阶段

> [!example] Phase 1 — per-rollout 提取
> session 结束后**等 6 小时 idle**，才会触发：
> 1. 按 strict schema 提取
> 2. 脱敏密钥
> 3. 写入本地 state DB（**还没进 memory 目录**）

> [!example] Phase 2 — global 合并
> 加锁后，consolidation sub-agent 执行：
> 1. 把 state DB 中的待整理项 merge / patch / drop
> 2. 写 diff 到 `MEMORY.md` 等文件
>
> 约束：
> - bound：最多 256 个 rollout
> - age-prune：30 天后剪除
> - rate-limit aware：高负载时延迟合并

## 读路径：grep + 截断

读路径上 Codex **没有任何语义召回**：

- `memory_summary.md` **硬截断到 5,000 token**——超出的内容静默丢，agent 不知道
- 其他内容靠 grep 命中 `MEMORY.md`——**substring 匹配**，paraphrase 看不见（"429 errors" 找不到 "rate limiting"）

这条路径符合 [[memory-harness-shortcomings|harness memory 的"检索基本是 keyword"短板]]。

## 与 Claude Code Auto Memory 的对比

> [!compare] Codex memories vs Claude Code Auto Memory
> | 维度 | Codex memories | [[auto-memory\|Claude Code Auto Memory]] |
> |---|---|---|
> | **默认状态** | off（`features.memories` flag） | on |
> | **写时机** | session 后 6 小时 idle gate | 实时由 Claude 决定写不写 |
> | **写流程** | 两阶段：提取 → 合并 | 单步：写入 topic 文件 |
> | **读机制** | grep + 5k token 硬截断 | 另一个 Sonnet 选最多 5 条按全文注入 |
> | **检索单位** | substring | 文件名 + description |
> | **持久化** | local state DB + markdown | 本机 markdown |

两条路线都没有语义检索；都是 [[memory-three-tiers|external memory 三层]]里"靠规约+精挑读"的设计。Codex 更保守（默认关 + idle gate），Claude Code 更主动（默认开 + 实时写）。

## 已知坑

> [!warning] silent truncation + 区域限制
> - `memory_summary.md` 超 5,000 token 静默截断
> - grep substring-only：paraphrase 找不到
> - 6 小时 idle gate：**back-to-back session 可能永远不 consolidate**——连续高强度使用的开发者会发现记忆"看着写了但读不到"
> - state 是 local-only
> - 上线时在 **EEA / UK / Switzerland 不可用**（功能 flag 区域受限）

## 用 Mem0 替代

OpenAI 没有官方解，但 [[mem0|Mem0]] 出了 Codex MCP server 走 [[mcp|MCP]] 协议注入——把 Codex 的本地 markdown 换成跨 harness 的 vector + KG，绕开 grep + 5k 硬截断。

## 相关页面

- [[codex|Codex]] — 工具本身
- [[auto-memory|Claude Code Auto Memory]] — 同类设计的不同选择
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — Codex 命中其中四条（无 staleness/isolation/语义检索/跨工具）
- [[mem0|Mem0]] — 官方之外的补丁
- [[memory-three-tiers|Agent Memory 三层]] — Codex 全在 external 层
