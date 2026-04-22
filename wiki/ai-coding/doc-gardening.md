---
title: Doc Gardening Agent
tags: [agent, doc-rot, harness-engineering]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex]]"
last-ingested: 2026-04-22
status: draft
---

文档腐烂（doc rot）是所有大型代码库的宿命，在 Agent-First 仓库里更糟——Agent 会基于过期文档继续生产代码，错误以复利速度扩散。**Doc Gardening Agent** 是 OpenAI Codex 团队的解法：定期运行的后台 Agent，**扫描不再反映真实代码行为的过期/废弃文档，自动开 fix-up PR**。

> [!example] 运行机制
> - 定时任务（cron / 后台 Codex）扫描 `docs/` 全量
> - 对每份文档，对照真实代码行为做 diff 检查
> - 发现漂移 → 自动开 PR 修文档
> - 大多数 PR 可以在不到一分钟内 Review 并自动合并

**配套的 Linter + CI Job**：除了 Doc Gardening Agent，还需要专门的 linter 验证知识库的**时效性、交叉引用、结构正确性**——这些机械化检查作为基础设施，Doc Gardening 作为兜底修复，组成两层防线。

**为什么这条工程化是必须的**：在传统团队，文档维护靠"工程师道德"。在 Agent-First 仓库里，这是**Entropy Management 的必要组件**——见 [[harness-成熟度|Harness 三层成熟度]] 的第三层。没有 Doc Gardening，[[agent-可读性|Agent Legibility]] 必然衰减；衰减到一定程度，Agent 就开始"基于幻觉的幻觉"。

**和 [[agents-md|AGENTS.md]] 的协同**：AGENTS.md 是入口，docs/ 是 System of Record，Doc Gardening 是维护 SoR 时效性的工程机制。三者一起才构成可持续运行的 Context Engineering 层。
