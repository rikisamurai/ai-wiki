---
title: 五种控制流模式
tags: [workflow, orchestration, agent-patterns]
date: 2026-05-16
sources:
  - "[[sources/clippings/你不知道的 Agent：原理、架构与工程实践]]"
last-ingested: 2026-05-16
status: draft
---

大多数 AI 系统可以拆解为五种基础控制流模式的组合。Anthropic 将"执行路径由代码预先确定"归类为 **Workflow**，"由 LLM 动态决定下一步"归类为 **Agent**——核心区别在于控制权。很多标着 Agent 的产品深入看更接近 Workflow，两者无高下之分，关键是为任务找到更合适的设计。

## 五种模式

> [!note] 提示链 Prompt Chaining
> 任务拆成顺序步骤，每步 LLM 处理上一步输出，中间可加代码校验点。
> **适合**：先写大纲再写正文、生成后翻译、线性流水线任务。

> [!note] 路由 Routing
> 对输入分类，导向对应的专用处理流程。
> **适合**：简单问题走轻量模型 / 复杂问题走强模型、技术咨询和账单查询走不同逻辑。

> [!note] 并行 Parallelization
> 两种变体：
> - **分段法**：把任务拆成独立子任务并发执行
> - **投票法**：同一任务跑多次取共识，适合高风险决策或需要多视角的场景

> [!note] 编排器-工作者 Orchestrator-Workers
> 中央 LLM 动态分解任务并委派给工作者 LLM，综合多个结果。
> 对应 [[coordinator-模式|Coordinator 模式]]，这是多 Agent 并行执行的标准拓扑。

> [!note] 评估器-优化器 Evaluator-Optimizer
> 生成器产出，评估器给反馈，循环直到达标。
> **适合**：翻译、创意写作等质量标准难以用代码精确定义的任务。

## 选择依据

| 模式 | 控制权 | 适用场景 | 典型实现 |
|---|---|---|---|
| 提示链 | 代码 | 线性、步骤确定 | 顺序 API 调用 |
| 路由 | 代码 | 输入有明确分类 | if/switch + 分发 |
| 并行 | 代码 | 独立子任务 / 需要多视角 | Promise.all |
| 编排器-工作者 | LLM | 任务边界动态 | Coordinator Loop |
| 评估器-优化器 | LLM | 质量标准模糊 | 反馈循环 |

## 相关页面

- [[agent-loop|Agent Loop]] — 单个 LLM 调用的 ReAct 主循环
- [[coordinator-模式|Coordinator 模式]] — 编排器-工作者的落地实现
- [[workflow/parallel-sprints|Parallel Sprints]] — 并行模式在 AI 工程中的应用
- [[agent-engineering/philosophy/harness-engineering|Harness Engineering]] — 让任务可以被自动验证的基础设施
