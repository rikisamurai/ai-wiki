---
title: AI Code Review
tags: [ai-cr, code-review, anti-pattern]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！]]"
last-ingested: 2026-04-22
status: stable
---

AI Code Review（AI CR）是当下"工程效能标配"的热门方向，但很多团队的 AI CR 实际上在做 **Lint 已经能做好的事**——挑 `console.log`、纠 `let/const`、抓 React Hooks 误用。这违背了 [[shift-left|Shift Left]] 原则，把"应该编码时拦截"的问题推迟到了 PR 阶段。**核心原则：Lint 能做的事，不要交给 AI**；AI 的算力应该用在 Lint 表达不出来的私域业务逻辑上。

> [!warning] AI CR 的三大局限
> | 维度 | Lint | AI CR |
> |---|---|---|
> | **时机** | 编码时 / pre-commit（极早） | PR 提交后（偏晚） |
> | **速度** | 秒级反馈 | 分钟级 |
> | **确定性** | 通过 / 不通过 | 概率性，伴随幻觉与噪音 |
> | **成本** | 几乎为零 | 按 token 计费 |

**Review 疲劳**：当一个 PR 上有 20 条 AI 评论，其中 18 条是"建议改个变量名"，开发者会无视所有评论——包括那 2 条真正重要的。低信噪比的反馈比没有反馈更糟。

## 让 AI 各司其职

> [!example] 两个正确姿势
> - **AI 写 Lint**：把团队的特殊规范（如"所有 API 请求必须经过统一封装"）描述给 AI，让它生成 ESLint 自定义规则。范式见 [[ai-写-lint]]——AI 算力花一次，Lint 跑一辈子。
> - **AI CR 聚焦私域业务逻辑**：结合 PRD + 测试用例分析业务风险点，审查"并发竞态""缓存策略合理性"这类无法规则化的问题。这才是 AI 唯一不可替代的价值。

**和已有概念的关联**：AI CR 大量低价值评论是 [[review-带宽瓶颈|Review 带宽]]的二阶浪费——人不仅要 Review AI 产出，还要 Review AI 对 AI 产出的 Review。在 [[harness-engineering|Harness Engineering]] 的三层成熟度里，Lint + pre-commit + CI 属于 Architectural Constraints 层，是 AI CR 的前置基础设施，不是 AI CR 的替代品。

## 引申：扁鹊长兄

扁鹊说长兄医术最高——长兄治病于未发之前，世人不知其能。AI CR 像扁鹊在 CR 阶段"发现"问题；Lint + 工程基建像扁鹊长兄，在编码阶段就把问题拦截了。追求 AI CR 的"召回率"不如先把 Lint 基建搭好——投入产出比更高。
