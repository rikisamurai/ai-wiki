---
title: AI 写 Lint
tags: [pattern, lint, ai-cr]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！]]"
last-ingested: 2026-04-22
status: draft
---

不要让 AI 在 PR 阶段反复检查"团队特殊规范是否被违反"，而是**让 AI 把规范一次性翻译成 ESLint 自定义规则**。AI 算力花一次，Lint 跑一辈子。这是把 [[ai-code-review|AI CR]] 的概率性、滞后反馈，转换成 Lint 的确定性、即时反馈的范式。

> [!example] 流程
> 1. 把团队规范用自然语言描述给 AI（"所有 API 请求必须经过 `@/utils/request` 封装"、"禁止在组件中直接调用 `localStorage`"）
> 2. AI 生成对应的 ESLint 规则
> 3. 加入项目配置（含 pre-commit hook 和 CI 卡点）
> 4. 编码时编辑器直接报错，提交时 hook 直接拦截

工具参考：[eslint-gpt](https://github.com/ycjcl868/eslint-gpt)——输入示例代码即可生成 ESLint 规则。

> [!compare] AI CR 方案 vs AI + Lint 方案
> | | AI CR 方案 | AI + Lint 方案 |
> |---|---|---|
> | **执行频次** | 每次 PR 都跑一遍 | 规则写好后零成本运行 |
> | **确定性** | 概率性，可能漏报误报 | 100%，零遗漏 |
> | **反馈时机** | PR 阶段（违背 [[shift-left]]） | 编码时 + pre-commit |
> | **成本** | 持续按 token 计费 | 一次性生成 |

**适用条件**：规范本身能被规则表达。如果规范是"这个缓存策略在高流量下是否合理"这种需要上下文理解的判断，就只能留给 [[ai-code-review|AI CR]] 或人工 Review，落不到 Lint 层。

这条范式在 [[harness-engineering|Harness Engineering]] 视角下属于 Architectural Constraints 层的扩展——把 AI 当作"规则生成器"而不是"规则执行器"。
