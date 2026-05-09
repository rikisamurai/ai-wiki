---
title: Research Agent Eval
tags: [evals, research-agent, browsecomp]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

Research agent（市场扫描、尽职调查、科研综述）的评估特别难——**"comprehensive / well-sourced / correct" 都依赖上下文**：市场扫描、并购尽调、科学综述对"好"的标准完全不同。专家本身可能在"是否全面"上分歧，参考材料还在持续变化，开放式输出又给错误留了大空间。BrowseComp 是该方向的代表 benchmark。

## 三类必做检查

> [!note] groundedness / coverage / source quality
> 单测在这里几乎用不上，但有一组 model-based grader 可复用：
> - **Groundedness**：每个 claim 是否有检索到的 source 支撑？无支撑的 claim = 幻觉
> - **Coverage**：好答案应该包含的关键事实是否都覆盖到？设计 task 时要先列 expected facts
> - **Source quality**：引用的 source 是不是权威的，还是只是检索结果第一条？

对**有客观正确答案**的 task（"X 公司 Q3 营收是多少"），exact match 仍可用。开放式综述则只能靠 LLM 评 coherence 和 completeness。

## BrowseComp：大海捞针

[BrowseComp](http://arxiv.org/abs/2504.12516) 测 agent 能否在开放 web 上"找针"——题目设计成**易验证、难求解**的形式。这是 research agent 评估的一个干净抽象：要求 agent 在巨大搜索空间里精准定位。

## 模型作裁判 ≠ 模型说了算

> [!important] 必须周期性人工校准
> 因为 research quality 主观，**LLM-based rubric 必须频繁与专家人工判断校准**——参见 [[eval-grader-三类|LLM-as-judge 校准]]。否则 LLM 裁判会漂移：可能慢慢偏向"长就是好"或"列点多就是好"，而专家想要的是"准确 + 简洁 + 来源可靠"。
>
> 实操建议：
> - rubric 拆细，每个维度独立 LLM-as-judge
> - 给 LLM 留 `Unknown` 出口防硬掰幻觉
> - 定期抽样让人工和 LLM 都打一遍，看分歧大不大

## 度量取舍：pass@k 偏多

研究类任务很多场景"试几次有一次对就行"——产出报告之后人会读、会进一步追问。所以 [[pass-at-k-vs-pass-power-k|pass@k]] 比 pass^k 更常用。除非是面向终端用户的 research bot（每次都要可靠），那时再切到 pass^k。

## 和 RAG / Browser-Use 的关系

Research agent 的底层 retrieval 路径决定了 grader 设计：

- 走 [[wiki/retrieval/rag/agentic-rag|Agentic RAG]] 路线：grader 可访问 retrieval log，groundedness 检查能直接核对引用 chunk
- 走 [[wiki/retrieval/browser/browser-use|Browser-Use]] / Anthropic computer use 路线：grader 需要从 transcript 还原 agent 实际访问过的 URL；source quality 检查要走 URL 白名单

## 关联

- 总览：[[agent-evals]]
- 同类不同 agent：[[coding-agent-eval]]、[[conversational-agent-eval]]、[[computer-use-agent-eval]]
- 检索基础：[[wiki/retrieval/rag/rag|RAG]]、[[wiki/retrieval/browser/agent-browser]]
- 校准：[[eval-grader-三类]]
