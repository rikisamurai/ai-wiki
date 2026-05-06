---
title: 动态上下文（Dynamic Context）
tags: [context, harness, evolution]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: draft
---

动态上下文是"agent 在工作过程中**按需拉取**信息进上下文窗口"的工程范式，对照面是**静态 guardrails**（会话开始就一次性塞给 agent 的代码库布局、语义匹配片段、附件压缩等）。[[cursor|Cursor]] 在 2024 末到 2026 初的演进可视作这条路线的样本：模型能力变强后，原本的护栏被大量撤掉、改由模型自己决定何时拉取何种上下文。

## 静态 guardrails 时代

> [!example] 早期 Cursor 的静态做法
> - 会话开始预先喂代码库**文件夹布局**
> - 用 embedding 选**语义匹配片段**
> - 用户**附件**压缩后塞进系统 prompt
> - 每次编辑后**主动喂 lint / 类型错误**给 agent
> - 限制单轮工具调用次数
> - 改写"读太少行"的文件读取请求
>
> 那时模型自选上下文能力弱，护栏是必需的——否则 agent 容易陷入读不到关键信息或读太多 token 的两个极端。

## 动态拉取时代

> [!important] 模型变强后的策略反转
> 模型可靠后：
> - 静态注入**大幅缩减**——只保留实用兜底（OS、git status、当前/最近查看文件）
> - 大量决定权下放给模型——它自己 grep、读文件、调工具拿"实时"上下文
> - **当下需要才拉**：过往对话、活跃终端会话、相关 MCP 工具按需进窗口

这是一个具体的"模型能力 ↔ 上下文工程"互动范例：模型变强 → 护栏减少 → harness 简化 → 上下文窗口被填的方式更"实时"。

## 与 [[wiki/agent-engineering/context/稳定前缀-动态后缀|稳定前缀-动态后缀]] 的关系

> [!compare] 两个层次
> | 维度 | 稳定前缀-动态后缀 | 动态上下文 |
> |---|---|---|
> | 优化目标 | KV/prefix cache 命中率 | 信息时新性 + token 效率 |
> | 控制方 | harness 设计者 | 模型自身（通过工具） |
> | 何时填 | 整个会话生命周期 | 推理过程中按需 |
>
> 两者非互斥——稳定前缀仍然存在（指令、工具描述、当前 git status 等），动态后缀里的"什么时候拉什么"决策权交给模型。

## 为什么不能直接全量动态化

> [!warning] 全动态的隐性代价
> 完全靠模型自选上下文有几个问题：
> - **冷启动慢**：每次新会话都要让模型先 explore 才能开始干活
> - **遗漏关键信息**：模型不知道"它不知道"——某些隐性约束（团队规范、安全策略）必须强制注入
> - **token 浪费**：模型容易反复读相同文件，没有 cache 优化
>
> 所以 Cursor 文章里强调"我们仍会提供一些实用的静态上下文"——动态化是**比例转换**，不是**全或无**。

## 与其他工具的对照

> [!example] 同范式的不同实现
> - **[[claude-code|Claude Code]]**：靠 [[wiki/skills/agent-skills|Skills]] + [[wiki/skills/渐进式披露|渐进式披露]]——按需加载长 markdown，不一次性塞完
> - **[[codex|Codex]]**：sandbox + approval 双维度让 agent 在受控环境里自己探
> - **[[wiki/retrieval/rag/agentic-rag|Agentic RAG]]**：retrieval 决策权下放给 agent 而不是 pipeline
> - **[[wiki/retrieval/browser/agent-browser|agent-browser]]**：浏览器内容也是动态上下文的一种来源
>
> 都是"模型变强 → 上下文获取从'pipeline 编排'转为'agent 自决策'"的具体实例。

## 关联

- 上游：[[harness-engineering]]、[[cursor]]
- 同源 context 工程：[[wiki/agent-engineering/context/context-window]]、[[wiki/agent-engineering/context/稳定前缀-动态后缀]]、[[wiki/agent-engineering/context/隐性知识与上下文]]
- 风险面：[[wiki/agent-engineering/context/context-rot|Context Rot]]、[[context-anxiety]]——动态上下文如果让窗口塞满会触发新问题
- agentic 化：[[wiki/retrieval/rag/agentic-rag]]
