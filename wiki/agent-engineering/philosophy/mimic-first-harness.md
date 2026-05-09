---
title: Mimic-First Harness（找模仿对象）
tags: [harness, philosophy, ai-coding]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: stable
---

[[harness-engineering|Harness Engineering]] 在战术层最干脆的实操：**给 AI 一个已有的实现作为参照，让它照着复刻一份，而不是凭空创造**。得物团队的总结："就像给一个新入职的工程师说'你照着这个模块的风格，写一个类似的'，而不是'你自由发挥'——前者往往能更快产出符合团队规范的代码。"

## 四条具体原则

> [!example] Mimic-First 操作规范
> | 原则 | 怎么落地 |
> |---|---|
> | **找相似实现** | 先在代码库找到功能最相似的已有实现作为参照 |
> | **复用优先** | 能复用的组件、接口封装、数据结构直接复用，不再写一份新的 |
> | **模仿着复制** | 哪怕"抄一份改一改"也比"用新方式写"好——用新方式 = 引入风格分裂 |
> | **约束生成范围** | 在 prompt 里**明确指定参考文件、参考接口**（@filepath 引用） |

## prompt 上的对照

> [!compare] 凭空创造 vs Harness 约束
> | 凭空创造（不推荐） | Harness 约束（推荐） |
> |---|---|
> | "请实现一个结束语管理的 CRUD 接口" | "请参照现有'场景欢迎语'功能（后端接口 `/api/v1/feature/list`，前端入口 `FeatureTable/index.tsx:53-58`）实现'结束语'功能。数据结构、分层方式、命名风格都保持一致。新增场景 code：`categoryCode = 'SCENARIO_CLOSING'`" |
>
> 差距不在于 AI 是否"聪明"，而在于**给了 AI 多少约束和上下文**。约束越精准，生成代码的可用性越高。

## 与 [[harness-engineering|Harness Engineering]] 的层次关系

> [!important] 战略 vs 战术
> - **Harness Engineering**（战略）：构建让 AI 安全跑的整套系统——monorepo、确定性流水线、可读日志、自动审查门
> - **Mimic-First Harness**（战术）：每次给 AI 写 prompt 时给参照
>
> 两者必须配合——
> - 战略层缺：参照存在但 AI 看不到（碎片化代码库、无 [[codebase-indexing|Codebase Indexing]]）→ 战术层失效
> - 战术层缺：好基础设施但每次 prompt 都让 AI 自由发挥 → AI 写出 [[alien-code|外星代码]]，前面的工程投入被浪费

## 为什么不让 AI 发挥它的"通识能力"

> [!warning] 通识 ≠ 项目契合
> AI 的通识能力让它能写**通用上**正确的代码，但项目里"对"的代码定义不只是通用正确：
> - 命名要符合团队规范
> - 错误处理要走项目封装而非裸 try/catch
> - 数据访问要走 Repository 不能直接拿 ORM 调
> - HTTP 请求要走团队 axios 拦截器封装
>
> AI 没参照只能猜——猜对一次也未必下次还猜对。**给参照的成本远低于事后纠正"看起来对但风格不对"的成本**——这是 [[plausible-code|plausible code]] 在团队规范层面的对应。

## 与 [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]、[[spec-coding|Spec Coding]] 的关系

> [!compare] 三种"约束写在哪"
> | 范式 | 约束载体 |
> |---|---|
> | [[spec-coding\|Spec Coding]] | 自然语言 Spec 文档 |
> | [[wiki/agent-engineering/workflow/采访驱动-spec\|采访驱动 SPEC]] | AI 反过来采访用户填的 SPEC.md |
> | **Mimic-First Harness** | **指向已有代码的 @ 引用** |
>
> Mimic-First 是三者里**最具体、最可执行**的——直接指 commit、行号、接口名。它的隐含前提是"项目已有相似实现"，所以适合**在成熟代码库的增量开发**，不适合 0→1。

## 关联

- 上游战略：[[harness-engineering]]、[[wiki/agent-engineering/philosophy/yagni-与-dry-反论|YAGNI 反论]]
- 战术配套基础设施：[[codebase-indexing]]（让 AI 真的能找到参照）、[[全栈工作区]]（跨仓库的参照）
- 反例：[[alien-code|AI 外星代码]]、[[plausible-code]]
- 同源约束论：[[约束悖论]]——更高自主性需要更严格约束
- 适用边界：[[ai-first-适用边界]]——0→1 项目缺参照时这条范式弱
