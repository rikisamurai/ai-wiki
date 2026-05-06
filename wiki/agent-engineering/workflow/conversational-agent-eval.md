---
title: Conversational Agent Eval
tags: [evals, conversational-agent, tau-bench]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: draft
---

Conversational agent（客服、销售、coaching）评估的特殊难点：**对话本身就是被评估的产物**——不仅要看任务有没有做成，还要看交互过程是否得体。这类 eval 通常需要**第二个 LLM 模拟用户**，再用多维 rubric 同时评 outcome 和 transcript。代表 benchmark 是 τ-Bench 和 τ2-Bench。

## 为什么需要 LLM 模拟用户

> [!note] 多轮 + 状态 + 用户 persona
> 跟 [[coding-agent-eval|coding agent]] 的"给输入跑出来打分"不同，conversational agent 必须**和某人来回多轮**。让真人参与评估太慢太贵，所以业界做法是：
> - 一个 LLM 扮演用户（带 persona、目标、性格特征——例如"愤怒的退款客户"）
> - 被测 agent 处理对话、调工具、修改状态
> - eval grader 评估**最终状态 + 整段对话质量**
>
> Anthropic 的 alignment auditing agents 用同样思路在长对话里压力测试模型——LLM 模拟用户进行 adversarial 对话。

## τ-Bench / τ2-Bench

[τ-Bench](https://arxiv.org/abs/2406.12045) 和后继 [τ2-Bench](https://arxiv.org/abs/2506.07982) 在 retail support、airline booking 等域跑模拟多轮交互——一个模型扮 user persona、agent 在真实场景里做事。

> [!example] τ2-Bench 的"loophole"插曲
> Opus 4.5 在某个订机票 task 上"失败"——但实际上它**发现了 policy 中的漏洞**，给用户找到了更好的解决方案。eval 写的标准说它没过，但实际是它太聪明了。这正是 [[读-transcript|为什么必须读 transcript]]——只看分数会错过这种类型的"failed but actually better"。

## 多维成功

> [!important] 一次成功是多个维度的合取
> Support task 的"成功"通常拆成：
> - **state check**（outcome）：ticket 真的 resolved 了吗？退款真的 processed 了吗？
> - **transcript constraint**：是不是在 ≤10 轮里完成？
> - **LLM rubric**（quality）：语气是否合适？是否同理心？解释是否清楚？是否基于 fetch_policy 工具结果而不是瞎编？
> - **tool calls**：必需的 verify_identity、process_refund、send_confirmation 都调了吗？

## 一个 task 的样例（取自原文）

```yaml
graders:
  - type: llm_rubric
    rubric: prompts/support_quality.md
    assertions:
      - "Agent showed empathy for customer's frustration"
      - "Resolution was clearly explained"
      - "Agent's response grounded in fetch_policy tool results"
  - type: state_check
    expect:
      tickets: {status: resolved}
      refunds: {status: processed}
  - type: tool_calls
    required:
      - {tool: verify_identity}
      - {tool: process_refund, params: {amount: "<=100"}}
      - {tool: send_confirmation}
  - type: transcript
    max_turns: 10
```

> [!warning] 实际只用必要的几个
> 同样是"全口味"展示。实际项目通常**主要用 model-based grader 评 communication 质量 + goal completion**——很多对话 task（"帮我推荐一支股票"）有多个"正确"解，无法用单一 deterministic grader 覆盖。

## 度量首选 pass^k

Conversational agent 通常面向终端用户——一次失败就是一个不满意的客户。所以 [[pass-at-k-vs-pass-power-k|pass^k]] 比 pass@k 更重要：每次都要稳定，不能"试 3 次有一次对就行"。

## Descript 与 Bolt 两条起步路径

> [!example] 业界两种起步路径
> - **Descript**：从早期就建 eval，围绕"don't break things / do what I asked / do it well"三维度，从手工评估演化到 LLM 评估 + 周期性人工校准（参见 [[eval-grader-三类|LLM-as-judge 校准]]），现在跑 quality 和 regression 两套独立 suite
> - **Bolt**：晚加 eval，已上线后再补——3 个月内搭出系统，跑 agent + 静态分析评输出 + 浏览器 agent 测应用 + LLM judge 评行为

两条路径都成立，但**早建 eval 成本更低**——晚加要从生产数据反向工程成功标准。

## 关联

- 总览：[[agent-evals]]
- LLM 模拟用户的方法学复用：[[research-agent-eval]]、[[computer-use-agent-eval]]
- 客服场景常用的延迟指标：跟 [[agent-等待时间]] 相关
- grader 选型：[[eval-grader-三类]]
