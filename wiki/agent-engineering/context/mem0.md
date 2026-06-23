---
title: Mem0（跨 harness 记忆基础设施）
tags: [memory, infrastructure, agent-engineering]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

Mem0 把 agent memory 从"每个 harness 自己造一套"抬出 harness 边界，做成跨工具的基础设施层。架构是混合的：向量存储做语义检索 + 知识图谱做关系推理 + KV 做快速元数据。它在 Claude Code、Codex、Hermes、OpenClaw、AWS Strands 上都有 first-class 集成，瞄准的是 [[memory-harness-shortcomings|harness-native memory 的五大共同短板]]。

## v3 算法（2026-04）的三个关键改动

> [!note] v3 = ADD-only + 多信号 + KG 进 vector
> - **Single-pass ADD-only 提取**：不再做 update/delete 多轮 reasoning
> - **多信号 retrieval**：semantic + BM25 + entity linking 一次 pass 同时跑（见 [[hybrid-retrieval]]）
> - **Entity linking 内置 vector store**：v2 还要外挂 graph DB，v3 把这件事吃进去了

成本数字（v3 vs full-context retrieval）：

| 指标 | Mem0 v3 | full-context |
|---|---|---|
| token / query | ~6,900 | ~26,000 |
| latency / query | 1.44s | 17.12s |

## 针对的具体 gap

> [!compare] Mem0 对应的 harness 短板
> | harness 短板 | Mem0 的对应方案 |
> |---|---|
> | 本地 + 容量上限（[[auto-memory\|Claude Code]] 25KB / [[hermes-agent\|Hermes]] 2.2k / [[codex-memory\|Codex]] 5k token） | external store，**无 cap** |
> | 关键词检索（filename / grep / FTS5） | multi-signal：语义 + BM25 + 实体链接 |
> | Harness-scoped（[[claude-code-memory\|Claude Code]] 的记忆 Codex 看不见） | 跨 21 框架 + 20 vector store 的统一层 |
> | isolation 是 afterthought（[[memory-harness-shortcomings\|57–71% 跨用户污染]]） | identity-scoped namespace，跨用户不漏 |

## 它的"跨 harness"具体意思

> [!example] 一份记忆走多个工具
> - **Claude Code plugin** — 替代 [[auto-memory|auto memory]] 的本地 markdown
> - **Codex MCP server** — 走 [[mcp|MCP]] 注入 Codex
> - **Hermes / OpenClaw 一等公民 provider** — `MEM0_USER_ID` scoping + circuit breaker（服务挂了内建层照常工作）
> - **AWS Bedrock AgentCore / Strands 原生** — Anthropic [[managed-agents-memory|Managed Agents]] 之外的另一条 hosted 路线

这件事的意义是 [[跨厂商共识协议|跨厂商共识]]在 memory 这一层冒出来：记忆变成基础设施，不是每个 harness 自己的 feature。

> [!important] "记忆是基础设施" vs "记忆是 harness feature"
> 后者是 2025 的范式（每家 harness 自带 memory）。前者是 Mem0 押的方向：**memory 应该是 stateless harness 之外的有状态层**，跨 session、跨工具、跨设备、跨用户**隔离**。是否成立要看 BEAM 这种生产级 benchmark（见 [[memory-benchmarks]]）能不能给出独立数据。

## Shortcoming 与开放问题

- 加一层 infra 意味着多一个外部依赖——Hermes / OpenClaw 的 circuit breaker 设计是这一现实的承认
- v3 的 ADD-only 简化了写路径，但 [[memory-benchmarks|selective forgetting]] 仍未解决
- 跨用户隔离的真实数字还需要更多独立 reproduction

## 相关页面

- [[memory-three-tiers|Agent Memory 三层]] — Mem0 是 external 层的"基础设施化"路线
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — Mem0 的目标读者
- [[hybrid-retrieval|混合检索（Hybrid Retrieval）]] — 多信号 retrieval 的通用做法
- [[managed-agents-memory|Anthropic Managed Agents]] — 另一条把 memory 抬出本地的路线
