---
title: ai-wiki Activity Log
---

# Log

> append-only 时间线，记录所有 ingest / query / lint / migrate-next 操作。
> 格式：`## [YYYY-MM-DD HH:MM] <op> | <subject>`，便于 `grep '## \[2026-'`。

## [2026-04-22 16:30] init | ai-wiki 重构落地
- 建立 sources/ wiki/ .claude/commands/ 骨架
- 写入 4 个 slash commands
- 改写 AGENTS.md 为 LLM Wiki schema
- 创建 index.md / log.md / migration-backlog.md / *.base

## [2026-04-22 17:30] migrate-next | 1/41 · Agentic Coding 的边界
- 新建：[[wiki/ai-coding/agentic-coding]]、[[wiki/ai-coding/plausible-code]]、[[wiki/ai-coding/yagni-与-dry-反论]]、[[wiki/ai-coding/review-带宽瓶颈]]、[[wiki/ai-coding/隐性知识与上下文]]、[[wiki/ai-coding/worse-is-better]]
- source: sources/inbox/Agentic Coding 的边界.md

## [2026-04-22 17:36] migrate-next | 2/41 · Prefix Cache：Long Horizon Agent 的效率基石
- 新建：[[wiki/ai-coding/prefix-cache]]、[[wiki/ai-coding/kv-cache]]、[[wiki/ai-coding/long-horizon-agent]]、[[wiki/ai-coding/cache-命中率]]、[[wiki/ai-coding/cache-失效陷阱]]、[[wiki/ai-coding/稳定前缀-动态后缀]]、[[wiki/ai-coding/冻结快照模式]]
- source: sources/inbox/Prefix Cache：Long Horizon Agent 的效率基石.md

## [2026-04-22 17:42] migrate-next | 3/41 · 为什么你的"AI 优先"战略可能大错特错？
- 新建：[[wiki/ai-coding/ai-first-vs-ai-assisted]]、[[wiki/ai-coding/harness-engineering]]、[[wiki/ai-coding/vibe-coding]]、[[wiki/ai-coding/ai-first-工程前提]]、[[wiki/ai-coding/ai-first-适用边界]]、[[wiki/ai-coding/self-healing-loop]]、[[wiki/ai-coding/架构师-操作员二分]]
- source: sources/inbox/为什么你的"AI 优先"战略可能大错特错？.md

## [2026-04-22 17:51] migrate-next | 4/41 · 使用 Claude Code：会话管理与 100 万 上下文【译】
- 新建：[[wiki/ai-coding/context-window]]、[[wiki/ai-coding/context-rot]]、[[wiki/ai-coding/会话管理动作]]、[[wiki/ai-coding/compact-vs-clear]]、[[wiki/ai-coding/rewind-胜过纠正]]、[[wiki/ai-coding/subagent-上下文隔离]]
- source: sources/inbox/使用 Claude Code：会话管理与 100 万 上下文【译】.md
- 备注：subagent-上下文隔离 同时引用 source 7（搞懂缓存机制），届时 ingest 7 时复用

## [2026-04-22 17:55] migrate-next | 5/41 · 告别复制粘贴：浏览器一键剪藏到 Obsidian
- 新建：[[wiki/obsidian/obsidian-web-clipper]]、[[wiki/obsidian/inbox-工作流]]
- source: sources/inbox/告别复制粘贴：浏览器一键剪藏到 Obsidian.md
- 备注：obsidian 域首次 ingest，index.md Obsidian 段从占位符切到实链

## [2026-04-22 18:02] migrate-next | 6/41 · 我的 Vibe Coding 项目
- 新建：[[wiki/ai-coding/opc-一人公司]]、[[wiki/ai-coding/vibe-coding-的代价]]
- 更新：[[wiki/ai-coding/vibe-coding]]（加 cross-link 到代价）、[[wiki/ai-coding/架构师-操作员二分]]（加 idoubicc OPC 实证案例）
- source: sources/inbox/我的 Vibe Coding 项目.md

## [2026-04-22 18:15] migrate-next | 7/41 · 搞懂缓存机制，从 Gemma4 到 Claude Code 省 80% Token
- 新建：[[wiki/ai-coding/cache-keep-alive]]
- 更新：[[wiki/ai-coding/kv-cache]]（加 QKV 三角色 + Decoder-only 前提 + Gemma vs Qwen 实验）、[[wiki/ai-coding/prefix-cache]]（加 Claude Code 4-block 内部结构 + 两档 TTL + 断裂检测）、[[wiki/ai-coding/稳定前缀-动态后缀]]（加 DYNAMIC_BOUNDARY 源码佐证）、[[wiki/ai-coding/cache-失效陷阱]]（加第 6 陷阱"切换模型"）、[[wiki/ai-coding/subagent-上下文隔离]]（加 querySource+agentId 源码细节）
- source: sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token.md
- 备注：inbox 全部 7 条 ingest 完毕，下一步进入 posts/* 阶段

## [2026-04-22 18:30] migrate-next | 8/41 · 从投资视角分析 JS 开发者市场
- 新建：[[wiki/frontend/vercel]]、[[wiki/frontend/js-盈利模式分类]]、[[wiki/frontend/per-seat-licensing]]、[[wiki/frontend/headless-ui]]、[[wiki/frontend/shadcn-ui]]、[[wiki/frontend/webcontainers]]、[[wiki/frontend/bun]]、[[wiki/ai-coding/vibe-coding-对-saas-的通缩]]
- 更新：[[wiki/ai-coding/vibe-coding-的代价]]（加 cross-link 到 SaaS 通缩 + frontmatter 加 source）
- source: sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析.md
- 备注：frontend 域首次 ingest，index.md FrontEnd 段从占位符切到实链；posts/frontend 还剩 4 条

## [2026-04-22 18:42] migrate-next | 9/41 · No useEffect：Factory 团队的前端规则
- 新建：[[wiki/frontend/no-useeffect-rule]]、[[wiki/frontend/派生状态]]、[[wiki/frontend/usemounteffect]]、[[wiki/frontend/key-重置组件]]、[[wiki/frontend/组件强制函数]]
- source: sources/posts/frontend/React/Blog/Why we banned React's useEffect.md
- 备注：5 个 React 模式页面全部互链；强制函数 cross-link 到 ai-coding/agentic-coding + plausible-code

## [2026-04-22 18:59] migrate-next | 10/41 · FlashList
- 新建：[[wiki/frontend/flash-list]]、[[wiki/frontend/view-recycling]]
- source: sources/posts/frontend/React/React Native/learning/flash-list.md
- 备注：React Native 域首次 ingest；2 个页面互链

## [2026-04-22 19:05] migrate-next | 11/41 · React Native 核心组件
- 新建：[[wiki/frontend/react-native-core-components]]、[[wiki/frontend/pressable-vs-touchable]]
- source: sources/posts/frontend/React/React Native/learning/react-native-core-components.md
- 备注：核心组件页 cross-link 到 flash-list / view-recycling / pressable-vs-touchable

## [2026-04-22 19:08] migrate-next | SKIP · react-native tips
- SKIP 原因：源文件仅含一条外链（vercel-react-native-skills），无可抽取概念
- source: sources/posts/frontend/React/React Native/react-native tips.md

## [2026-04-22 20:44] migrate-next | 12/41 · HTTP/3 入门指南
- 新建：[[wiki/frontend/http-3]]、[[wiki/frontend/quic]]、[[wiki/frontend/head-of-line-blocking]]、[[wiki/frontend/0-rtt-握手]]、[[wiki/frontend/connection-migration]]
- source: sources/posts/obsidian/HTTP3 入门指南.md

## [2026-04-22 20:46] migrate-next | SKIP · Cross Walls
- SKIP 原因：仅为机场/客户端链接收藏，无可抽取概念，且主题不在 4 个 wiki domain 内
- source: sources/posts/obsidian/🧱Cross Walls.md

## [2026-04-22 20:55] migrate-next | 13/41 · obsidian-quick-start
- 新建：[[wiki/obsidian/knowledge-graph]]、[[wiki/obsidian/templater]]、[[wiki/obsidian/dataview]]、[[wiki/obsidian/para-方法]]、[[wiki/obsidian/zettelkasten]]、[[wiki/obsidian/moc-索引笔记]]
- 备注：Callouts/block-reference/内部链接 留给后续专题 source 各自专门页面
- source: sources/posts/obsidian/obsidian/🚀obsidian-quick-start.md

## [2026-04-22 21:05] migrate-next | 14/41 · Claudian - Obsidian × Claude Code
- 新建：[[wiki/obsidian/claudian]]、[[wiki/aigc/plan-mode]]、[[wiki/aigc/inline-edit]]、[[wiki/aigc/mcp]]、[[wiki/aigc/permission-modes]]
- 备注：aigc/ 首批入驻；Skills/Custom Agents 留给后续专题 source
- source: sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code.md

## [2026-04-22 21:18] migrate-next | 15/41 · obsidian-claude/skills (kepano)
- 新建：[[wiki/aigc/agent-skills]]、[[wiki/obsidian/obsidian-skills]]、[[wiki/obsidian/obsidian-bases]]、[[wiki/obsidian/json-canvas]]、[[wiki/obsidian/defuddle]]、[[wiki/obsidian/obsidian-cli]]
- source: sources/posts/obsidian/obsidian/obsidian-claude/skills.md

## [2026-04-22 21:25] migrate-next | 16/41 · obsidian-callouts
- 新建：[[wiki/obsidian/callouts]]
- 备注：单页面综合 Callout 语法/13 种内置类型/折叠/嵌套/CSS 自定义
- source: sources/posts/obsidian/obsidian/obsidian-tips/obsidian-callouts.md

## [2026-04-22 21:32] migrate-next | 17/41 · block-link-demo
- 新建：[[wiki/obsidian/block-reference]]
- 备注：source 主要是块引用语法演示；下一条 block reference use cases 会补充使用场景页
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/block-link-demo.md

## [2026-04-22 21:38] migrate-next | 18/41 · block reference use cases
- 新建：[[wiki/obsidian/block-reference-use-cases]]
- 更新：[[wiki/obsidian/block-reference]]（frontmatter sources 追加）
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 block reference use cases.md

## [2026-04-22 21:48] migrate-next | 19/41 · 内部链接（Internal Links）
- 新建：[[wiki/obsidian/wikilink]]、[[wiki/obsidian/embed-files]]、[[wiki/obsidian/aliases]]
- 备注：块引用部分已在 17/41、18/41 沉淀，此次不重复
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 内部链接（Internal Links）.md

## [2026-04-23 00:10] migrate-next | 26/41 · Claude Code 深度使用指南 - HiTw93
- 新建：[[wiki/aigc/claude-code-六层架构]]、[[wiki/aigc/handoff-md]]
- 更新：[[wiki/aigc/mcp]]（追加 MCP 隐形成本 + defer_loading）、[[wiki/aigc/skill-编写实践]]（追加三种类型 + 描述符 token 优化 + auto-invoke 频率分级）、[[wiki/ai-coding/compact-vs-clear]]（追加 Compact Instructions）、[[wiki/aigc/hooks]]（追加三层叠加：CLAUDE.md+Skill+Hook）、[[wiki/aigc/claude-code]]（链接六层架构 + HANDOFF.md）、[[wiki/aigc/claude-code-memory]]（NEVER/ALWAYS 模板 + #追加技巧）、[[wiki/aigc/agent-skills]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93.md
- 备注：本条主要走"追加补充"模式，深度指南扩展 25/41 建立的 CC 主框架

## [2026-04-22 23:35] migrate-next | 25/41 · Claude Code 最佳实践
- 新建：[[wiki/aigc/claude-code]]、[[wiki/ai-coding/验证驱动]]、[[wiki/ai-coding/探索-规划-编码-验证]]、[[wiki/aigc/hooks]]、[[wiki/ai-coding/两次纠正规则]]、[[wiki/ai-coding/writer-reviewer-模式]]、[[wiki/ai-coding/采访驱动-spec]]
- 更新：[[wiki/aigc/claude-code-memory]]、[[wiki/ai-coding/compact-vs-clear]]、[[wiki/ai-coding/rewind-胜过纠正]]、[[wiki/aigc/plan-mode]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践.md
- 备注：建立 wiki/aigc/claude-code.md 主框架页，后续 26/41 深度指南、28/41 claude-tips 走追加补充

## [2026-04-22 23:08] migrate-next | 24/41 · Claude Code Memory 机制详解
- 新建：[[wiki/aigc/claude-code-memory]]、[[wiki/aigc/claude-rules]]、[[wiki/aigc/auto-memory]]
- 更新：[[wiki/ai-coding/agents-md]]（指向 Claude Code 实现）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code Memory 机制详解.md

## [2026-04-22 22:58] migrate-next | 23/41 · Harness Engineering：Agent-First 时代利用 Codex
- 新建：[[wiki/ai-coding/agent-可读性]]、[[wiki/ai-coding/enforce-invariants]]、[[wiki/ai-coding/doc-gardening]]、[[wiki/ai-coding/高吞吐合并哲学]]
- 更新：[[wiki/ai-coding/harness-engineering]]（追加 Codex 案例 + 关联）、[[wiki/ai-coding/agents-md]]（追加 OpenAI 实证：目录而非百科）、[[wiki/aigc/渐进式披露]]（同原则映射到根目录）
- source: sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex.md

## [2026-04-22 22:48] migrate-next | 22/41 · 构建 Claude Code 的经验：如何使用 Skills
- 新建：[[wiki/aigc/skills-9-分类]]、[[wiki/aigc/渐进式披露]]、[[wiki/aigc/skill-编写实践]]
- 更新：[[wiki/aigc/agent-skills]]（追加深入章节，frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/blog/🛠️ 构建 Claude Code 的经验：如何使用 Skills.md

## [2026-04-22 22:38] migrate-next | 21/41 · AI CR 的理想与现实
- 新建：[[wiki/ai-coding/ai-code-review]]、[[wiki/ai-coding/shift-left]]、[[wiki/ai-coding/ai-写-lint]]
- 更新：[[wiki/ai-coding/review-带宽瓶颈]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！.md

## [2026-04-22 21:57] migrate-next | 20/41 · 从 Spec Coding 到 Harness
- 新建：[[wiki/ai-coding/spec-coding]]、[[wiki/ai-coding/约束悖论]]、[[wiki/ai-coding/ralph-loop]]、[[wiki/ai-coding/agent-等待时间]]、[[wiki/ai-coding/agents-md]]、[[wiki/ai-coding/行为正确性]]、[[wiki/ai-coding/harness-成熟度]]、[[wiki/ai-coding/任务三维划分]]
- 更新：[[wiki/ai-coding/harness-engineering]]（追加约束悖论/反应式生长/三层成熟度等关联，frontmatter sources 追加）、[[wiki/ai-coding/vibe-coding]]（TL;DR 补 Karpathy 出处与"大号 demo"，frontmatter sources 追加）
- 备注：开启 posts/aigc 第一条；OpenClaw / 自定义 Skills / Bytedcli 等留作后续 source 专题
- source: sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结.md
