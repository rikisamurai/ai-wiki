---
title: Codex
tags: [codex, openai, agentic-coding]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/codex/Codex Best Practices]]"
last-ingested: 2026-04-23
status: stable
---

Codex 是 OpenAI 的代理式编码环境，与 [[claude-code|Claude Code]] 同属 [[wiki/agent-engineering/philosophy/agentic-coding|Agentic Coding]] 范式——能读文件、跑命令、改代码、做验证。OpenAI 自己用 Codex review 100% 的 PR，是把代码 agent 跑成生产基础设施的少数案例之一。

> [!important] 核心心智：把 Codex 当团队成员，不是助手
> Codex Best Practices 反复强调：**不要每次重新教它项目约定，而是把约定写进 AGENTS.md / Skills / Automations**——一次配置，反复受益。这跟"每次都精心写 prompt"的助手心态正好相反，是 [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]] 在 Codex 上的具体表现。

> [!compare] Codex vs Claude Code 概念对照表
> 两者高度同构，主要差别在术语：
> | Claude Code | Codex | 用途 |
> |---|---|---|
> | CLAUDE.md | [[wiki/agent-engineering/workflow/agents-md\|AGENTS.md]] | 项目级 Agent 备忘录 |
> | `.claude/skills/` | `.agents/skills/` 或 `~/.agents/skills/` | 可复用 [[agent-skills\|Skills]] |
> | `/clear` `/compact` `/resume` | 同名命令 + `/fork` `/agent` | 会话管理 |
> | [[permission-modes\|YOLO/Safe/Plan]] | [[codex-sandbox-approval\|Approval Mode + Sandbox Mode]] | 权限控制（Codex 拆成两个独立维度） |
> | [[plan-mode\|Plan Mode]] | `/plan` 同名 | 探索 → 规划 → 执行 |
> | [[mcp\|MCP]] | MCP（同标准） | 接外部系统 |
> | Hooks | Automations | 触发式工作流 |

**Codex 独有概念**

- **Reasoning Level**：Low（快速）/ Medium（标准）/ High（复杂）/ Extra High（长链 agent 任务）——显式控制推理深度，Claude Code 没有等效物
- **[[codex-sandbox-approval|Sandbox Mode + Approval Mode]]**：把"能改什么"和"何时要确认"拆成两个正交维度
- **[[skills-vs-automations|Skills vs Automations]]**：方法 vs 调度——一个明确的分工原则
- **GitHub 自动 review 集成**：可配置 Codex 自动 review 仓库的所有 PR

> [!example] Codex 的 4 要素 prompt 模板
> Codex 官方推荐的 prompt 结构（与 [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]的 4 要素几乎一致）：
> | 要素 | 说明 |
> |---|---|
> | **Goal** | 你要改变或构建什么 |
> | **Context** | 哪些文件/文档/报错相关，可用 `@<file>` 引用 |
> | **Constraints** | 标准、架构、安全要求 |
> | **Done when** | 任务完成的可观测标志（测试通过 / 行为变化） |
>
> "Done when" 这条等同于 [[wiki/agent-engineering/workflow/验证驱动|验证驱动]]——没有验收标准的任务等于无限探索。

> [!warning] Codex 用户最常踩的 8 个坑
> 1. 把持久规则堆 prompt 而不写进 AGENTS.md
> 2. 没告诉 Codex 怎么跑 build 和 test
> 3. 复杂任务跳过规划阶段
> 4. 不熟悉工作流就给完全权限
> 5. 同一文件多个活跃线程不用 [[wiki/skills/superpowers|git worktree]]
> 6. 工作流不稳定就转 Automations
> 7. 逐步盯着 Codex 跑而不并行干别的事
> 8. 每个项目只用一个线程导致 [[wiki/agent-engineering/context/context-window|context]] 膨胀
>
> 第 8 条是最高频的——参考 [[compact-vs-clear|/clear 时机]]。

**与 Claude Code 的协作**：Codex 可以通过 [[codex-plugin|Codex Plugin for Claude Code]] 接入 Claude Code 当 reviewer 或 rescue 后台，是 [[wiki/agent-engineering/workflow/writer-reviewer-模式|Writer/Reviewer]]模式的产品化。
