---
title: Devin Knowledge / DeepWiki（人工审批的 memory）
tags: [devin, memory, claude-code]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

Cognition Devin 在 memory 设计上选了和其他 harness 相反的方向：**没有 auto-capture，所有持久化 memory 必须人工审批**。它把 memory 分成两块：Knowledge（trigger-content 事实，Devin 建议 + 人审批）和 DeepWiki（reference docs，规格固定）。这条路线把"质量"放到"采集量"之上——但代价是不审批的团队什么都积累不起来。

## 两块 memory 的分工

> [!compare] Knowledge vs DeepWiki
> | 维度 | Knowledge | DeepWiki |
> |---|---|---|
> | **形态** | trigger-content 事实对（条件 → 行为） | 长文 reference docs |
> | **采集** | Devin session 后 suggest，**人审批才落库** | 人维护 |
> | **上限** | — | 30 页 × 100 notes × 10,000 字符 each |
> | **典型用途** | "看到 X 就用 Y" 类约定 | 架构说明、API 大段文档 |

Knowledge 的 "trigger-content 对" 结构和 [[skill-编写实践|Skill 描述符的 if-then 模式]]同构——只是触发引擎不同：Skill 由 LLM 在每轮决定要不要打开；Knowledge 由 Devin 在匹配触发条件时自动注入。

## 与"全自动"路线的根本分歧

> [!compare] 三种 memory 治理哲学
> | 哲学 | 代表 | 取舍 |
> |---|---|---|
> | **全自动 + 全保留** | [[auto-memory\|Claude Code Auto Memory]] | 召回多，质量参差 |
> | **idle gate + 合并 sub-agent** | [[codex-memory\|Codex memories]] | 写慢，过滤一层 |
> | **人工审批** | **Devin Knowledge** | 质量高，**审批是 friction** |

Devin 的押注：memory 错了比没有更糟——记错的 trigger-content 会**反复**误导 agent。这与 [[ai-代码-attribution|AI 代码 attribution]]里的"自报"机制相邻：宁可显式记录少，也不要悄悄沉淀。

## Shortcoming

> [!warning] 审批不发生 = 记忆为零
> Devin 的 memory 质量取决于团队是否真的会去 review session 后的建议。**不审批 = 记忆为零**——比"自动记错"更糟的失败模式是"什么都没记"。

> [!warning] curated for Devin，不可移植
> Knowledge 的格式与 Devin 的运行时绑定。换到 [[claude-code|Claude Code]] / [[codex|Codex]] / 其他 harness 完全用不了——命中 [[memory-harness-shortcomings|harness-scoped 短板]]。
>
> [[mem0|Mem0]] 给出的"跨 harness 基础设施"路线在 Devin 这里目前不适用，因为 Devin 不是开放生态。

> [!note] DeepWiki 容量真的不大
> 30 页 × 100 notes × 10,000 字符 ≈ 3 千万字符，分散到 30 页的话单页平均仅 100 万字符——对一个中型项目的架构 + API 文档**很容易撑满**。Devin 把上限定在这里反映的是它对"记忆即上下文，不是知识库"的克制。

## 适用判断

- 团队**真的会审批** + 想要稳定记忆质量 → Devin Knowledge 合理
- 团队**没有评审带宽** → Devin Knowledge 不会沉淀，应改用 Claude Code Auto Memory 类自动路线（接受质量噪声）
- 想要**跨工具共享**记忆 → Devin Knowledge 不适用，看 [[mem0|Mem0]]

## 相关页面

- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — Devin 因人审批绕过了 staleness 风险，但仍 harness-scoped
- [[skill-编写实践|Skill 编写实践]] — Knowledge 的 trigger-content 与 Skill if-then 描述同构
- [[auto-memory|Claude Code Auto Memory]] · [[codex-memory|Codex Memories]] — 对立的"自动"路线
- [[ai-代码-attribution|AI 代码 Attribution]] — "宁少不错"的相同思路
- [[人人对齐-人机对齐|人人对齐 → 人机对齐]] — 审批门是人人对齐在 memory 这一层的落地
