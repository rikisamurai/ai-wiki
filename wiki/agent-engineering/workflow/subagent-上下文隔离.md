---
title: Subagent 上下文隔离
tags: [subagent, context-management, claude-code]
date: 2026-04-22
sources:
  - "[[sources/inbox/使用 Claude Code：会话管理与 100 万 上下文【译】]]"
  - "[[sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
  - "[[sources/posts/aigc/ai-coding/tools/Superpowers - AI 编码工作流框架]]"
last-ingested: 2026-04-23
status: stable
---

# Subagent 上下文隔离

> [!note] TL;DR
> 子智能体是一种管理 [[context-window|上下文窗口]] 的绝佳手段：派一个**有自己崭新上下文窗口**的子 agent 去干活，等它做完只把最终报告交还给主 Claude。**判断该不该用的"灵魂拷问"**：以后我还需要看这些工具运行的详细输出吗，还是只想要一个最终结论？答案是后者，就派 subagent。

## 工作原理

```
主线程 Claude (你的会话)
   │
   │  "派一个 subagent 去做 X"
   ↓
[ Subagent (全新 context window) ]
   │
   │  自由折腾：读 50 个文件、跑 30 次 grep、试 10 种方案
   ↓
   只把最终结论 (一段文字) 返回主线程
   │
   ↓
主线程 Claude  ← 上下文只增加了"那段结论"，中间垃圾全留在 subagent 里
```

## 三种典型用法

> [!example] 主动指派的姿势
> - **验证已完成的工作**：
>   "派个 subagent 去，根据下面这份规范文件，验证一下我们刚才做的工作对不对"
> - **跨代码库学习实现**：
>   "派个 subagent 去通读另一个代码库，总结它是怎么实现身份验证流程的，然后你照猫画虎在这边也实现一遍"
> - **生成附属产出**：
>   "派个 subagent 去，根据我的 Git 修改记录，给这个新功能写份说明文档"

共同特征：**中间过程会产生大量"阅后即焚"的内容**——读了的文件、跑过的 grep、试过的草稿——这些不该进主线程上下文。

## 跟其他动作的对比

| 动作 | 适合场景 |
|---|---|
| Continue | 任务连续，没有"阅后即焚"的中间产物 |
| [[rewind-胜过纠正\|Rewind]] | 已经踩过坑，要回到干净节点 |
| [[compact-vs-clear\|/compact]] | 历史还有用但太长 |
| [[compact-vs-clear\|/clear]] | 任务换了，从头开始 |
| **Subagent** | **预知**某段任务会产生大量噪声 |

Subagent 的独特价值是 **"预防式上下文管理"**：在噪声进入主线程之前就把它隔离掉，事后不需要清理。

## 缓存代价：几乎不复用主线程缓存

> [!warning] 每个 subagent ≈ 一次"迷你冷启动"
> Subagent 跟主线程几乎共享不到任何 [[prefix-cache|Prefix Cache]]：
> 
> - **工具集不同**：主线程有全套工具（Read/Write/Edit/Bash/Agent…），Explore subagent 只有子集（Read/Grep/Glob/Bash）
> - **消息历史完全独立**：subagent 没有主线程的对话上下文
> - **可能用不同模型**：subagent 可能用 Haiku（更便宜），主线程用 Opus
> 
> 任何一项不同，缓存链就断了。Sub-agent 启动等于一次冷启动——所以 Claude Code 不滥用 subagent，简单的文件搜索直接用 Grep / Glob 就行。

源码层面，Claude Code 的缓存状态是按 `querySource + agentId` 分开追踪的——每个 agent 有自己**独立的缓存链**。这不是疏忽，是设计：sub-agent 的工具集 / 历史 / 模型都可能不同，强行共用缓存反而会引发 [[cache-失效陷阱|失效检测]] 报警。

## 在 CLAUDE.md 里写 "多用 agent 并行" 之前

要意识到每个 agent 都有独立的缓存开销。"多用 agent 并行"在以下场景才划算：

- 任务真的能并行（依赖图允许）
- 每个 agent 的产出价值 >> 它的冷启动 + 调用开销
- 主线程上下文确实容不下这么多中间结果

否则不如直接用工具或主线程做。

## 源码层：「你是工人不是经理」

为防止子 Agent 又生成子 Agent 引发递归爆炸，Claude Code 在每个 fork worker 启动时硬编码了一段约束 prompt：

```
STOP. READ THIS FIRST.
You are a forked worker process. You are NOT the main agent.
RULES (non-negotiable):
1. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps
3. USE your tools directly: Bash, Read, Write, etc.
4. Keep your report under 500 words.
5. Your response MUST begin with "Scope:". No preamble.
```

这是 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 能成立的前提——**经理只能有一个**这条不变量靠 prompt 强制注入到每个 worker。同时还有一个缓存优化的副产品：所有 fork worker 的工具结果统一替换成占位符 `'Fork started — processing in background'`，使 N 个并行 worker 的前缀完全一致，**只有第一个冷启动，后面 N-1 个直接命中缓存**。

## "你是工人不是经理"约束

源码里 sub-agent 启动时被注入硬约束 prompt，防止递归生成更多 sub-agent：

```
STOP. READ THIS FIRST.
You are a forked worker process. You are NOT the main agent.
RULES (non-negotiable):
1. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps.
3. USE your tools directly: Bash, Read, Write, etc.
4. Keep your report under 500 words.
5. Your response MUST begin with "Scope:". No preamble.
```

**经理只能有一个**这个不变量是写在 prompt 而非代码里的——因为它需要被模型理解才能遵守。这与 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 的"主控分发"配套使用：主 Agent 是经理，所有 sub-agent 强制成为 worker。

## 缓存优化的占位符技巧

为了让多个并发 sub-agent 能命中相同缓存前缀，Claude Code 让所有 fork 子代理的工具结果使用**同一个占位符文本**：

```
'Fork started — processing in background'
```

10 个 sub-agent 前缀完全一致 → 只有第 1 个冷启动，剩下 9 个直接命中缓存。这是"为什么 Coordinator 模式的并行成本不会线性增长"的具体实现。

## 关联

- 上层概念：[[context-window]] / [[会话管理动作]] / [[context-rot]]
- 替代方案：[[compact-vs-clear]] / [[rewind-胜过纠正]]
- 缓存层细节：[[prefix-cache]] / [[cache-失效陷阱]]
- 编排模式：[[wiki/agent-engineering/workflow/coordinator-模式]]
- 极致用法：[[subagent-driven-development]]（计划里每个 task 都派一个 subagent）
