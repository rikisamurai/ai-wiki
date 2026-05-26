---
title: Matt Pocock Skills
tags: [skills, workflow, framework]
date: 2026-05-26
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Matt Pocock Skills - 人类满分工程师的自我蒸馏]]"
last-ingested: 2026-05-26
status: draft
---

Matt Pocock（TypeScript 教育者）整理的开源 [[wiki/skills/agent-skills|Agent Skills]] 集，GitHub 已 10.4 万 Stars，把数十年软件工程方法论（DDD、XP、TDD、敏捷）蒸馏成 AI 时代可执行的 Skill 命令。和 [[wiki/skills/superpowers|Superpowers]] 同属"反 [[wiki/agent-engineering/philosophy/vibe-coding|vibe coding]]、强工程纪律"流派，但更偏个体工程师日常工作流，而不是完整流水线 SOP。

> [!abstract] 它解决的核心问题
> Matt Pocock 把 AI 编码的失败归到四个根因——**需求没说清、没有共享词汇、没有反馈信号、不抗熵增**——并为每个根因配一个或多个 Skill 命令。整套定位是"工程经验压缩包"，不是 vibe coding 工具。

## 四大挑战 ↔ Skill 映射

| 根因 | 对应 Skill | wiki 页面 |
|------|-----------|-----------|
| 需求对齐：AI 与人的沟通鸿沟 | `/grill-me` `/grill-with-docs` | [[wiki/agent-engineering/workflow/采访驱动-spec\|采访驱动 SPEC]] |
| 领域语言：AI 不懂行话 | `CONTEXT.md` + `/grill-with-docs` | [[wiki/agent-engineering/workflow/context-md-词汇表\|CONTEXT.md 词汇表]] |
| 反馈循环：AI 盲飞 | `/tdd` `/diagnose` | [[wiki/agent-engineering/workflow/tdd-red-green-refactor\|TDD 红绿重构]]、[[wiki/agent-engineering/workflow/diagnose-debug-循环\|diagnose 调试循环]] |
| 代码质量：[[wiki/agent-engineering/philosophy/ai-加速腐化\|AI 加速熵增]] | `/to-prd` `/zoom-out` `/improve-codebase-architecture` | 见左 |

## 七步流水线

```
grill-me → to-prd → to-issues → tdd → diagnose → zoom-out → improve-architecture
```

> [!example] 阶段语义
> - 🔍 `grill-me`：AI 反复追问澄清需求（70% 返工来自需求没说清）
> - 📋 `to-prd`：把对话变成正式 PRD，留下决策记录
> - 🎯 `to-issues`：拆成可独立处理的 GitHub Issue
> - 🧪 `tdd`：给 AI 明确的"完成"标准
> - 🔬 `diagnose`：系统化调试不乱猜
> - 🔭 `zoom-out`：回顾全局架构防局部正确-整体混乱
> - 🏗 `improve-architecture`：主动重构抗熵增

> [!compare] 与 Superpowers 的差异
> | 维度 | Matt Pocock Skills | [[wiki/skills/superpowers\|Superpowers]] |
> |---|---|---|
> | **执行单元** | 个体命令，按需调用 | 主-子 agent 编排，强串联 |
> | **重点** | DDD 词汇表、PRD、debug | brainstorm、subagent、verify |
> | **TDD** | 独立 `/tdd` skill | 嵌在 `subagent-driven-development` 内 |
> | **交接** | `/handoff` 压缩对话 | 跨 worktree 的多 agent 协议 |
> | **风格** | 单 Repo 工程师日常 | 长 horizon 自治 agent |
>
> 两者都信"反 vibe + 强结构"，但 Superpowers 把整条流水线交给 agent 自治执行，Matt Pocock 留更多控制权给人类。

## Skills 全景

**工程类**：`/diagnose` `/grill-with-docs` `/triage` `/improve-codebase-architecture` `/setup-matt-pocock-skills` `/tdd` `/to-issues` `/to-prd` `/zoom-out` `/prototype`

**效率类**：`/caveman`（→ [[wiki/agent-engineering/context/caveman-超压缩通信|caveman 超压缩]]）/ `/grill-me` / `/handoff`（→ [[wiki/claude-code/handoff-md|HANDOFF.md]]）/ `/write-a-skill`

**杂项**：`/git-guardrails-claude-code` `/setup-pre-commit` `/scaffold-exercises`

## 安装

```bash
npx skills@latest add mattpocock/skills
# 在 Agent 里运行
/setup-matt-pocock-skills
```

安装器会问 Issue tracker（GitHub / Linear / 本地文件）、分类标签、文档目录位置，per-repo 配置。

> [!tip] 不必整套照搬
> 类似 Superpowers，最该借鉴的是少量普适命令：`/grill-me`（需求对齐）、`/tdd`（验收信号）、`/caveman`（token 优化）。其它命令更绑定 GitHub-issue 流水线，团队不用 GitHub 收益有限。

## 关联

- 同类框架：[[wiki/skills/superpowers|Superpowers]]、[[wiki/claude-code/everything-claude-code|Everything Claude Code]]
- 思想根：[[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]、[[wiki/agent-engineering/philosophy/spec-coding|Spec Coding]]、[[wiki/agent-engineering/philosophy/vibe-coding-的代价|vibe coding 的代价]]
- 单 Skill 落地：[[wiki/agent-engineering/workflow/context-md-词汇表|CONTEXT.md]]、[[wiki/agent-engineering/workflow/tdd-red-green-refactor|TDD]]、[[wiki/agent-engineering/workflow/diagnose-debug-循环|diagnose]]、[[wiki/agent-engineering/context/caveman-超压缩通信|caveman]]
