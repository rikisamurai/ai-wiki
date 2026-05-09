---
title: Agent Evals（智能体评估）
tags: [evals, agent-ops, methodology]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

Agent eval 是给 AI 智能体写的"自动化测试"：给定输入、跑完一个 agent loop、用 grader 给输出和最终环境状态打分。它和单轮 LLM eval 的区别在于必须评估**多轮工具调用 + 环境状态变化**——错误会沿轨迹传播放大，模型也常在轨迹中找出设计者没想到的有效解。没有 evals 的团队会陷在"用户说变差了 → 复现 → 修 → 祈祷没坏别的"的反应式循环里。

## 七个绕不开的术语

> [!note] Anthropic 的术语约定
> - **Task / Problem / Test case**：一个有明确输入和成功判据的测试单元
> - **Trial**：对一个 task 的一次尝试。模型不确定性高，所以同一 task 通常跑多次取统计
> - **Grader**：给某个维度打分的逻辑（一个 task 可有多个 grader，每个含多个 assertion/check）
> - **Transcript / Trace / Trajectory**：一次 trial 的完整记录——所有输出、工具调用、推理、中间结果。Anthropic API 里就是 trial 结束时的完整 messages 数组
> - **Outcome**：trial 结束时**环境的最终状态**。Agent 可能在 transcript 里说"已订票"，但 outcome 是数据库里有没有这条 reservation
> - **Evaluation harness**：跑 eval 的基础设施（提供工具、并发执行、记录步骤、聚合结果）
> - **Agent harness / scaffold**：让模型作为 agent 行动的系统（处理输入、编排工具、返回结果）。**评估"一个 agent"实际上是在评估 harness × model 的组合**——这是为什么 [[harness-engineering]] 的成熟度会直接影响 eval 分数
> - **Evaluation suite**：一组围绕同一目标的 task 集合（如 customer-support 套件含退款/取消/升级）

## 三类 grader 与组合策略

每个 task 可挂多个 grader，分别评估 transcript 或 outcome。三类 grader 各有强弱（详见 [[eval-grader-三类]]）：

- **Code-based**：字符串匹配、单测、静态分析、状态校验、工具调用校验、轨迹分析。快、便宜、可复现，但脆
- **Model-based**：rubric 打分、自然语言断言、成对比较、多裁判共识。灵活但非确定性，需 [[eval-grader-三类|与人工校准]]
- **Human**：SME review、众包、抽样、A/B、标注员一致性。金标准但慢且贵

打分聚合三种模式：加权（达到阈值即过）、二元（全过才过）、混合。

## Outcome vs Transcript：分清楚评估对象

> [!important] 评 outcome 还是评 transcript
> - **Outcome 评估**回答"事情有没有做成"——典型如订票任务最后数据库里是否真的有 reservation
> - **Transcript 评估**回答"过程是否合理"——用了多少 token、走了多少轮、有没有调用必需的工具
>
> 普遍误区是**强行规定工具调用顺序**。Anthropic 明确建议"评 agent 产出的东西，而不是它走的路径"——agent 经常找到设计者没想到的有效解，规定 tool order 会无谓地惩罚创造性。

## 四种主流 agent 类型的评估范式

| 类型 | 关键技术 | 代表 benchmark | 详细 |
|---|---|---|---|
| Coding agent | 单测 + 代码质量 LLM rubric | SWE-bench Verified、Terminal-Bench | [[coding-agent-eval]] |
| Conversational agent | LLM 模拟用户 + 多维 rubric + state check | τ-Bench、τ2-Bench | [[conversational-agent-eval]] |
| Research agent | groundedness + coverage + source quality | BrowseComp | [[research-agent-eval]] |
| Computer use agent | 沙箱执行 + 后端状态校验 | WebArena、OSWorld | [[computer-use-agent-eval]] |

## 关键实践（按 roadmap 的 8 步精简）

> [!tip] 从零到 1 的最小可行 eval 集
> 1. **不要等到完美才开始**：20–50 个真实失败案例就够了。等久了只能"反向工程"成功标准
> 2. **从手工测试和 bug tracker 入手**：把每条用户反馈转成一个 task
> 3. **任务无歧义 + 提供 reference solution**：两位领域专家应能独立得出相同的过/不过判断；reference solution 同时验证 task 可解、grader 配置正确
> 4. **平衡正反样本**：只测"该触发"会练出"什么都触发"的模型——参见 Claude.ai web search 反复调正反平衡的故事
> 5. **隔离环境**：每次 trial 从干净环境起步，否则会因残留文件/缓存/git 历史等共享状态导致相关性失效（Anthropic 内部 eval 真的踩过 Claude 偷看上一轮 git log 作弊）
> 6. **graders 设计要慎重**：能 deterministic 就 deterministic、必要时上 LLM、人工只用于校准
> 7. **读 transcript**：参见 [[读-transcript]]——不读 transcript 你不知道 grader 是不是在瞎打分
> 8. **eval 是活物**：核心 infra 由 dedicated team 管，task 由 PM/CSM/销售用 Claude Code 直接 PR 贡献

> [!warning] 0% pass@100 的诊断信号
> 前沿模型在某 task 上多次 trial 拿 0%，**几乎一定是 task 写坏了或 grader 配错了**，不是模型不行。CORE-Bench 上 Opus 4.5 一开始 42%，研究员发现 grader 把 "96.12" 判错（标准答案是 "96.124991…"）、task 描述歧义、随机 task 不可复现——修完后跳到 95%。

## 与其他评估方式的关系

> [!note] Swiss Cheese 模型
> 自动化 eval 是**多层防御**之一，单层无法捕获所有问题。完整图景见 [[eval-方法矩阵]]——automated eval / production monitoring / A/B test / user feedback / manual transcript review / systematic human study 各补一层。

## 关联

- 范式：[[eval-driven-development]]——build evals to define planned capabilities before agents can fulfill them
- 上游：[[harness-engineering]]——eval 评估的是 harness × model
- 下游：[[capability-vs-regression-eval]]、[[pass-at-k-vs-pass-power-k]]
- 反例：[[plausible-code]]——没 eval 时模型生成"看着对的代码"难以被发现
