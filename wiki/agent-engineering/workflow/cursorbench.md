---
title: CursorBench
tags: [evals, benchmark, cursor]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: draft
---

[CursorBench](https://cursor.com/blog/cursorbench) 是 [[cursor|Cursor]] 公开的 agent 质量 benchmark，用于跨时间对比 [[harness-engineering|harness]] + 模型组合的表现。Cursor 把它定位为**快速、标准化的近似信号**，配合内部 eval 套件 + 在线 A/B 实验形成"多层衡量体系"。

## 在 Cursor 评估栈里的位置

> [!example] 三层评估
> | 层 | 工具 | 角色 |
> |---|---|---|
> | 1. 公开 benchmark | **CursorBench** | 跨时间标准化趋势 |
> | 2. 内部 eval 套件 | Cursor 私有 task 集 | 覆盖私有/敏感场景 |
> | 3. 在线 A/B | 真实流量分桶对比 | 抓离线 eval 抓不到的真实分布问题 |
>
> Cursor 的明确警告："**最好的 benchmark 也只能近似反映真实使用情况**——完全依赖它们就会错过重要信号。"——CursorBench 是趋势仪表盘，不是真理裁判。

## 为什么要公开

> [!important] 公开 benchmark 的策略价值
> 把 benchmark 公开有几个好处：
> - **跨厂商对话语言**：模型提供方在调优时可看到 Cursor 的 benchmark 怎么打分
> - **可信度**：第三方可独立复跑，不只是 Cursor 自己说了算
> - **跨时间**：版本号绑定 benchmark 分数，回归更显眼
>
> 类比 [[coding-agent-eval|SWE-bench Verified]] 之于 coding agent——成熟生态需要公开 benchmark 当公共坐标。

## 不能只看 benchmark 分数

> [!warning] benchmark 与真实 distribution 总是错配
> CursorBench 也跑不开 [[agent-evals|agent evals]] 提到的几个通病：
> - benchmark task 集是**有限快照**，真实用户会在意想不到的方向上失败
> - benchmark **饱和**后小提升被掩盖（[[capability-vs-regression-eval|eval saturation]]）
> - benchmark 评的是**一次性 task**，但真实使用是多轮交互（要靠 [[keep-rate]] 和 [[语义满意度信号]] 补）
>
> Cursor 因此把 benchmark 当**第一层信号**，下面还要叠 [[keep-rate|Keep Rate]]、[[语义满意度信号|语义满意度]]、A/B 三层。

## 与其他 coding benchmark 的对照

> [!compare] 三个 coding 域 benchmark
> | benchmark | 任务来源 | 主要 grader | 当前状态 |
> |---|---|---|---|
> | **CursorBench** | Cursor 自定 + 公开 | Cursor 内部说明 | 跨时间趋势 |
> | **[[coding-agent-eval\|SWE-bench Verified]]** | GitHub issue 真实 PR | 仓库自带单测 | 一年从 40% → >80%（接近饱和） |
> | **Terminal-Bench** | 端到端真实技术任务 | task-specific 验证脚本 | 仍有大空间 |
>
> 三者形态不同、覆盖不同场景，**理想做法是同时跑**，而不是只盯一个。

## 关联

- 上游工具：[[cursor]]
- 评估理论：[[agent-evals]]、[[eval-grader-三类]]、[[capability-vs-regression-eval]]
- 同族 coding benchmark：[[coding-agent-eval]]
- 配合补足的度量：[[keep-rate]]、[[语义满意度信号]]
- 多模型对比：[[wiki/agent-engineering/code-review/cross-model-second-opinion|跨模型 second opinion]]——benchmark 也能用来跨模型比
