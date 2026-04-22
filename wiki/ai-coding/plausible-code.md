---
title: Plausible Code（似是而非的代码）
tags: [llm, ai-coding, code-quality]
date: 2026-04-22
sources:
  - "[[sources/inbox/Agentic Coding 的边界]]"
last-ingested: 2026-04-22
status: draft
---

Plausible Code 指 LLM 针对任意通用任务都能生成"看起来正确"的方案/代码——能编译、能跑、命名合理、注释通顺，但常在性能、并发、边界条件上隐藏问题。它是 [[wiki/ai-coding/agentic-coding|Agentic Coding]] 的默认产出形态，也是其能力上限的体现。

## 成因

> [!note] 两个机制
> 1. 大模型本质是基于概率生成最可能的下一个 token，输出会被 [[wiki/ai-coding/big-ball-of-mud-语料|训练语料的中位数水平]]拉平
> 2. 模型厂商有动机在 RLHF 阶段倾向"用最小推理成本生成像那么回事的输出"，赌用户就此满足

## 经典例子

- 号称 LLM-driven 用 Rust 重写的 SQLite，简单查询 SQLite 原版 0.09ms，重写版 1815.43ms（上万倍差距）。但单次任务也就一秒——如果你的需求到此为止，"似是而非"已经满足
- AI 写并发代码丢三落四：因为开源并发代码本身大量包含考虑不全的竞态条件

## 与质量评判的张力

> [!compare] 两条路
> - **No Obvious Bugs**：能跑就行，有 bug 再修。AI 默认走这条
> - **Obviously Bug-Free**：从设计上排除一类错误。需要人先奠基约束
>
> 详见 [[wiki/ai-coding/worse-is-better|Worse is Better]]。

测试覆盖率不能拯救 plausible code——你能写出"被一大堆测试包围但仍然错的代码"，正如谚语所说"测试只能证明功能存在，不能证明 BUG 不存在"。

## 应对

不是不用 AI，而是承认产出默认 plausible，把人力放在 [[wiki/ai-coding/review-带宽瓶颈|Review]] 与核心代码奠基上，让 AI 仿照风格扩展。
