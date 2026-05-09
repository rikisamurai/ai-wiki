---
title: Cursor
tags: [cursor, ide, agent-harness]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: stable
---

Cursor 是 Anysphere 出品的 AI 代码编辑器，2024 年末开始走 [[harness-engineering|harness-engineering]] 路线——把 IDE 包成一个完整的 agent 框架。它的思路跟 [[claude-code|Claude Code]]、[[codex|OpenAI Codex CLI]]、[[gstack|gstack]] 同源（都是把模型 + 工具 + 上下文管理打包），但形态不同：Cursor 是 GUI-first、内嵌编辑器；Claude Code/Codex 是 CLI-first；gstack 是 Skill 包。

## 核心工程实践

> [!note] Cursor 公开过的 harness 实践
> - **[[dynamic-context|动态上下文]]**：从 2024 年末"模型不会自选上下文 → 静态 guardrails 喂饱"演进到 2026 年"模型按需 dynamic 拉取"
> - **[[cursorbench|CursorBench]]**：公开 benchmark 跨时间对比 agent 质量
> - **[[keep-rate|Keep Rate]]**：用户保留多少 AI 改动作为质量度量
> - **[[语义满意度信号]]**：LLM 读用户回复推断"用户是否满意"
> - **[[工具错误分类法]]**：InvalidArguments / UnexpectedEnvironment / ProviderError / UserAborted / Timeout 五类预期错误
> - **[[per-model-harness|每模型定制 harness]]**：OpenAI 偏 patch 编辑、Anthropic 偏 string-replace；prompt 也按 provider 分别写
> - **[[mid-chat-model-switch|聊天中途切换模型]]**：自动切换 prompt + 工具集 + 注入"中途接手"指令
> - **[[context-anxiety|Context Anxiety]]**：观察到的模型怪癖，通过 prompt 缓解

## 跟其他 AI 代码工具的边界

> [!compare] Cursor vs Claude Code vs Codex vs gstack
> | 维度 | Cursor | [[claude-code\|Claude Code]] | [[codex\|Codex]] | [[gstack\|gstack]] |
> |---|---|---|---|---|
> | 形态 | GUI / IDE | CLI | CLI | Skill 包（装在 Claude Code 上） |
> | 模型 | 多 provider（OpenAI / Anthropic / Cursor 自训 Composer 等） | Anthropic 为主 | OpenAI | 跨 10 个 host |
> | Harness 重点 | 编辑器内嵌 + 多模型切换 + 动态上下文 | Subagents / Skills / Hooks | Sandbox + Approval 双维度 | 23 个角色 sprint 流水线 |
> | Benchmark | [[cursorbench\|CursorBench]] 公开 | Anthropic 内部 | OpenAI 内部 | 借用其他 benchmark + `gstack-model-benchmark` |

## 协同编排是 framework 的、不是 agent 的

> [!important] Cursor 的范式判断
> 文章末尾的判断："系统不再把每个子任务都交给单一智能体处理，而是学会在专业化的智能体和子智能体之间进行委派"——这跟 [[specialist-roles-模型|gstack 的多角色模型]]、[[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 同向。
>
> Cursor 把"协同编排能力"明确归到 **framework 层而非 agent 本身**——这是 [[harness-engineering|Harness Engineering]] 范式最干脆的表态：单 agent 性能不是终点，**让多 agent 协作的那一层才是关键资产**。

## Cursor 自动化软件工厂

文章里描述的内部流程跟 [[self-healing-loop|Self-Healing Loop]] 是同一范式：**每周自动 agent 扫日志 → 找新出现/激增问题 → Linear 建/更新 工单 → 修复 → 验证**。Cursor 还把 [Linear 触发 cloud agent](https://cursor.com/blog/linear) 作为产品化能力。

## 子智能体作为模型切换的替代

> [!tip] 切换模型的两条路
> 用户想换模型时有两个选择：
> 1. **[[mid-chat-model-switch|聊天中途切换]]**——同一 thread，自动切 framework，但要处理缓存失效和"对话历史是别的模型生成的"问题
> 2. **请求 [[subagent-driven-development|子智能体]] 用特定模型跑**——干净 context 起步，避开切换成本
>
> 第 2 条更干净，是 Cursor 推荐姿势。这跟 [[subagent-上下文隔离]] 的设计哲学一致。

## 关联

- 范式：[[harness-engineering]]、[[per-model-harness]]、[[dynamic-context]]
- 度量：[[cursorbench]]、[[keep-rate]]、[[语义满意度信号]]
- 工程：[[工具错误分类法]]、[[mid-chat-model-switch]]、[[context-anxiety]]
- 同族工具：[[claude-code]]、[[codex]]、[[gstack]]、[[everything-claude-code]]
- 自动化运维：[[self-healing-loop]]、[[doc-gardening]]
