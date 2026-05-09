---
title: Eval Grader 三类（code / model / human）
tags: [evals, grader, llm-as-judge]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

Agent eval 的 grader 按打分主体分三类：code-based（确定性代码）、model-based（LLM 当裁判）、human（人工）。**优先选确定性的、必要时上 LLM、人工只在校准 LLM 裁判时介入**——这是 Anthropic 给的默认顺序。

## 三类对比

> [!compare] 强弱与适用场景
> | 类型 | 典型方法 | 强 | 弱 |
> |---|---|---|---|
> | **Code-based** | 字符串/正则/模糊匹配、单测（fail-to-pass / pass-to-pass）、静态分析（lint/type/security）、outcome 校验、tool 调用校验、轨迹分析（n_turns / n_tokens） | 快、便宜、客观、可复现、易调试 | 对"等价但不完全匹配"的输出脆，缺乏 nuance |
> | **Model-based** | rubric 打分、自然语言断言、成对比较、reference-based 评估、multi-judge consensus | 灵活、可扩展、能捕捉 nuance、能处理开放式输出 | 非确定性、比代码贵、需和人工校准 |
> | **Human** | SME review、众包、抽样、A/B test、标注员一致性 | 金标准、贴合专家用户判断、用来校准 model grader | 慢、贵，常需要稀缺专家 |

## 选用顺序

> [!tip] 默认决策树
> 1. 这事能写单测吗？→ 写单测（[[coding-agent-eval|coding agent]] 的 SWE-bench/Terminal-Bench 全靠它）
> 2. 单测覆盖不到的部分（代码风格、对话语气、综述完整性）→ LLM rubric
> 3. LLM rubric 拿不准 → 抽样人工校准
>
> 不要因为"LLM 听得懂自然语言所以更智能"就直接上 LLM——能确定性化就确定性化，省钱、省时间、还可复现。

## 容易踩的两个坑

**别强行规定 tool call 的顺序**。这是常见冲动，结果是测试过于脆弱——agent 经常找到设计者没想到的有效路径。**评 agent 产出，不评它走的路径**。

**多组件 task 要给 partial credit**。一个 support agent 正确识别问题、验证客户、但最后没成功 process refund，和一上来就挂掉，差距很大。结果应反映这个连续光谱，而不是一刀切的过/不过。

## LLM-as-judge 的校准

LLM 当裁判要拿到"接近人类专家"的精度，必须做几件事：

> [!important] 让 LLM 裁判靠谱
> - **给它"我不知道"的出口**：rubric 里允许返回 `Unknown`，避免硬掰一个分而生成幻觉
> - **每个维度独立 LLM 裁判**：与其让一个 LLM 一次评所有维度，不如把 rubric 拆成多个清晰小项、每项跑独立的 LLM-as-judge
> - **定期与人工对齐**：直到 model 与 human 的判断分歧足够小，再放心让 model 接管
> - **稳定后才能减少人工**：上线前要花精力做这步，之后偶尔抽样维持即可

[[capability-vs-regression-eval|Eval saturation]] 和 grading bug 经常被低估：CORE-Bench 上 Opus 4.5 一开始 42%、修完 grading 漏洞后跳到 95%——别把分数当面子。

## 加权 vs 二元 vs 混合

每个 task 可挂多个 grader，最终聚合三种模式：

- **加权**：所有 grader 分数加权后达阈值即过
- **二元**：所有 grader 必须全过
- **混合**：核心 grader 走二元 + 辅助 grader 走加权

选哪种取决于产品需求——退款流程的"实际有没有打钱"必须二元，"语气是否得体"可以加权。

## 关联

- 总览：[[agent-evals]]
- agent-type 专用 grader 设计：[[coding-agent-eval]]、[[conversational-agent-eval]]、[[research-agent-eval]]、[[computer-use-agent-eval]]
- 校准的兜底：[[读-transcript]]——不读 transcript 永远不知道 grader 在瞎打还是真打
