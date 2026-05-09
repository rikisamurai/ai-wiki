---
title: Specialist Roles 模型（多角色专家化）
tags: [workflow, multi-agent, persona]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: stable
---

把单个通用 agent 拆成多个 persona 化的"专家角色"——CEO / Designer / Eng Manager / QA Lead / Security Officer / Release Engineer——每个角色有独立的 prompt、独立的 forcing question 集、独立的输出格式。这是 [[gstack]]、[[everything-claude-code|ECC]]、[[wiki/skills/superpowers|Superpowers]] 共同采用的范式：**让 LLM 在同一对话里轮流扮演不同角色，比让它"全能"输出更稳**。

## 为什么角色化有效

> [!important] 角色 = 上下文限定 + 评判标准固化
> 一个通用 prompt "请帮我 review 代码"得到的输出常常面面俱到但不深入。换成"你是 Staff Engineer，找的是能过 CI 但生产爆炸的 bug"——LLM 的注意力被锚定到一个明确的评判标准上：
>
> - **缩小搜索空间**：`/cso`（Chief Security Officer）只看 OWASP Top 10 + STRIDE，不会跑去给你建议变量命名
> - **固化输出格式**：`/plan-design-review` 强制 0-10 评分 + "10 长什么样"+ 编辑计划达到 10
> - **forcing question**：`/office-hours` 6 个 forcing question、`/plan-devex-review` 20-45 个 forcing question——把 LLM 从"回答"切换到"提问"模式
>
> 这是 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 在 prompt 层面的实现——不需要真的开 [[subagent-driven-development|subagent]]，单 LLM 顺序扮演多个角色就能拿到大部分收益。

## 典型角色矩阵

> [!example] gstack 23 个角色按职能分组
> | 职能群 | 角色 | 关注 |
> |---|---|---|
> | **战略** | YC Office Hours、CEO/Founder | 重新框定问题、challenge 前提 |
> | **架构** | Eng Manager、Staff Engineer、Debugger | 数据流 / 状态机 / 边界条件 / 根因调试 |
> | **设计** | Senior Designer、Design Partner、Design Engineer、Design Explorer、Designer Who Codes | mockup / design system / HTML 实现 / Slop 检测 |
> | **DX** | Developer Experience Lead、DX Tester | onboarding / TTHW / 文档可达性 |
> | **质量** | QA Lead、QA Reporter、Multi-Agent Coordinator | 真浏览器测试 / 缺陷报告 / 跨 agent 协作 |
> | **安全** | Chief Security Officer | OWASP + STRIDE + 利用场景 |
> | **发布** | Release Engineer、SRE、Performance Engineer、Technical Writer | PR 编排 / 部署 / Canary / 文档同步 |
> | **回顾** | Eng Manager（retro 模式）、Memory | 周复盘 / 跨会话学习 |

## 与 [[writer-reviewer-模式|Writer/Reviewer 模式]] 的关系

> [!compare] 两种角色化结构
> | 维度 | Writer/Reviewer | Specialist Roles |
> |---|---|---|
> | 角色数 | 2 个（写 + 评） | 5–25+ 个 |
> | 关系 | 顺序对抗 | 流水线协作 |
> | 触发 | 同一个 task 上 | 跨 sprint 阶段 |
>
> Specialist Roles 在 review/test 阶段**内部**仍可用 Writer/Reviewer——例如 `/review` 可被理解为 Reviewer 单独跑，`/codex` 是另一个独立 Reviewer 形成 [[cross-model-second-opinion|跨模型互评]]。两者是不同粒度的角色化。

## 反范式：单一万能 agent

> [!warning] "All in one prompt" 的失败模式
> 不做角色拆分时常见的失败：
> - 模型同时关注代码风格、安全、性能、UX、命名——每个维度只浅尝辄止
> - LLM 倾向"安全输出"——给出"看似全面"但缺乏关键 push back 的反馈
> - 忘记 forcing question——直接接受用户的初始 framing 而不挑战
>
> 这正是 [[plausible-code|似是而非的代码]] 在 review 层面的对应——评论看着都对，但生产 bug 没被抓到。

## 角色化 ≠ 角色扮演剧场

> [!tip] 不是 RPG，是 prompt engineering
> 把 LLM 的角色化简单理解成"穿不同戏服讲不同台词"会浪费它。真正起作用的是：
> - 每个角色 prompt 里**明确给出输出 schema**（例如 0-10 评分 + 10 长什么样 + 编辑计划）
> - **forcing question** 替代 open-ended 提问（"列出 6 个具体场景"比"想想用户在做什么"信息密度高 10 倍）
> - **明确不评什么**（CSO 不 review 代码风格、CEO 不 review 数据流），避免角色越界稀释信号

## 关联

- 流水线整体：[[sprint-七阶段范式]]
- 具体落地：[[gstack]]、[[everything-claude-code]]、[[wiki/skills/superpowers]]
- 编排范式：[[coordinator-模式]]、[[subagent-driven-development]]
- 互评变种：[[writer-reviewer-模式]]、[[cross-model-second-opinion]]
- 反例：[[plausible-code]]
