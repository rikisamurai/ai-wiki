---
title: Agent 可读性（Legibility）
tags: [harness-engineering, context-engineering, agent]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex]]"
last-ingested: 2026-04-22
status: draft
---

OpenAI Codex 团队的核心设计原则：**从 Agent 的视角看，运行时无法访问的上下文 = 不存在**。Google Docs、Slack 讨论、存在于人脑中的知识——对系统来说都是不可见的。**只有仓库内的、版本化的 artifact（代码、Markdown、Schema、执行计划）才是 Agent 能看到的全部**。把更多上下文推入仓库，就是在为 [[harness-engineering|Harness Engineering]] 扩容。

> [!important] 一句话
> 那个在 Slack 上达成共识的架构决策？如果 Agent 发现不了，就跟三个月后入职的新人不知道一样。

**两层 Legibility**

- **代码可读性**：仓库本身就是 Agent 的"项目说明书"——目录结构、命名约定、文件大小限制都按 Agent 视角优化
- **应用可读性（Application Legibility）**：让运行中的应用对 Agent 可观测——每个 worktree 独立启动、接入 Chrome DevTools Protocol、本地可观测性栈暴露 LogQL/PromQL 查询能力。这样 Prompt "确保服务启动在 800ms 内完成"或"这四个关键用户路径中没有 span 超过 2 秒"才变得可执行

**和 [[agents-md|AGENTS.md]] 的关系**：AGENTS.md 是"门牌"，docs/ 是"档案室"。Legibility 优化的是**整个仓库 + 运行时环境**对 Agent 的暴露面，AGENTS.md 只是其中一块入口。

**和 [[隐性知识与上下文]] 的对偶**：隐性知识强调"不要让 AI 猜你脑子里的事"，Legibility 把这条原则推到极限——不仅要写出来，还要写在 Agent 真能看到的地方。Slack 不行，Google Docs 不行，必须 in-repo + version-controlled。
