---
title: Harness 三层成熟度
tags: [harness-engineering, framework, maturity]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
last-ingested: 2026-04-22
status: draft
---

Martin Fowler 把 [[harness-engineering|Harness Engineering]] 的完整体系归纳为三层，可用来评估当前团队的成熟度。**大多数团队处于第一、二层的初级阶段**——第三层 Entropy Management 才是 Harness 能否持续运转的关键，也是最容易被忽视的一层。

> [!compare] 三层框架
> | 层次 | 内容 | 典型实践 |
> |---|---|---|
> | **Context Engineering** | 给 Agent 正确的上下文 | [[agents-md\|AGENTS.md]]、[[隐性知识与上下文\|Skills]]、文档体系 |
> | **Architectural Constraints** | 刚性的架构约束 | 分层规则、Lint、CI/CD 作为核心基础设施 |
> | **Entropy Management** | 对抗熵增 | 持续清理 AI slop、[[行为正确性\|行为正确性]]验证 |

**为什么第三层最难**：前两层是一次性投入的基础设施，建好就放在那。Entropy Management 是日常的、持续的——AI 每天产出新的 slop，你每天要消化或挡住。它没有"完成"状态，只有"维持"状态。

**自检清单**

- 你的 CI 能挡住语法错、测试挂、Lint 失败吗？→ Architectural Constraints 已建立
- 你的 AGENTS.md 是高密度的关键信息，不是百科全书吗？→ Context Engineering 已建立
- 你有机制定期清理过时代码、压缩重复抽象、验证用户价值 E2E 吗？→ Entropy Management 才刚起步

相关：[[约束悖论]]、[[agent-等待时间]]
