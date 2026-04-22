---
title: Enforce Invariants, Not Implementations
tags: [harness-engineering, architecture, principle]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex]]"
last-ingested: 2026-04-22
status: draft
---

OpenAI Codex 团队的核心架构原则：**强制不变量，不微观管理实现**。Agent 在边界严格、结构可预测的环境中最有效——你深切关注**边界、正确性、可复现性**，但在边界之内给 Agent 充分的表达自由。产出的代码不一定符合人类的风格偏好，**没关系**——只要输出正确、可维护、对未来 Agent 运行可读，就达标。

> [!example] Codex 团队的分层架构
> ```
> Types → Config → Repo → Service → Runtime → UI
> ```
> 每个业务领域固定层数，依赖方向严格验证；跨领域关注点（Auth、Connectors、Telemetry、Feature Flags）只能通过 **Providers** 单一显式接口接入，其他方式被禁止并机械化执行。

**为什么是早期前置条件**：这种架构通常在团队上百人时才推行。但在 Agent 编码场景下它是**早期必备**——正是这些约束让速度不带来衰减和架构漂移。约束就是速度的来源，与 [[约束悖论]] 同构。

**品味的机械化**

- 自定义 Linter + 结构化测试执行规则
- Lint 的**错误信息本身就是修复指引**，直接注入 Agent 上下文
- 要求 Codex 在边界处 [Parse, Don't Validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)，但**不规定具体用什么库**——这就是"管边界，不管实现"

**人类品味的复利反馈**

> 当文档不够时，就把规则提升为代码（promote the rule into code）。

Review 评论 → 文档更新；重构 PR → 编码为工具约束；用户可见的 Bug → 直接编码到 Lint 规则中。这是 [[harness-engineering|Harness Engineering]] 反应式生长（见 [[约束悖论]]）的具体姿态。
