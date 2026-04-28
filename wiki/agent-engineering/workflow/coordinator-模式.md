---
title: Coordinator 模式（经理模式）
tags: [claude-code, multi-agent, orchestration]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-23
status: stable
---

Coordinator 模式是 [[claude-code|Claude Code]] 内部的多 Agent 编排模板：主 Agent 不直接干活，**变成纯任务编排者**，把工作分发给一群 [[wiki/agent-engineering/workflow/subagent-上下文隔离|子 Agent]]。源码里这套模式有明确的四阶段结构。

> [!example] 标准四阶段
> ```
> Phase 1: Research        → 3 个 worker 并行搜索代码库
> Phase 2: Synthesis       → 主 Agent 综合所有发现
> Phase 3: Implementation  → 2 个 worker 分别修改不同文件
> Phase 4: Verification    → 1 个 worker 跑测试
> ```

**核心原则："Parallelism is your superpower"**

源码里这条原则被反复强调，落地规则有两条：

| 任务类型 | 执行方式 | 原因 |
|---|---|---|
| **只读任务**（搜索、调研、grep） | 并行 | 无副作用，不会冲突 |
| **写文件任务** | **按文件分组串行** | 同一文件的并发写会冲突 |

按文件分组的精妙之处：不是"所有写都串行"，而是"**同一文件**的写串行"——不同文件之间仍可并行。这把并发收益最大化的同时把冲突风险降到零。

**与 [[wiki/agent-engineering/workflow/writer-reviewer-模式|Writer/Reviewer]] 的差异**

| 维度 | Writer/Reviewer | Coordinator |
|---|---|---|
| **角色数量** | 2（写 + 审） | 主 + 多 worker |
| **协调方** | 你或 Agent Teams | 主 Agent 自己 |
| **典型场景** | 单个功能的质量门控 | 大任务拆解（探索 + 合成 + 实现 + 验证） |
| **数据流** | 双向反馈 | 主控分发 + 汇总 |

**子 Agent 的 "你是工人不是经理"约束**

为防止 Coordinator 模式失控（worker 又生成 worker，递归爆炸），Claude Code 在子 Agent 启动时注入硬约束：

```
STOP. READ THIS FIRST.
You are a forked worker process. You are NOT the main agent.
RULES (non-negotiable):
1. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps
3. USE your tools directly
4. Keep your report under 500 words.
5. Your response MUST begin with "Scope:". No preamble.
```

这是 [[wiki/agent-engineering/workflow/enforce-invariants|Enforce Invariants]] 在子 Agent 系统里的应用——**经理只能有一个**这个不变量是写在 prompt 而非代码里的，因为它需要被模型"理解"才能遵守。

> [!warning] 不要把所有任务都套 Coordinator
> Coordinator 模式有显著开销：每个 worker 是 [[wiki/agent-engineering/workflow/subagent-上下文隔离|独立上下文]]、独立缓存链、独立模型调用。**只在任务**真的能拆成"3+ 个独立可并行子任务"**时才划算**。简单任务直接主线程跑——避免为了"看起来用了多 agent"而牺牲缓存效率。
