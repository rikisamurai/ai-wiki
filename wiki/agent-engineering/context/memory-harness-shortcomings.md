---
title: Harness Memory 五大共同短板
tags: [memory, harness, agent-engineering]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

把 Claude Code、Codex、Copilot、OpenClaw、Hermes、Bedrock AgentCore、Windsurf、Devin、Anthropic Managed Agents 九家的 memory 设计摆一起，会发现五个相同的 gap 反复出现：**存储 bounded & local**、**检索基本是 keyword**、**harness-scoped**、**几乎没 staleness**、**isolation 是 afterthought**。这五条是 harness 边界的物理极限——见 [[mem0|Mem0]] 把它们当作要解决的清单。

## 五大短板速查

> [!compare] 9 个 harness 的共同 gap
> | gap | 表现 | 典型证据 |
> |---|---|---|
> | **存储 bounded & local** | 容量上限低、不离机 | [[auto-memory\|Claude Code]] MEMORY.md 25KB · [[hermes-agent\|Hermes]] 2,200 字符 · [[codex-memory\|Codex]] 5,000-token 加载预算 · Windsurf 单机 |
> | **检索 = 关键词** | 没有语义召回 | [[auto-memory\|Claude Code]] 按文件名 · [[codex-memory\|Codex]] grep · [[hermes-agent\|Hermes]] SQLite FTS5 |
> | **harness-scoped** | 一个工具的记忆别的工具看不见 | Claude Code memory ↔ Codex memory 完全隔离 |
> | **staleness 几乎没** | 旧事实长期留在记忆里 | 唯一例外是 [[jit-citation-verification\|Copilot 的 JIT 引用验证 + 28 天过期]] |
> | **isolation = afterthought** | 跨用户/跨 session 污染 | 论文 [arXiv:2604.01350](https://arxiv.org/abs/2604.01350) 实测 57–71% 跨用户污染；poisoning 攻击 6–38% 成功 |

## 短板 1：存储 bounded & local

> [!note] 数字
> - [[auto-memory|Claude Code Auto Memory]]：MEMORY.md 索引 200 行 / 25KB，4 类（user/feedback/project/reference）
> - [[hermes-agent|Hermes Agent]]：MEMORY.md 2,200 字符 + USER.md 1,375 字符，~1,300 token 总体
> - [[codex-memory|Codex memories]]：memory_summary.md 硬截断 5,000 token；MEMORY.md grep
> - Windsurf：workspace-scoped local
> - [[managed-agents-memory|Anthropic Managed Agents]]：8 store per workspace × ~100KB

容量上限不仅是数字，**还配套了 silent truncation**：超过 cap 的内容静默掉，agent 不知道丢了什么，也不会报警。

## 短板 2：检索是 keyword 的

- Claude Code：另一个 Sonnet **按文件名和描述**选最多 5 条注入；语义匹配做不到，名字相关性赢过内容相关性
- Codex：MEMORY.md 走 grep——**substring 匹配**，paraphrase 不可见（"429 errors" 找不到"rate limiting"）
- Hermes：SQLite FTS5，同样是关键词

唯二做语义的：OpenClaw（70% 向量 + 30% BM25，但本地 + compaction 限制）和 AWS Bedrock AgentCore（cloud-locked）。这条短板正是 [[hybrid-retrieval|混合检索]]要解决的——但混合检索本身不解决跨 harness 共享问题。

## 短板 3：harness-scoped

> [!warning] 没有跨工具的"我"
> 一个工程师在 Claude Code 里告诉模型"always pnpm not npm"，切到 Codex 同一台机器同一仓库——Codex 不知道。9 家中除 [[mem0|Mem0]] 之外没有任何一家解决这件事。这是把 memory 当 harness feature 而不是基础设施的必然结果。

## 短板 4：staleness 几乎没

唯一有 staleness 设计的是 [[jit-citation-verification|GitHub Copilot]]：memory item 携带 file:line citation，使用前在当前 branch 验证，contradict 就 rewrite；28 天 auto-expire。**这也是唯一一个有 published A/B 数据**（PR merge rate 83% → 90%，p<0.00001）的 memory 设计。其他家把这件事推给"用户手动整理"或"靠 LLM 自己决定写不写"。

## 短板 5：isolation = afterthought

> [!important] 量化的攻击面
> - 论文 [No Attacker Needed](https://arxiv.org/abs/2604.01350)：normal usage 下跨用户污染率 **57–71%**
> - 论文 [arXiv:2601.05504](https://arxiv.org/abs/2601.05504)：memory poisoning 攻击成功率 **6–38%**
>
> 这两个数字在 [[prompt-injection-通用|prompt injection]] 之外开了第二条攻击面：写入 memory 的恶意内容会在未来任意 session 被召回。

## 五条短板的统一根因

这五条是同一件事的不同表现：**memory 被当作 harness 的本地 feature 实现**，于是必然带着 harness 的边界——上限、单机、不共享、不会过期、不隔离。要把这五条同时按下去，要么每家 harness 各自重做，要么把 memory 抬到 harness 之外做基础设施，后者正是 [[mem0|Mem0]] 押的方向。

## 相关页面

- [[memory-three-tiers|Agent Memory 三层]] — 五大短板都发生在 external 层
- [[mem0|Mem0]] — 这五条的对位解决方案
- [[memory-benchmarks|Memory Benchmarks]] — 用什么衡量这些短板是否被解决
- [[jit-citation-verification|JIT 引用验证]] — 唯一解决了 staleness 的设计
- [[auto-memory|Claude Code Auto Memory]] · [[codex-memory|Codex memories]] · [[hermes-agent|Hermes Agent]] · [[managed-agents-memory|Managed Agents]] · [[devin-knowledge|Devin Knowledge]] — 具体 harness 实现
