---
title: 聊天中途切换模型
tags: [workflow, model-switching, harness]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: draft
---

用户在同一对话里换模型——听起来简单，对 [[per-model-harness|per-model harness]] 的 agent 来说是一组复杂工程问题：要切 prompt、切工具集、注入"中途接手"指令、应对 prefix cache 失效。[[cursor|Cursor]] 把这套都做出来了，但官方建议依然是"**没明确理由就别在中途切**"。

## 三个核心挑战

> [!important] 切模型不是切个 ID
> | 挑战 | 解 |
> |---|---|
> | **新模型对工具集不熟** | 自动加载新模型对应的 prompt + 工具集（[[per-model-harness]]） |
> | **历史是别的模型生成的，分布外** | 注入自定义指令"你是中途从另一个模型接手的"+ 引导避免调对话历史里出现但本模型没有的工具 |
> | **缓存失效** | 新模型的 prefix cache 完全不命中——首轮慢且贵 |

## 缓存失效的代价

> [!warning] 切换瞬间的延迟与成本
> [[wiki/agent-engineering/context/prefix-cache|Prefix cache]] 是 provider × 模型特定的——切到另一个 provider 后整个 prefix 重新算一次。对长对话尤其痛：
> - 5 万 token 的对话，新模型首轮要 prefill 全部
> - 延迟从 2 秒变 20 秒
> - 成本相应放大
>
> Cursor 试过的缓解：**切换时让 LLM 总结当前对话**，给新模型一份摘要再开始。但有缺点——**复杂任务的关键细节会被摘要丢掉**。所以默认不开。

## 推荐解：用 [[subagent-driven-development|子智能体]] 替代切换

> [!tip] 干净起步比中途切换便宜
> Cursor 的最佳实践：**让用户用特定模型起一个 [[subagent-driven-development|子智能体]]**，而不是中途切主对话。
> - 子智能体从全新上下文窗口开始——没有 prefix cache 失效的事
> - 不用注入"我是接手的"指令——它本来就是新会话
> - 不用担心历史里有它不会的工具——历史是干净的
>
> 这跟 [[subagent-上下文隔离|subagent 上下文隔离]] 设计哲学一致：**新任务、新会话、新模型，三者一起切最干净**。

## 跟 [[wiki/agent-engineering/context/cache-失效陷阱|Cache 失效陷阱]] 的关系

中途切模型本身就是 cache 失效陷阱的一个具体场景。其它常见触发：
- 系统 prompt 里有动态时间戳/计数器
- 用户加的附件改变了 prefix
- harness 升级换了 system prompt 模板

每一类都让 prefix cache 命中率掉到 0%。中途切模型是其中**最干脆**的一种——直接换模型 = 直接换 cache namespace。

## 不是所有切换都是中途切

> [!compare] 三种切模型场景
> | 场景 | 是否中途切 | 推荐做法 |
> |---|---|---|
> | 新会话指定模型 | 否 | 直接选 |
> | 中途用子智能体跑特定模型 | 否 | Cursor 推荐姿势 |
> | 中途主对话切模型 | **是** | 谨慎使用，理解延迟/成本代价 |
>
> 第三种是这页主题。前两种没有这些问题。

## 跨工具实现差异

- **[[cursor|Cursor]]**：完整支持中途切换 + 自定义指令
- **[[claude-code|Claude Code]]**：主要走 Anthropic，模型间切（Sonnet ↔ Opus）成本低，没切 provider 那种问题
- **[[codex|Codex]]**：单 provider（OpenAI），无切换问题
- **[[gstack|gstack]]**：跨工具但每个 host 内一般用其默认模型，少在 chat 内切换

## 关联

- 范式根因：[[per-model-harness]]
- 缓存代价：[[wiki/agent-engineering/context/prefix-cache|Prefix Cache]]、[[wiki/agent-engineering/context/cache-失效陷阱|Cache 失效陷阱]]、[[wiki/agent-engineering/context/cache-命中率|Cache 命中率]]
- 替代方案：[[subagent-driven-development]]、[[subagent-上下文隔离]]
- 同类摘要权衡：[[wiki/agent-engineering/context/compact-vs-clear|Compact vs Clear]]——切换时摘要 vs 重起会话
- 上游工具：[[cursor]]
