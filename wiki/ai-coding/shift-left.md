---
title: Shift Left（左移）
tags: [engineering-principle, quality, ai-cr]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！]]"
last-ingested: 2026-04-22
status: draft
---

Shift Left 是工程效能的核心理念之一：**让问题在尽可能早的阶段被发现和解决**。代码质量的反馈链路通常是 `IDE → 保存 → pre-commit → CI → PR Review → QA → 生产`，越早发现修复成本越低；越晚发现，开发者切换上下文、重新理解、反复提交的开销越大。

> [!note] 反馈延迟 ≈ 修复成本
> 编码时发现一个问题改一行就好；等到 PR 阶段才发现，开发者需要切回上下文、理解评论、修改代码、再次提交。**反馈越晚，修复成本越高。**

> [!warning] AI CR 的反 Shift Left
> [[ai-code-review|AI Code Review]] 在 PR 阶段挑 `console.log` 这类问题，本质上是把"应该编码时拦截"的工作推迟到了 Review 阶段。用"召回率"庆祝并不能改变方向走偏的事实——更值得问的是：为什么会有这么多伤口？

## 工程上怎么落地

按时机从早到晚：

- **编辑器实时**：ESLint / Stylelint / TypeScript Server 在保存时报错
- **pre-commit hook**：提交前跑 Lint + 类型检查，不通过不让提交
- **CI 卡点**：PR 级别的 Lint / 测试 / 类型检查，确保不合入主干
- **AI CR**：仅审查 Lint 表达不了的业务逻辑（[[ai-code-review]]）
- **人工 Review**：架构与意图（[[review-带宽瓶颈]]）

每一层只解决"上一层做不到"的事，避免重复劳动。这与 [[harness-engineering|Harness Engineering]] 的 Architectural Constraints 层是同一回事——把约束工程化、自动化，越早执行越好。
