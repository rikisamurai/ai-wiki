---
title: SDD 隐性功能陷阱
tags: [sdd, anti-pattern, testing]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: draft
---

[[spec-coding|Spec-Driven Development]] 在 [[mimic-first-harness|Mimic-First Harness]] 加持下的特有陷阱：**AI 模仿参考代码时会自动复刻参考代码里的"隐性功能"——这些功能没写进 SDD 文档，但实际已经悄悄实现了**。得物的核心总结："**SDD 描述的是技术上怎么实现，而不是业务上所有的行为**。"

## 三类典型隐性功能

> [!example] AI 复刻参考实现时偷偷加的逻辑
> | 类型 | 示例 |
> |---|---|
> | **变量/表单清除** | 关闭弹窗时自动 `form.resetFields()` + 清空内容列表（参考代码有，AI 复刻时也加） |
> | **数据格式转换** | 永久有效时自动清除起止日期；某条件下自动转换字段类型 |
> | **默认值补齐** | 新增时优先级自动递增（`getMaxSequence() + 1`）——SDD 文档没说，AI 自己加 |
>
> 共同特征：**参考代码里"理所当然"的辅助逻辑，AI 认为不值得写进 SDD**。

## 为什么 SDD 抓不住

> [!important] 文档天然不能穷举
> SDD 描述"做什么"和"怎么实现"，但写文档的人（人或 AI）会**默认省略**：
> - "明显的"清理动作（关闭窗口当然要清状态）
> - "约定俗成的"边界处理（永久有效当然不能有起止日期）
> - "顺手的"业务默认值（新建当然该有合理初值）
>
> 这些在参考代码里**用代码表达了**，在新代码里 AI **也用代码表达了**——但**没用文档表达**。所以 review SDD 看不到、code review 不仔细看也看不到。

## 跟 [[plausible-code|plausible code]]、[[karpathy-四种失败模式|Wrong Assumptions]] 的关系

> [!compare] 三种"看着对"的失败
> | 维度 | [[plausible-code\|plausible code]] | [[karpathy-四种失败模式\|Wrong Assumptions]] | SDD 隐性功能陷阱 |
> |---|---|---|---|
> | 表面 | 代码看似实现了需求 | AI 没问就猜 | 代码完成了 SDD 列的所有 task |
> | 暗藏 | 实际没正确实现 | 边界条件被 AI 默认了 | SDD 没说但代码里多了一堆行为 |
> | 来源 | AI 推理错误 | AI 不问导致 | AI 模仿太忠实（包括没文档化的部分） |
> | 治理 | review + 测试 | forcing question | 主动找隐性功能 + 行为级测试 |
>
> 三者经常混合出现。SDD 隐性功能陷阱的特征是：**所有显性 task 都做完了**——一切看起来都"按 spec 完成"，但代码里多了 spec 没规定的行为。

## 治理：测试介入三阶段

> [!tip] 测试不能只看 SDD
> 得物给的测试介入指南：
>
> | 阶段 | 测试关注点 |
> |---|---|
> | **SDD Review 阶段** | 接口契约是否完整、字段定义是否对应需求 |
> | **代码 Review 阶段** | **重点：对照 SDD 和实际代码的差异、主动找隐性功能** |
> | **联调测试阶段** | 不要只测 SDD 描述的 happy path，覆盖边界场景和隐性行为 |
>
> 给测试同学的实操心法："**把 SDD 当起点而不是终点**——主动问'参考功能有哪些隐性行为？这些行为在新功能中是否合适？'"

## 与 [[mimic-first-harness|Mimic-First Harness]] 的张力

> [!warning] 一刀两面
> Mimic-First Harness 让 AI 复刻参考代码——这件事既消除 [[alien-code|外星代码]]（好），又制造了隐性功能陷阱（坏）。两者本质同源：**AI 太忠实地继承了参考代码里的所有东西**。
>
> 平衡点：
> - **明确告诉 AI 不要复刻什么**：在 prompt 里加"参考代码里的 X 行为不需要"
> - **隐性行为白名单**：把"团队习惯应当被复刻的"行为列出来作为 [[wiki/agent-engineering/workflow/agents-md|AGENTS.md]] 一部分
> - **接受隐性功能存在 + 用测试守底线**：实操中往往最划算——AI 复刻效率高，让测试覆盖反而比反复约束 prompt 划算

## 跟 [[wiki/agent-engineering/workflow/eval-grader-三类|state-check grader]] 的对应

[[wiki/agent-engineering/workflow/agent-evals|Agent eval]] 里有 state_check 类 grader——验证最终环境状态符合预期。这正是抓隐性功能陷阱的工具：SDD 没写的功能在 state_check 里**该没有**就该没有，**有了**就要分析是合理隐性行为还是 bug。

## 关联

- 上游 trade-off：[[mimic-first-harness]]、[[alien-code]]
- 同族失败：[[plausible-code]]、[[karpathy-四种失败模式]]
- 流程位置：[[openspec]]（verify-change 阶段）、[[三阶段联调]]
- 测试方法：[[wiki/agent-engineering/workflow/agent-evals|Agent Evals]]、[[wiki/agent-engineering/workflow/eval-grader-三类|state_check]]
- 上游范式：[[spec-coding]]
