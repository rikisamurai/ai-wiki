---
title: CONTEXT.md 项目词汇表
tags: [ddd, agent-context, workflow]
date: 2026-05-26
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Matt Pocock Skills - 人类满分工程师的自我蒸馏]]"
last-ingested: 2026-05-26
status: draft
---

CONTEXT.md 是项目根目录下一份**人与 AI 共享的领域词汇表**——把项目里出现的概念、流程、状态转移等 jargon 用一两句话定义清楚，让后续会话里人和 AI 可以用 1 个术语而不是 20 个词描述同一件事。它是 Eric Evans"统一语言"（[Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html)）在 AI 编码时代的具体落地。

> [!example] 写 vs 不写
> - **没有 CONTEXT.md**：「当课程某节课被'真实化'（即在文件系统中获得位置）时出现了问题」
> - **有 CONTEXT.md**：「materialization cascade 出了问题」
>
> 一个对话里省下来的不止 token，更是"对方需要在头脑里重新搭模型"的成本。

> [!important] AI 比人更需要词汇表
> 人类工程师有时间慢慢从代码里悟出概念，AI 每开一个新会话都是冷启动。把团队隐性概念 ([[wiki/agent-engineering/context/隐性知识与上下文|隐性知识]]) 写进 CONTEXT.md，等于给 AI 一份**可缓存的领域 onboarding**——既省解释成本，也避免 AI 用近义词漂移出团队语境。

## 与其它"项目级 markdown 文件"的分工

| 文件 | 作用 | 谁读 |
|------|------|------|
| `CONTEXT.md` | 共享词汇定义、流程命名 | 人 + AI |
| [[wiki/claude-code/claude-code-memory\|CLAUDE.md / AGENTS.md]] | 工作约束、风格、禁止项 | AI 为主 |
| `SHARED-CONTEXT.md`（[[wiki/agent-engineering/workflow/sub-agent-纪律\|sub-agent 纪律]]） | 多 sub-agent 共享任务 briefing | sub-agent 第一动作必读 |
| `HANDOFF.md`（[[wiki/claude-code/handoff-md\|跨会话交接]]） | 当下进度、决策、下一步 | 下一会话冷启动 |

> [!compare] CONTEXT.md vs CLAUDE.md
> CLAUDE.md 说"怎么做"（"测试用 vitest"、"先读再编"），CONTEXT.md 说"是什么"（"materialization cascade = 把课程层级映射到文件系统的过程"）。两者**不要混写**——CONTEXT.md 一旦塞了规范，AI 会按规范执行而忘了它本来只是查词；CLAUDE.md 一旦塞词汇表，词汇就会和约束一起被压缩或截断。

## 维护节奏

1. **/grill-with-docs 触发**：Matt Pocock 的做法是每次"烤问会话"（grill）之后，把会话里 AI 新学到的概念追加到 CONTEXT.md
2. **ADR 配套**：重大决策走 [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]] 出 ADR，CONTEXT.md 只放术语本身，不放决策理由（理由进 ADR）
3. **手动触发**：发现自己第二次在解释同一个东西 → 立即让 AI 把它写进 CONTEXT.md

> [!tip] 写词汇表的格式建议
> - 一行一个术语，加粗术语 + 一两句定义
> - 涉及实体关系时附 1 张简图（mermaid 或 ASCII），AI 在跨术语推理时受益最大
> - 不写常识词（"组件"、"hook"）——只写**项目独有**的命名

## 关联

- 思想根：[[wiki/agent-engineering/philosophy/人人对齐-人机对齐|人人对齐 → 人机对齐]]——团队自己没词汇表，CONTEXT.md 写完也是各人各解
- 兄弟概念：[[wiki/agent-engineering/context/隐性知识与上下文|隐性知识]]、[[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]
- 上层框架：[[wiki/skills/matt-pocock-skills|Matt Pocock Skills]]（CONTEXT.md 是其四大支柱之一）
