---
title: pass@k vs pass^k
tags: [evals, metrics, non-determinism]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: draft
---

Agent 行为在 trial 间会变，所以同一 task 要跑 k 次后用统计量描述。最常用的两个度量正好相反：**pass@k** 度量"k 次里至少有 1 次成功的概率"，**pass^k** 度量"k 次全部成功的概率"。前者随 k 上升，后者随 k 下降。

## 数学直觉

> [!compare] 上升 vs 下降
> | 度量 | 定义 | 单 trial 成功率 75% 时，k=3 的值 | 适用场景 |
> |---|---|---|---|
> | **pass@k** | k 次中至少 1 次成功 | 1 − (0.25)³ ≈ **98.4%** | "试一次行就行"——coding 一发命中、研究找答案 |
> | **pass^k** | k 次全部成功 | (0.75)³ ≈ **42.2%** | "每次都得行"——客服、生产管线、面向终端用户的 agent |
>
> k=1 时两者相等（=单 trial 成功率）。k 增大后两者分道扬镳——k=10 时 pass@k 趋近 100%、pass^k 趋近 0%。

## 用哪个看产品要求

> [!important] 产品形态决定度量
> - **pass@k**：开发者愿意"重新生成一次"或工具能给多个候选——典型如代码补全、文案稿
> - **pass^k**：用户期待每次稳定——客服、订票、医疗问答；这里 75% 单次成功率意味着每 4 次有 1 次让用户失望，pass^k 才能照出这件事多严重
>
> Coding 通常关心 pass@1（要"第一次就对"），但配合 pass@k 可以判断"再试几次能不能对"。

## 为什么必须跑多 trial

> [!note] 单 trial 的不可解读
> 假设 agent 在某 task 上"实际"成功率 60%，单跑一次给你的信号要么是"过"要么是"不过"——你完全不知道这个 task 是 90% 那种还是 50% 那种。**eval 真正关心的常常是分布、不是单次结果**。
>
> 这也是为什么 [[读-transcript|读 transcript]] 重要：单次失败可能是真问题、可能是常态分布的下沉，需要看轨迹判断。

## 与 [[capability-vs-regression-eval]] 的配合

- Capability eval 的分数应是 pass@k 形式（追求"能做到"，多 trial 留出空间）
- Regression eval 的分数应是 pass^k 形式（追求"每次都做到"，对掉点零容忍）

同一组 task 走 capability → regression 的"毕业"过程时，度量也跟着切换。

## 关联

- 总览：[[agent-evals]]
- 上游不确定性来源：[[harness-engineering]]、模型采样温度、环境状态（参见 [[读-transcript]]）
- 隔离环境为什么重要：trial 间共享状态会让"独立 trial"假设失效，pass@k / pass^k 计算就成了垃圾
