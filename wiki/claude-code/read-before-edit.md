---
title: Read-Before-Edit 铁律
tags: [claude-code, tool-design, safety]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-23
status: draft
---

[[claude-code|Claude Code]] 的 FileEditTool 内置一条硬规则：**调用 Edit 前必须先在同一会话里 Read 过该文件**——没读直接报错，不让改。这是源码层强制的安全不变量，不是模型自觉。这条铁律解释了为什么 Claude Code 不会"凭空写一段代码覆盖你的文件"。

> [!example] 这条规则的力量
> ```
> 用户：把 src/auth.ts 里的 JWT 过期时间改成 1 小时
> Claude：[直接 Edit] → 报错：Must Read file first
> Claude：[先 Read src/auth.ts] → 现在能 Edit
> ```
> 强制 Read 的副产品是：Claude 在 Edit 前**必然看到了文件当前状态**——不会基于"它以为该文件长什么样"去改。

**为什么不靠模型自觉**

理论上模型可以"被训练成习惯先 Read 再 Edit"。但 [[wiki/agent-engineering/philosophy/agentic-coding|Agentic Coding]] 场景下：

- 长会话中模型会**忘记**文件被外部进程改过
- 模型可能**幻觉**文件内容，写出基于错误前提的 diff
- 训练时的"建议性"规则在压力下会被模型自己合理化绕过

把规则写进**工具实现**，模型连绕过的可能都没有——这是 [[wiki/agent-engineering/workflow/enforce-invariants|Enforce Invariants]] 在 Agent 工具层的应用。

**与 [[fail-closed-tool-defaults|Fail-Closed 默认]]同源**：两者都是"不要让模型决定安全"——Fail-Closed 在工具属性层，Read-Before-Edit 在工具调用顺序层。共同思路：**把可被模型违反的规则"硬化"成工具/系统强制约束**。

> [!tip] 在自己的工具里加同款检查
> 写自定义工具时，凡是"修改外部状态"的操作都该带前置条件检查——比如：
> - DB 写工具要求先有一次 SELECT/EXPLAIN
> - 部署工具要求先有一次 dry-run
> - 文件删除工具要求先列出将要删除的文件
>
> 不是为了卡住 Agent，而是为了让"修改"必然基于"观察"——这与 [[wiki/agent-engineering/workflow/验证驱动|验证驱动]] 的"提供反馈源"是同一逻辑的两端。
