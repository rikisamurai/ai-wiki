---
title: Agent 工作量分布（90% 在 AI 之外）
tags: [agentic-coding, architecture, harness]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-23
status: draft
---

[[claude-code|Claude Code]] 51 万行源码里，**真正调用 LLM API 的部分可能不到 5%**。其余 95% 是脚手架——安全检查、权限系统、上下文管理、错误恢复、多 Agent 协调、UI 交互、性能优化。这条统计揭示了一条工程定律：**做 AI Agent 产品，模型只是冰山一角**。

> [!compare] Claude Code 51 万行的成分构成
> | 类别 | 典型占比 | 例 |
> |---|---|---|
> | **安全检查** | ~5% | BashTool 单工具就有 18 个安全文件 / 9 层审查 |
> | **权限系统** | ~5% | allow/deny/ask/passthrough 四态 + 200ms 防误触 |
> | **上下文管理** | ~10% | 三层压缩 + AI 检索记忆 |
> | **错误恢复** | ~5% | 熔断器 + 指数退避 + Transcript 持久化 |
> | **多 Agent 协调** | ~10% | 蜂群编排 + 邮箱通信 |
> | **UI 交互** | ~30% | 389 个 React 组件 + IDE Bridge |
> | **性能优化** | ~10% | Prompt cache 稳定性 + 启动时并行预取 |
> | **工具实现** | ~20% | 53+ 个工具 |
> | **真正调用 LLM** | <5% | API 客户端 + 流式解析 |

> [!important] 对 AI Agent 开发者的启示
> **不是模型够不够聪明，是你的脚手架够不够结实**。这条与 [[harness-engineering|Harness Engineering]] 的核心论断完全一致——决定 Agent 上限的不是 prompt，而是它的运行环境。

**为什么是这个比例**

Agent 与 ChatBot 的根本差别在副作用范围：ChatBot 只输出文字，Agent 会**改你的文件、跑你的命令**。每一种副作用都需要：

1. **审查**——这个动作安全吗
2. **权限**——用户授权了吗
3. **回滚**——出错怎么办
4. **审计**——谁做了什么、为什么

四件事每一件都不能让模型"自由发挥"——必须在外面写硬代码。结果就是 95/5 的工作量分布。

**与 [[harness-成熟度|Harness 三层成熟度]]的对应**

| Harness 层 | Claude Code 里的具体实现 | 占代码量 |
|---|---|---|
| **L1 Prompt** | `prompts.ts` + 各 tool 的 `prompt.ts` | <5% |
| **L2 Context Engineering** | CLAUDE.md / Skills / 三层压缩 / KAIROS 记忆 | ~25% |
| **L3 Workflow Automation** | 工具系统 / Hooks / Subagents / Coordinator | ~70% |

L3 才是大头——这与"Vibe Coding 阶段堆 prompt 没用"的经验完全自洽。

**OS 类比是字面意义的**

Claude Code 把传统 OS 概念几乎一一映射了：

| 传统 OS | Claude Code |
|---|---|
| 系统调用 | 53+ 工具 |
| 用户权限管理 | 权限四态系统 |
| 应用商店 | [[wiki/aigc/agent-skills\|Skills]] |
| 设备驱动 | [[wiki/aigc/mcp\|MCP]] |
| 进程管理 | [[wiki/aigc/coordinator-模式\|Agent 蜂群]] |
| 内存管理 | [[wiki/ai-coding/compact-vs-clear\|上下文压缩]] |
| 文件系统 | Transcript 持久化 |

不是比喻——是同一种"管理资源 + 协调多任务 + 强制安全边界"的工程。这也是为什么 Anthropic 自己把 Claude Code 称为 **agent 时代的操作系统**而不是"AI 编程助手"。
