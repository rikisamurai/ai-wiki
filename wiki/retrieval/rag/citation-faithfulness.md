---
title: 引用忠实度（Citation Faithfulness）
tags: [rag, citation, hallucination]
date: 2026-05-09
sources:
  - "[[sources/clippings/youzingwasc-search-skill]]"
last-ingested: 2026-05-09
status: draft
---

引用忠实度是 [[rag|RAG]] 系统能不能被信任的硬指标：模型在答案里写"`[S2]` 来源说市场规模 540 亿美元"时，`S2` 这条来源是否真的支持这个数字？[Huang et al., 2024](https://arxiv.org/abs/2412.18004) 把 RAG 系统中的"引用幻觉"定义为常见失败模式——**模型声称引用某来源，但实际内容不匹配**。[[wiki/skills/wasc-search-skill|wasc-search-skill]] 给了一个工程化解法：per-claim inline citation + 机械化引用 ID 验证 + 多源冲突检测三件套。

> [!important] 引用幻觉的两种典型形态
> 1. **ID 幻觉**：模型写 `[S7]`，但 citation 列表里只有 S1-S5——直接 ID 不存在
> 2. **内容幻觉**：模型写 `[S3]`，S3 是真的，但 S3 的原文里没有这个数字——ID 对得上，内容对不上
>
> ID 幻觉可以机械化拦截，内容幻觉则需要更重的 [[wiki/agent-engineering/workflow/eval-grader-三类|eval grader]]（model-graded 或 human-graded）。

## 三件套工程化方案

### 1. Per-claim inline citation（逐条 `[S#]`）

每条陈述后必须带至少一个 `[S#]`——而不是把所有引用堆在段落末尾。这样做的好处：

> [!example] 段落级 vs 句级引用
> ```
> // 段落级（错）：
> "市场规模 540 亿美元，OpenAI 占 35%，融资超 300 亿元。[S1][S2][S3]"
>            ↑ 哪个数字来自哪条来源？没人知道
>
> // 句级（对）：
> "市场规模 540 亿美元 [S2]。OpenAI 占 35% [S2]。融资超 300 亿元 [S4]。"
>            ↑ 每条事实都可独立溯源验证
> ```

句级引用让用户可以**逐句 click-through 验证**，也让自动化校验（下面 §2）能精确定位到陈述-来源对。

### 2. 机械化引用 ID 验证

LLM 输出后立刻用代码扫一遍：

> [!example] 验证伪代码
> ```ts
> const citedIds = extractAllCitations(answer)        // ["S1","S2","S2","S4"]
> const validIds = new Set(citations.map(c => c.id))  // {"S1","S2","S3","S4"}
> const ghosts = citedIds.filter(id => !validIds.has(id))
> if (ghosts.length > 0) throw new CitationError(ghosts)
> ```
>
> wasc 在 5 级降级里把这步放在每一级输出后——只要 ID 对不上就触发降级，**不让幻觉答案外溢**。

这一步只能拦 ID 幻觉，但它**几乎免费**（一段正则 + Set lookup），ROI 极高。

### 3. 多源冲突检测

[FaithfulRAG (Li et al., 2025)](https://arxiv.org/abs/2506.08938) 的策略：当多个来源对同一事实给出不同数字时，**自动标注冲突**而不是默默选一个。

> [!example] wasc 的输出 schema
> ```json
> {
>   "answer": "...",
>   "citations": [...],
>   "confidence": "high | medium | low",
>   "conflicts": "S2 与 S4 对融资额数据不一致（300 亿 vs 280 亿）"
> }
> ```
>
> `conflicts` 字段是模型主动暴露不确定性的渠道——比"挑一个写出来"诚实得多。下游消费方看到 `conflicts != ""` 就可以选择展示双源、降级回答、或回退给人审。

## 为什么三件套必须一起做

> [!compare] 单独做某一件的失败模式
> | 只做 | 失败模式 |
> |---|---|
> | 仅 per-claim 引用 | LLM 仍可能编造 ID（"`[S99]`"） |
> | 仅 ID 校验 | 拦不住"ID 真但内容假" |
> | 仅冲突检测 | 引用本身可能就是假的 |

三件套是层层收紧：**句级引用让校验有抓手 → ID 校验拦最便宜的一类幻觉 → 冲突检测把"模型必须挑边"的隐性幻觉显式化**。少任何一环都会留漏洞。

## 与 RAG 流水线其他位置的关系

> [!note] citation faithfulness 不是 generate 阶段的事
> 它是**贯穿 retrieve → rerank → generate 三阶段的契约**：
> - retrieve 阶段必须给每条候选分配稳定 ID（URL hash 或 source rank）
> - rerank 阶段保留 ID 不丢失
> - generate 阶段强制 prompt 让模型输出 `[S#]` 格式
> - 输出后机械化验证
>
> 任何一段断了（比如 RRF 融合后没保留 ID 映射），整个忠实度链就垮。

## 关联

[[rag|RAG]] / [[wiki/skills/wasc-search-skill|wasc-search-skill]] / [[rag-降级|RAG 5 级降级]] / [[wiki/agent-engineering/workflow/eval-grader-三类|Eval Grader 三类]]
