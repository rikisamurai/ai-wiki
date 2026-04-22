---
title: Spec Coding
tags: [spec-coding, ai-coding, methodology]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
last-ingested: 2026-04-22
status: draft
---

Spec Coding（规约编程）是对 [[vibe-coding|Vibe Coding]] 的反思——先把需求写成详尽的 Spec，再让 AI 按 Spec 生成代码。它解决了 Vibe Coding 的"许愿编程"问题，但引入了新的痛点：**Spec 自身的维护成本与生命周期问题**——代码会演进，作为快照的 Spec 几乎注定腐烂成技术负债。这一困境催生了下一阶段的 [[harness-engineering|Harness Engineering]]。

## 三种实践形态

> [!compare] 三流派对比
> | 形态 | 核心理念 | 优点 | 核心挑战 |
> |---|---|---|---|
> | **规即源码 (Spec-as-source)** | Spec 是唯一源文件，人只改 Spec，代码全由 AI 生成 | 终极自动化 | 自然语言模糊性 → 微小修改可能产生巨大代码差异；模型迭代让结果难以复现 |
> | **以规为锚 (Spec-anchored)** | 同时维护 Spec 和代码，Spec 作为后续迭代参考（如 Spec-Kit） | 理想与现实的平衡 | 流程可能死板；Spec 的历史价值有限，最终仍会过时 |
> | **先规后码 (Spec-first)** | 仅在单次迭代前写 Spec，用完即抛 | 务实易落地 | 一次性 Spec 解决不了长期维护；过时 Spec 反而误导新人与模型 |

## 为什么走向 Harness

Spec Coding 暴露三大难题：人工测试/Review 耗时、Spec 遵守性差、Spec 维护成本高。OpenAI 因此提出 [[harness-engineering|Harness Engineering]]——**与其依赖易变的自然语言 Spec，不如构建一个刚性的、自动化的"约束"环境**。在 Harness 视角下，"测试用例是最好的文档"，CI/CD 保证的测试集远比静态 Markdown 文档更可靠、更与时俱进。

相关：[[agentic-coding]]、[[ai-first-vs-ai-assisted]]
