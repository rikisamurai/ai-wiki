---
title: TDD 红绿重构循环
tags: [tdd, workflow, feedback-loop]
date: 2026-05-26
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Matt Pocock Skills - 人类满分工程师的自我蒸馏]]"
last-ingested: 2026-05-26
status: draft
---

TDD（Test-Driven Development）的 RED → GREEN → REFACTOR 三步循环对 AI 编码尤其关键：红灯测试是"不会说谎的需求说明书"，绿灯是"完成"的客观信号，重构是在安全网下清理。没有这个循环，AI 不知道"完成"的边界，可能写了很多代码看起来对、其实偏了。

> [!example] 三步循环
> **🔴 RED — 先定义"完成"长什么样**
> 在写任何实现代码前，先写一个描述目标行为的测试。它此时必然失败——因为功能还不存在。价值：**强迫你在动手之前想清楚要什么**。
>
> **🟢 GREEN — 用最小代价达成目标**
> 写刚好能让测试通过的代码，不多不少。目的不是优雅，是让测试变绿。防止 AI 过度设计或跑题。
>
> **🔵 REFACTOR — 在安全网下清理**
> 测试已经通过，现在可以放心删重复、改命名、简化逻辑。测试会立即告诉你有没有改坏。

## 为什么对 AI 比对人类更刚需

> [!important] 客观验收信号 > 人眼审阅
> 人类工程师有"代码品味"做内部验收，AI 没有——它只能从环境信号判断"是否完成"。红灯测试是**自动化的、不会含糊的**验收：通了就是通了，没通就是没通。这同时切到 [[wiki/agent-engineering/workflow/验证驱动|验证驱动]]——agent 在自称"完成"前必须有证据。

## 与现有工作流的位置

| 框架 | TDD 的位置 |
|---|---|
| [[wiki/skills/matt-pocock-skills\|Matt Pocock Skills]] | 独立 `/tdd` skill，按需调用 |
| [[wiki/skills/superpowers\|Superpowers]] | 嵌在 `subagent-driven-development` 里，每个 subagent 任务**强制**走 RED-GREEN-REFACTOR |
| [[wiki/agent-engineering/workflow/探索-规划-编码-验证\|探索-规划-编码-验证]] | 隐含——"验证"阶段的核心手段 |

> [!compare] TDD vs Eval-Driven Development
> TDD 验"代码行为对不对"（确定性断言）；[[wiki/agent-engineering/philosophy/eval-driven-development|Eval-Driven Development]] 验"AI 系统的输出质量"（语义/概率打分）。两者不替代：传统代码逻辑用 TDD，agent/LLM 链路用 eval，混合系统两者都要。

## "一次一个垂直切片"原则

Matt Pocock 的 `/tdd` skill 强调每次 RED 只写**一个**测试：覆盖**一个**端到端的最小行为切片，而不是先把所有测试写完。这与 [[wiki/agent-engineering/workflow/sprint-七阶段范式|短 sprint]] 的精神一致——**反馈速率就是速度上限**（The Pragmatic Programmer），切片越小，AI 偏离的窗口越短。

> [!tip] 避免 AI 写"假测试"
> 让 AI 先写测试时，常见反模式是它写一个"必然通过"的弱断言（比如只断言函数不抛错）来骗自己进 GREEN。对策：RED 阶段人类**至少瞄一眼断言条件**，确认它真的能区分"功能有 / 没有"。

## 关联

- 上层框架：[[wiki/skills/matt-pocock-skills|Matt Pocock Skills]]、[[wiki/skills/superpowers|Superpowers]]
- 配套实践：[[wiki/agent-engineering/workflow/验证驱动|验证驱动]]、[[wiki/agent-engineering/workflow/subagent-driven-development|subagent-driven-development]]
- 反面：[[wiki/agent-engineering/philosophy/plausible-code|Plausible Code]]——没有验收信号时 AI 产出的"看起来像对的"代码
