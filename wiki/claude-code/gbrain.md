---
title: GBrain（agent 持久知识库）
tags: [gbrain, memory, mcp]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: stable
---

[GBrain](https://github.com/garrytan/gbrain) 是 Garry Tan 开源的 AI agent 持久知识库——可以理解为"agent 真正记住跨会话内容的地方"。注册成 [[mcp|MCP server]] 后，Claude Code 把 `gbrain search`、`gbrain put_page` 当成 first-class typed tool 调用。配套 [[gstack]] 的 `/setup-gbrain` skill 一条命令完成部署 + MCP 注册 + 信任策略。

## 三种部署路径（按门槛递增）

> [!compare] 选哪条
> | 路径 | 门槛 | 数据位置 | 用例 |
> |---|---|---|---|
> | **PGLite local** | 零账号、零网络、~30 秒 | 本机隔离 brain | 试用 / 本机长期单人 |
> | **Supabase 既有 URL** | 已有 Supabase project | 你已有的 Supabase | 多设备共享同一 brain |
> | **Supabase 自动 provision** | 一个 Supabase Personal Access Token | 自动新建 project | 想要云、不想自己点 UI |
>
> PGLite → Supabase 可平滑迁移（`/setup-gbrain --switch`），无需重头建知识。

## Per-Repo 信任三档

> [!important] 多客户场景的隔离
> 每个 repo 在你机器上独立标记三档之一：
> - **read-write**：agent 可搜可写——用于"主项目"
> - **read-only**：可搜不可写——用于"咨询多客户时的次要 repo"，不污染共享 brain
> - **deny**：agent 完全无法访问 brain——敏感项目
>
> 决定**跨 worktree 和分支保留**——你不会因为换分支就被反复问。
>
> 这跟 [[fail-closed-tool-defaults|Fail-Closed Tool Defaults]] 同源——**默认问一次、之后行为可预测**，比每次都拦截高效。

## 与 [[wiki/claude-code/auto-memory|Auto Memory]] 的差异

> [!compare] 三种"记忆"层次
> | 维度 | [[wiki/claude-code/auto-memory\|Auto Memory]] | [[continuous-checkpoint\|Continuous Checkpoint]] | GBrain |
> |---|---|---|---|
> | 范围 | 单项目 / 单用户偏好 | 单会话 / 单任务的中间状态 | 跨项目、跨会话、跨设备 |
> | 存储 | 本地文件（.claude/memory） | git commit 的 message body | Postgres / PGLite |
> | 接口 | 系统 prompt 注入 | git log + /context-restore | MCP 工具 (`search` / `put_page`) |
> | 适合 | "我喜欢 tabs"、"用户是数据科学家" | "试过 X 失败了正在试 Y" | "那个客户的 architecture 决策"、"上季度的 incident 教训" |
>
> 三者非互斥，覆盖不同时间尺度。

## GStack Memory Sync（不是同一个东西）

> [!warning] 名字相近、目的不同
> "GStack Memory Sync"是 gstack 的另一个 feature——用 git 把你的 gstack 状态（learnings / CEO plans / design doc / retros / developer profile）同步到一个**私有 repo**，让你的 agent 记忆跟你跨机器走。
>
> - 一次性 privacy 提示：allowlisted everything / artifacts only / off
> - Defense-in-depth secret scanner：AWS key、token、PEM block、JWT 离机前都被 block
>
> 跟 GBrain 解耦：sync 同步的是 gstack 内部状态，GBrain 同步的是 agent 工作中沉淀的"知识"。可单用、可叠用。

## 注册成 MCP 的优势

> [!example] typed tool vs bash shell-out
> 不注册 MCP 时，agent 调 GBrain 要走 bash：
> ```bash
> gbrain search "previous architecture decision"
> ```
> 输出是 stdout 字符串、agent 要 parse、错误处理糟糕。
>
> 注册成 [[mcp|MCP]] 后：
> ```
> tool: gbrain.search(query: "previous architecture decision")
> → typed result with structured fields
> ```
> 这是 [[mcp|MCP]] 在"持久知识"场景的标准用法——把任意外部工具升级成 first-class typed tool。

## 适合什么样的项目

> [!tip] GBrain 的甜蜜点
> - 长期项目（≥6 个月），有大量"为什么当初这样设计"的隐性决策
> - 多 repo / 多 worktree（[[parallel-sprints|10–15 并行 sprint]] 时尤其需要共享 codebase 知识）
> - 多客户咨询（read-only 模式防污染）
>
> **不适合**：
> - 一次性脚本、demo 项目
> - 团队里有强 Wiki 文化、决策已经在 Confluence/Notion 沉淀（重复工作）

## 关联

- 工具栈：[[gstack]]
- MCP 基础：[[mcp]]
- 同族记忆：[[wiki/claude-code/auto-memory|Auto Memory]]、[[continuous-checkpoint]]、[[handoff-md]]、[[kairos-记忆蒸馏]]
- 反例对照：[[wiki/agent-engineering/context/隐性知识与上下文|隐性知识]]——GBrain 是把它显性化的载体之一
- 编排上游：[[parallel-sprints]]——并行 sprint 多时 GBrain 价值显著
