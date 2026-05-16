---
title: Agent Loop（ReAct 主循环）
tags: [agent-loop, workflow, react]
date: 2026-05-16
sources:
  - "[[sources/clippings/你不知道的 Agent：原理、架构与工程实践]]"
last-ingested: 2026-05-16
status: draft
---

Agent Loop 是所有 Agent 系统的核心机制：**感知 → 决策 → 行动 → 反馈** 四个阶段不断循环，直到模型返回纯文本（无工具调用）为止。它的实现极为稳定，核心逻辑抽象后不足 20 行代码。

> [!note] 最小实现（TypeScript）
> ```typescript
> const messages = [{ role: "user", content: userInput }];
> while (true) {
>   const response = await client.messages.create({ model, tools, messages });
>   if (response.stop_reason === "tool_use") {
>     const results = await Promise.all(
>       response.content.filter(b => b.type === "tool_use")
>         .map(async b => ({ type: "tool_result", tool_use_id: b.id,
>           content: await executeTool(b.name, b.input) }))
>     );
>     messages.push({ role: "assistant", content: response.content });
>     messages.push({ role: "user", content: results });
>   } else {
>     return response.content.find(b => b.type === "text")?.text ?? "";
>   }
> }
> ```

## 扩展方式：外挂，不改循环

从最小实现到支持子 Agent、上下文压缩、Skills 加载，**主循环本身几乎不需要改动**。新能力通过三种方式叠加在循环外部：

1. **扩展工具集和 handler** — 增加工具定义与执行逻辑
2. **调整系统提示结构** — 常驻层 / 按需层 / 运行时注入（见 [[context/dynamic-context|动态上下文]]）
3. **把状态外化到文件或数据库** — 跨 session 的持久化机制

循环体不应变成巨大状态机。原则：**模型负责推理，外部系统负责状态和边界**。

## 循环终止条件

| stop_reason | 含义 | 行为 |
|---|---|---|
| `tool_use` | 模型决定调用工具 | 执行工具，把结果追加到 messages，继续下一轮 |
| `end_turn` | 模型产出最终答案 | 返回文本，退出循环 |
| `max_tokens` | 超出 token 上限 | 通常需要外层处理（压缩/截断） |

## 与 [[control-flow-patterns|五种控制流模式]] 的关系

Agent Loop 是"LLM 控制执行路径"的 Agent 模式的运行时机制。五种控制流模式（Prompt Chaining、Routing、Parallelization、Orchestrator-Workers、Evaluator-Optimizer）都建立在 Loop 之上，只是在 Loop 的调用拓扑上做了不同的编排。

## 相关页面

- [[control-flow-patterns|五种控制流模式]] — 在 Loop 基础上的编排变体
- [[workflow/sub-agent-纪律|子 Agent 纪律]] — 子 Agent 的独立 messages\[\] 与摘要回传
- [[context/context-rot|Context Rot]] — Loop 长时间运行后的上下文衰减
- [[workflow/long-horizon-agent|Long Horizon Agent]] — 30-50 步以上 Loop 的工程挑战
