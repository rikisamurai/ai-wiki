---
title: Anthropic Managed Agents Memory（append-only event log + /mnt/memory）
tags: [anthropic, memory, claude-code]
date: 2026-06-03
sources:
  - "[[sources/clippings/State of Memory in Agent Harness]]"
last-ingested: 2026-06-03
status: draft
---

Managed Agents 是 Anthropic 的 hosted agent runtime，不是本地 [[claude-code|Claude Code]] 的延伸。它的 memory 设计有两个不寻常的选择：**session 是不可变的 append-only event log**——rollback 和审计是架构默认而不是补丁；**memory 以文件系统形式 mount 在 `/mnt/memory/`**，多 agent 可并发共享一个 store，每次 write 都是不可变版本。它的目标读者是 multi-agent 工作流，不是个人长期记忆。

## 两个关键架构选择

> [!note] append-only event log
> session 内发生的所有事件**只追加不修改**，于是：
> - **rollback 是免费的**——回到任意 event 之前的状态
> - **审计是免费的**——完整 history 永远可重放
> - **冲突解决变简单**——多个 agent 写入不会破坏过去事件，只是追加新事件
>
> 这与 [[continuous-checkpoint|Continuous Checkpoint Mode]]的精神一致：状态变化用追加，不用 in-place 修改。

> [!note] /mnt/memory/ 作为文件系统
> memory store mount 成路径：
> - 每个 workspace 最多 **8 个 store**
> - 每个 store **~100KB**
> - 每次 write 产生一个**不可变 version**
> - 多 agent 可并发挂同一个 store，操作落到 history 而不是冲突上

文件系统语义意味着 agent 用熟悉的 read/write 操作就能用 memory，不需要专门的 API。这与 [[skill-编写实践|Skill]] 把能力封成"可读文件"的思路相邻。

## Shortcoming：不是个人记忆设计

> [!warning] workspace-scaled，不是 user-scaled
> Managed Agents memory 是为 **multi-agent coordination at workspace scale** 设计的：
> - 100KB / store 容量上限低
> - workspace 作为最小作用域 → **个人跨 session 上下文**没有合适的层
> - 要在它之上再 pattern 出"我的偏好""我的历史"
>
> 想要个人记忆层，要么用 [[mem0|Mem0]] 类外部基础设施，要么自己在 workspace 之上做 sharding。

## 与本地 Claude Code 的关系

> [!compare] hosted vs local
> | 维度 | Managed Agents | [[claude-code\|Claude Code]] local |
> |---|---|---|
> | **运行位置** | Anthropic 托管 | 用户机器 |
> | **session 模型** | append-only event log | 单 session 内可变 |
> | **memory 介质** | `/mnt/memory/` 文件系统 + 不可变 version | 本地 markdown（[[auto-memory\|auto memory]] / CLAUDE.md） |
> | **多 agent 共享** | 内建（共享 store + history） | 通过 [[coordinator-模式\|coordinator]] 在 prompt 层协调 |
> | **作用域** | workspace | 仓库 / 用户 |
> | **回滚** | 架构内建 | 靠 git / [[continuous-checkpoint\|checkpoint]] |

两条路线服务不同场景：本地走"单人 + 单仓库 + IDE 紧耦合"；Managed Agents 走"团队 + 多 agent 并发 + 长期托管"。

## 与 AWS Bedrock AgentCore 的对比

AWS 的同位产品 **Bedrock AgentCore** 也是 hosted runtime + 托管 memory，但选择不同：

- **AgentCore Memory** 跑三个异步提取策略（语义事实 / 偏好 / 叙事摘要），extract ~20–40s，retrieve ~200ms
- 改变的事实标 **INVALID** 而不是删除，保留 lineage
- 公布的 benchmark：LoCoMo 70.58 / PrefEval 79 / PolyBench-QA 83.02——但 LoCoMo 数字明显落后于 leading memory 系统（参考 [[memory-benchmarks]] 对 LoCoMo 本身可信度的批评）

> [!compare] 两条 hosted agent memory 路线
> | 维度 | Anthropic Managed Agents | AWS Bedrock AgentCore |
> |---|---|---|
> | **memory 范式** | 文件系统 + 不可变 version | 异步提取 + INVALID 标记 |
> | **回滚** | 免费（append-only） | 用 INVALID 保 lineage |
> | **检索** | filesystem read（应用层决定） | 内建 retrieval（结构化） |
> | **生态锁定** | Anthropic 平台 | AWS 平台 |
> | **典型 shortcoming** | workspace-scaled，不是个人记忆 | 生态锁定 + LoCoMo 分数落后 |

## 相关页面

- [[memory-three-tiers|Agent Memory 三层]] — Managed Agents 是 external 层的 hosted 版本
- [[memory-harness-shortcomings|Harness Memory 五大共同短板]] — Managed Agents 因 hosted 架构绕开了 staleness 和 isolation 的部分问题，但没解决跨 workspace 的个人记忆
- [[claude-code|Claude Code]] · [[auto-memory|Claude Code Auto Memory]] — Anthropic 的本地路线
- [[coordinator-模式|Coordinator 模式]] — multi-agent 协调的另一种实现
- [[mem0|Mem0]] — workspace 之上叠加个人记忆的一种方案
