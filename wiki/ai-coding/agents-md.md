---
title: AGENTS.md
tags: [context-engineering, agent, project-config]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
  - "[[sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex]]"
last-ingested: 2026-04-22
status: draft
---

AGENTS.md（在 Claude Code 体系里也叫 CLAUDE.md）是项目级的"备忘录"，给 Agent 提供**只能从代码外部得到的关键信息**——部署架构、核心实体关系、团队约定。它的价值不在内容多寡，而在**信息密度**。

> [!warning] ETH Zurich 138 agentfile 实验
> 实验测试了 138 个 agentfile：**LLM 自动生成的 agentfile 反而损害 Agent 表现**，代价是额外 +20% token 消耗；**人工编写的 agentfile 平均提升只有约 4%**。
>
> 结论：不要让 AI 帮你写 AGENTS.md，也不要把它写成百科全书。低密度内容是负债不是资产。

**该写什么**

- **项目部署架构**：各环境、各集群的角色与交互方式（这种信息散落在配置和 wiki，AI 难以拼起来）
- **核心概念与关系图**：用最简洁的图或文字定义项目核心实体及关系，确保人和 AI "频道一致"
- **不成文约定**：团队习惯但代码注释里没写的规则（命名习惯、目录划分逻辑、为什么不用某个库）

**不该写什么**

- 任何 grep 一下就能找到的事实（接口签名、配置项列表）
- 任何会随代码演进而过期的快照（依赖版本、模块列表）
- 任何鼓励 AI 走捷径的"建议"（"如果不确定就用 X"——这是把人的犹豫转嫁给 AI）

这与 [[隐性知识与上下文]] 是同一回事：低信噪比的上下文比没有更糟。AGENTS.md 是 [[harness-engineering|Harness Engineering]] 三层成熟度框架里 [[harness-成熟度|Context Engineering 层]]的载体之一。

> [!tip] OpenAI Codex 团队的实证：AGENTS.md 是目录而非百科全书
> 他们尝试过"一个巨大的 AGENTS.md"并可预见地失败了——Context 是稀缺资源、什么都重要 = 什么都不重要、立刻腐烂、难以验证。最终方案：**`AGENTS.md` 只做入口（~100 行），主要是指向深层知识源的指针；真正的 System of Record 放在结构化的 `docs/` 目录里**（design-docs / exec-plans / product-specs / references）。这与 ETH 的实验数据完全一致，也是 [[渐进式披露]] 在项目根目录这一层的具体落地。
