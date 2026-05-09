---
title: RAG 5 级降级（永不返回空）
tags: [rag, reliability, fallback]
date: 2026-05-09
sources:
  - "[[sources/clippings/youzingwasc-search-skill]]"
last-ingested: 2026-05-09
status: draft
---

[[wiki/skills/wasc-search-skill|wasc-search-skill]] 在 RAG 合成阶段做了一件非常工程化的事：把 LLM 调用拆成 5 级渐进降级——tool-call → 纯文本 → mini-prompt → snippet 拼接 → LLM 知识兜底。**任何一级失败都自动落到下一级，直到产出非空答案为止**。这是把 Nygard *Release It!* 的 Stability Patterns（熔断器 / 舱壁 / 降级）翻译到 [[rag|RAG]] 场景的标准范式。

> [!important] 5 级降级的设计原则
> 每一级在"信息质量"和"调用成本"之间取不同平衡点。**降级不是简单重试**——每一级换的是 prompt 形态、调用方式或信息源，而不是同一个调用多试几次。

## 5 级具体内容

> [!example] 自上而下的降级阶梯
> | 级别 | 形态 | 触发条件 | 信息质量 | 成本 |
> |---|---|---|---|---|
> | **L1** | Tool-Call 结构化输出（3 次重试 + 指数退避） | 默认入口 | 最高（schema 强约束） | 最高 |
> | **L2** | 纯文本生成回退（2 次重试） | L1 tool-call 解析失败 | 高（仍带引用） | 中 |
> | **L3** | 最小化 prompt（仅 top-3 源） | L2 仍超时 / 失败 | 中（信息量减少） | 低 |
> | **L4** | Snippet 直接拼接（**零 LLM 调用**） | L3 失败或预算耗尽 | 低（无综合，只拼摘要） | ~0 |
> | **L5** | LLM 训练知识直答（不带检索源） | 所有搜索 API 都挂了 | 不可溯源（兜底） | 中 |

> [!compare] L4 是关键的"逃生舱"
> L4 的设计很巧妙：**不调用任何 LLM，只用 snippet 拼接**。这意味着即使 LLM 服务整个挂掉，系统仍然能返回一个有引用的、由检索原文拼成的答案。这是一种"零依赖外部模型"的安全网——很多 RAG 系统漏了这一层，导致 LLM 一抖整套就废。

## 为什么 5 级而不是 3 级

> [!note] 每跳降一个维度
> | 跳变 | 降的是什么 |
> |---|---|
> | L1 → L2 | 输出结构化约束（tool-call → 自由文本） |
> | L2 → L3 | 输入信息量（全部 → top-3） |
> | L3 → L4 | LLM 调用本身（生成 → 拼接） |
> | L4 → L5 | 信息源（检索 → 训练知识） |

每一跳只放弃一个维度，给系统留出"下一跳还能再退"的空间。如果只有 3 级，跳变粒度太大，要么"轻微失败就退到无 LLM"，要么"严重失败仍然在硬扛 LLM"。

## 与同类降级模式的关系

> [!compare] RAG 5 级 vs 一般微服务降级
> | 维度 | 一般微服务 | RAG 5 级 |
> |---|---|---|
> | 失败信号 | HTTP 5xx、超时 | 同上 + LLM 输出解析失败、引用 ID 校验失败 |
> | 降级目标 | 返回缓存 / 默认值 | **返回非空答案**（信息质量可降，但必须有答） |
> | 兜底层 | 静态错误页 | LLM 训练知识直答（仍可读但失去溯源） |

RAG 的特殊性在于：**答案的"非空"和"可信"是两个独立维度**。L1-L3 在追求"可信"，L4-L5 在保底"非空"。明确拆开这两个目标，才能设计出真正不挂的 RAG 系统。

## 工程实现的几个要点

> [!warning] 不要把 5 级写成一个超长 try-catch
> wasc 的实现把每一级封装成独立函数 + 显式 fallback chain，而不是嵌套 5 层 try-catch。这样：
> - 每一级可以被独立单元测试
> - 监控可以分级别打点（"L1 命中率 / L4 触发率"是关键 SRE 指标）
> - 新增一级只需在 chain 里插一个

> [!warning] 兜底层（L5）要标记 confidence=low
> L5 的答案没有任何检索来源支撑，必须在结构化输出里把 `confidence` 字段降到 `low` 并把 `citations` 留空。否则下游消费方会把训练知识当成检索结果，造成幻觉透出。

## 关联

[[wiki/skills/wasc-search-skill|wasc-search-skill]] / [[rag|RAG]] / [[citation-faithfulness|引用忠实度]] / [[wiki/agent-engineering/workflow/self-healing-loop|Self-Healing Loop]]
