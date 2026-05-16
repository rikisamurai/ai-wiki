---
title: LLM = CPU 类比
tags: [harness, mental-model, philosophy]
date: 2026-05-16
sources:
  - "[[sources/clippings/深度拆解：AI Agent Harness 的构造【译】]]"
last-ingested: 2026-05-16
status: draft
---

Beren Millidge（2023）的类比：**原生 LLM 就像一个没有内存、没有硬盘、没有 I/O 设备的 CPU**。它只能计算，无法感知或持久化。Agent 系统实际上是在重新发明冯·诺依曼架构（Von Neumann Architecture）。

> [!note] 完整类比映射
> | 计算机组件 | Agent 系统对应 | 特点 |
> |---|---|---|
> | **CPU** | LLM 模型本身 | 纯计算，无状态 |
> | **RAM（内存）** | 上下文窗口 | 快但容量有限 |
> | **HDD（硬盘）** | 外部数据库 / 文件系统 | 大但速度慢 |
> | **设备驱动** | 工具集成 | 与外部系统交互 |
> | **操作系统** | [[harness-engineering|Agent Harness]] | 统筹调度一切 |

这不是比喻，而是架构同构：任何需要持久化状态、I/O 交互和资源调度的计算系统，都会自然演化出这五个层次。

## 三层工程化同心圆

从这个视角出发，Agent 工程化从内到外分三层：

1. **提示词工程**（Prompt Engineering）：精心设计模型接收到的指令
2. **上下文工程**（Context Engineering）：管理模型在什么时间点能看到什么内容（[[context/dynamic-context|动态上下文]]）
3. **Harness 工程**（Harness Engineering）：覆盖上述两层，再加上工具编排、状态持久化、错误恢复、验证循环、安全执行和生命周期管理

三层的关键区别：Harness 不是"AI Wrapper"（只包裹提示词的套壳），而是**让模型能够自主行动的完整系统**。

## 一条简单定义

> **"如果你不是模型本身，那你就是 Harness。"** — Vivek Trivedy, LangChain

这条定义抓住了 Harness 的边界：模型权重之外的一切——调用逻辑、状态管理、工具执行、错误处理——都是 Harness 的一部分。

## 相关页面

- [[harness-engineering|Harness Engineering]] — Harness 的核心工程哲学
- [[agent-loop|Agent Loop]] — Harness 的核心运行时：ReAct 主循环
- [[context/context-rot|Context Rot]] — RAM（上下文窗口）的容量限制问题
- [[harness-协同进化|Harness 协同进化]] — 随模型能力提升，Harness 应如何演化
