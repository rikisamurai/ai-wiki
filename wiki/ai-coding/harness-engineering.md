---
title: Harness Engineering
tags: [harness-engineering, ai-first, infrastructure]
date: 2026-04-22
sources:
  - "[[sources/inbox/为什么你的\"AI 优先\"战略可能大错特错？]]"
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
  - "[[sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex]]"
last-ingested: 2026-04-22
status: stable
---

# Harness Engineering（脚手架工程）

> [!note] TL;DR
> OpenAI 在 2026 年 2 月正式提出的概念：**工程团队的核心工作不再是写代码，而是赋能 Agent，让它们去完成有价值的工作**。系统出错时，问的不是"再试一次"，而是"AI 缺什么能力？怎么让这个能力对 Agent 变得清晰可见、强制执行？"

## 名字从哪儿来

Harness 原意是马具/安全带，软件工程里指测试支架或脚手架。Harness Engineering 字面上就是"为 AI 提供工作环境和约束条件"的系统工程——既给 AI 套上能干活的套具，也给 AI 系上不出格的安全带。

CREAO 团队自己摸到了同一结论才知道有这个名字。这种"独立达成的共识"通常是个真信号：[[agentic-coding|Agentic Coding]] 时代的工程方法论正在收敛。

## 核心理念：把"系统能被 AI 检查/验证/修改"作为目标

> [!example] 杠杆原则
> "你把越多部分的系统转化为 AI 可以检查、验证和修改的形态，你获得的杠杆效应就越大。碎片化的代码库对 AI 是隐形的，统一的代码库对它们来说是清晰易读的。"

这条原则催生的具体决策：

- **Monorepo 优于多仓**：让 AI 能纵览全局、推理跨服务的连锁反应、跑本地集成测试
- **结构化日志 + 可查询信号**：CloudWatch 暴露 25+ 自动告警和自定义指标——"AI 读不懂日志，就无法诊断问题"
- **死磕到底的 6 阶段流水线**：验证 CI → 部署开发 → 测试开发 → 部署生产 → 测试生产 → 正式发布。**整条流水线是确定性的**，这样 AI 才能预测结果并推理失败原因
- **把"人在循环里"也变成确定性**：Claude Opus 4.6 三轮并行审查（代码质量 / 安全 / 依赖），是必过关卡而非建议

## 与 Vibe Coding 的对立

[[vibe-coding|Vibe Coding]] 调一调 prompt 让代码跑通就提交——可以做原型，做不了生产。Harness Engineering 关心的是**反过来的事**：怎么让一段 AI 写的代码，**在没有人盯着的情况下，仍然不会把生产搞挂**。

| 维度 | Vibe Coding | Harness Engineering |
|---|---|---|
| 工程师做什么 | 调 prompt 直到能跑 | 设计让 AI 安全跑的系统 |
| 产出 | 代码 | 系统 + 防护栏 |
| Prompts | 是核心 | 用完即弃 |
| 适用场景 | 原型、个人项目 | 生产、长期演进 |

## 与其他概念的关联

- 哲学层面：[[ai-first-vs-ai-assisted]]——Harness Engineering 是 AI First 的工程落地
- 反面：[[vibe-coding]]、过渡态：[[spec-coding]]
- 自动化骨架：[[self-healing-loop]]——Harness Engineering 在日常运维上的具体形态
- 谁在干：[[架构师-操作员二分]]中的"架构师"角色就是 Harness Engineer
- 上下文管理：[[隐性知识与上下文]]、[[agents-md]]——把人写的核心代码与项目级备忘录当 harness 让 AI 仿照
- 核心原则：[[约束悖论]]——更高自主性需要更严格约束
- 衡量指标：[[agent-等待时间]]——把 human wait 降为 0
- 成熟度框架：[[harness-成熟度]]（Context / Architectural / Entropy）
- 验证盲区：[[行为正确性]]——绿色信号 ≠ 真信号
- 架构层原则：[[enforce-invariants]]——管边界、不管实现
- 系统可观测：[[agent-可读性]]——运行时无法访问的上下文 = 不存在
- 文档维护：[[doc-gardening]]——周期性 Agent 自动修文档漂移
- 合并节奏：[[高吞吐合并哲学]]——纠正成本 < 等待成本

> [!example] OpenAI Codex 案例：0 手写代码
> 2025 年 8 月起，OpenAI 一支 3-7 人团队用 Codex 从空仓库出发，**0 手写代码**写出了 ~100 万行、~1500 PR 的内部产品（5 个月，人均 3.5 PR/天）。完整复盘见 source；佐证 Harness Engineering 三层成熟度全部就位时能跑出 ~10x 效率提升。
