---
title: Agentic Coding
tags: [agentic-coding, ai-coding]
date: 2026-04-22
sources:
  - "[[sources/inbox/Agentic Coding 的边界]]"
last-ingested: 2026-04-22
status: draft
---

Agentic Coding 是让 LLM 驱动的 Agent 端到端完成编程任务的范式：人提供需求和上下文，AI 生成方案、代码与测试。它的能力上限不取决于"AI 能不能写代码"，而取决于人是否能持续提供高密度上下文并消化 AI 产出。

## 边界与瓶颈

> [!note] 三大边界
> 1. 训练语料里的代码大量是 [[wiki/ai-coding/big-ball-of-mud-语料|低质量浆糊]]，导致 AI 倾向于喷射 [[wiki/ai-coding/plausible-code|似是而非的代码]]
> 2. 软件质量缺乏可量化的回归指标（不像围棋有终局胜负），AI 难以自我提升核心设计能力
> 3. 真正的瓶颈是 [[wiki/ai-coding/review-带宽瓶颈|Review 带宽]]，不是生成带宽

## 与软件工程实践的关系

Agentic Coding 不是要替代既有软工实践，而是让既有实践（领域驱动设计、限界上下文、活文档）更容易落地。控制代码复杂度 → 提升 AI 上下文信息密度 → 让 AI 输出更可靠。

避免：
- [[wiki/ai-coding/yagni-与-dry-反论|过度 DRY 抽象]]
- 教条式 TDD / 盲目追覆盖率

倾向：
- 用代码表达 spec（人写 harness，AI 学风格扩展）
- [[wiki/ai-coding/隐性知识与上下文|主动提供隐性知识]]
- 将设计模式视为 Agent 的 Skills 库

## 适用场景

> [!example] 适合 vs 不适合
> - **适合**：原型探索、stub 生成、模式化代码、行为可被业务指标验证的模块
> - **谨慎**：并发代码（语料天然有竞态）、创造性程序、用户体验关键路径
> - **必须人来**：核心架构奠基、首次抽象决策、unknown unknowns 的需求边界

## 与 [[wiki/ai-coding/worse-is-better|Worse is Better]] 的关系

AI 擅长"没有明显的缺陷"（No Obvious Bugs）路线——堆出能跑、看起来对的代码；要走"明显地没有缺陷"（Obviously Bug-Free）路线，必须先有人为代码库奠基风格和约束。
