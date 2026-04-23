---
title: Skill 编写实践
tags: [agent-skills, best-practice, claude-code]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🛠️ 构建 Claude Code 的经验：如何使用 Skills]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-22
status: draft
---

写 [[agent-skills|Skill]] 的核心心智：Skill 是**文件夹 + 配置**，不是 markdown 文件。Anthropic 内部几百个 Skills 沉淀出的实践，可以归为下面几条钢律。它们和 [[skills-9-分类]]、[[渐进式披露]] 一起构成完整的 Skill 工程化方法。

> [!important] 不要说显而易见的事
> Claude 对代码库已经非常了解。Skill 的价值在于**打破 Claude 的常规思维**——比如 Anthropic 的 `frontend-design` Skill 反复迭代去避免 Inter 字体和紫色渐变这种"AI 套路"。如果 Claude 默认就会做对的事情，写在 Skill 里只是浪费 token。

**踩坑点章节是信息密度最高的部分**。任何 Skill 中信息量最大的就是 Gotchas 章节，应该根据 Claude 真实使用 Skill 时遇到的失败逐步积累。Skill 的进化路径就是一个"踩坑→沉淀→规则化"的循环——和 [[harness-engineering|Harness Engineering]] 的反应式生长是同构的。

**`description` 字段是给模型看的，不是给人看的**。Claude Code 启动会话时会构建可用 Skills 清单，通过扫 description 判断何时触发。所以 description **不是摘要而是 if-then 条件**——读起来更像"当用户在 vault 内编辑 .md 文件时"而不是"Obsidian Markdown 编辑工具"。

> [!warning] 不要把 Claude 限制得太死
> Skills 复用性强，**指令不要写得太具体**。给 Claude 需要的信息，但留给它适应具体情况的灵活性。死板的 step-by-step 在跨场景复用时反而成为负担。

**存储脚本与生成代码**。给 Claude 提供脚本和库，让它把精力花在组合编排上——决定下一步做什么，而不是重新构造样板。这条与 [[渐进式披露]] 协同：脚本不进上下文，需要时才执行。

**记忆与数据存储**。Skills 可以通过存数据实现记忆——简单 JSON / 文本日志或 SQLite。数据应存在稳定文件夹（如 `${CLAUDE_PLUGIN_DATA}`），避免 Skill 升级时丢失。例如 `standup-post` 可以保留 `standups.log`，下次运行时让 Claude 读历史记录知道"从昨天到现在变了什么"。

**按需 Hooks（On Demand Hooks）**。Skills 可以包含只在被调用时才激活的 Hooks，整个会话期间保持生效。典型例子：

- `/careful` — 通过 PreToolUse 拦截 `rm -rf`、`DROP TABLE`、`force-push` 等危险操作
- `/freeze` — 阻止对特定目录之外的任何写操作，调试时防止误改

**衡量 Skill 效果**。用 PreToolUse hook 在内部记录 Skill 使用情况，能看到哪些 Skills 受欢迎、哪些触发率低于预期。这是 [[harness-engineering|Harness Engineering]] 在 Skill 维度的应用——把"Skill 是否有效"也变成可观测信号。

> [!compare] Skill 三种典型类型
> Tw93 的实践把 Skills 进一步归为三种工程化模式（与 [[skills-9-分类|9 大分类]] 是不同维度的切法）：
> | 类型 | 用途 | 关键字段 | 例 |
> |---|---|---|---|
> | **检查清单型** | 质量门禁 | 列表 + Pass/Fail | `release-check`：build / clippy / version 全过才放行 |
> | **工作流型** | 标准化操作 | 步骤 + Rollback | `config-migration`：dry-run → apply → verify → rollback |
> | **领域专家型** | 决策框架 | Decision Matrix | `runtime-diagnosis`：症状 → 首要排查项 → 根因分类 |
>
> 工作流型和领域专家型常带 `disable-model-invocation: true`——副作用大、必须显式触发。

**描述符 token 优化是高 ROI 操作**。每个启用的 Skill，描述符常驻上下文。把"This skill helps you review code changes in Rust projects, checks for common issues like unsafe code..."（~45 tokens）压成 `Use for PR reviews with focus on correctness.`（~9 tokens），跨 20 个 Skills 就是几百 token。Tw93 的 auto-invoke 频率分级：

- **高频（>1 次/会话）**：保持 auto-invoke，优化描述符
- **低频（<1 次/会话）**：`disable-auto-invoke`，手动触发省描述符
- **极低频（<1 次/月）**：移除 Skill，改成文档
