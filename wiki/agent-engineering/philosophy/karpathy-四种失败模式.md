---
title: Karpathy 的四种 AI Coding 失败模式
tags: [philosophy, ai-coding, failure-modes]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: stable
---

Andrej Karpathy 在他广为流传的 [AI coding rules](https://github.com/forrestchang/andrej-karpathy-skills)（17K stars 的 CLAUDE.md 风格规则集）里指出 AI 写代码的**四种典型失败**：**wrong assumptions / overcomplexity / orthogonal edits / imperative over declarative**。这四类失败不是 prompt 写得好就能避免——它们需要工作流层面的强制约束。[[gstack]] 把这四类映射到具体 skill 上声称"已经覆盖"。

## 四种失败模式

> [!example] 一类失败 + 一类工作流应对
> | # | 失败模式 | 表现 | 工作流级解 |
> |---|---|---|---|
> | 1 | **Wrong Assumptions**（错误假设） | Agent 没问就猜了边界条件 / 数据形状 / 用户意图 | [[gstack\|/office-hours]] 的 forcing question 强制把假设拉出来；Confusion Protocol 让 Claude 在架构决策前停下 |
> | 2 | **Overcomplexity**（过度复杂） | 一个 if 能解决的事拉出三层 abstract factory | [[gstack\|/review]] 检测无谓复杂度；[[wiki/agent-engineering/philosophy/yagni-与-dry-反论\|YAGNI 反论]] |
> | 3 | **Orthogonal Edits**（顺手乱改） | 让 Claude 修 bug A，它顺带"优化"了无关的 B、C、D | [[gstack\|/review]] flag drive-by edits；[[gstack\|/freeze]] 锁定可编辑目录 |
> | 4 | **Imperative over Declarative**（命令式优于声明式） | 应该用 SQL view / config / type 表达的，写成一堆命令式代码 | [[gstack\|/ship]] 把 task 转成 verifiable goals + test-first execution |

## 为什么 prompt 解决不了

> [!important] 单 prompt 是事后约束，工作流是事前约束
> "请不要做 XXX"加进 system prompt，对小任务有效。但跑 [[long-horizon-agent|长任务]] 时：
> - 任务一拆解，每条子任务的 prompt 重新评估"什么算复杂"——单点判断容易过
> - "顺手改一下"的诱惑常发生在 agent 已经看到代码时——后置 prompt 警告很弱
> - "wrong assumption"在 agent 没意识到自己在猜时被埋下——它需要的不是更长的 prompt，是**有人/有工具问它"你假设了什么"**
>
> Karpathy 的规则集是**事后纠正**的 prompt 集合；[[gstack]] 主张配合**事前约束**的 workflow skill 才能让规则真正生效。

## "工作流执行层"的具体含义

> [!note] CLAUDE.md ≠ 工作流执行
> 很多人把 Karpathy rules 抄进自己的 CLAUDE.md 就以为完事了。问题：
> - CLAUDE.md 规则只在每次新对话开头提醒一次
> - 长 sprint 中 agent 会逐渐"忘掉"规则（[[wiki/agent-engineering/context/context-rot|context rot]]）
> - 单 prompt 规则不抗 [[wiki/agent-engineering/context/cache-命中率|cache miss]] 后的状态变化
>
> 真正的执行层需要：
> - **Stage gate**：每个 [[sprint-七阶段范式|sprint 阶段]] 结束前由独立 skill 检查
> - **Independent reviewer**：[[cross-model-second-opinion|跨模型 review]] 抓单模型的系统盲点
> - **File scope freeze**：物理上禁止 agent 编辑某些文件，比 prompt 警告更刚

## 与 [[plausible-code|plausible code]] 的关系

> [!compare] 同一现象的两种切角
> - **Karpathy 的视角**：四种**机制级**失败——每种都对应一个具体的 reasoning 缺陷
> - **plausible code 的视角**：失败的**结果**——产出"看起来对但实际不对"的代码
>
> 四种失败模式是 plausible code 的**根因清单**。修 plausible code 的根本方法是逐项消除这四类——而不是花更多力气 review 输出。

## 关联其他范式

> [!tip] 同源思想
> - **Wrong Assumptions** 对应 [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]——把假设逼到 SPEC 阶段说出来
> - **Overcomplexity** 对应 [[wiki/agent-engineering/philosophy/worse-is-better|Worse is Better]]、[[wiki/agent-engineering/philosophy/yagni-与-dry-反论]]
> - **Orthogonal Edits** 对应 [[enforce-invariants|Enforce Invariants, Not Implementations]]——让 lint/type 把"该改"和"不该改"分开
> - **Imperative over Declarative** 对应 [[wiki/agent-engineering/philosophy/spec-coding|Spec Coding]] 的"先写约束后写实现"思路

## 关联

- 工作流应对：[[gstack]]、[[sprint-七阶段范式]]、[[specialist-roles-模型]]
- 同族失败论：[[plausible-code]]、[[wiki/agent-engineering/philosophy/vibe-coding-的代价]]
- prompt vs workflow：[[wiki/claude-code/claude-rules|.claude/rules/]]、[[wiki/claude-code/auto-memory]]
- 跨 agent 适用：Karpathy 规则集是 agent / 模型无关的，跟 [[wiki/skills/agent-skills|Agent Skills]] 同样可跨 host
