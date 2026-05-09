---
title: Pre-PR（提交前 AI 自审）机制
tags: [code-review, ai-cr, workflow]
date: 2026-05-08
sources:
  - "[[sources/clippings/用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践]]"
last-ingested: 2026-05-08
status: stable
---

提交 PR 之前要求 RD 先用 AI 多轮自查、修复所有 AI 能发现的问题，再走标准 PR 流程。Reviewer 拿到的是"已过滤掉基础规范错误"的高质量代码，只需聚焦核心业务语义。这是 AI Coding 提速后缓解 [[wiki/agent-engineering/code-review/review-带宽瓶颈|Review 带宽瓶颈]] 的关键左移手段。

> [!note] 为什么要单独立一道"预审"
> AI 编码极大压缩了写代码时间，压力系统性地向下游 CR 集中。如果还按"提交后 Reviewer 全责审"的老流程，AI 提速的红利会被 CR 瓶颈吞掉——"木桶效应"。Pre-PR 把规范类、Bug 类、异常处理、一致性、可扩展性、性能等问题在提交前就消化掉。

## 机制要点

> [!example] 美团团队的 Pre-PR 流程
> 1. **多轮 AI 自查**：RD 用 AI 反复扫描代码，修复所有 AI 能发现的问题
>    - 规范类、Bug 类、异常处理
>    - 一致性、可扩展性、性能
> 2. **标准 PR 文档**：AI 按模板生成（重点说明改动点、影响范围、需重点 Review 的业务逻辑）
> 3. **Reviewer 聚焦业务语义**：基础规范错误已过滤，认知负担显著降低

## 人工 CR 的角色变化

> [!compare] AI Coding 时代的 CR 价值迁移
> | 维度 | 旧 CR 价值 | Pre-PR 之后的 CR 价值 |
> |---|---|---|
> | 关注问题 | "你写得对吗？" | "我们是否在正确的约束下解决正确的问题？" |
> | 谁审规范 | 人工 | AI（Pre-PR） |
> | 谁审业务 | 人工 | 仍然人工，但前置到技术方案评审 |
> | 谁审实现 | 人工 | 人工，重点是和技术方案的一致性 |
>
> 见 [[wiki/agent-engineering/code-review/shift-left|Shift Left]]——Pre-PR 是把基础质量左移到提交前。

## 与多模型 CR 的叠加

> [!tip] Pre-PR + Cross-model
> Pre-PR 阶段可以叠加：
> - **高阶模型审查低阶模型**：用高配模型作为 Judge Model，审查低阶模型产出的编码
> - **不同厂商对抗审核**：见 [[wiki/agent-engineering/code-review/cross-model-second-opinion|跨模型 Second Opinion]]
>
> 这两层是 Pre-PR 的"加强版本"，关键 PR 用、日常修改可只用基础 Pre-PR。

## 与 [[wiki/agent-engineering/code-review/ai-code-review|AI Code Review]] 的关系

> [!note] 都用 AI 审，但时机不同
> - **Pre-PR**：提交前 RD 自己跑、自己修
> - **AI CR**：提交后系统性跑、产出 Review 评论
>
> Pre-PR 是 [[wiki/agent-engineering/code-review/shift-left|左移]] 到 RD 个人工作流；AI CR 是平台化、对所有 PR 统一执行。两者不冲突，理想状态是 Pre-PR 已经过滤掉绝大部分问题，AI CR 只用于兜底 + 留痕。

## 关联

- 直接驱动：[[wiki/agent-engineering/code-review/review-带宽瓶颈|Review 带宽瓶颈]]、[[wiki/agent-engineering/code-review/shift-left|Shift Left]]
- 叠加增强：[[wiki/agent-engineering/code-review/cross-model-second-opinion|跨模型 Second Opinion]]、[[wiki/agent-engineering/code-review/ai-code-review|AI Code Review]]
- 测试侧对应：[[wiki/agent-engineering/workflow/ai-辅助测试-sop|AI 辅助测试 SOP]]
