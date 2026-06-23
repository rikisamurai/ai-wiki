---
title: Hermes Agent（三层 memory + 8 providers）
tags: [hermes, memory, claude-code]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

NousResearch 的 Hermes Agent（135k stars，200+ 模型支持）的 memory 设计有两个值得抄的点：内建三层（working / skills / session search）+ 8 个 pluggable provider slot。它的工作记忆只有 ~800 token durable，但前缀缓存友好——写盘后系统 prompt 仍持有 frozen snapshot 直到下个 session，以保 [[prefix-cache|prefix cache]] 命中。

## 内建三层

> [!compare] Hermes memory 三层
> | 层 | 文件 / 介质 | 容量 | 触发 |
> |---|---|---|---|
> | **Layer 1 working** | `MEMORY.md` (2,200 字符) + `USER.md` (1,375 字符) ≈ 1,300 token | 80% capacity → consolidation | §-分隔 + utilization gauge |
> | **Layer 2 skills** | procedural docs | — | 完成 5+ tool-call 任务后写；定时 curate |
> | **Layer 3 session search** | SQLite FTS5 全 session 索引 | — | on-demand 摘要 |

> [!example] §-delimited 结构
> Hermes 用 `§` 段落标记和 utilization gauge 把固定容量分成可视的子段，让 LLM 自己能看到"还剩多少容量"再决定是否触发 consolidation。

## prefix cache 友好写

> [!important] 写盘 ≠ 替换 prompt
> 当 Layer 1 触发 consolidation：**新内容落盘，但系统 prompt 持有的是 frozen snapshot**，直到下个 session 启动才换上新内容。
>
> 为什么：[[prefix-cache|prefix cache]] / KV cache 一旦 prompt 变就 invalidate；如果每次写入都改 prompt，缓存命中率塌方。Hermes 的做法和 [[冻结快照模式|冻结快照模式]]同构——**写是异步的，读还是冻结那一帧**。

## Layer 2 skills 的"5 次门槛"

不是任何任务都生成 [[skill-编写实践|skill]]。规则是：完成 **5+ tool-call** 的任务才会触发 procedural memory 写入。背后逻辑：少于 5 步的任务太短，固化成 skill 没有 ROI；多于 5 步的才是值得"打包成程序"的复用对象。

## Layer 3 的局限

> [!warning] FTS5 是 keyword 的
> Session search 用 SQLite FTS5 做全文索引——但 FTS5 是 **keyword only**。
> - "429 errors" 不匹配 "rate limiting"
> - "auth bug" 不匹配 "session token expired"
>
> 这条命中 [[memory-harness-shortcomings|harness memory 的"检索基本是 keyword"短板]]。

## 8 个 pluggable provider

Hermes 的设计预留 provider slot，让 memory 后端可替换。**Mem0 是其中一个 first-class provider**，接进去后：

- cap 消失（不再受 2,200 字符限制）
- semantic retrieval
- 提取走 server-side
- `MEM0_USER_ID` scoping
- **circuit breaker**：Mem0 服务挂了，内建三层继续工作——不强耦合

> [!note] circuit breaker 是 provider 模式的关键
> Hermes 不要求 provider 永远在线。第三方 memory 服务降级时不能拖垮内建路径——这是 provider 抽象成立的工程前提。参见 [[fail-closed-tool-defaults|fail-closed]]的反向：这里要的是 fail-open + 内建兜底。

## 与 Claude Code / Codex 的对比

> [!compare] 三家三种选择
> | 维度 | [[auto-memory\|Claude Code]] | [[codex-memory\|Codex]] | Hermes |
> |---|---|---|---|
> | **工作记忆容量** | 25KB MEMORY.md 索引 | 5,000 token 截断 | 2,200 + 1,375 字符 |
> | **写时机** | 实时由 Claude 写 | 6h idle gate + 两阶段 | 触发 80% capacity |
> | **prefix cache 兼容** | 重启 session 才换 | 重启换 | **frozen snapshot 至下个 session** |
> | **provider 可换** | ❌ | ❌ | ✅ 8 slot |
> | **检索方式** | Sonnet 选文件 | grep + 5k 截断 | FTS5 关键词 |

Hermes 的 frozen snapshot + provider slot 是另外两家都没有的——这两个抽象让它能"无痛"接入 [[mem0|Mem0]]。

## 相关页面

- [[memory-three-tiers|Agent Memory 三层]] — Hermes 三层是 working 的细化
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — Hermes 命中"bounded local"和"keyword 检索"
- [[mem0|Mem0]] — Hermes 的 8 个 provider 之一
- [[prefix-cache|Prefix Cache]] · [[冻结快照模式|冻结快照模式]] — frozen snapshot 设计依赖的原理
- [[skill-编写实践|Skill 编写实践]] — Layer 2 写入的 procedural 单位
- [[codex-memory|Codex Memories]] · [[auto-memory|Claude Code Auto Memory]] — 同类对比
