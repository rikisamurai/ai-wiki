---
title: Memory Benchmarks（LoCoMo / LongMemEval / MemoryArena / BEAM）
tags: [memory, evals, agent-engineering]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

衡量 agent memory 的 benchmark 是当前最弱的一环：常用的几乎全在测"能不能从过去对话里捞回事实"，而真正决定 agent 价值的是"记忆能不能引导更好的决策"。多个常用 benchmark 已接近饱和，高分不等于线上好用。读 memory 系统的 leaderboard 要带着怀疑读，包括 [[mem0|Mem0]] 自己的。

## 四个常被引用的 benchmark

> [!compare] benchmark 谱系
> | 名字 | 来源 / 年份 | 测什么 | 主要问题 |
> |---|---|---|---|
> | **LoCoMo** | 早期 | 10 个长对话的事实回忆 | grep baseline 就能拿 ~74%；对抗题与目标共享 surface 相似度 → 模式匹配就赢 |
> | **LongMemEval** | — | 5 类能力 × 500 题，向 1.5M token 扩 | 仍 recall-centric，但比 LoCoMo 真实 |
> | **MemoryArena** | [arXiv:2602.16313](https://arxiv.org/abs/2602.16313)（Stanford/UCSD/Princeton, 2026-02） | 必须用记忆才能做对的**行动决策** | 在 LoCoMo / LongMemEval 接近饱和的系统在这里失败 |
> | **BEAM** | ICLR 2026 | 唯一面向 10M+ token 生产规模（其他 cap 在 1.5M） | 多数系统不报 |

## "为什么这些 benchmark 容易被刷"

- **LoCoMo 的对抗题**与正确目标共享 surface 相似度 → 模型靠模式匹配赢，不靠"记得"
- 10 条对话样本量不足以让差异显著
- 大量题目其实**不需要**记忆，trivial grep 就能拿 74%

论文 [Anatomy of Agentic Memory](https://arxiv.org/abs/2602.19320) 把这个批评做了形式化：现存 benchmark 测的是"检索内容相似度"而不是"任务效用"，且都接近饱和。

## 它们都没测的事

> [!warning] 记忆是为了行动，不是为了背诵
> MemoryArena 的视角：测 memory 必须测它能不能引导 **action** 改善。LoCoMo / LongMemEval 测的是问答精度——这两件事在生产里几乎无关。

> [!note] selective forgetting 是被遮盖的能力缺口
> MemoryAgentBench（[arXiv:2507.05257](https://arxiv.org/abs/2507.05257)）总结四种 memory 能力：检索 / 整合 / 选择性遗忘 / 跨会话推理。各家系统**都搞定了检索**，但**没人解决"选择性遗忘"**——unlearn 一条 stale 事实同时保留其周边结构。

> [!example] 唯一一个生产指标
> 大部分 memory 报告的是 benchmark 分数。**唯一一个 published 的真实生产 A/B 测试结果**来自 [[jit-citation-verification|GitHub Copilot 的 JIT 引用验证]]：PR merge rate 从 83% 升到 90%，p<0.00001。其他都是 LoCoMo / LongMemEval 数字。

## 怎么读这些数字

- 看到只报 LoCoMo 的：大概率打不动 MemoryArena
- 看到只报 1.5M 以内的：到 BEAM 量级（10M+）就崩
- 看 LoCoMo 分数时先扣掉 grep 基线（~74%）
- 优先看是否有跨用户污染、staleness、selective forgetting 这三件的数据——通常没有

> [!important] 当前结论
> "the field needs a new memory benchmark"——见 [[memory-harness-shortcomings|harness memory 五大共同短板]]。在新 benchmark 普及之前，把 leaderboard 当作 sanity check，决策还是回到真实任务上的 keep rate 与 [[采纳率]]。

## 相关页面

- [[memory-three-tiers|Agent Memory 三层（working / external / parametric）]] — benchmark 衡量的是 external 层
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — benchmark 是其中一项短板
- [[agent-evals|Agent Evals（智能体评估）]] — agent 评估的通用原理
- [[capability-vs-regression-eval|能力 eval vs 回归 eval]] — benchmark 偏 capability，生产更要 regression
- [[jit-citation-verification|JIT 引用验证]] — 唯一 published 生产 A/B 结果
