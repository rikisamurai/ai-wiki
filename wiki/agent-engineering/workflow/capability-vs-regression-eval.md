---
title: 能力 eval vs 回归 eval
tags: [evals, regression, methodology]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

Eval suite 在生命周期里扮演两种角色：**capability eval**（能力评估，回答"能做到什么"）和 **regression eval**（回归评估，回答"还能做到原来的"）。两者的目标通过率正好相反——capability 要起点低留出爬坡空间，regression 要接近 100% 守住底线。

## 两者目标对照

> [!compare] 起点 / 终点 / 用法
> | 维度 | Capability eval | Regression eval |
> |---|---|---|
> | 别名 | "Quality" eval | "Backsliding" eval |
> | 起点通过率 | 应**低**（给团队一座要爬的山） | 应**接近 100%** |
> | 主要诉求 | 让分数往上爬 | 不让分数掉下去 |
> | 失败的含义 | 模型/prompt 还差点 | 出 bug 了，要修 |
> | 触发频率 | 改 prompt / 升级模型时 | 每次 commit / 模型升级 |

## "毕业"机制

> [!note] capability → regression 的自然演化
> Agent 上线并优化后，**通过率高的 capability eval 应"毕业"为 regression suite**——它已经不再回答"能不能做到"，而是回答"还能可靠地做到吗"。同一组 task 在不同生命周期阶段被赋予完全不同的角色。
>
> 要避免的是只跑一个角色：
> - 只跑 capability：模型能力上去了但悄悄回退了某些场景，没人知道
> - 只跑 regression：永远不会有 hill to climb，团队失去对模型/产品天花板的判断

## Eval Saturation：饱和的诊断

**Eval saturation** 指 agent 已经把所有可解 task 都过了，剩下空间几乎为零。代表事件是 SWE-bench Verified——一年内从 30% 涨到 >80%，前沿模型已逼近饱和。

> [!warning] 饱和会让进步被掩盖
> 饱和后，**大幅能力提升只会表现为微小分数变化**。Qodo 起初对 Opus 4.5 不感冒，因为他们的 one-shot coding eval 抓不到模型在长任务/复杂任务上的提升——他们后来专门搭了一套 agentic eval framework 才看出真实差距。
>
> 见到饱和的应对：
> - 升级 task 难度（或换更难的 benchmark）
> - 把饱和的旧 suite 转为 regression（顺其自然完成"毕业"）
> - **绝不要**只盯分数判断模型——分数停滞不等于能力停滞

## 平衡的反例：单边优化

> [!example] Claude.ai web search 的反复调整
> 团队想"该搜的时候搜、不该搜的时候别搜"。如果只测"该搜时是否搜"，会优化出一个**什么都搜**的模型。所以 eval 必须同时覆盖：
> - 该搜时是否搜（如 "今天天气怎样"）
> - 不该搜时是否别搜（如 "苹果的创始人是谁"）
>
> 反复调正反平衡花了多轮迭代——这是 capability eval 必须**class-balanced** 的实例。

## 与其他评估的边界

- regression eval 不替代 [[读-transcript|transcript review]]：通过率守住不代表轨迹质量没退
- capability eval 不替代 production monitoring：评估集再大也是 synthetic，真实 distribution 永远会带来意外（[[eval-方法矩阵]]）

## 关联

- 总览：[[agent-evals]]
- 度量：[[pass-at-k-vs-pass-power-k]]——同一 task 跑多 trial 才能算稳定的 capability/regression 分数
- 范式背景：[[eval-driven-development]]——build evals before agents can fulfill them
