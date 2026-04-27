---
title: HANDOFF.md 跨会话交接
tags: [claude-code, session-management, technique]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-23
status: stable
---

HANDOFF.md 是开新会话前**让 Claude 自己写的"交接信"**——记录进度、尝试过什么、什么有效、下一步该做什么。它解决的是 [[wiki/ai-coding/compact-vs-clear|/compact 的有损本质]]带来的信息丢失问题：默认压缩算法会把架构决策和约束理由当无关内容删掉。

> [!example] 标准触发
> 长会话快爆 / 准备 `/clear` 之前，发一条：
> ```
> 当前任务还没收尾。请把目前进度写入 HANDOFF.md，包括：
> - 已完成的部分（具体到文件和函数）
> - 关键决策（为什么选 A 不选 B）
> - 已尝试但被否决的方案（避免下次重试）
> - 下一步具体动作
> - 验证命令（测试/构建/lint）
> ```
> 然后 `/clear`，新会话起手让 Claude 读 HANDOFF.md。

**与 ["从这里开始总结"](compact-vs-clear) 的差异**

| 维度 | `summarize from here` | HANDOFF.md |
|---|---|---|
| **载体** | 对话内文字（消息） | 文件（git 可追踪） |
| **跨会话** | 复制粘贴 | 直接 `Read HANDOFF.md` |
| **跨人** | 难（你的对话别人看不到） | 容易（同事可接手） |
| **持久性** | 关掉窗口可能丢 | 文件常驻 |

**与 Compact Instructions 的分工**

[[wiki/ai-coding/compact-vs-clear|Compact Instructions]]（写在 CLAUDE.md 里告诉 `/compact` 保留什么）是**自动**机制，HANDOFF.md 是**手动**机制：

- `/compact` 适合任务还没换、只是想腾空间——Compact Instructions 控制保留方向
- HANDOFF.md 适合任务进入新阶段 / 要换会话 / 要换人——把"刚学到的教训"显式化

> [!tip] HANDOFF.md 也是项目沉淀
> 这种文件不仅给"下一个会话"读，也是给"下一个开发者"的最佳交接。Tw93 的实践：HANDOFF.md 写完 commit，PR 描述就是它的内容。**短期 = 会话交接，长期 = 项目知识库**——和 [[claude-code-memory|CLAUDE.md]] 形成互补：CLAUDE.md 是不变的契约，HANDOFF.md 是当下的进度。

**与 [[wiki/ai-coding/采访驱动-spec|采访驱动 SPEC]] 同构**：两者都是"让 Claude 把当前会话的隐性信息显性化到文件"，区别只是时机——SPEC.md 在任务**开始前**写，HANDOFF.md 在任务**未完成时**写。
