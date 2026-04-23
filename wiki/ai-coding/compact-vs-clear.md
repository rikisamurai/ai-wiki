---
title: Compact vs Clear
tags: [session-management, compaction, claude-code]
date: 2026-04-22
sources:
  - "[[sources/inbox/使用 Claude Code：会话管理与 100 万 上下文【译】]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-22
status: stable
---

# Compact vs Clear

> [!note] TL;DR
> 给一个超长会话"减负"有两条路：`/compact` 让 Claude 把历史压成摘要继续干活；`/clear` 直接抛掉所有上下文重新开始，由你写交接说明。**前者省力但有损（Claude 决定保留什么）；后者费劲但精确（你决定保留什么）**。两者用在不同场景，没有谁绝对更好。

## 操作差异

> [!compare] 两条路径对比
> | 维度 | `/compact` | `/clear` |
> |---|---|---|
> | 谁决定保留什么 | Claude（有损） | 你自己写 |
> | 起手成本 | 一条命令 | 要写一段交接 |
> | 上下文残余 | 摘要 + 之后的对话 | 100% 你写的内容 |
> | [[prefix-cache\|Prefix Cache]] 影响 | 消息历史变了→断裂 | 完全冷启动 |
> | 适合场景 | 还想沿着原方向继续 | 任务换了 / 上下文已经污染严重 |

## /compact 的有损本质

`/compact` 让模型把目前的对话总结为摘要，然后**用摘要替换冗长的历史记录**。Claude 自己决定什么该保留、什么可以丢。

> [!tip] 给 compact 下指令
> 你可以掌控压缩方向，比如：
> ```
> /compact 将重点放在身份验证模块的重构上，丢掉那些关于测试调试的内容
> ```
> 这能避免 Claude 自作主张丢掉你接下来要用的信息。

## /compact 翻车的典型场景

> [!warning] 模型压缩时智商最不在线
> 自动 compaction 触发时，窗口已经撑到极限——这正是 [[context-rot|Context Rot]] 最严重的时候。让一个被噪声淹没的模型判断"什么重要"，会丢掉关键信息。

经典翻车：

```
前面 2 小时调试 foo.ts 的一个 bug
（顺便看到 bar.ts 有个待修的 warning，没动）
触发自动 /compact，摘要全在讲 foo.ts 怎么修的
↓
你：现在把 bar.ts 那个 warning 也修了
↓
Claude："请问是哪个 warning？我没看到。"
（bar.ts 的 warning 在压缩时被当无关内容扔了）
```

应对方法：

1. **主动 /compact**，在窗口还有空间、模型还清醒时手动触发
2. **带指令**，明确告诉它接下来要做什么、什么必须保留
3. 100 万 token 的真正价值在这里：**有充裕空间提前 compact**，不必等到爆满才动手

**/clear 的精确性优势**：`/clear` 后你自己写新会话的交接说明，比如：

```
我们正在重构身份验证的中间件
当前限制条件：X、Y
关键文件：A、B
已经排除了方法 Y
请基于这些信息继续，不需要再读一遍历史代码
```

费劲，但产生的新上下文**百分百是你认为相关的精华**。没有 Claude 自作主张的取舍。

**"从这里开始总结"——介于两者之间**：`summarize from here` 功能让 Claude 自己生成一段交接说明，让"刚踩了坑的未来版 Claude，给过去那个还没开始的自己留张字条"。然后你拿这段总结去 [[会话管理动作|/clear]] 开新会话。这是 compact 的精确性 + clear 的干净性的组合。

## 源码层的三层压缩实现

`/compact` 不是单一动作，而是 Claude Code 内部的**三层压缩流水线**——按代价从低到高依次尝试：

| 层 | 触发 | 做了什么 | 代价 |
|---|---|---|---|
| **微压缩** | 旧工具结果失效 | 把"10 分钟前读的文件"替换成 `[Old tool result content cleared]`；提示词和对话主线完全保留 | 几乎为零 |
| **自动压缩** | token 达到窗口的 **87%**（窗口大小 - 13K buffer） | 主动收缩历史 | 中等 |
| **完全压缩** | 自动压缩仍不够 | LLM 对整段对话生成摘要替换历史 | 一次完整 LLM 调用 |

完全压缩有**熔断器**：连续 3 次失败后停止尝试，避免死循环。生成时还有严厉前置指令 `CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.`——确保压缩这一步不会"顺手"再触发工具调用浪费 turn。

压缩后的 token 预算（写死在源码里的 budget）：
- 文件恢复：50,000 tokens
- 单文件上限：5,000 tokens  
- 技能内容：25,000 tokens

> [!tip] 在 CLAUDE.md 里写 Compact Instructions
> 默认压缩算法会把早期 Tool Output 和文件内容优先删掉，连带丢失架构决策。在 [[wiki/aigc/claude-code-memory|CLAUDE.md]] 中写明压缩优先级，强制保留关键信息：
> ```markdown
> ## Compact Instructions
> When compressing, preserve in priority order:
> 1. Architecture decisions (NEVER summarize)
> 2. Modified files and their key changes
> 3. Current verification status (pass/fail)
> 4. Open TODOs and rollback notes
> ```
> 这是 compact 自动机制的"配置层"。手动机制是 [[wiki/aigc/handoff-md|HANDOFF.md]]——任务进入新阶段时，让 Claude 把进度写进文件再 `/clear`。

## 关联

- 上层概念：[[context-window]] / [[context-rot]] / [[会话管理动作]]
- 缓存层影响：[[cache-失效陷阱]]——/compact 会破坏缓存链
- 替代方案：[[rewind-胜过纠正]]（点准时机回退） / [[subagent-上下文隔离]]（事先隔离）
