---
title: KAIROS 模式与记忆蒸馏
tags: [claude-code, memory, kairos]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-23
status: draft
---

KAIROS 是 [[claude-code|Claude Code]] 源码里的一个实验性 [[auto-memory|Auto Memory]] 模式：长会话中的记忆按日期写入**追加式日志**，由一个 `/dream` 技能在"夜间"（用户低活跃期）自动运行，把原始日志**蒸馏**成结构化的主题文件。

> [!example] 数据流
> ```
> 长会话发生 → 追加到原始日志
>   logs/2026/03/2026-03-30.md
>   logs/2026/03/2026-03-31.md
>
>          ↓ 低活跃期 /dream 蒸馏
>
>   memory/user_preferences.md   ← 用户口味/偏好
>   memory/project_context.md    ← 项目背景/约束
>   memory/api_conventions.md    ← API 设计决策
> ```

**关键设计：写入和提炼分离**

把记忆系统拆成两个阶段是这个设计的核心：

| 阶段 | 时机 | 成本 | 信息密度 |
|---|---|---|---|
| **追加日志** | 实时 | 几乎为零 | 低（原始材料） |
| **蒸馏** | 异步、低活跃期 | 一次 LLM 调用 | 高（结构化主题） |

实时阶段不能跑昂贵的"决定要不要记忆"判断——会拖慢主对话。**异步蒸馏**让昂贵的归类工作不出现在用户路径上。这也是大多数离线 ETL 的思路——只是搬到了 AI 记忆系统里。

**与 AI 检索记忆配合**

Claude Code 的[[auto-memory|Auto Memory]] 不靠关键词搜索找记忆，而是用 Sonnet 扫描所有记忆文件的标题和描述、选出最多 5 条最相关的全文注入。蒸馏阶段产出的**结构化主题文件**远比原始日志好检索——标题清晰、描述精确，召回质量直接受益于蒸馏质量。

> [!tip] 你也可以手动模拟 KAIROS
> 如果你的 Claude Code 还没启用 KAIROS，可以手动复刻：
> 1. 长会话结束时让 Claude 把今天的关键发现追加到 `logs/YYYY-MM-DD.md`
> 2. 周末跑一次："读 `logs/2026/04/*.md`，整理出 user_preferences.md / project_context.md，去重合并"
> 3. 平时让 Claude 直接读这些主题文件，不读原始日志
>
> 本质是 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 在记忆维度的反应式生长——**先记下来再说，定期把噪声蒸馏成知识**。

**为什么叫 KAIROS**：希腊语里 chronos 是"线性时间"，kairos 是"恰当的时机"。这个命名暗示了设计意图——记忆**不是按时间均匀流动的，而是在合适的时机才被沉淀**。
