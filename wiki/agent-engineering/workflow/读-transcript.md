---
title: 读 Transcript（Read the Transcripts）
tags: [evals, transcript, observability]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: draft
---

"Read the transcripts"是 Anthropic 在 [[agent-evals|agent eval]] 工作流里反复强调的最关键实践——**不读 transcript 你永远不知道 grader 在瞎打分还是真打分**。一次失败的 trial，transcript 告诉你 agent 是真错了、还是 grader 把一个有效解判错了。

## 为什么不能只看分数

> [!warning] 分数是后验，transcript 是 prior
> Anthropic 的内部规则：**"我们不把 eval 分数当真，直到有人钻进 eval 细节并读了一些 transcript。"** 不公平的 grader、歧义的 task、有效解被判错、harness 限制了模型——任何一项都能让分数失真。
>
> CORE-Bench 上 Opus 4.5 一开始 42%，Anthropic 研究员通过读 transcript 发现：
> - 死板的 grader 把 "96.12" 判错（标准答案 "96.124991…"）
> - 有些 task 描述不清
> - 有些 task 是随机的，根本无法精确复现
>
> 修完 + 用更宽松 scaffold 后，**分数跳到 95%**。差 53 个百分点，全在 transcript 里。

## 读 transcript 在判什么

> [!note] 读的是这几件事
> - **失败是不是 fair**：失败原因要清晰可见——agent 哪步走错了、为什么走错
> - **grader 是不是在打它该打的事**：valid solution 被判错的，要修 grader
> - **agent 有没有作弊**：Anthropic 真踩过 Claude 偷看上一轮 git history 拿到答案的 case
> - **harness 限制了什么**：是不是某个工具的接口让 agent 走不通；这是评估"harness × model"的特征
> - **task 是不是被破坏过**：scaffold 改动、依赖升级可能让原本可解的 task 突然 0% pass

> [!important] 0% pass@100 是 task 出问题的信号
> 前沿模型在某 task 上多次 trial 全挂，**几乎一定**是 task 写坏了或 grader 配错了。先不要怀疑模型——读 transcript、找出 grader bug 或 task 歧义。

## 是工具还是纪律

读 transcript 是**纪律 + 工具**：

- 工具：Anthropic 内部投资了 transcript viewer，把 messages 数组渲染成可读的对话/工具调用序列
- 纪律：定期分配时间读取——不强制就不会发生

这跟 [[agent-可读性|Agent 可读性]] 是一体两面：要让 agent 的轨迹好读，不然读 transcript 的成本会高到没人愿意做。

## 与生产监控的关系

读 transcript 在 [[eval-方法矩阵]] 里横跨多个层：

| 场景 | transcript 来源 |
|---|---|
| Pre-launch eval | eval harness 产生的 transcript |
| Production monitoring | 真实用户会话的 transcript |
| User feedback triage | 用户报告的失败案例对应的 transcript |
| LLM-as-judge 校准 | 同一组 transcript 让 model 和 human 都打一遍分 |

不论哪一层都需要**人愿意打开 transcript 文件读**——这是 AI eval 流程里少数无法自动化的瓶颈。

## 关联

- 总览：[[agent-evals]]
- 校准 LLM 裁判：[[eval-grader-三类]]——transcript 是 LLM 与 human 对齐的共同载体
- 失败要 fair：[[capability-vs-regression-eval]]——"分数不涨"必须先确认是模型问题不是 eval 问题
- 写得让 transcript 可读：[[agent-可读性]]
