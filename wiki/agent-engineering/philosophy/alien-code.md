---
title: AI 外星代码（Alien Code）
tags: [ai-coding, anti-pattern, code-quality]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: draft
---

得物团队给"AI 凭空生成的代码"起的形象名字：**外星代码**——能跑、看似实现了需求，但**和项目现有代码格格不入**。三个典型病征：风格不一致、复用率低、采纳率低。它跟 [[plausible-code|plausible code]] 是同族失败，但侧重点不同——前者是"写对了但不像本项目写的"，后者是"看着对其实不对"。

## 三个典型病征

> [!example] 怎么辨认外星代码
> | 病征 | 表现 |
> |---|---|
> | **风格不一致** | 命名规范不同（camel/snake 混用）、目录结构不同、分层方式不同 |
> | **复用率低** | 没用项目已有的公共组件、工具函数、请求封装、错误处理 |
> | **采纳率低** | Code Review 时同事看到"外来风格"的代码会产生大量修改意见 |
>
> 净结果：**AI 生成了代码，但 Review 成本和返工成本反而更高了**——这是 AI 编码声称"提效"但实际"增加摩擦"的最常见根因。

## 与 [[plausible-code|plausible code]] 的对照

> [!compare] 同族但不同病
> | 维度 | plausible code | 外星代码 |
> |---|---|---|
> | 表面 | 看起来正确 | 风格不像本项目 |
> | 实质问题 | 实际不正确 | 正确但不可维护 / 不被采纳 |
> | 谁能发现 | 跑测试或仔细 review 才能发现 | code review 第一眼就能看出来 |
> | 解法 | 加测试、加 [[wiki/agent-engineering/workflow/读-transcript\|review]] | [[mimic-first-harness\|找模仿对象]] + [[codebase-indexing\|代码库索引]] |
>
> 两者经常**叠加出现**：AI 既写了风格不对的代码（外星），又在某些边界 case 上写错了（plausible）。先治外星（短期 high signal），再深挖 plausible（需要 eval/测试投入）。

## 根因：AI 没有项目上下文就只能凭"通识"

> [!important] 通识能力是把双刃剑
> AI 模型有"写 Python web 服务"的通识能力——给个需求它确实能生成跑得起来的 FastAPI + SQLAlchemy 代码。但你的项目可能：
> - 用 Flask 不用 FastAPI
> - 用 Tortoise ORM 不用 SQLAlchemy
> - 接口分层是 Controller/Service/Repository 不是 router/handler
>
> AI 不知道这些就只能按它训练数据里的"主流写法"生成——主流 = 外星。

## 解法栈

> [!tip] 治外星代码的四件事
> 1. **[[mimic-first-harness|找模仿对象]]**：每次 prompt 给 AI 指向已有相似实现
> 2. **[[codebase-indexing|Codebase Indexing]]**：让 AI 通过语义检索自己找到模仿对象
> 3. **[[wiki/claude-code/claude-rules|.claude/rules/]]** / [[wiki/agent-engineering/workflow/agents-md|AGENTS.md]]**：把团队规范 / 反模式硬编码进 system prompt
> 4. **[[采纳率|采纳率]] 监控**：把"外来风格"导致的高改动率作为生产指标，跌破阈值就告警
>
> 单靠任何一条都不够——4 件事一起上才能压住外星代码的发生率。

## 与 [[karpathy-四种失败模式|Karpathy 四种失败]] 的对应

外星代码主要对应 **Wrong Assumptions**（AI 假设"主流写法 = 团队写法"）和 **Imperative over Declarative**（AI 不知道项目有 declarative 工具如 schema/decorator/config）的混合。Karpathy 列的 4 类是机制级根因；外星代码是它们叠加产生的可观测现象。

## 一个早期信号

> [!warning] 当你听到这句话
> 团队同事开始说："这 PR 一看就是 AI 写的、不像我们项目的代码"——这是外星代码已经成系统问题的信号。这时候要做的不是"AI 改用新模型"，而是回头补上面 4 条解法栈。

## 关联

- 解法：[[mimic-first-harness]]、[[codebase-indexing]]、[[全栈工作区]]
- 同族失败：[[plausible-code]]、[[karpathy-四种失败模式]]
- 度量：[[采纳率]]、[[wiki/agent-engineering/workflow/keep-rate|Keep Rate]]
- 团队规范持久化：[[wiki/claude-code/claude-rules|.claude/rules/]]、[[wiki/agent-engineering/workflow/agents-md|AGENTS.md]]
