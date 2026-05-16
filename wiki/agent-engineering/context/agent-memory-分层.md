---
title: Agent 记忆四分层
tags: [memory, context, agent-engineering]
date: 2026-05-16
sources:
  - "[[sources/clippings/你不知道的 Agent：原理、架构与工程实践]]"
last-ingested: 2026-05-16
status: draft
---

Agent 不具备原生的时间连续性——会话结束后上下文随之清空。跨会话一致性需要独立设计记忆层，这是基础设施，不是可以事后补上的能力。记忆的四种类型按"解决什么问题"而非"存储介质"来划分。

## 四种记忆

> [!note] 工作记忆 — 上下文窗口
> **当前任务所需的最小信息**，存在于 `messages[]`，随会话结束清空。Token 有限，需主动管理（见 [[context-rot|Context Rot]]）。

> [!note] 程序性记忆 — Skills
> **"怎么做某件事"的操作流程和领域规范**。文件按需加载，不默认常驻上下文，避免消耗 token 预算。描述符常驻、完整内容触发时再注入（见 [[skills/skill-编写实践|Skill 编写实践]]）。

> [!note] 情景记忆 — JSONL 会话历史
> **发生了什么**。磁盘持久化，支持跨会话检索。保留完整过程，可以"回到历史文件里检索"而不是依赖摘要。

> [!note] 语义记忆 — MEMORY.md
> **Agent 主动写入认为重要的稳定事实**，每次启动时注入系统提示。不是所有信息都进 MEMORY.md——只沉淀在未来会话中仍有价值的事实。

## 整合触发与回退

记忆整合应有可回退机制，不能是不可恢复的硬截断：

1. **触发阈值**：`tokenUsage / maxTokens >= 0.5` 时触发整合
2. **成功路径**：对待整合消息做 LLM 摘要 → 追加到 MEMORY.md → 更新 `lastConsolidatedIndex`
3. **失败路径**：把原始消息写入 `archive/` → 保留完整历史，整合失败后仍可回到存档继续

**最关键的不是摘要写得漂亮，而是流程可回退**：系统只移动指针，不删除原始消息。

## 与 ChatGPT / OpenClaw 的实现对比

> [!compare] 两种产品实现
> **ChatGPT 四层**（不用向量数据库）：Session Metadata（不持久化）→ User Memory（约 33 条偏好事实，持久化）→ Conversation Summary（约 15 条轻量摘要，持久化）→ Current Session（滑动窗口）
>
> **OpenClaw 混合检索**：`memory/YYYY-MM-DD.md`（追加写日志）+ `MEMORY.md`（Agent 主动维护的精选事实）+ `memory_search`（70% 向量相似度 + 30% 关键词权重）

对大多数 Agent 而言，结构化 Markdown 加关键词搜索已经足够。只有当记忆库规模超过几千条且确实需要语义相似度检索时，再引入向量存储。

## 相关页面

- [[context/context-rot|Context Rot]] — 工作记忆的衰减问题
- [[claude-code/claude-code-memory|Claude Code Memory]] — Claude Code 的具体记忆实现
- [[skills/skill-编写实践|Skill 编写实践]] — 程序性记忆的工程化方式
- [[workflow/long-horizon-agent|Long Horizon Agent]] — 跨 session 任务对记忆整合的依赖
