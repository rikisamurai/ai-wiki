---
title: Claude Code
tags: [claude-code, agentic-coding, tool]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
last-ingested: 2026-04-22
status: draft
---

Claude Code 是 Anthropic 出品的**代理式编码环境**（agentic coding environment）：不只回答问题，而是能主动读文件、跑命令、改代码、自我验证。它把 [[wiki/ai-coding/agentic-coding|Agentic Coding]] 范式做成了具体工具，核心约束只有一句话——**[[wiki/ai-coding/context-window|上下文窗口]] 是最稀缺的资源**。

> [!important] 一切最佳实践都在解一个问题
> Claude Code 的所有实践（验证驱动 / Plan Mode / Hooks / Subagent / Skills / 会话管理）本质上都在回答同一个问题：**如何在有限的上下文窗口里塞进高密度信息、避免噪声、让 Claude 自我闭环**。理解这一点，就能从一堆功能列表里看出主线。

**七大主题**

| 主题 | 关键页面 | 核心思想 |
|---|---|---|
| **验证闭环** | [[wiki/ai-coding/验证驱动\|验证驱动]] / [[wiki/ai-coding/探索-规划-编码-验证\|四阶段工作流]] | 提供测试/截图/预期输出，Claude 才能自我闭环 |
| **上下文管理** | [[wiki/ai-coding/会话管理动作\|五个会话动作]] / [[wiki/ai-coding/两次纠正规则\|两次纠正规则]] | Continue/Rewind/Clear/Compact/Subagent 的决策矩阵 |
| **Memory 体系** | [[claude-code-memory\|CLAUDE.md+rules+auto]] | 跨会话持久化的三层结构 |
| **扩展机制** | [[agent-skills\|Skills]] / [[hooks\|Hooks]] / [[mcp\|MCP]] / Subagents / Plugins | 把工具能力按需注入 Claude |
| **权限与安全** | [[permission-modes\|权限模式]] / [[plan-mode\|Plan Mode]] | YOLO / Safe / Plan 三档收紧 |
| **协作模式** | [[wiki/ai-coding/writer-reviewer-模式\|Writer/Reviewer]] / [[wiki/ai-coding/采访驱动-spec\|采访驱动 SPEC]] | 多会话并行、Claude 反向采访你 |
| **自动化** | 非交互模式 `claude -p` | CI/pre-commit/批处理 |

> [!compare] 在哪个层做扩展，怎么选
> | 需求 | 用什么 | 为什么 |
> |---|---|---|
> | 必须每次都执行、零例外（如 lint） | [[hooks\|Hooks]] | 确定性强制 |
> | 给项目级约定（如代码风格） | [[claude-code-memory\|CLAUDE.md]] | 每次会话加载 |
> | 给特定文件类型规范 | [[claude-rules\|.claude/rules/]] | 路径匹配按需加载 |
> | 给可复用领域知识 / 工作流 | [[agent-skills\|Skills]] | 相关时自动应用 |
> | 委派隔离任务 | [[wiki/ai-coding/subagent-上下文隔离\|Subagent]] | 独立上下文 + 工具权限 |
> | 接外部系统（Notion/Figma/DB） | [[mcp\|MCP]] | 标准协议 |

> [!tip] 反模式自查
> 文档列了 5 个高频反模式：**大杂烩会话**（任务间不 `/clear`）、**反复纠正**（→ [[wiki/ai-coding/两次纠正规则|两次纠正规则]]）、**臃肿的 CLAUDE.md**（→ [[claude-code-memory|200 行经验法则]]）、**信任-验证缺口**（→ [[wiki/ai-coding/验证驱动|验证驱动]]）、**无限探索**（→ [[wiki/ai-coding/subagent-上下文隔离|用 subagent]]）。每条反模式都对应一个最佳实践页面，不是孤立现象。

**与 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 的关系**：Claude Code 是 [[wiki/ai-coding/harness-成熟度|Harness 三层成熟度]]里 **L2 Context Engineering** + **L3 Workflow Automation** 的具体实现——CLAUDE.md/rules 管上下文、Hooks/Skills/Subagents 管工作流。
