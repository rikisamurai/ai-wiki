---
title: Worse is Better
tags: [philosophy, software-engineering]
date: 2026-04-22
sources:
  - "[[sources/inbox/Agentic Coding 的边界]]"
last-ingested: 2026-04-22
status: stable
---

Worse is Better 是 Richard Gabriel 提出的编程哲学：在"明显地没有缺陷"（Obviously Bug-Free，MIT 路线）和"没有明显的缺陷"（No Obvious Bugs，New Jersey 路线）之间，后者往往胜出——因为它先跑起来、先占领生态，再慢慢补质量。

## 两条路线对比

> [!compare] MIT vs New Jersey
> - **Obviously Bug-Free（MIT）**：设计上从源头排除一类错误，接口正交、语义清晰，但落地慢
> - **No Obvious Bugs（New Jersey）**：能跑、看起来对、有问题再补，落地快但 bug 是潜伏的

## 与 AI 编程的强相关

> [!note] AI 默认走 New Jersey
> 自动补齐下一个 token 是 LLM 的原生能力——只要不限制，AI 能无限把代码编下去，产出的就是典型的 [[wiki/ai-coding/plausible-code|Plausible Code]]：能跑、看起来很对、bug 在路上。

要让 AI 走 Obviously Bug-Free 路线并非不可能，但需要：
- 人先为代码库奠基（核心架构、关键约束、风格基线）
- AI 在已有约束内仿照扩展
- 人持续介入回顾和修正——修正动作本身可由 AI 执行，但触发点必须由人把握

详见 [[wiki/ai-coding/agentic-coding|Agentic Coding]] 与 [[wiki/ai-coding/隐性知识与上下文|隐性知识与上下文]]。

## 与测试的关系

把测试本身当成黄金指标，是 New Jersey 路线的极端版本——"被一大堆测试包围"≠ 高质量代码。测试只能证明功能存在，不能证明 bug 不存在。详见 [[wiki/ai-coding/yagni-与-dry-反论|YAGNI 与 DRY 反论]]中关于 TDD 的反思。

## 一句话总结

如果你愿意承担 plausible code 的隐性成本，新泽西派给你最大化的速度；如果你做关键基础设施，请提前在 MIT 路线上付出。AI 让两条路的成本结构都变了，但没改变这个根本权衡。
