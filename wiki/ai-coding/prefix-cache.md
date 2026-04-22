---
title: Prefix Cache
tags: [prefix-cache, llm-inference, cost]
date: 2026-04-22
sources:
  - "[[sources/inbox/⁠‬⁠​​‬⁠​‍⁠​​​‬​‌​​​​​​⁠﻿​​﻿‬⁠﻿﻿​‬‌⁠​‬﻿⁠⁠​​﻿‌﻿‍‍Prefix Cache：Long Horizon Agent 的效率基石]]"
  - "[[sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token]]"
last-ingested: 2026-04-22
status: stable
---

# Prefix Cache

> [!note] TL;DR
> Prefix Cache 是 [[kv-cache|KV Cache]] 的跨请求延伸：当多个请求共享同一段 token 前缀（系统提示词、工具定义、参考文档）时，只对该前缀做一次 Prefill，后续请求直接复用 KV 张量，跳过整段预填充。对 [[long-horizon-agent|Long Horizon Agent]] 而言，它不是优化项，是能否跑得起的基础设施。

## 工作原理

三个阶段：

- **⚙️ Prefill**：模型对输入做完整前向传播，生成所有 token 的 KV 张量。计算最密集，耗时与 prompt 长度正相关。
- **🖊️ Decode**：逐 token 生成输出，每步只处理新 token。
- **♻️ Prefix Reuse**：下一个请求到来时，匹配前缀直接复用 KV，整段 Prefill 跳过。

> [!warning] 字节级精确匹配
> 前缀匹配是字节级的。哪怕只有一个 token 不同，从该位置起的所有 KV 缓存均告失效——这条约束直接催生了[[稳定前缀-动态后缀|稳定前缀-动态后缀]]的 prompt 设计法则，也是大量 [[cache-失效陷阱|失效陷阱]]的根源。

**与 KV Cache 的关系**：

| 维度 | [[kv-cache\|KV Cache]] | Prefix Cache |
|---|---|---|
| 作用范围 | 单次请求内部 | 跨多个独立请求 |
| 优化阶段 | Decode（生成） | Prefill（预填充） |
| 是否默认开启 | 是 | 需要前缀匹配 |
| 内存共享 | 每个请求独占 | 多请求共享物理块 |

两者互补，不是竞争关系。生产 Agent 系统里，缺一不可。

## 各平台实现概览

> [!example] 平台对比
> - **Anthropic**：显式 `cache_control` 断点，最高 90% 折扣，每请求 4 个断点，TTL 5 分钟（可升到 1 小时）。最小可缓存前缀：Claude 4.6 系列要 4,096 tokens。
> - **OpenAI**：全自动，零代码改动，1024+ tokens 自动以 128 token 增量缓存。命中节省约 50%。
> - **vLLM**（APC）：哈希链式块池（16 token/块，SHA256 哈希），LRU 淘汰。
> - **SGLang**（[[radix-attention|RadixAttention]]）：基数树存储，token 级匹配，天然支持对话树分支，最高 6.4× 吞吐提升。

设计哲学差异：Anthropic 把控制权给开发者（精确但繁琐），OpenAI 把决策埋进 API（省心但粗放）。这个权衡贯穿了所有 LLM 平台 API 设计——参见 [[worse-is-better]] 里"接口简单 vs 实现完美"的同款张力。

## Claude Code 的内部 4-block 结构

Claude Code 不是把 prompt 当一整块发出去，而是**精心拼接的多层结构**（来自源码逆向）：

```
┌─────────────────────────────────────────────────┐
│ system（系统提示词，~20K tokens）                │
│   Block 1: 计费归因头              → 不缓存       │
│   Block 2: CLI 前缀               → 不缓存       │
│   Block 3: 静态指令（行为规则等）   → global 缓存 │ ← 全球所有用户共享！
│   ──── DYNAMIC_BOUNDARY ────                    │
│   Block 4: 动态内容（CLAUDE.md 等） → org 缓存   │
├─────────────────────────────────────────────────┤
│ tools（工具 schema，session 内冻结）             │
├─────────────────────────────────────────────────┤
│ messages（对话历史）                             │
│   最后一条消息上放 cache_control 标记            │
└─────────────────────────────────────────────────┘
```

关键源码函数：

- `getSystemPrompt()` (prompts.ts:444) — 组装系统提示词
- `splitSysPromptPrefix()` (api.ts:321) — 按 `DYNAMIC_BOUNDARY` 切分
- `buildSystemPromptBlocks()` (claude.ts:3214) — 加 `cache_control` 标记
- `addCacheBreakpoints()` (claude.ts:3064) — 在最后一条消息上标记缓存断点

这套结构对应到 prompt 设计法则就是 [[稳定前缀-动态后缀]]——`DYNAMIC_BOUNDARY` 就是它说的 cache-prefix boundary 在 Anthropic 内部的实现。

## 两档 TTL（Anthropic）

| 档位 | 时长 | 适用对象 |
|---|---|---|
| 默认 | 5 分钟 | 所有用户 |
| 扩展 | 1 小时 | Pro/Max 订阅未超额、Anthropic 员工 |

源码 `claude.ts:408-413`：

```typescript
userEligible =
  process.env.USER_TYPE === 'ant' ||
  (isClaudeAISubscriber() && !currentLimits.isUsingOverage)
```

TTL 在**每次读取时刷新**——这条机制催生了 [[cache-keep-alive|Cache Keep-Alive]] 续命技巧。

## 缓存断裂检测

Claude Code 监控每次调用的 `cache_read_input_tokens`，如果比上次下降 **>5%** 且绝对值 **>2000 tokens**，判定为断裂，并分析原因：系统提示词变了？工具增减了？TTL 过期了？模型切了？

跟 Ollama "缓存没了你自己猜"形成鲜明对比——Anthropic 在缓存可观测性上投入很重。详见 [[cache-失效陷阱]]。

**经济性：Break-even 分析**：Anthropic 缓存写入收费 1.25×（比标准输入贵 25%），但读取只要 0.10×。盈亏平衡只需 **1.4 次缓存读取**。Agent 场景下系统提示词会被读取数十上百次，ROI 极高。实测数据（论文《Don't Break the Cache》arXiv 2601.06007）：长链路 Agentic 任务在三大平台获得 **41%–80% 成本节省**，TTFT 改善 **13%–31%**。

## 与其他主题的关联

- 谁在受益：[[long-horizon-agent]]——输入/输出 token 比 100:1，几乎所有钱都花在重读已读内容上
- 怎么测量：[[cache-命中率]]——llm-d 团队称之为"生产级 Agent 最重要的单一指标"
- 怎么避免破坏：[[cache-失效陷阱]] / [[稳定前缀-动态后缀]]
- 怎么主动维持：[[cache-keep-alive]]——TTL 内 ping 一下就能续命
- 谁是榜样：[[冻结快照模式]]（Hermes）把系统提示词当照片封存
- Sub-agent 缓存为什么不通：[[subagent-上下文隔离]]
- 跟成本/带宽的关系：[[review-带宽瓶颈]]——AI 时代的瓶颈从写代码移到了 review，而 cache 是 review 链路成本的关键支点
