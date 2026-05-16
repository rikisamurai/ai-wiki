---
title: Harness 协同进化原则
tags: [harness, philosophy, design]
date: 2026-05-16
sources:
  - "[[sources/clippings/深度拆解：AI Agent Harness 的构造【译】]]"
last-ingested: 2026-05-16
status: draft
---

**随着模型能力提升，Harness 的复杂程度应该逐渐降低**——这是 Harness 与 LLM 之间的协同进化关系。模型在训练时已将 Harness 的存在纳入考量；如果 Harness 设计得好，当模型升级时，无需增加复杂度，性能就会自动提升。

> [!note] 脚手架类比
> 建筑脚手架是临时性基础设施，让工人触及原本够不到的高度。脚手架本身不盖房子，但没有它，工人就上不去高层。**房子盖好后，脚手架要拆除**。这正是 Harness 的演化方向：随模型变强而变薄，但永远不会消失。

即便最强大的模型，也需要 Harness 来管理窗口、执行代码、保存状态并验证工作。变薄的是机械化逻辑，不变的是架构职责。

## 七个 Harness 设计维度

每个 Harness 架构师都要在这 7 个维度做取舍：

| 维度 | 选项 A | 选项 B | 默认倾向 |
|---|---|---|---|
| **规模** | 单 Agent | 多 Agent | 先充分挖掘单 Agent 上限 |
| **决策模式** | ReAct（灵活但贵） | 先规划后执行（快） | 视任务边界清晰度 |
| **上下文策略** | 摘要对话 | 动态按需加载 | 动态加载 |
| **验证机制** | 硬性代码测试 | LLM-as-judge | 两者组合 |
| **权限风格** | 速度优先自动批准 | 安全优先步步确认 | 视操作可逆性 |
| **工具范围** | 暴露所有工具 | 最小当前所需 | 最小工具集 |
| **Harness 厚度** | 逻辑大量写死 | 最大程度留给模型 | 随模型变强逐渐变薄 |

**最关键的维度是"Harness 厚度"**：多少逻辑编码进系统，多少逻辑留给模型动态决定。这条边界随模型能力的提升而移动。

## 实证：改 Harness 比换模型影响更大

LangChain 的实验数据：**仅改变 Harness 架构**（模型参数不变），在 TerminalBench 2.0 基准上排名从 30 名开外提升至第 5 名。另一项研究让 LLM 自己优化 Harness 架构，实现了 76.4% 的通过率，超过人类精心设计的系统。

## 相关页面

- [[harness-engineering|Harness Engineering]] — Harness 工程的核心理念
- [[llm-as-cpu|LLM = CPU 类比]] — Harness 的架构定位：操作系统层
- [[harness-成熟度|Harness 三层成熟度]] — 如何评估 Harness 的工程成熟度
- [[agent-loop|Agent Loop]] — Harness 的核心运行时
