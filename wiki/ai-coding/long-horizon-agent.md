---
title: Long Horizon Agent
tags: [long-horizon-agent, agentic-coding]
date: 2026-04-22
sources:
  - "[[sources/inbox/⁠‬⁠​​‬⁠​‍⁠​​​‬​‌​​​​​​⁠﻿​​﻿‬⁠﻿﻿​‬‌⁠​‬﻿⁠⁠​​﻿‌﻿‍‍Prefix Cache：Long Horizon Agent 的效率基石]]"
last-ingested: 2026-04-22
status: stable
---

# Long Horizon Agent

> [!note] TL;DR
> Long Horizon Agent 指能在单次任务中执行 **30–50 步甚至更多工具调用**的 AI 系统：深度研究 Agent、代码 Agent、跨系统工作流自动化。和简单 Agent 的根本区别在于——每一步工具调用后，模型要处理的上下文持续增长（系统提示词 + 全部历史操作 + 全部工具返回结果），所以输入/输出 token 比常常超过 **100:1**。

## 它属于 [[agentic-coding|Agentic Coding]] 的哪一档

参考 [[agentic-coding]] 中的能力光谱：Long Horizon Agent 处于**最右端**——人类只在任务起点和终点出现，中间几十步全部自主决策。这也是为什么它对基础设施（[[prefix-cache]]、上下文管理、错误恢复）的依赖远高于一次性 LLM 调用。

## 没有 [[prefix-cache|Prefix Cache]] 时的成本结构 💸

典型场景：系统提示词 20,000 tokens，任务执行 40 步，平均每步新增 500 tokens。

不开 Prefix Cache：

```
第1步：20,000 tokens 完整 Prefill
第2步：20,500 tokens 完整 Prefill   ← 全部重读
...
第40步：39,500 tokens 完整 Prefill
总输入：约 1,190,000 tokens
```

Claude Sonnet 4.6 单价 $3/M，**单次任务约 $3.57**。1000 用户 × 每天 5 次 = **$17,850/天**，月度 **$535,500**——这个数字直接决定 Agent 能不能上生产。

开了 Prefix Cache（90% 命中）后：约 **$0.68/任务**，节省 81%。从"睡不着觉"变成"可以投了"。

## 延迟：用户等的不是回复，是模型在重读课本 📖

每步工具调用后，模型若没有 Prefix Cache 就要把整本"课本"从头翻到尾。30K tokens 的上下文在标准 GPU 上一次重读要 **10–16 秒**。40 步任务，每步等 10 秒，用户对着 loading 动画干瞪眼。

llm-d 分布式调度的实测：启用 Cache-Aware Routing 后，P90 TTFT 从 **31 秒降到 0.54 秒**，57 倍提升。

## 上下文增长是核心特征，不是 bug

Long Horizon Agent 的上下文不会"压缩到一个固定大小"——历史是它的工作记忆。这就把它和 [[prefix-cache]]、[[cache-命中率]]、[[稳定前缀-动态后缀]] 紧紧绑在一起：上下文越长，缓存命中率越是决定生死的指标。

参见 [[review-带宽瓶颈]]：当 LLM 把"写"的成本砍到接近零，"读/审"的成本就成为瓶颈——同样的逻辑也作用在模型自己身上。
