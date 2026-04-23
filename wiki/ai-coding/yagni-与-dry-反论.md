---
title: YAGNI 与 DRY 反论
tags: [yagni, software-engineering, ai-coding]
date: 2026-04-22
sources:
  - "[[sources/inbox/Agentic Coding 的边界]]"
last-ingested: 2026-04-22
status: stable
---

DRY（Don't Repeat Yourself）原则在 Coding Agent 时代容易被滥用：Claude Code 和 Codex 都倾向于一遇相似就抽方法/模块、自己发散出"未来可能用到"的可复用设计，结果是过度抽象。YAGNI（You Aren't Gonna Need It）是对此的反论——只为当前真实需求写代码。

## 黄金准则

> [!note] 三次法则
> - 第一次写：顺着写下来
> - 第二次遇到相同逻辑：复制粘贴
> - 第三次重复：才考虑抽取
>
> 抽取时判断：是逻辑上意涵相同，还是只是碰巧用了相似的代码实现？后者不要抽。

## 为什么 AI 时代更危险

太过超前的抽象就是 Premature Optimization。在 [[wiki/ai-coding/agentic-coding|Agentic Coding]] 流程下，错误的抽象会误导 AI 在歧路上越走越远——因为 AI 仿照风格的能力很强，一旦地基歪了，后续生成的代码会持续放大错误。

> [!example] 典型反模式
> 用 DRY 抽出来的"公共函数"，从一开始就要为不同调用路径提供不同的配置参数来调整内部行为。这种 DRY 是无效的——不同调用路径的行为本就不同，抽取只是把分支推进函数内部。

## 与其他原则的关系

- 与 [[wiki/ai-coding/plausible-code|Plausible Code]] 互为表里：AI 输出的"看起来很设计"的抽象，往往就是过早泛化的产物
- 与 KISS（Keep It Simple, Stupid）一脉相承
- 参考：Martin Fowler 的 Yagni 一文、John Carmack on Inlined Code

## 实践建议

让 Agent 按 YAGNI 写代码：在 prompt / skill 里明确告知"不要为未来的需求做设计"、"不要抽取仅出现 1-2 次的逻辑"，并把这条作为 [[wiki/ai-coding/review-带宽瓶颈|Review]] 时的硬性检查项。
