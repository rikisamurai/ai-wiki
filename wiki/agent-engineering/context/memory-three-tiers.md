---
title: Agent Memory 三层（working / external / parametric）
tags: [memory, context, agent-engineering]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

把"memory"按**存在哪里**切成三层：working（上下文窗口）、external（权重之外的向量库/图/文件）、parametric（梯度下降进权重）。2026 年所有生产级 agent memory 几乎全在 external 这一层；parametric 零生产部署。这层划分与 [[agent-memory-分层|认知科学的 semantic / episodic / procedural]] 三分正交——后者描述"存什么类型的信息"，本页描述"信息存在哪儿"。

## 三层的对比

> [!compare] 三层 = 不同的失败模式
> | 层 | 介质 | 会话结束后 | 谁修改 | 典型失败 |
> |---|---|---|---|---|
> | **working** | 上下文窗口（`messages[]`） | 清空 | LLM 本身在 token 里写 | 窗口满 → [[compact-vs-clear\|compaction]] 时丢什么 |
> | **external** | 向量库、KG、文件、SQLite | 保留 | 外部读写流程（提取/检索 sub-agent） | 检索召回错、容量上限、staleness |
> | **parametric** | 模型权重 | 训练写入后永久 | gradient descent | 灾难性遗忘、训练成本 |

> [!note] 为什么 parametric 在 2026 还没生产
> 论文 [Contextual Agentic Memory is a Memo, Not True Memory](https://arxiv.org/abs/2604.27707) 给了上限：retrieval 需要 Ω(k²) 存储例子才能匹配 parametric 用 O(d) 次权重更新能做到的泛化。当前所有 harness 都在这条上限之下——它们做的是"备忘录"，不是"真正记得"。

## 为什么"在哪里"比"什么类型"先决定

- **working** 的限制是 token，调优手段是 [[context-rot|context rot]] / [[compact-vs-clear|compact vs clear]] / [[caveman-超压缩通信|caveman 压缩]]
- **external** 的限制是检索精度和上限，调优手段是 [[hybrid-retrieval|混合检索]] / [[memory-benchmarks|benchmark 校准]] / [[mem0|跨 harness 基础设施]]
- **parametric** 的限制是训练成本和稳定-塑性权衡——硬塞进权重就会冲掉别的

把这三件事混着叫"memory"是 harness 文档里最常见的歧义来源。

## harness 实践基本都在 external

观察 9 个主流 harness：

- [[auto-memory|Claude Code Auto Memory]]、[[codex-memory|Codex memories]]、[[hermes-agent|Hermes MEMORY.md]]、Windsurf — 全是本地 markdown
- [[managed-agents-memory|Anthropic Managed Agents]] — `/mnt/memory/` 文件系统 + append-only event log
- AWS Bedrock AgentCore — 托管的语义事实/偏好/叙事三策略提取
- OpenClaw — markdown + 每 agent SQLite + 70/30 向量/BM25 混合检索
- [[devin-knowledge|Devin Knowledge / DeepWiki]] — human-curated trigger-content
- [[mem0|Mem0]] — 跨 harness 的 vector + KG + KV 基础设施

> [!important] external memory 不是"自动救场"
> 论文 [When Continual Learning Moves to Memory](https://arxiv.org/abs/2604.27003) 显示：迁到 external 没有终结 catastrophic forgetting——新旧记忆争夺 retrieval slot 的方式和当年争夺权重一样。"加个向量库"不等于"问题解决"。

## 相关页面

- [[agent-memory-分层|Agent 记忆四分层（工作/程序/情景/语义）]] — 正交的"信息类型"分类
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — external 层的工程现实
- [[mem0|Mem0（跨 harness 记忆基础设施）]] — 把 external 抬出 harness 边界
- [[memory-benchmarks|Memory Benchmarks（LoCoMo / LongMemEval / MemoryArena / BEAM）]] — 衡量 external 层的工具
