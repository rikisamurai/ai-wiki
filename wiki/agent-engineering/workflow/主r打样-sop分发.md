---
title: 主 R 打样 → SOP 分发 → 全组并行
tags: [workflow, ai-coding, refactor]
date: 2026-05-08
sources:
  - "[[sources/clippings/用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践]]"
last-ingested: 2026-05-08
status: draft
---

团队规模化执行 AI Coding 任务的三步范式：先由重构主 R 亲自做完最复杂的两个样本、在过程中沉淀可让 AI 执行的标准化 SOP，再把 SOP 分发给全组并行跑。重构不再依赖某一个人的经验，团队成员只需指导 AI 执行 SOP + 业务语义验收。

> [!note] 为什么不能让每个人都自己摸索
> 同一类重构任务（如工程分层迁移）改造规则相对明确，但涉及范围极广、重复劳动密集。如果每个人自己摸索，AI 会跟着每个人当前文件附近的模式继续生成 → 风格分歧 → 见 [[wiki/agent-engineering/philosophy/ai-加速腐化|AI 不会自动收敛复杂度]]。让一个人先把 SOP 跑通再分发，是把"人人对齐"前置到执行层。

## 三步范式

> [!example] 美团工程分层迁移的实操
> 1. **主 R 打样**：重构主 R 亲自完成两个最复杂包的迁移（按需求建包 → Starter / Application / Infrastructure / Common 四层），过程中沉淀步骤
> 2. **沉淀为 SOP**：步骤标准化、AI 可执行（每一步给 AI 的 prompt、判断条件、产出形态都明确）
> 3. **全组并行**：其他成员按 SOP 指导 AI 完成剩余包迁移，自己聚焦业务语义验收 + Code Review
>
> 通过这种方式快速完成了 10 余个核心包的工程结构迁移。

## 关键判断点：什么样的任务适合这套范式

> [!compare] 适合 vs 不适合
> | 任务特征 | 适合 SOP 分发 | 不适合 |
> |---|---|---|
> | 改造规则 | 相对明确、可枚举 | 高度依赖业务语义判断 |
> | 重复度 | 同类操作要做 N 遍 | 每个 case 都不一样 |
> | AI 可执行度 | AI 能按步骤执行 | 需要人持续做架构决策 |
> | 典型例子 | 工程分层迁移、批量 API 改名、批量错误处理补齐 | 业务模型设计、跨服务边界重新切分 |

## 与 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 的关系

> [!note] 同源不同层
> Coordinator 模式讨论的是单次任务里"人定边界、agent 在边界内自主"。本页讨论的是组织规模化的"一人打样、N 人并行"。两者经常组合使用：每个并行执行的工程师对自己的 AI agent 用 Coordinator 模式做边界控制，整体团队层用主 R 打样 + SOP 分发协调。

## 关联

- 哲学基础：[[wiki/agent-engineering/philosophy/人人对齐-人机对齐|人人对齐 → 人机对齐]]——SOP 是人人对齐的执行载体
- 协调模式：[[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]]、[[wiki/agent-engineering/workflow/parallel-sprints|Parallel Sprints]]
- 应用场景：[[wiki/agent-engineering/workflow/渐进式重构|渐进式重构]]——SOP 分发是渐进式重构的执行手段之一
