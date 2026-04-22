---
title: Cache 命中率
tags: [cache-hit-rate, observability, agent-metrics]
date: 2026-04-22
sources:
  - "[[sources/inbox/⁠‬⁠​​‬⁠​‍⁠​​​‬​‌​​​​​​⁠﻿​​﻿‬⁠﻿﻿​‬‌⁠​‬﻿⁠⁠​​﻿‌﻿‍‍Prefix Cache：Long Horizon Agent 的效率基石]]"
last-ingested: 2026-04-22
status: stable
---

# Cache 命中率

> [!note] TL;DR
> `命中率 = 缓存命中 token 数 / 总输入 token 数`。llm-d 团队的判断：**KV Cache 命中率是生产级 AI Agent 最重要的单一指标，直接决定延迟和成本**。它没有日志报错——账单和 P90 延迟才是它的报警器。

## 不同场景的目标区间

| 场景 | 可达命中率 |
|---|---|
| 固定系统提示词 + 多轮对话 | 80%–95% |
| RAG（相同文档，多次查询） | 70%–90% |
| 多 Agent 共享相同系统提示 | 90%–99% |
| 动态内容混入前缀 | 5%–30%（糟糕） |

低于 50% 时基本可以认为命中机制失效，要立刻去查 [[cache-失效陷阱]]。

## 为什么没人盯着它就出事

[[prefix-cache|Prefix Cache]] 失效**不会报错**。Token 还在算，结果还在返回，Agent 还在工作——只是悄悄变慢、变贵。OpenClaw 的 GitHub Issue #23715 就是典型：用户发现 Cache 莫名失效，没有任何信号，**直到月底账单飙了 5 倍**才意识到。

> [!warning] 监控该长这样
> - **核心指标**：每个请求记录 `cached_input_tokens` / `total_input_tokens`
> - **告警线**：滚动平均命中率掉到目标线 50% 以下立即告警
> - **维度切片**：按系统提示词版本、工具定义版本、租户分别统计——有些破坏只发生在特定切片

## 提高命中率的工程杠杆

- **结构层面**：严格执行 [[稳定前缀-动态后缀]]
- **基础设施层面**：会话粘性路由（Sticky Routing）。OpenAI 用 `prompt_cache_key`，自建推理用会话 ID 一致性哈希。实测可以把命中率从 60% 拉到 87%。
- **避坑层面**：消除所有 [[cache-失效陷阱]]
- **TTL 层面**：长任务用 Anthropic extended TTL（1 小时）避免中途过期

## 跟其他指标的关系

命中率不是孤立指标。它直接驱动：

- 单次任务成本（[[long-horizon-agent]]）
- P90 TTFT
- API 速率限制余量（命中读不占配额，等于免费扩容）

在 [[long-horizon-agent|Long Horizon Agent]] 上，这一个指标几乎决定了系统能否上线。
