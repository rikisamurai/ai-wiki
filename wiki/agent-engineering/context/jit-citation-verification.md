---
title: JIT 引用验证（GitHub Copilot 的 memory staleness 机制）
tags: [memory, staleness, agent-engineering]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

GitHub Copilot 的 memory 设计有一个其他 harness 都没做的事：每条 memory 携带 `file:line` 级别的代码引用，**使用前在当前 branch 重新验证**——代码若已改写，memory 当场被覆写而不是被静默信任。加上 28 天 auto-expire，这是 [[memory-harness-shortcomings|harness memory 五大短板]]里唯一被解决的 staleness 设计，也是唯一一个有 published 生产 A/B 数据的 memory 机制。

## 结构

> [!note] memory item 是结构化对象
> 每条 memory = `{subject, factual content, citation: file:line, reasoning}`
>
> 注意 `citation: file:line` 是**强约束字段**——没有可对齐到代码的位置就无法构造记忆。

## 使用流程

> [!example] just-in-time 验证
> 1. agent 取出候选 memory
> 2. 检查 `citation` 指向的 `file:line` 在当前 branch 是否还在
> 3. 若代码已变，**让 agent 当场 rewrite memory**（不沉默使用旧记忆）
> 4. 28 天未被验证使用 → 自动过期删除

这种设计把 staleness 检测推到"使用前"，而不是"周期性扫"或"靠用户清理"。

## 唯一被 A/B 测过的生产指标

> [!important] 7 个点的 PR merge rate 提升
> - 开关：memory on vs off
> - 显著性：**p < 0.00001**
> - PR merge rate：**83% → 90%**
> - code-review 精度：**+3%**
> - code-review 召回：**+4%**
>
> 这是 coding agent memory 领域**唯一一个 published real-world 生产数据**。其他家全都是 LoCoMo / LongMemEval 这类 [[memory-benchmarks|benchmark 分数]]——而 benchmark 本身的可信度有限。

## Shortcoming

> [!warning] citation schema 装不下"偏好"
> 这个设计的代价是：**ungroundable / preference-based 的事实存不进去**——"prefers minimal abstraction"、"avoid magic strings" 这类没法挂到具体 `file:line` 上的偏好，schema 直接拒绝。Claude Code 的 [[auto-memory|auto memory]] 反向：偏好类记忆是核心，但代码 ground truth 没有强约束。
>
> 另一限制：**repo-scoped**——记忆不跨仓库流动。

## 为什么其他家没抄

抄不了的原因是这套设计的"代码强 ground truth"假设只在 coding agent 里成立：

- 通用 agent（[[managed-agents-memory|Managed Agents]]、AgentCore）的 memory 大量是"对话/偏好/事实"，没有 `file:line` 可挂
- 即使在 coding agent 里，[[auto-memory|Claude Code]] / [[codex-memory|Codex]] 也选了"四类记忆 + 用户偏好"的路线——这部分本来就装不进 citation schema

但代价：staleness 在这些 harness 里**没有任何机制**，只能依赖人手清理或 LLM 自觉重写。

## 相关页面

- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — staleness 是其中一条
- [[memory-benchmarks|Memory Benchmarks]] — 为什么除 Copilot 外都只能报 benchmark
- [[auto-memory|Claude Code Auto Memory]] — 偏好类记忆为主，与 Copilot 互补
- [[ai-写-lint|AI 写 Lint]] — 类似的"机器可验证的事实"思路
