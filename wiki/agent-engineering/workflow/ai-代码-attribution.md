---
title: AI 代码 Attribution（自报 vs 检测）
tags: [attribution, ai-coding, metric]
date: 2026-05-08
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Git AI - 追踪 AI 生成代码的 Git 扩展]]"
last-ingested: 2026-05-08
status: stable
---

AI 生成代码的归因有两条路：让 agent 在写代码时自报家门（precise，需要 agent 协作），或者事后用 ML 模型基于代码风格猜（noisy，无需 agent 协作）。[[wiki/claude-code/git-ai|Git AI]] 的作者把"基于风格的 ML 检测"明确列为 anti-pattern——AI 代码风格越来越像人，靠"嗅探"区分注定不准。

> [!compare] 自报 vs 检测
> | 维度 | 自报（Self-Report） | 检测（Detection） |
> |---|---|---|
> | 数据来源 | agent 在生成时主动落到元数据 | 事后用模型分析代码风格 |
> | 精度 | 行级精确，含 prompt / model 等字段 | 概率性、且随模型进化逐年变差 |
> | 工程依赖 | agent 端要支持（Git AI 已对接 12 家） | 无 |
> | 可被对抗 | agent 故意不报就丢失 | 通过 reformatter / lint 也容易绕过 |
> | 适合场景 | 团队治理 / 合规审计 / 质量度量 | 学术研究的粗略统计 |

## 为什么"自报"是更可靠的范式

> [!note] 同一思路在 Eval 里也出现
> Anthropic 在《Demystifying evals for AI agents》里讨论过类似判断：评估 agent 行为时，"agent 自报 transcript"比"事后用模型逆推 agent 做了什么"更可靠。
>
> 共同直觉：信息源头本来就在 agent 那里，让 agent 写下来比让另一个模型猜要便宜得多、也准得多——见 [[wiki/agent-engineering/workflow/读-transcript|读 Transcript]]。

## 在度量栈里的位置

> [!example] AI Coding 度量的三层
> 1. **Pre-launch**：[[wiki/agent-engineering/workflow/agent-evals|Agent Evals]] / [[wiki/agent-engineering/workflow/cursorbench|CursorBench]]——synthetic task 上的 pass 率
> 2. **In-product 实时**：[[wiki/agent-engineering/workflow/keep-rate|Keep Rate]] / [[wiki/agent-engineering/workflow/采纳率|采纳率]] / [[wiki/agent-engineering/workflow/语义满意度信号|语义满意度信号]]——AI 改动留存比例
> 3. **Commit 级事后归因（本页）**：行级精确，含 prompt 元数据
>
> 三层不可互相替代：第 1 层告诉你模型行不行，第 2 层告诉你产品体验好不好，第 3 层告诉你"哪行 AI 写的 / 用什么 prompt 写的"——以后回头追问题、做合规审计、分析采纳率失败模式都靠它。

## 工程落地的最小依赖

> [!tip] 不需要专门的 attribution 平台
> attribution 可以用 git 自带的 [[wiki/agent-engineering/workflow/git-notes-ai-元数据|git notes]] 存——零基础设施依赖：
> - 不发明新存储
> - 不改 commit hash（attribution 是 side-channel）
> - rebase / cherry-pick 自动跟随
>
> 这是 [[wiki/claude-code/git-ai|Git AI]] 的核心选型。

## 关联

- 工具实现：[[wiki/claude-code/git-ai|Git AI]]
- 底层机制：[[wiki/agent-engineering/workflow/git-notes-ai-元数据|git notes 作为 AI 元数据载体]]
- 度量同族：[[wiki/agent-engineering/workflow/keep-rate|Keep Rate]]、[[wiki/agent-engineering/workflow/采纳率|采纳率]]
- 类似自报范式：[[wiki/agent-engineering/workflow/读-transcript|读 Transcript]]
