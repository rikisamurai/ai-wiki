---
title: 跨模型 Second Opinion
tags: [code-review, multi-model, codex]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
  - "[[sources/clippings/用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践]]"
last-ingested: 2026-05-08
status: draft
---

让**另一个 vendor 的模型**独立 review 同一段 diff——典型如 Claude 写代码 → 调 OpenAI Codex CLI 复审。这是 [[ai-code-review|AI Code Review]] 的反偏置补丁：单模型 review 会有系统性盲点（同一族模型在某些反模式上有共同偏好），引入异源模型能照出这些盲点。[[gstack]] 的 `/codex` 是当前最完整的范式实现。

## 三种使用模式

> [!example] /codex 的三档
> | 模式 | 用法 | 输出 |
> |---|---|---|
> | **Code Review** | 给 Codex 当 pass/fail gate | 是否合并的二元判断 |
> | **Adversarial Challenge** | 让 Codex 主动尝试 break 你的代码 | 攻击思路 + 反例 |
> | **Open Consultation** | 跨会话连续对话 | 对设计/架构的开放式建议 |
>
> Adversarial mode 是 Anthropic [[agent-evals|alignment auditing agents]] 范式在 review 层的对应——让另一个模型扮演"对手"才能逼出隐藏问题。

## 跨模型分析（重要）

> [!important] overlap × unique 的诊断价值
> 当 `/review`（Claude）和 `/codex`（OpenAI）都跑完同一 branch 时，gstack 输出**两类分类**：
> - **Overlap findings**：两个模型都发现的问题——**置信度极高，几乎一定是真问题**
> - **Unique to Claude / Unique to Codex**：只有一边发现的——可能是真问题（被对方漏了），也可能是 false positive（被对方正确忽略）
>
> 这是个最便宜的"贝叶斯式"信号——两个独立 prior 同时报一件事，后验置信度会显著拉高。

## 与 [[writer-reviewer-模式|Writer/Reviewer]] 的关系

> [!compare] 同源 vs 跨源 reviewer
> | 维度 | 同源 Writer/Reviewer | 跨源 Second Opinion |
> |---|---|---|
> | Reviewer 模型 | 跟 Writer 同模型（不同 prompt） | 异源模型（OpenAI / Gemini / Anthropic 互评） |
> | 主要价值 | "rubber duck"——slow down + recheck | 抓系统性盲点 |
> | 成本 | 只多一次 LLM 调用 | 需要 multi-vendor auth + 多份 token 配额 |
> | 何时上 | 默认 | 关键 PR / merge 前 / 安全敏感改动 |
>
> 两者非互斥——同源 Writer/Reviewer 是"日常防护"，跨源 second opinion 是"关键节点的额外保险"。

## gstack-model-benchmark：把跨模型评估常态化

> [!tip] 跨模型 benchmark 工具
> gstack 还附了 `gstack-model-benchmark` CLI——同一 prompt 同时跑 Claude / GPT（via Codex CLI）/ Gemini，对比 latency / tokens / cost / LLM-judge 质量分。`--dry-run` 验证 auth 不花钱。
>
> 这是把"跨模型对比"从手工操作变成**可重复 eval**——参见 [[wiki/agent-engineering/workflow/agent-evals|Agent Evals]] 的多模型对比实践。哪个模型在哪类 task 上更强，跑一遍就清楚。

## 适用与不适用

> [!warning] 不要把 second opinion 当 default
> 跨模型 review 成本高（多份 API key、多份配额、慢一倍）。建议姿势：
>
> **该上**：
> - merge 前的最终守门
> - 安全敏感改动（结合 [[gstack|/cso]]）
> - 已知模型有偏置的 task（例如 [[plausible-code|plausible code]] 高发场景）
>
> **不必上**：
> - typo 修复 / 文档改动 / 重命名
> - 已经被 deterministic 测试覆盖的纯逻辑改动
> - 时间敏感的 hotfix（先合再补 second opinion）

## 团队工程实践（不只是个人 dev 工具）

> [!example] 美团 31 万行重构里的两条 CR 实操
> - **高阶模型审查低阶模型**：使用高配模型作为 Judge Model，审查低阶模型产出的编码——同一族内的"高位 second opinion"
> - **不同厂商对抗审核**：让不同厂商模型互相审查对方产出——通过差异化能力形成互补，实测 CR 覆盖面更全
>
> 这两条把跨模型 CR 从"个人开发者的 second opinion"扩展成了"团队 CR 流水线的常规一环"，配合 [[wiki/agent-engineering/code-review/pre-pr|Pre-PR 机制]] 一起前置。

## 关联

- 上游：[[ai-code-review]]、[[writer-reviewer-模式]]、[[wiki/agent-engineering/code-review/pre-pr|Pre-PR 机制]]
- 同族 review 范式：[[gstack|gstack 的 /review + /cso + /codex 三层]]、[[ai-写-lint]]
- 多模型用作 eval：[[wiki/agent-engineering/workflow/agent-evals]]
- 工具：[[codex|OpenAI Codex CLI]]、[[codex-plugin]]
- 反例：[[plausible-code]]——单模型 review 的主要漏掉对象
