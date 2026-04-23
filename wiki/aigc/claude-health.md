---
title: claude-health（六层架构审计 Skill）
tags: [claude-code, audit, skill]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/tools/some-skills]]"
last-ingested: 2026-04-23
status: draft
---

claude-health 是 tw93 做的开源 Skill，把 [[claude-code-六层架构|六层架构]]（CLAUDE.md → rules → skills → hooks → subagents → verifiers）变成一个**可自动运行的诊断工具**。运行 `/health` 后并行跑 2 个诊断 agent，输出按优先级排序的修复报告。这是少数把"审计自己的 Claude Code 配置"工程化的工具。

> [!important] 它解决了什么问题
> Claude Code 配置随时间会**累积熵**：CLAUDE.md 越写越长、skills 越装越多、hooks 配了忘了改、规则同一件事在 3 个地方都说一遍。靠人工很难发现这些问题。claude-health 把六层架构每一层的**反模式清单**做成自动检查——本质是把 [[wiki/ai-coding/lint|AI 写 Lint]] 的思路用在 Claude Code 配置上。

> [!compare] 6 层 + 横切关注的检查项
> | 层级 | 检查项 |
> |---|---|
> | **CLAUDE.md** | 信噪比、缺 Verification/[[compact-vs-clear\|Compact Instructions]]、散文冗余 |
> | **rules/** | 语言规则放置、覆盖缺口 |
> | **skills/** | 描述 token 数、触发清晰度、auto-invoke 策略 |
> | **skill 安全性** | Prompt 注入、数据泄露、危险命令、硬编码凭证 |
> | **hooks** | Pattern 字段、文件类型覆盖、过期条目 |
> | **MCP** | Server 数量、token 开销估算、上下文压力 |
> | **Prompt Cache** | 动态时间戳、工具重排、会话中途切模型 |
> | **三层防御** | 关键规则是否同时被 CLAUDE.md + Skill + Hook 覆盖 |

**3 档优先级输出**

- 🔴 **Critical** —— 立即修：规则违反、危险权限、缓存破坏、MCP 开销 >12.5%、安全问题
- 🟡 **Structural** —— 尽快修：内容错放、缺 hooks、单层关键规则
- 🟢 **Incremental** —— 锦上添花：上下文卫生、HANDOFF.md 采用、skill 调优

> [!tip] MCP 开销 >12.5% 这条标准
> claude-health 用 12.5% 作为 MCP 占 [[wiki/ai-coding/context-window|context]] 开销的红线——超过就提示拆分。这个数字不是凭空来的：Anthropic 自己测过 5 个 MCP server 平均吃 25K tokens，超过窗口的 12.5% 就开始挤占代码本身的空间。**这是 [[mcp|MCP 隐性成本]]最具操作性的量化标准**。

**安装**

```bash
# 推荐：npx skills
npx skills add tw93/claude-health

# 或 Claude Plugin
claude plugin marketplace add tw93/claude-health
claude plugin install health
```

会话中跑 `/health` 即可。

> [!example] 怎么把审计结果用起来
> 输出报告本身只是开始。真正有价值的是建立一个 cadence：
> 1. **新建项目**：装好后立刻跑一次，建立基线
> 2. **每周一次**：跟踪 Critical/Structural 是否清零
> 3. **改完 CLAUDE.md / skills 后**：跑一次确认没引入新反模式
>
> 把 `/health` 自己也接进 [[hooks|hooks]] 的 `Stop` 事件——会话结束时静默跑一次，是 [[skills-vs-automations|Skill → Automation 升级]]的一个具体案例。

**关联**：[[claude-code-六层架构|Claude Code 六层架构]]（理论基础） / [[hooks|Hooks]] / [[wiki/aigc/auto-memory|Auto Memory]]（health 的检查项之一） / [[wiki/aigc/mcp|MCP]]（开销估算）
