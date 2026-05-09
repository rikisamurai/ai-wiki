---
title: wasc-search-skill（低成本高精度 RAG Skill 范例）
tags: [agent-skills, rag, mcp]
date: 2026-05-09
sources:
  - "[[sources/clippings/youzingwasc-search-skill]]"
last-ingested: 2026-05-09
status: stable
---

`wasc-search-skill` 是 2026 世界 AI 技能锦标赛 4 月赛题"低成本高精度搜索"的参赛作品，把一个产线级 RAG 系统压缩成 ~3,350 tokens/次（比常规 RAG 低 65-75%），并以 MCP server 的形式发布。它示范了"**Skill = 一份带 budget 的 retrieve-rerank-generate 编排**"——可作为任何"把 RAG 包成 [[wiki/skills/agent-skills|Agent Skill]] / [[wiki/claude-code/mcp|MCP]]"项目的参考骨架。

> [!note] 设计目标先于架构
> 它不是一个"功能完整的 RAG"，而是一个"**给定 token 预算，最大化引用忠实度和召回质量**"的优化问题。这个 framing 决定了下面三个支柱性子模块——少了任何一个，预算或忠实度就会塌。

## 三段式架构 + 三个支柱模块

> [!example] Retrieve → Rerank → Generate 三阶段
> ```
> L1 精确缓存（SHA256） ──命中──▶ <5ms 直返
>   │ 未命中
>   ▼
> Stage 1: 异构多源检索（Tavily 关键词 + LangSearch 混合 + Exa 神经）
>   │ 每源独立熔断器
>   ▼
> Stage 2: 渐进式精炼（URL 去重 → RRF 融合 → Readability → BM25 ~200 字 → token 截断 ≤2,200）
>   ▼
> Stage 3: 忠实合成（5 级降级：tool-call → 纯文本 → mini-prompt → snippet 拼接 → LLM 知识兜底）
>   ▼
> 引用 ID 校验 → JSON 修复 → 缓存写回 → 结构化输出
> ```

三个值得抽出来单看的子模块：

1. **[[wiki/retrieval/rag/rrf|RRF（Reciprocal Rank Fusion）]]**——把 3 个异构源的排名融合成一个全局排序，不需要训练数据。
2. **[[wiki/retrieval/rag/rag-降级|RAG 5 级降级]]**——Stage 3 的核心；任何一级失败都自动落到下一级，**永不返回空**。
3. **[[wiki/retrieval/rag/citation-faithfulness|逐条引用忠实度]]**——每条陈述带 `[S#]` + 机械化 ID 校验 + 多源冲突标注。

## 为什么这三件事必须同时做

> [!compare] token-budget RAG 的三难
> | 痛点 | 单独解法 | 三件套联动 |
> |---|---|---|
> | token 成本高 | 截断输入 | BM25 段落选择把网页压到 ~200 字，但前提是 RRF 已经选对了 top URL |
> | 引用幻觉 | post-hoc 验证 | 5 级降级里 L1 用 tool-call 强制结构化，L2-L4 都仍带 `[S#]` |
> | 单点失败 | 重试 | 异构 3 源 + 熔断器 + 5 级 LLM 降级 = 失败概率乘性下降 |

单挑任何一项都不够：只压 token 会丢精度，只做引用校验会留兜底空答，只做降级会让答案漂移。**wasc 的价值是把三件事编成一个 pipeline，并且每段都可独立替换**——这与 [[wiki/skills/skill-编写实践|Skill 编写实践]]里"存储脚本与生成代码"原则一致：模块化 + 显式 budget。

## 工程细节里的几个 takeaway

> [!important] 几个值得抄的工程决策
> - **每源独立熔断器（[Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)）**：单源故障不拖累其他源，借用 `opossum` 实现。
> - **场景感知路由**：政策法规 / 行业信息 / 学术文献 / 通用 4 类查询走不同的 prompt 模板，命中率明显高于一刀切。
> - **L1 SHA256 精确缓存**：同问同答 <5ms 直返；这是 [[wiki/agent-engineering/context/cache-命中率|Cache 命中率]]在外部检索系统里的应用形态。
> - **零原生编译**：6 个 npm 包跑通整个 pipeline，比赛环境 Ubuntu 24.04 + Docker 直接拉起。
> - **MIT-0 协议**：连署名都免，对参赛 / 复用都极友好。

## 与本 wiki 其他概念的连接

> [!compare] wasc 命中的几条范式
> | 范式 | 命中点 |
> |---|---|
> | [[wiki/retrieval/rag/rag\|RAG]] | retrieve → rerank → generate 三阶段经典范式 |
> | [[wiki/retrieval/rag/hybrid-retrieval\|混合检索]] | RRF 融合 + BM25 段落选择 |
> | [[wiki/retrieval/rag/rrf\|RRF]] | 跨源融合具体配置（k=60，3 路） |
> | [[wiki/retrieval/rag/rag-降级\|RAG 5 级降级]] | 永不返回空的可靠性兜底 |
> | [[wiki/retrieval/rag/citation-faithfulness\|引用忠实度]] | 每条陈述 `[S#]` + ID 校验 |
> | [[wiki/skills/skill-编写实践\|Skill 编写实践]] | budget + 模块化 + 显式降级 |
| [[wiki/claude-code/mcp\|MCP]] | 以 stdio MCP server 形式发布，多客户端可消费 |
