---
title: 采访驱动 SPEC
tags: [spec-coding, claude-code, technique]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
  - "[[sources/posts/aigc/ai-coding/tools/Superpowers - AI 编码工作流框架]]"
last-ingested: 2026-04-23
status: stable
---

对于较大的功能，**让 Claude 反过来采访你**——用 `AskUserQuestion` 工具深挖你可能没考虑的边界情况、UI/UX 细节、技术权衡，最后把完整规格写进 `SPEC.md`。然后**开新会话**用 SPEC.md 执行实现。这是 [[spec-coding|Spec Coding]] 在 Claude Code 里最自然的落地方式。

> [!example] 提示词模板
> ```
> 我想构建 [简要描述]。用 AskUserQuestion 工具深入采访我。
>
> 问技术实现、UI/UX、边界情况、顾虑和权衡。
> 不要问显而易见的问题，挖掘我可能没考虑到的难点。
>
> 采访完成后，将完整规格写入 SPEC.md。
> ```

**为什么颠倒提问方向有用**

直接让 Claude 实现，它只能基于"你已经想到并说出口的"信息——而真正的失败往往来自"你没想到所以没说"的边界。让 Claude 主动采访，相当于让它扮演资深 PM/架构师角色，逼出隐性需求。这是把 [[隐性知识与上下文|隐性知识]] 显性化的具体技巧。

> [!tip] 采访完务必开新会话
> 采访阶段的对话历史很长，包含大量你回答时的犹豫和探索。用同一个会话直接实现，相当于带着 [[context-rot|噪声]] 进入编码——**SPEC.md 写完后 `/clear` 开新会话**，干净上下文里只读 SPEC.md，专注实现。

**与 [[spec-coding|Spec Coding]] 的差异**

| 维度 | 传统 Spec Coding | 采访驱动 SPEC |
|---|---|---|
| **谁写 SPEC** | 人写 / Architect 写 | Claude 通过采访收集，Claude 落笔 |
| **触发场景** | 先有需求文档，再交给 AI | 你只有模糊想法，Claude 帮你梳理 |
| **耗时** | 前期投入大 | 一次会话 + 一次 /clear |
| **适用** | 团队有产品经理 | 个人项目 / 早期探索 |

**与 [[约束悖论|约束悖论]] 的关系**：采访让你被迫提前回答"边界条件"，把约束写在 SPEC 里——这正是约束悖论的正向应用：**约束写得早，自由度反而高**，因为减少了 Claude 在实现期"猜你意图"的发挥空间。

> [!example] [[wiki/aigc/superpowers|Superpowers]] 把它做成了 Skill
> Superpowers 框架的第一步 `brainstorming` Skill 走的就是这套——苏格拉底式提问 + 把 Spec 切成可消化小块给你确认。差别是 Superpowers 不止采访，还接 `writing-plans` 把 SPEC 转成 2-5 分钟粒度的实施计划，再转 `subagent-driven-development` 串起来。也就是说，**采访驱动 SPEC 是入口，Superpowers 是把入口接到完整流水线**。
