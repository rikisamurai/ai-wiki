---
title: Parallel Sprints（10-15 并行 sprint）
tags: [workflow, parallelism, conductor]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: stable
---

[[gstack]] 实测能跑 **10–15 个并行 sprint**——每个 sprint 是一个独立 Claude Code 会话、跑独立的 [[sprint-七阶段范式|7 阶段流水线]]、在独立 worktree 里。这是个体开发者最大化吞吐的当前实践上限：再多就管不过来；再少就浪费了 [[gstack|多角色专家化 + 流水线]] 带来的并行潜力。

## 为什么"流程"是并行的前提

> [!important] 没有流程的 10 个 agent = 10 个混乱源
> Garry Tan 原话："**Without a process, ten agents is ten sources of chaos. With a process — think, plan, build, review, test, ship — each agent knows exactly what to do and when to stop.**"
>
> [[sprint-七阶段范式]] 在并行场景才显出真正价值：
> - 每个 agent 知道自己处于哪个阶段，知道何时停下等你审
> - 你只在"决策点"出现：`/office-hours` 完成时审 framing、`/plan-ceo-review` 完成时审 scope、`/review` 完成时审 race condition fix
> - 其余时间 agent 自己跑

## Conductor 是当前最简的并行化工具

> [!example] Conductor 跑多 Claude Code 会话
> [Conductor](https://conductor.build/) 让你在一个 UI 里：
> - 同时启动 10+ Claude Code 会话，每个在独立 worktree
> - 一个跑 `/office-hours` 探索新点子
> - 一个跑 `/review` 在某 PR 上
> - 一个实现某个 feature
> - 一个跑 `/qa` 在 staging URL 上
> - 其余 6 个跑别的分支
>
> 类似工具：[[wiki/agent-engineering/philosophy/opc-一人公司|OPC]] 派的 Container Use、Crystal、Backlog.md（每个都是"多 agent 多 worktree"的不同 UI 取向）。

## CEO 心态：管 vs 干

> [!tip] 像 CEO 一样管十个员工
> "**You manage them the way a CEO manages a team: check in on the decisions that matter, let the rest run.**"
>
> 实操：
> - 不要试图"看每个 agent 的每条输出"——那等于把自己降级成审稿员
> - 用 [[gstack|gstack]] 的 Review Readiness Dashboard 看哪个 sprint 准备好让你审、哪个还在跑
> - 决策点：framing、scope、race condition 这种**值得人类判断的**问题
> - 其它（lint 修复、测试编写、文档同步）放手让 agent 跑

## 跟其他并行范式的关系

> [!compare] 三种并行的层次
> | 层次 | 单元 | 工具 |
> |---|---|---|
> | **Sprint 并行** | 10-15 个 7 阶段流水线 | Conductor + gstack |
> | **Subagent 并行** | 一个 sprint 内 N 个独立任务 | [[subagent-driven-development|SDD]]、Coordinator 模式 |
> | **Tool 并行** | 一次响应内多 tool call | Claude Code 默认支持 |
>
> 三层叠加：你跑 12 个 Sprint，每个 Sprint 内可能开 3 个 [[subagent-driven-development|subagent]]，每个 subagent 可能在一次响应里发 5 个 tool call。理论吞吐 12×3×5 = 180 个并发动作，但实际瓶颈是**人审决策点的吞吐**——这才是为什么 [[gstack|gstack]] 投入很多 prompt 工程减少需要审的决策数。

## 上限是认知带宽，不是工具

> [!warning] 为什么是 10–15 而不是 100
> 每个 sprint 都会冒出"该不该升级 scope""这个 race condition 怎么修""设计要走哪个 variant"的决策点。即使 [[gstack]] 已经把决策数压到最小，10–15 个并发 sprint 已经能填满一个人的工作日。
>
> 想突破这个上限的方向：
> - 把更多决策权下放给 agent（[[wiki/agent-engineering/philosophy/ai-first-vs-ai-assisted|AI First]] 极端形态）
> - 用 [[self-healing-loop|Self-Healing Loop]] 把"监控 + 修复 + 验证"也自动化掉
> - 多人协作分担决策（每个人审 3-5 个 sprint）

## 配套基础设施需求

跑 10+ 并行 sprint 的硬性要求：

- **多 worktree**：避免 git 冲突——参见 [[handoff-md|HANDOFF.md]] 风格的跨会话协作
- **Continuous Checkpoint**：[[continuous-checkpoint]] WIP commit 防止任一 sprint 崩溃丢工作
- **明确的 review 路由**：哪些 review 必走、哪些可跳，避免 10 个 sprint 全部把决策推给你
- **持久知识库**：[[gbrain|GBrain]]——agent 之间共享 codebase 知识，否则每个 sprint 都要重学

## 关联

- 范式来源：[[gstack]]
- 流水线模板：[[sprint-七阶段范式]]
- 单 sprint 内并行：[[subagent-driven-development]]、[[coordinator-模式]]
- 个体最大化吞吐主题：[[wiki/agent-engineering/philosophy/opc-一人公司|OPC（一人公司）]]、[[wiki/agent-engineering/philosophy/agent-工作量分布]]
