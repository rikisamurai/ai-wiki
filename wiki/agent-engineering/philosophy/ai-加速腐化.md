---
title: AI 不会自动收敛复杂度
tags: [ai-coding, tech-debt, ai-first]
date: 2026-05-08
sources:
  - "[[sources/clippings/用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践]]"
last-ingested: 2026-05-08
status: stable
---

一个反直觉的事实：当 90% 以上代码由 AI 生成、且系统没有统一规范的时候，AI Coding 不仅不会让代码变干净，反而会成倍放大风格差异、加速代码库腐化。决定系统走向的不是谁写得更快，而是约束 AI 的能力。

> [!warning] AI 没有"风格收敛"的内生倾向
> 大模型生成代码时强依赖当前上下文 + 现有代码模式。如果同一个仓库里 A 同学写 MVC、B 同学写四层分层、C 同学按需求建包，AI 会模仿每个人当前文件附近的模式继续写下去——差异不会自动收敛，只会持续叠加。

## 美团 31 万行的具体形态

> [!example] 三种典型加速形态
> - **结构腐化**：长期"按需求建包"，Controller 与各种业务逻辑揉在同一个包，"面条式代码"在 31 万行体量下让任何改动都"牵一发而动全身"
> - **隐性技术债**：调用链极长、隐式逻辑与历史兼容分支藏在细节里，AI 会沿着这些路径继续生成而不会主动重构
> - **团队规模放大效应**：一年内成员增至 3 倍 + 跨技术栈 + 90% AI 编码 → 不可控腐化的速度比单人模式快一个数量级

## 治理的两个前置条件

要让 AI Coding 不腐化代码，至少需要：

1. **人人对齐先于人机对齐**：见 [[wiki/agent-engineering/philosophy/人人对齐-人机对齐|人人对齐 → 人机对齐]]——团队自己没有共识，Rule 写得再好也会被不同人解释成不同版本
2. **规范作为基础设施**：always 级别的 [[wiki/claude-code/claude-rules|Rule]] + 渐进式 [[wiki/skills/agent-skills|Skill]]，规范不落地到 AI 工具链就只是一纸空文

## 与"工程师角色变化"的关系

> [!compare] 写代码 vs 维护工程环境
> 当 AI 承担 90% 的编码动作，团队成员的工作重心应从"写代码"转向"设计并维护一个能让 AI 可靠产出代码的工程环境"——见 [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]。AI 加速腐化和 Harness 工程是同一个硬币的两面：没有 Harness，AI 只会加速腐化。

## 关联

- 治理路径：[[wiki/agent-engineering/philosophy/人人对齐-人机对齐]]、[[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]
- 关联现象：[[wiki/agent-engineering/philosophy/plausible-code|Plausible Code]]、[[wiki/agent-engineering/philosophy/vibe-coding-的代价|Vibe Coding 的代价]]
- 落地实践：[[wiki/agent-engineering/workflow/渐进式重构|渐进式重构]]——已腐化的库怎么修
