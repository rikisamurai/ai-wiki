---
title: Subagent-Driven Development（每任务一个 subagent）
tags: [subagent, workflow, claude-code, superpowers]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Superpowers - AI 编码工作流框架]]"
last-ingested: 2026-04-23
status: stable
---

Subagent-Driven Development 是 [[wiki/aigc/superpowers|Superpowers]] 框架里的核心模式：**实施计划的每一个任务都派一个独立 subagent 执行，主线程 Claude 只负责 review 和决策**。这是把 [[wiki/ai-coding/subagent-上下文隔离|subagent 上下文隔离]]从"偶尔派一个"升级成"默认每任务派一个"。

> [!important] 为什么要"每任务一个"
> 普通用法：写完任务 1，看任务 2，思路飘了一下，"哎不如顺手把任务 4 也改了"——结果任务 4 改坏了任务 1 的隐含约定。
>
> Subagent-driven：任务 1 完整闭包给 subagent，它返回 PR/diff/测试结果。主线程根本看不到中间过程，**没办法被诱惑去顺手改其他任务**。这强制了任务的原子性。

> [!compare] 三种 subagent 用法对比
> | 模式 | 主线程做什么 | subagent 做什么 | 适合 |
> |---|---|---|---|
> | **临时派遣**（[[subagent-上下文隔离\|经典模式]]） | 还在做主任务，需要时派 | 一次性研究/验证 | 探索性任务 |
> | **Coordinator 编排**（[[wiki/aigc/coordinator-模式\|经理模式]]） | 拆任务、合并结果 | 并行执行 N 个相似任务 | 批量处理 |
> | **Subagent-driven** | 走计划、review、决策 | 串行执行每个 plan task | 长任务（数小时） |

**前置条件：必须有详细 plan**

Subagent-driven 跑得动的前提是 **[[wiki/aigc/superpowers|writing-plans]] 阶段把任务切到 2-5 分钟粒度**——粒度太粗，subagent 上下文里塞不下；粒度太细，调度开销 > 执行开销。

> [!example] 工作循环
> ```
> 主线程 Claude: 读 plan task #N
>   ↓ 派 subagent
> Subagent: 接 task 描述 + 相关文件路径
>   ↓ TDD: 写测试 → 跑测试 → 实现 → 跑测试
>   ↓ 返回: diff + 测试通过证据
> 主线程 Claude: review diff，符合 plan？
>   ↓ 是 → 标记 task #N 完成，下一个
>   ↓ 否 → 修改 plan 或回滚
> ```
>
> 主线程的 context 里只有：plan 文件 + 每个 task 的最终 diff。**中间所有的探索/试错/失败测试都关在 subagent 里**——这是它能跑数小时不爆 context 的原因。

> [!tip] 与 [[wiki/ai-coding/writer-reviewer-模式|Writer/Reviewer]] 的关系
> Writer/Reviewer 是**任务级**的——一个 task 上 Writer 写 + Reviewer 审。
>
> Subagent-driven 是**计划级**的——主线程是 planner+reviewer，subagent 是 worker。
>
> 两者可以叠加：主线程派 worker subagent A 写代码，再派 reviewer subagent B 审 A 的输出，主线程只看最终结论。这是 [[wiki/aigc/coordinator-模式|Coordinator 模式]]的最复杂形态，但极端情况下能让 Claude 真的"自主跑半天"。

> [!warning] 不要用 subagent-driven 做需要主线程上下文连贯的任务
> 如果任务 N 依赖任务 N-1 的"思考过程"（不只是结果文件），subagent 的全新 context 会丢掉这部分——这正是 [[wiki/ai-coding/subagent-上下文隔离|subagent 隔离]]的反面。判断标准：**task 的输入是否能用文件路径 + plan 描述完整传达？** 能 → 用 subagent；不能 → 留在主线程。

**关联**：[[wiki/ai-coding/subagent-上下文隔离|Subagent 上下文隔离]]（理论基础） / [[wiki/aigc/superpowers|Superpowers]]（实现框架） / [[wiki/aigc/coordinator-模式|Coordinator 模式]]（编排理论）
