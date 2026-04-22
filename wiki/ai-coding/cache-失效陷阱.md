---
title: Cache 失效陷阱
tags: [cache-pitfalls, anti-pattern, prompt-design]
date: 2026-04-22
sources:
  - "[[sources/inbox/⁠‬⁠​​‬⁠​‍⁠​​​‬​‌​​​​​​⁠﻿​​﻿‬⁠﻿﻿​‬‌⁠​‬﻿⁠⁠​​﻿‌﻿‍‍Prefix Cache：Long Horizon Agent 的效率基石]]"
  - "[[sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token]]"
last-ingested: 2026-04-22
status: stable
---

# Cache 失效陷阱

> [!note] TL;DR
> [[prefix-cache|Prefix Cache]] 是字节级精确匹配，下面这六类操作几乎一定会让 [[cache-命中率|命中率]] 从 90% 跌到个位数——而且全程**不会报错**。它们是真实从 OpenClaw、SWE-agent、Hermes 等开源项目 issue 里捞出来的。

## 六大经典陷阱

### 1. 在系统提示词开头插入时间戳/请求 ID

经典反例：`current_time: 2026-04-21 09:03:12`。每次请求都变化，又被放在工具定义之前——20K tokens 的稳定前缀全部失效，每步工具调用重新 Prefill。

> [!example] OpenClaw Issue #49700
> 用户发现 Anthropic 命中率只有 ~10%。元凶：一个心跳时间戳被混进了系统提示词的"稳定"区域。每隔几秒时间戳变了，整个前缀就跟着失效。

### 2. 动态用户信息放在静态工具定义之前

顺序错了一切就废了。用户名、租户 ID、个性化偏好这些动态字段必须放在工具定义**之后**。参见 [[稳定前缀-动态后缀]] 的黄金法则。

### 3. JSON 序列化 Key 顺序不稳定

Go 的 `map`、Swift 的 `Dictionary`、Python `dict`（3.7 前）默认随机顺序。同一份数据序列化两次产生两份不同的字节序列，前缀匹配直接失败。

> [!warning] 修法
> JSON dump 永远加 `sort_keys=True`，工具 Schema 用稳定的 key 排序。

### 4. 对话历史非追加式修改

中途压缩、重排序、修改之前的消息——任何"非追加"的操作都会破坏哈希链。

> [!example] 反面教材
> 一个常见的"上下文管理优化"会把历史中的工具返回结果做摘要替换。看似省了 token，实际把整段后续历史的 cache 全废了，反而更贵。

### 5. 工具定义动态变化

根据权限动态添加/删除工具是个常见诱惑。但每次工具列表变化，整段工具 schema 的前缀就失效。

> [!tip] 修法
> 工具列表保持完整，用 Anthropic 的 `tool_choice` 参数限制本次可用工具，**不要修改工具列表本身**。

### 6. 工作中切换模型

Opus / Sonnet / Haiku 的权重不同，**KV 张量不能互用**。切一次模型，整段上下文（系统提示词 + CLAUDE.md + 工具 schema + 消息历史）都要全价重算。

源码 `promptCacheBreakDetection.ts` 专门追踪了 `modelChanged` 标记。

> [!warning] 实际场景
> "刚才用 Opus 调试一个复杂 bug，现在想用 Sonnet 写点简单 CRUD 节省额度"——切过去那一下，50K+ tokens 全价重算。
> 
> 节省下来的钱可能远小于切模型的成本。
> 
> **修法**：按工作阶段切，不要在一个 session 里来回换。**下班前最后半小时尤其不要切**——TTL 内切回还能命中旧缓存。

## OpenClaw 血泪四件套

源 article 把这四个 issue 作为典型踩坑记录：

| Issue | 教训 |
|---|---|
| #49700 | 心跳时间戳混入稳定前缀 → 命中率 ~10% |
| #23715 | Cache 静默失效 → 月度账单飙 5× |
| #40256 | 系统提示词 section 顺序写错 → 本地模型缓存全废 |
| #21999 | 系统提示词膨胀到 150K+ → 触发专项性能优化 |

这些教训最终凝练为 OpenClaw 的 cache-prefix boundary 设计，把"永远不变"和"每次都在变"彻底隔离。详见 [[稳定前缀-动态后缀]]。

## 防御性工程：怎么提前发现

- 每次提交检查工具 schema diff——意外变化必须 review
- 监控 [[cache-命中率]] 滚动均值，掉线即告警
- 系统提示词写自动化测试：序列化两次比对字节相等
- 长 prompt 拆出"稳定块"和"动态块"两个明确的变量名，强制 review 时分开看
- Anthropic 自家的姿势：Claude Code 监控 `cache_read_input_tokens`，下降 >5% 且 >2000 tokens 就判定断裂——这套 SaaS 友好的可观测性是值得抄的设计范式
