---
title: Subagent 模式 vs Team 模式
tags: [workflow, multi-agent, claude-code]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: draft
---

[[claude-code|Claude Code]] 提供的两种多 Agent 协作模式——**Subagent 模式**（hub-and-spoke，主 agent 派单 + 子 agent 单向汇报）和 **Team 模式**（队友间可直接沟通、共享任务列表、长连接）。前者适合一次性独立子任务，后者适合需要反复协作的工作。

## 核心差异

> [!compare] 4 个维度的对比
> | 特性 | Subagent 模式 | Team 模式 |
> |---|---|---|
> | **沟通方式** | 子 agent 只向主 agent 汇报 | 队友之间可直接沟通 |
> | **协调方式** | 主 agent 管理一切（hub-and-spoke） | 共享任务列表、自我协调 |
> | **生命周期** | 任务完成即结束 | 队友保持空闲状态直到被关闭 |
> | **信息可见性** | 主 agent 只看到最终结果 | 主 agent 和队友可随时交换信息 |

## 各自适合什么

> [!example] 选哪个
> | 场景 | 推荐 | 理由 |
> |---|---|---|
> | 全栈：前端 + 后端并行写代码 | **Subagent** | 两个任务独立、SDD 已对齐接口、不需要中途互相问 |
> | Code review：分别跑 lint / security / design review | **Subagent** | 每个 review 独立、产出汇总给主 agent |
> | 研究 → 计划 → 实现的级联 | **Subagent**（顺序） | 每步只需上一步结果 |
> | 长跑 sprint：多角色（CEO / EM / QA）反复参与 | **Team** | 角色之间需要互相挑战、共享上下文 |
> | 调试：debugger 找 bug → fixer 修 → tester 验 | **Team** | fixer 修完要让 tester 直接验，少走主 agent 这道弯 |

## 与 [[coordinator-模式|Coordinator 模式]] 的位置关系

> [!important] 三层抽象
> | 抽象层 | 对应 |
> |---|---|
> | **范式层** | [[coordinator-模式\|Coordinator 模式]]——经理派单的思想 |
> | **机制层** | Subagent 模式 / Team 模式（Claude Code 的两种实现） |
> | **应用层** | [[subagent-driven-development\|SDD]]、[[specialist-roles-模型\|Specialist Roles 模型]]、[[parallel-sprints\|Parallel Sprints]] |
>
> Coordinator 模式是哲学，Subagent / Team 是 Claude Code 提供的两个具体执行原语。

## Subagent 配置 schema

> [!example] 一个 subagent 的最小配置
> ```json
> {
>   "description": "前端代码生成专家",
>   "tools": ["Read", "Edit", "Write", "Bash", "Grep"],
>   "permissionMode": "bypass",
>   "model": "sonnet",
>   "skills": ["前端编码规范"]
> }
> ```
>
> 关键字段：
> - **tools**：限制工具集 = 限制爆炸半径（典型 [[fail-closed-tool-defaults|Fail-Closed]] 思路）
> - **permissionMode**：`bypass` / `safe` / `plan`（参见 [[permission-modes|权限模式]]）
> - **model**：每个 subagent 可用不同模型（小任务用 haiku 省钱）
> - **skills**：注入特定 [[wiki/skills/agent-skills|Skill]] 让子 agent 进入"专家心态"

## 全栈开发的典型派单

> [!example] 多 subagent 协作架构
> ```
> 主 Agent（你在对话的 Claude Code）
>   ├── Subagent 1：读前端 SDD → 写前端代码
>   │     ├── model: sonnet
>   │     ├── tools: Read, Edit, Write, Bash
>   │     └── 任务：按 tasks.md 生成前端组件
>   │
>   ├── Subagent 2：读后端 SDD → 写后端代码
>   │     ├── model: sonnet
>   │     ├── tools: Read, Edit, Write, Bash
>   │     └── 任务：按 tasks.md 生成后端接口
>   │
>   └── Subagent 3：（可选）生成接口 Mock 数据
>         ├── model: haiku
>         └── 任务：根据后端 SDD spec.md 生成 Mock
> ```

## 实践建议

> [!tip] 4 条心法
> | 建议 | 说明 |
> |---|---|
> | **SDD 先行** | 确保 SDD 已对齐接口契约后再启动并行——否则两个 subagent 输出对不上 |
> | **一个 Agent 一个职责** | 不要让一个 subagent 同时干前端和后端，单一职责才便于调试 |
> | **接口契约是桥梁** | 前端 subagent 依赖的接口定义 = 后端 subagent 实现的接口定义 |
> | **分阶段验证** | 配合 [[三阶段联调]]——前端 Mock 验证、后端编译验证、最后联调 |

## Cursor 那边怎么实现

> [!compare] Cursor vs Claude Code 多 agent
> Cursor 的多 Agent 是**多 Tab 并行 Composer 会话**——每个 Tab 一个独立 Agent，UI 上可视。Claude Code 的 Subagent 是程序化派出，没有可视化窗口（除非用 [[parallel-sprints|Conductor]] 之类工具）。
>
> 两者底层范式相同（subagent 模式），UI 形态不同。

## 关联

- 范式上游：[[coordinator-模式]]、[[subagent-driven-development]]
- 应用：[[specialist-roles-模型]]、[[parallel-sprints]]、[[全栈工作区]]
- Claude Code 集成：[[claude-code]]、[[permission-modes]]、[[fail-closed-tool-defaults]]
- 工具栈：[[cursor]]、[[gstack]]
- 上下文隔离：[[subagent-上下文隔离]]
