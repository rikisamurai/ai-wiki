---
title: ai-wiki Index
date: 2026-04-22
---

# ai-wiki

> [!note] 三层架构
> `sources/`（原料，只读） · `wiki/`（精华，可改） · `AGENTS.md`（schema）
>
> 用 `/ingest` `/query` `/lint` `/migrate-next` 操作。详见 [[AGENT]]。

## AI Coding

- [[wiki/ai-coding/agent-可读性|Agent 可读性（Legibility）]]
- [[wiki/ai-coding/agent-工作量分布|Agent 工作量分布（90% 在 AI 之外）]]
- [[wiki/ai-coding/agent-等待时间|Agent 等待时间（Human Wait）]]
- [[wiki/ai-coding/agentic-coding|Agentic Coding]]
- [[wiki/ai-coding/agents-md|AGENTS.md]]
- [[wiki/ai-coding/ai-code-review|AI Code Review]]
- [[wiki/ai-coding/ai-first-vs-ai-assisted|AI First vs AI-Assisted]]
- [[wiki/ai-coding/ai-写-lint|AI 写 Lint]]
- [[wiki/ai-coding/ai-first-工程前提|AI First 工程前提]]
- [[wiki/ai-coding/ai-first-适用边界|AI First 适用边界]]
- [[wiki/ai-coding/cache-keep-alive|Cache Keep-Alive]]
- [[wiki/ai-coding/cache-命中率|Cache 命中率]]
- [[wiki/ai-coding/cache-失效陷阱|Cache 失效陷阱]]
- [[wiki/ai-coding/compact-vs-clear|Compact vs Clear]]
- [[wiki/ai-coding/context-rot|Context Rot]]
- [[wiki/ai-coding/context-window|Context Window]]
- [[wiki/ai-coding/doc-gardening|Doc Gardening Agent]]
- [[wiki/ai-coding/enforce-invariants|Enforce Invariants, Not Implementations]]
- [[wiki/ai-coding/harness-engineering|Harness Engineering]]
- [[wiki/ai-coding/harness-成熟度|Harness 三层成熟度]]
- [[wiki/ai-coding/kv-cache|KV Cache]]
- [[wiki/ai-coding/long-horizon-agent|Long Horizon Agent]]
- [[wiki/ai-coding/opc-一人公司|OPC（一人公司）]]
- [[wiki/ai-coding/plausible-code|Plausible Code（似是而非的代码）]]
- [[wiki/ai-coding/prefix-cache|Prefix Cache]]
- [[wiki/ai-coding/ralph-loop|Ralph Loop]]
- [[wiki/ai-coding/review-带宽瓶颈|Review 带宽瓶颈]]
- [[wiki/ai-coding/rewind-胜过纠正|Rewind 胜过纠正]]
- [[wiki/ai-coding/self-healing-loop|Self-Healing Loop]]
- [[wiki/ai-coding/shift-left|Shift Left]]
- [[wiki/ai-coding/spec-coding|Spec Coding]]
- [[wiki/ai-coding/subagent-上下文隔离|Subagent 上下文隔离]]
- [[wiki/ai-coding/subagent-driven-development|Subagent-Driven Development（每任务一个 subagent）]]
- [[wiki/ai-coding/vibe-coding|Vibe Coding]]
- [[wiki/ai-coding/vibe-coding-的代价|Vibe Coding 的代价]]
- [[wiki/ai-coding/vibe-coding-对-saas-的通缩|Vibe Coding 对 SaaS 的结构性通缩]]
- [[wiki/ai-coding/worse-is-better|Worse is Better]]
- [[wiki/ai-coding/writer-reviewer-模式|Writer/Reviewer 模式]]
- [[wiki/ai-coding/yagni-与-dry-反论|YAGNI 与 DRY 反论]]
- [[wiki/ai-coding/两次纠正规则|两次纠正规则]]
- [[wiki/ai-coding/任务三维划分|任务三维划分]]
- [[wiki/ai-coding/会话管理动作|会话管理动作]]
- [[wiki/ai-coding/冻结快照模式|冻结快照模式]]
- [[wiki/ai-coding/架构师-操作员二分|架构师-操作员二分]]
- [[wiki/ai-coding/探索-规划-编码-验证|探索-规划-编码-验证四阶段]]
- [[wiki/ai-coding/采访驱动-spec|采访驱动 SPEC]]
- [[wiki/ai-coding/稳定前缀-动态后缀|稳定前缀-动态后缀]]
- [[wiki/ai-coding/约束悖论|约束悖论]]
- [[wiki/ai-coding/行为正确性|行为正确性]]
- [[wiki/ai-coding/验证驱动|验证驱动（Verification-Driven）]]
- [[wiki/ai-coding/隐性知识与上下文|隐性知识与上下文]]
- [[wiki/ai-coding/高吞吐合并哲学|高吞吐合并哲学]]

## AIGC

- [[wiki/aigc/agent-skills|Agent Skills 规范]]
- [[wiki/aigc/auto-memory|Auto Memory（自动记忆）]]
- [[wiki/aigc/claude-code|Claude Code]]
- [[wiki/aigc/claude-code-memory|Claude Code Memory 体系]]
- [[wiki/aigc/claude-code-六层架构|Claude Code 六层架构]]
- [[wiki/aigc/claude-health|claude-health（六层架构审计）]]
- [[wiki/aigc/claude-hud|Claude HUD（Statusline 仪表盘）]]
- [[wiki/aigc/claude-rules|.claude/rules/ 规则系统]]
- [[wiki/aigc/codex|Codex]]
- [[wiki/aigc/codex-plugin|Codex Plugin for Claude Code]]
- [[wiki/aigc/codex-sandbox-approval|Codex Sandbox + Approval（双维度权限）]]
- [[wiki/aigc/coordinator-模式|Coordinator 模式（经理模式）]]
- [[wiki/aigc/everything-claude-code|Everything Claude Code]]
- [[wiki/aigc/fail-closed-tool-defaults|Fail-Closed 工具默认]]
- [[wiki/aigc/handoff-md|HANDOFF.md 跨会话交接]]
- [[wiki/aigc/hooks|Hooks（钩子）]]
- [[wiki/aigc/inline-edit|Inline Edit]]
- [[wiki/aigc/kairos-记忆蒸馏|KAIROS 模式与记忆蒸馏]]
- [[wiki/aigc/mcp|MCP（Model Context Protocol）]]
- [[wiki/aigc/permission-modes|权限模式（YOLO / Safe / Plan）]]
- [[wiki/aigc/plan-mode|Plan Mode]]
- [[wiki/aigc/read-before-edit|Read-Before-Edit 铁律]]
- [[wiki/aigc/settings-scopes|Settings Scopes（5 层作用域）]]
- [[wiki/aigc/skill-编写实践|Skill 编写实践]]
- [[wiki/aigc/skills-9-分类|Skills 9 大分类]]
- [[wiki/aigc/skills-marketplace|Skills 分发与市场]]
- [[wiki/aigc/skills-vs-automations|Skills vs Automations（方法 vs 调度）]]
- [[wiki/aigc/superpowers|Superpowers（AI 编码工作流框架）]]
- [[wiki/aigc/渐进式披露|渐进式披露]]

## FrontEnd

- [[wiki/frontend/0-rtt-握手|0-RTT 握手]]
- [[wiki/frontend/bun|Bun]]
- [[wiki/frontend/connection-migration|连接迁移]]
- [[wiki/frontend/flash-list|FlashList]]
- [[wiki/frontend/head-of-line-blocking|队头阻塞]]
- [[wiki/frontend/headless-ui|Headless UI]]
- [[wiki/frontend/http-3|HTTP/3]]
- [[wiki/frontend/js-盈利模式分类|JS 库的 5 种盈利模式]]
- [[wiki/frontend/key-重置组件|key 重置组件]]
- [[wiki/frontend/no-useeffect-rule|No useEffect 规则]]
- [[wiki/frontend/per-seat-licensing|Per-Seat Licensing]]
- [[wiki/frontend/pressable-vs-touchable|Pressable vs TouchableOpacity]]
- [[wiki/frontend/quic|QUIC]]
- [[wiki/frontend/react-native-core-components|React Native 核心组件]]
- [[wiki/frontend/shadcn-ui|shadcn/ui]]
- [[wiki/frontend/usemounteffect|useMountEffect]]
- [[wiki/frontend/vercel|Vercel]]
- [[wiki/frontend/view-recycling|View 回收]]
- [[wiki/frontend/webcontainers|WebContainers]]
- [[wiki/frontend/派生状态|派生状态]]
- [[wiki/frontend/组件强制函数|组件强制函数]]

## Obsidian

- [[wiki/obsidian/aliases|Aliases（别名）]]
- [[wiki/obsidian/block-reference|块引用]]
- [[wiki/obsidian/block-reference-use-cases|块引用使用场景]]
- [[wiki/obsidian/callouts|Callouts]]
- [[wiki/obsidian/claudian|Claudian]]
- [[wiki/obsidian/dataview|Dataview]]
- [[wiki/obsidian/defuddle|Defuddle]]
- [[wiki/obsidian/embed-files|嵌入文件]]
- [[wiki/obsidian/inbox-工作流|Inbox 工作流]]
- [[wiki/obsidian/json-canvas|JSON Canvas]]
- [[wiki/obsidian/knowledge-graph|知识图谱]]
- [[wiki/obsidian/moc-索引笔记|MOC（Maps of Content）]]
- [[wiki/obsidian/obsidian-bases|Obsidian Bases]]
- [[wiki/obsidian/obsidian-cli|Obsidian CLI]]
- [[wiki/obsidian/obsidian-skills|Obsidian Skills (kepano)]]
- [[wiki/obsidian/obsidian-web-clipper|Obsidian Web Clipper]]
- [[wiki/obsidian/para-方法|PARA 方法]]
- [[wiki/obsidian/templater|Templater]]
- [[wiki/obsidian/wikilink|Wikilink]]
- [[wiki/obsidian/zettelkasten|Zettelkasten]]

---

## 动态视图

最近 7 天更新的 wiki 页面：
![[index.base#recent-wiki]]

待 ingest 的 sources：
![[index.base#pending-sources]]
