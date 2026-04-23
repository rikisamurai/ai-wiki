---
title: Claude Code 六层架构
tags: [claude-code, architecture, mental-model]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-23
status: draft
---

把 [[claude-code|Claude Code]] 拆成六层来理解，是治理它的前提：**只强化其中一层就会失衡**。这套模型的价值不是"知识图谱"，而是**故障定位的查表**——结果不稳定查上下文层，自动化失控查控制层，长会话质量下降查会话层。

> [!compare] 六层职责
> | 层 | 职责 | 关键问题 | 对应页面 |
> |---|---|---|---|
> | **CLAUDE.md / rules / memory** | 长期上下文："是什么" | 加载顺序、信息密度 | [[claude-code-memory]] / [[claude-rules]] / [[auto-memory]] |
> | **Tools / MCP** | 动作能力："能做什么" | 工具数量、schema 大小 | [[mcp]] |
> | **Skills** | 按需方法论："怎么做" | 触发条件、描述符密度 | [[agent-skills]] / [[skill-编写实践]] |
> | **Hooks** | 强制执行 | 阻断点、性能 | [[hooks]] |
> | **Subagents** | 隔离上下文的工作者 | 权限收敛、产出格式 | [[wiki/ai-coding/subagent-上下文隔离]] |
> | **Verifiers** | 验证闭环 | 退出码 / 测试 / 监控 | [[wiki/ai-coding/验证驱动]] |

> [!important] 选层心法
> - 给 Claude **新动作能力** → Tool / MCP
> - 给它一套**工作方法** → Skill
> - 需要**隔离执行环境** → Subagent
> - 要**强制约束和审计** → Hook
> - **跨项目分发** → Plugin（打包以上几样）

**为什么"统一编排循环"在最外层**

六层之上还有一个最外层的循环：**收集上下文 → 采取行动 → 验证结果 → 完成 or 回到收集**。这个循环就是 Claude Code 的"心跳"。前五层都是为它服务的——CLAUDE.md/Skills 在"收集上下文"环节注入，Tools/MCP 在"采取行动"环节执行，Hooks/Subagents/Verifiers 在"验证结果"环节把关。

**与 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 的关系**：六层架构是 [[wiki/ai-coding/harness-成熟度|Harness 三层成熟度]]在 Claude Code 这个具体载体里的展开——L1 Prompt 对应单次调用，L2 Context Engineering 对应 CLAUDE.md/rules/memory 三层，L3 Workflow Automation 对应 Skills + Hooks + Subagents + Verifiers 四层。

> [!tip] 用六层视角排查问题
> 排查"Claude 表现奇怪"时按层逐查：
> 1. 它**知道**该做什么吗？→ 查上下文层（CLAUDE.md/Skills 是否触发）
> 2. 它**能**做吗？→ 查工具层（MCP 是否连上、权限是否允许）
> 3. 它**做对了**吗？→ 查 Verifier 层（有没有验证手段）
>
> 三层都过了还出问题，往往是上下文被噪声污染——参考 [[wiki/ai-coding/会话管理动作|会话管理动作]]。
