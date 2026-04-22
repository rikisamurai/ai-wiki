---
title: KV Cache
tags: [kv-cache, llm-inference]
date: 2026-04-22
sources:
  - "[[sources/inbox/⁠‬⁠​​‬⁠​‍⁠​​​‬​‌​​​​​​⁠﻿​​﻿‬⁠﻿﻿​‬‌⁠​‬﻿⁠⁠​​﻿‌﻿‍‍Prefix Cache：Long Horizon Agent 的效率基石]]"
  - "[[sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token]]"
last-ingested: 2026-04-22
status: stable
---

# KV Cache

> [!note] TL;DR
> 每个 Transformer LLM 推理时都会计算自注意力，每个 token 在每层生成对应的 Key 和 Value 张量。KV Cache 把这些张量缓存下来，生成第 N 个 token 时不用重算前 N-1 个 token——单次请求内部的标配优化，没它生成第 500 个 token 就要对前 499 个全部重新前向传播。

## QKV 三角色：为什么只缓存 K 和 V

注意力公式：`Attention(Q, K, V) = softmax(Q · Kᵀ / √d) · V`

| 角色 | 含义 | 是否能缓存 |
|---|---|---|
| **Q（Query）** | 当前新 token "我要找什么" | ❌ 每次都不同 |
| **K（Key）** | 历史 token 的索引 "我有什么" | ✅ 算完就固定 |
| **V（Value）** | 历史 token 的内容 | ✅ 算完就固定 |

K 和 V 一旦算出就再也不变——这是缓存能存在的前提。

## 这件事可行的根本前提：Decoder-only

当前所有主流大模型（Claude / GPT / Gemini / Llama / Gemma / Qwen）都是 **Decoder-only**——单向注意力，每个 token 只看前面的 token。

```
因果掩码（causal mask）：
       T₁  T₂  T₃  T₄
T₁  ✅  ❌  ❌  ❌
T₂  ✅  ✅  ❌  ❌
T₃  ✅  ✅  ✅  ❌    ← T₃ 的 KV 永远不变
T₄  ✅  ✅  ✅  ✅    ← 新增 T₄ 不影响 T₁₂₃
```

> [!warning] BERT 为什么做不了生成式 AI
> 双向注意力下，加一个新 token 会改变**所有** token 的表示——KV 全废。这就是为什么 Encoder 架构没法做高效生成。

**类比：写作时不重读全文**——每写一个新字，你不需要把前面所有字重新理解一遍，大脑已经把前文的语境"缓存"起来了。KV Cache 做的就是这件事，机制级别。

## 实证：模型越大，缓存收益越大

> [!example] 同一段对话在 Mac 上跑 Gemma 4 vs Qwen3.5（来自 minlibuilds 的本地实验）
> | 模型 | 未命中（Prefill） | 命中（仅读 KV） | 加速比 |
> |---|---|---|---|
> | Gemma 4（4.5B active） | ~25,000ms | ~170ms | **148×** |
> | Qwen3.5（0.8B） | ~566ms | ~173ms | **3.3×** |
> 
> 命中时两个模型几乎同速（都在 3-5K tok/s）——瓶颈从 GPU 计算变成内存读取。**模型越大，KV 计算越昂贵，缓存收益越大。**

这也是为什么 Claude Code（Opus 4.7、Sonnet 4.6 这些大模型）在缓存上做了大量精细工程——参见 [[prefix-cache]]。

## 与 [[prefix-cache|Prefix Cache]] 的边界

KV Cache 解决的是**单次请求内部**的重复计算（Decode 阶段）。Prefix Cache 把复用范围扩展到**多个独立请求之间**（Prefill 阶段）。两者互补：

- KV Cache 始终开启，每个请求独占内存
- Prefix Cache 需要前缀匹配，多请求共享物理块

详细对比见 [[prefix-cache#与 KV Cache 的关系]]。

## 缓存是否无损？

**完全无损。** Transformer 的计算是确定性的，KV 从缓存加载和现场计算的结果**逐 bit 相同**。

但 output token 的 KV 不进 prompt 缓存——每次生成内容不同（temperature > 0），存了也没法复用。不过有个精妙之处：**下一轮对话中，上轮的生成结果被拼回 prompt，变成"输入"的一部分，自然被缓存覆盖**。这就是多轮对话能从 N(N+1)/2 二次增长 → 近似线性增长的根本机制。

## 在 Agent 链路中的角色

对一个跑 40 步工具调用的 [[long-horizon-agent|Long Horizon Agent]] 来说：

- KV Cache 让每一步**内部**生成 token 的过程不退化为 O(n²)
- [[prefix-cache|Prefix Cache]] 让每一步**之间**不重复处理 20K tokens 的系统提示词

少了任何一个，Agent 都跑不动。
