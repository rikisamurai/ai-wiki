---
title: Codebase Indexing
tags: [retrieval, cursor, code-search]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: draft
---

[[cursor|Cursor]] 等 IDE 类 AI 工具的**项目级语义索引**：对工作区内所有代码做向量化嵌入，建立检索结构，让 AI 能用自然语言查询找到相关代码片段而不依赖精确路径。是 [[mimic-first-harness|Mimic-First Harness]] 在工程层的关键基础设施——没有索引，"找模仿对象"会退化成手工 grep。

## 它解决什么

> [!example] 没索引 vs 有索引
> | 场景 | 没索引（[[claude-code\|Claude Code]] 现状） | 有索引（[[cursor\|Cursor]]） |
> |---|---|---|
> | "场景欢迎语是怎么实现的" | AI 用 grep 试 keyword，命中率看模型能力 | 语义检索直接定位 Controller / Service / 前端组件 |
> | "照着欢迎语写结束语" | 你必须手动 @ 引用所有相关文件 | AI 自动检索到欢迎语的前后端完整链路 |
> | 跨仓库引用 | 完全做不到（每仓单独 grep） | 在 [[全栈工作区\|多仓工作区]] 下统一索引、跨仓识别调用关系 |

## 为什么"语义"比 grep 强

> [!important] grep 的盲区
> grep 找的是字符串。它找不到：
> - "处理用户付款的代码" → 实际函数叫 `handleCheckout` / `processOrder` / `pay()`，没字符串"用户付款"
> - "我们的 API 错误处理范式" → 散在 N 个 middleware / decorator 里，没单一关键词
> - "和登录相关的所有逻辑" → auth 模块 + session 中间件 + cookie 工具，名字毫无共同 prefix
>
> 语义索引把代码（含注释、函数名、调用关系）embed 成向量，用 query embedding 做近邻召回——"语义上相关"就够了，不需要字面匹配。

## 索引的工程代价

> [!tip] 不是免费的
> Cursor 的实测：
> - **首次索引**几分钟（中型 repo）—— "确保索引完成后再开始让 AI 生成代码"
> - **持续维护**：commit / pull / 文件改动后增量更新索引
> - **存储**：embedding + 元数据本地缓存（一般几十 MB ~ 几 GB）
>
> 这是为什么 [[claude-code|Claude Code]] 类 CLI 默认不带——CLI 假设你随时换项目，全量索引每个项目代价高。CLI 选 grep + LLM 推理替代，trade off 是检索质量。

## 与 [[wiki/retrieval/rag/rag|RAG]]、[[wiki/retrieval/rag/agentic-rag|Agentic RAG]] 的关系

> [!compare] 三种检索范式
> | | 传统 RAG | Agentic RAG | Codebase Indexing |
> |---|---|---|---|
> | 索引对象 | 文档 chunk | 文档 chunk + 工具 | 代码（函数级 / 文件级 / 项目级） |
> | 触发方式 | pipeline 自动召回 | agent 决定何时检索 | 同时支持 agent 主动检索 + IDE 隐式注入 |
> | 召回粒度 | top-k chunk | agent 决定 | 函数 + 调用链 |
> | 跨"文档"理解 | 弱（chunk 之间无语义关联） | 中等 | 强（call graph / type hierarchy） |
>
> Codebase Indexing 是 RAG 在代码域的特化——索引粒度更细、能利用代码的结构信息（AST、调用图、类型）。

## 与 [[mimic-first-harness|Mimic-First Harness]] 配套

> [!important] 索引让"找模仿对象"自动化
> Mimic-First Harness 要 AI 模仿已有实现——但 AI 怎么找到要模仿的实现？
> - **手工**：你 @ 文件路径——每次都要你想"哪个文件最像"
> - **Codebase Indexing**：AI 自己用语义检索找——你只需描述要做什么
>
> 两者协同：
> - **冷启动**：你用手工 @ 引导，培养 AI 对项目结构的理解
> - **稳态**：依赖索引让 AI 自主找参照，你只给业务描述

## 为什么得物把 Cursor vs Claude Code 的差异主要归到这一点

得物文章里 Cursor vs Claude Code 全栈开发对比表的**第一行**就是：
- Cursor：grep + 代码段语义相似度检索 / 速度快、理解能力全面
- Claude Code：仅支持 grep / 准确度严重依赖模型能力

这是工具选型的关键变量——团队全栈开发场景下 Codebase Indexing **几乎决定了 AI 的有效性**。Claude Code 类 CLI 工具补这块的方向：[[wiki/claude-code/mcp|MCP]] 接外部索引服务、[[wiki/claude-code/gbrain|GBrain]] 类持久知识库、[[wiki/claude-code/handoff-md|HANDOFF.md]] 风格的人工"索引摘要"。

## 关联

- 上游战术：[[mimic-first-harness]]
- 同源检索范式：[[wiki/retrieval/rag/rag|RAG]]、[[wiki/retrieval/rag/agentic-rag|Agentic RAG]]、[[wiki/retrieval/rag/hybrid-retrieval|混合检索]]
- 工具栈：[[cursor]]、[[claude-code]]
- 跨仓拓展：[[全栈工作区]]
- 同源知识持久化：[[wiki/claude-code/gbrain|GBrain]]
