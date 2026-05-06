---
title: Domain Skills（per-site 浏览器记忆）
tags: [browser, memory, agent-skills]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: draft
---

[[gstack]] 浏览器（[[wiki/retrieval/browser/agent-browser|browser agent]] 形态）的 per-hostname 记忆机制：agent 在某个站点学到一条经验（"LinkedIn 的 Apply 按钮在 iframe 里"），保存为 domain skill，**下次访问同 hostname 时自动加载**。是 [[wiki/skills/agent-skills|Agent Skills 规范]] 在浏览器自动化领域的微缩对应物。

## 触发与晋升流程

> [!example] Quarantine → Active → Global
> 1. Agent 第一次解决某站点上的某问题，调 `$B domain-skill save` 写入 skill。**默认 quarantined**——不会自动加载，避免误学的经验干扰
> 2. **手工标记或经过 3 次成功使用后**自动晋升为 active——下次访问该 hostname 时 system prompt 自带这条 skill
> 3. 在多个项目里都验证有效后，可 `$B domain-skill promote-to-global` 提升到全局 skill 池——所有项目都受益
>
> 存储在 `/learn`（[[wiki/claude-code/auto-memory|Auto Memory]] 风格的 per-project learnings）旁边，文件可 grep / 编辑。

## 为什么按 hostname 而不是按项目

> [!important] hostname 是稳定的"上下文键"
> 浏览器自动化的"经验"本质上跟**站点结构**绑定，而不是跟项目绑定：
> - "LinkedIn 的 Apply 按钮在 iframe 里"——所有项目都成立
> - "Notion 编辑器需要先 click empty area 再 type"——所有项目都成立
> - "Stripe Dashboard 的某 button 触发新 tab"——所有项目都成立
>
> 按项目存会重复劳动；按 URL path 存太碎片；hostname 是甜蜜点。

## 与 Agent Skills 规范的对应

> [!compare] domain skills vs 标准 skills
> | 维度 | 标准 [[wiki/skills/agent-skills\|Agent Skills]] | Domain Skills |
> |---|---|---|
> | 加载触发 | LLM 判断 description 命中 | hostname 匹配自动加载（确定性） |
> | 粒度 | 一个完整工作流（QA、review、ship） | 一条经验 / 一段 selector / 一个 workaround |
> | 写入方式 | 人手写（或 [[wiki/skills/skill-编写实践\|skill-creator]]） | agent 自动写 + 人审核晋升 |
> | 上下文成本 | 较大（一整个 skill） | 极小（几行 markdown） |
>
> domain skills 是 agent skills 的**自动化、轻量化、确定性触发**变种——专门为浏览器自动化的高频小经验设计。

## Quarantine 机制：防误学

> [!warning] 为什么不直接 active
> Agent 在某个 task 偶然成功了一次的"经验"未必是普适规律。直接 active 会污染未来会话。Quarantine + 3 次验证：
>
> - 第一次：可能是巧合
> - 第二次：增加置信度
> - 第三次成功：通过统计 prior，晋升 active
>
> 这是**防止"看似有效但实际偶然"的范式**——跟 [[plausible-code|plausible code]] 在浏览器知识层的对应。

## 与传统 RAG 的差异

> [!compare] 不是检索，是确定性注入
> | | 传统 RAG | Domain Skills |
> |---|---|---|
> | 触发 | 语义检索（embedding） | 字符串匹配 hostname |
> | 召回 | top-k 模糊召回 | 全部命中（per-hostname all-in） |
> | 写入 | 人工/批量入库 | agent 自写 + quarantine |
>
> Domain Skills 不是 [[wiki/retrieval/rag/rag|RAG]] 的另一种实现，而是**给 agent 用的 lightweight 记忆**——确定性、可解释、易管理。当 agent 行为复现性比召回率更重要时（浏览器自动化的典型需求），它优于 RAG。

## CDP escape hatch：与 raw 浏览器协议的边界

> [!tip] 当 domain skill 不够时
> Domain skill 是"agent 在 curated 高层命令上的经验"。极少数情况需要 raw [[wiki/retrieval/browser/cdp|CDP]] 调用，gstack 提供 `$B cdp <Domain.method>` 作为 escape hatch：
> - 默认 deny——必须显式加进 `cdp-allowlist.ts` 并附一行 justification
> - Two-tier mutex 序列化：browser-scoped 和 per-tab 的 CDP 调用不会互踩
> - 数据外泄类方法（如 `Network.getResponseBody`）的输出被 wrap 进 UNTRUSTED envelope

## 关联

- 范式来源：[[gstack]]
- 浏览器代理基础：[[wiki/retrieval/browser/agent-browser|agent-browser]]、[[wiki/retrieval/browser/browser-use|Browser-Use]]、[[wiki/retrieval/browser/cdp|CDP]]
- skills 生态对照：[[wiki/skills/agent-skills|Agent Skills]]、[[wiki/skills/渐进式披露|渐进式披露]]
- 持久化同族：[[wiki/claude-code/auto-memory|Auto Memory]]、[[continuous-checkpoint]]
- 防误学：[[plausible-code]] 的浏览器知识对应
