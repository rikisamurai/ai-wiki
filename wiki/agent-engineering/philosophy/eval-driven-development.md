---
title: Eval-Driven Development
tags: [evals, methodology, edd]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: draft
---

Eval-Driven Development（EDD）是 Anthropic 给"AI 产品 / agent 开发"提的范式：**先把 capability eval 写出来定义未来要做到的能力，然后让 agent 去爬这座山，最后用 regression eval 把成果钉死**。它是 [[spec-coding]] 在 AI 产品时代的精神继承——eval 比 Spec 更"刚"、更可执行，能避免 Spec 几个月就过时的问题。

## 核心循环

> [!note] EDD 的三步
> 1. **Define**：写 capability eval 表达"我希望模型/agent 几个月后能做到 X"——一开始通过率应该低
> 2. **Iterate**：改 prompt、改 agent harness、等更强模型——监控 capability eval 通过率上升
> 3. **Lock**：通过率高到一定程度后，eval "毕业"为 regression suite，永久守住底线（[[capability-vs-regression-eval]]）
>
> 关键句："**Internally we often build features that work 'well enough' today but are bets on what models can do in a few months. Capability evals that start at a low pass rate make this visible.**"

## 与其他范式的关系

> [!compare] EDD vs TDD vs Spec Coding
> | 范式 | 核心约束物 | 局限 |
> |---|---|---|
> | **TDD** | 单元测试 | 只验证确定性逻辑，对 agent 行为质量无能为力 |
> | **[[spec-coding]]** | 自然语言 Spec | Spec 自身腐烂、模型解读漂移 |
> | **EDD** | 一组 task + grader | 评估自身需要维护、grading bug 会带偏决策（参见 [[读-transcript]]） |
>
> EDD 不是替代 TDD，而是补一层 agent 行为质量；EDD 也部分替代 Spec——eval task 是**可执行的 Spec**，比 Markdown 更不容易过时。

## 为什么是 evals 而不是更多 Spec

> [!important] 测试用例是最好的文档
> [[harness-engineering]] 的核心信念之一就是"与其依赖易变的自然语言 Spec，不如构建刚性、自动化的约束环境"。EDD 把这个信念落到产品决策层：
>
> - 两位工程师读同一份 Spec 可能得出不同的边缘 case 处理；写一组 eval task 强制把这些边缘 case 解决
> - **定义 eval task 是检验产品需求是否足够具体**的最好方式——写不出 task 就说明需求还没想清楚
> - 新模型发布时，跑一遍 eval suite 几小时内就能告诉你"哪些押注成了"

## 谁来写 eval

Anthropic 内部经过多种尝试后的结论：

> [!tip] 分工
> - **Dedicated eval 团队**拥有核心基础设施（harness、并发执行、报告）
> - **Domain expert 和产品团队**贡献绝大部分 task 并跑评估
> - PM、CSM、销售用 Claude Code 直接以 PR 形式提 eval task——离用户最近的人最懂成功长什么样

这跟"AI infra 团队 + 业务团队"的分工模式高度对称——参见 [[架构师-操作员二分]]。

## 不写 eval 的代价

> [!warning] "flying blind"
> 没 eval 的团队会陷在反应式循环：等用户抱怨 → 复现 → 修 → 祈祷别的没坏。无法区分真 regression 和噪声、无法在上线前自动测几百个场景、无法度量改进。
>
> 等到 AI 产品上规模再回来补 eval，要"反向工程"成功标准——而此时 active user 的真实使用模式早已偏离当初的预设。**evals get harder to build the longer you wait**。

## 关联

- 实现层：[[agent-evals]]、[[eval-grader-三类]]
- 范式同源：[[spec-coding]]、[[harness-engineering]]、[[验证驱动|验证驱动（Verification-Driven）]]
- 心态：[[行为正确性]]——eval 评的是行为正确性，单测评的是逻辑正确性
- 反例：[[plausible-code]]——没 eval 时模型生成"看着对的代码"难以被发现
