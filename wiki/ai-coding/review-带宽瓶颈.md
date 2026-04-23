---
title: Review 带宽瓶颈
tags: [ai-coding, code-review, agentic-coding]
date: 2026-04-22
sources:
  - "[[sources/inbox/Agentic Coding 的边界]]"
  - "[[sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！]]"
last-ingested: 2026-04-22
status: stable
---

Agentic Coding 的真实生产力上限不在 AI 生成代码的速度，而在人 Review AI 产出的带宽。生成是无限的（自动补齐下一个 token 是 LLM 的原生能力），但消化、验证、修正是有限的。

## 为什么 Review 这么贵

> [!note] 三个原因
> 1. AI 没有稳定的行为特征，会犯人不会犯的错——你不能用 Review 同事代码的直觉去 Review AI 代码
> 2. 在你搞清楚 AI 通常会犯什么错之前，Review 一个 AI patch 的开销 ≈ 自己写一遍或至少在脑里大致走一遍
> 3. 人天性懒惰——一旦 handoff 给 AI，相当一段时间内你会"啥也不看就 accept"，等到遇到瓶颈再回头填坑，扭转习惯比一开始就 Review 还贵

## 与 [[wiki/ai-coding/plausible-code|Plausible Code]] 的关系

正因为 AI 默认产出 plausible code（看起来对、跑得起来），Review 不能只是"看一眼通过"，而要校验：
- 边界条件是否覆盖
- 是否堆出了不必要的抽象（[[wiki/ai-coding/yagni-与-dry-反论|YAGNI 反论]]）
- 是否引入了 unknown unknowns 中的"流行做法"（如登录鉴权场景）

## 工程上的应对

> [!example] 生产高质量软件场景下的提效上限
> 1. 用 AI 探索可能性
> 2. 让 AI 生成 stub
> 3. 由人定期维护核心设计和框架实现
> 4. 把人写的代码当 harness/spec，让 AI 仿照
>
> 见 [[wiki/ai-coding/agentic-coding|Agentic Coding]] 的边界讨论。

AI Review（让 AI 来 Review AI patch）目前 false positive 率虽在下降，但意见仍不能全听——多一道工序但不能替代人的最终判断。

## 反例：可以放松 Review 的场景

如果你是 Vibe Coding 的目标用户（业务不严苛、用户即测试者），那"先 accept 再说"是合理策略——海量 researcher 用 pickle dump 数据模型也没什么问题。
