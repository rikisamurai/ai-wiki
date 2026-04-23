---
title: Agentic RAG
tags: [rag, agentic, llm]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/rag/intro]]"
last-ingested: 2026-04-23
status: draft
---

Agentic RAG 是 [[rag|RAG]] 在 2025-2026 最大的范式转变——把"线性管道"换成"循环结构"，**LLM 不是消费检索结果的下游，而是决定检索策略的推理引擎**。如果首轮检索不够，智能体重新构造查询再检索；不够好就再循环。

> [!important] 范式对比：管道 vs 循环
> ```
> 朴素 RAG（管道）：     query → retrieve → generate → done
> Agentic RAG（循环）：  query → reason → retrieve → reflect → reason → retrieve → ... → generate
> ```
> 关键差别：**LLM 在 retrieve 之前**。它判断"我现在缺什么信息"再决定怎么查；查回来后再判断"够不够"。

**四种实现模式**

> [!example] ReAct 风格推理
> "思考 → 行动（搜索）→ 观察 → 再思考"的循环。适用单次检索不够的场景：
>
> ```
> Thought: 用户问 X，我先搜 Y
> Action: search(Y)
> Observation: 找到 Z 但缺 W
> Thought: 现在搜 W
> Action: search(W)
> ...
> ```
>
> 是 LangGraph 的默认骨架，参考 [[wiki/ai-coding/long-horizon-agent|Long Horizon Agent]]。

> [!example] 多智能体并行
> 多个 agent 在不同系统中并行搜索，最后由聚合器合并——本质就是 [[wiki/ai-coding/subagent-上下文隔离|Subagent 上下文隔离]] 的应用。
>
> Deep Research 就是这种模式：把"研究 X"拆成 N 个子方向，每个 subagent 独立搜+总结，主 agent 合并成最终答案。和 [[wiki/ai-coding/subagent-driven-development|Subagent-Driven Development]] 同源——只是任务从"写代码"换成"找信息"。

> [!example] Self-RAG
> 让模型自己决定**何时需要检索**，并对自己的输出做批判性评估。
>
> ```
> 问题来了 → 模型问自己"这个我会吗"？
>   ├── 会 → 直接答（省 token）
>   └── 不会 → 检索 → 答 → "我答得对吗"？
>                   ├── 对 → 输出
>                   └── 不对 → 改写 query 重新检索
> ```
>
> 比无脑 retrieve 节省 token，幻觉率显著下降。

> [!example] 层级化 Agentic RAG
> 把多粒度检索接口暴露给模型——关键词搜索 / 语义搜索 / 块级阅读 / 文档级阅读，让 LLM 动态选用。
>
> **量化效果**：在 HotpotQA 多跳问答数据集上达到 **94.5% 准确率**——朴素 RAG 在多跳任务上常不到 50%。

**与 Subagent / Long-Horizon Agent 的关系**

Agentic RAG ≈ "把检索作为唯一动作的 [[wiki/ai-coding/long-horizon-agent|Long Horizon Agent]]"。所以 Long Horizon Agent 的所有挑战在 Agentic RAG 里同样存在：

- [[wiki/ai-coding/context-window|上下文窗口]]爆炸（每轮观察都进上下文）
- [[wiki/ai-coding/cache-命中率|Cache 命中率]]（多轮迭代的 prompt 前缀稳定性）
- [[wiki/aigc/coordinator-模式|Coordinator 模式]]（协调多 subagent 的结果）

> [!tip] 工程实操：LangGraph + LangSmith 是当前事实标准
> - **LangGraph**：基于 LangChain 的图状 agent 工作流编排——节点是"检索/评估/重写"，边是状态流转
> - **LangSmith**：调试和监控 agent 决策链——在生产里"为什么 agent 选错检索路径"是头号问题
>
> 没有可观测性的 Agentic RAG 是黑盒，迭代效率会断崖式下降。

> [!warning] 代价：延迟 + 成本 + 失败循环
> - **延迟**：N 轮检索 = N 倍延迟。Browser-Use 类基准里看到 47s → 113s 的差距，Agentic RAG 同理
> - **成本**：每轮都消耗 LLM token，复杂查询很容易 5-10 轮
> - **死循环风险**：query 改写策略不好时会反复检索同一类无关文档——必须设最大步数兜底
>
> 用 Agentic RAG 之前先问："朴素 RAG + 好的 chunking + 重排序"是不是已经够用？很多场景里它就是更好的选择。

**关联**：[[rag|RAG]] / [[hybrid-retrieval|混合检索]] / [[graph-rag|GraphRAG]] / [[wiki/ai-coding/long-horizon-agent|Long Horizon Agent]] / [[wiki/ai-coding/subagent-上下文隔离|Subagent 上下文隔离]] / [[coordinator-模式|Coordinator 模式]]
