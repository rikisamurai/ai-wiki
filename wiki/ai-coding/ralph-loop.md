---
title: Ralph Loop
tags: [agent, long-horizon, pattern]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
last-ingested: 2026-04-22
status: draft
---

Ralph Loop 是应对长程任务（跨天甚至跨周的重构、迁移）的一种工程模式：**用一个外部循环反复重启 AI Agent**（如 Claude Code），把每次的进度和状态持久化到 `progress.txt` 和 `git commit` 里。它绕开了 [[context-window|上下文窗口]]无限增长带来的性能衰减与成本爆炸，同时保证任务可中断、可恢复。

> [!example] 典型循环
> ```
> while task_not_done:
>   start fresh agent session
>   agent reads progress.txt
>   agent picks the next subtask
>   agent runs tests, commits
>   agent appends progress.txt
> ```

**适用场景**：[[long-horizon-agent|长程 Agent]] 任务，且约束完备（测试用例、Lint、CI 都齐备）——程序员退化为监控者，偶尔介入解决死循环。这类任务在 [[任务三维划分]] 里属于"长程强约束"。

**为什么有效**：单次会话的上下文与 [[compact-vs-clear|compact/clear]] 都有边际收益递减。把 session 当成短命计算单元，让"持久化产物"（git commit、文件状态）来承载长程语义，效率显著高于堆长 context。

相关：[[harness-engineering]]、[[prefix-cache]]
