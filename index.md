---
title: ai-wiki Index
date: 2026-04-22
---

# ai-wiki

> [!note] 三层架构
> `sources/`（原料，只读） · `wiki/`（精华，可改） · `AGENTS.md`（schema）
>
> 用 `/ingest` `/query` `/lint` `/migrate-next` 操作。详见 [[AGENT]]。

## Agent Engineering

### philosophy

- [[wiki/agent-engineering/philosophy/agent-工作量分布|Agent 工作量分布（90% 在 AI 之外）]]
- [[wiki/agent-engineering/philosophy/agentic-coding|Agentic Coding]]
- [[wiki/agent-engineering/philosophy/ai-first-vs-ai-assisted|AI First vs AI-Assisted]]
- [[wiki/agent-engineering/philosophy/ai-first-工程前提|AI First 工程前提]]
- [[wiki/agent-engineering/philosophy/ai-first-适用边界|AI First 适用边界]]
- [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]
- [[wiki/agent-engineering/philosophy/harness-成熟度|Harness 三层成熟度]]
- [[wiki/agent-engineering/philosophy/opc-一人公司|OPC（One Person Company）]]
- [[wiki/agent-engineering/philosophy/plausible-code|Plausible Code（似是而非的代码）]]
- [[wiki/agent-engineering/philosophy/spec-coding|Spec Coding]]
- [[wiki/agent-engineering/philosophy/vibe-coding|Vibe Coding]]
- [[wiki/agent-engineering/philosophy/vibe-coding-对-saas-的通缩|Vibe Coding 对 SaaS 的结构性通缩]]
- [[wiki/agent-engineering/philosophy/vibe-coding-的代价|Vibe Coding 的代价]]
- [[wiki/agent-engineering/philosophy/worse-is-better|Worse is Better]]
- [[wiki/agent-engineering/philosophy/yagni-与-dry-反论|YAGNI 与 DRY 反论]]
- [[wiki/agent-engineering/philosophy/架构师-操作员二分|架构师-操作员二分]]
- [[wiki/agent-engineering/philosophy/约束悖论|约束悖论（Constraint Paradox）]]
- [[wiki/agent-engineering/philosophy/行为正确性|行为正确性（Behavioral Correctness）]]
- [[wiki/agent-engineering/philosophy/高吞吐合并哲学|高吞吐合并哲学]]

### context

- [[wiki/agent-engineering/context/cache-keep-alive|Cache Keep-Alive]]
- [[wiki/agent-engineering/context/cache-命中率|Cache 命中率]]
- [[wiki/agent-engineering/context/cache-失效陷阱|Cache 失效陷阱]]
- [[wiki/agent-engineering/context/compact-vs-clear|Compact vs Clear]]
- [[wiki/agent-engineering/context/context-rot|Context Rot（上下文衰减）]]
- [[wiki/agent-engineering/context/context-window|Context Window]]
- [[wiki/agent-engineering/context/kv-cache|KV Cache]]
- [[wiki/agent-engineering/context/prefix-cache|Prefix Cache]]
- [[wiki/agent-engineering/context/会话管理动作|会话管理动作]]
- [[wiki/agent-engineering/context/冻结快照模式|冻结快照模式]]
- [[wiki/agent-engineering/context/稳定前缀-动态后缀|稳定前缀-动态后缀]]
- [[wiki/agent-engineering/context/隐性知识与上下文|隐性知识与上下文（Tacit Knowledge）]]

### workflow

- [[wiki/agent-engineering/workflow/agent-可读性|Agent 可读性（Legibility）]]
- [[wiki/agent-engineering/workflow/agent-等待时间|Agent 等待时间（Human Wait）]]
- [[wiki/agent-engineering/workflow/agents-md|AGENTS.md]]
- [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式（经理模式）]]
- [[wiki/agent-engineering/workflow/doc-gardening|Doc Gardening Agent]]
- [[wiki/agent-engineering/workflow/enforce-invariants|Enforce Invariants, Not Implementations]]
- [[wiki/agent-engineering/workflow/long-horizon-agent|Long Horizon Agent]]
- [[wiki/agent-engineering/workflow/ralph-loop|Ralph Loop]]
- [[wiki/agent-engineering/workflow/rewind-胜过纠正|Rewind 胜过纠正]]
- [[wiki/agent-engineering/workflow/self-healing-loop|Self-Healing Loop]]
- [[wiki/agent-engineering/workflow/subagent-driven-development|Subagent-Driven Development（每任务一个 subagent）]]
- [[wiki/agent-engineering/workflow/subagent-上下文隔离|Subagent 上下文隔离]]
- [[wiki/agent-engineering/workflow/writer-reviewer-模式|Writer/Reviewer 模式]]
- [[wiki/agent-engineering/workflow/两次纠正规则|两次纠正规则]]
- [[wiki/agent-engineering/workflow/任务三维划分|任务三维划分]]
- [[wiki/agent-engineering/workflow/探索-规划-编码-验证|探索-规划-编码-验证四阶段]]
- [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]
- [[wiki/agent-engineering/workflow/验证驱动|验证驱动（Verification-Driven）]]

### code-review

- [[wiki/agent-engineering/code-review/ai-code-review|AI Code Review]]
- [[wiki/agent-engineering/code-review/ai-写-lint|AI 写 Lint]]
- [[wiki/agent-engineering/code-review/review-带宽瓶颈|Review 带宽瓶颈]]
- [[wiki/agent-engineering/code-review/shift-left|Shift Left（左移）]]

## Claude Code（CLI 工具系）

- [[wiki/claude-code/auto-memory|Auto Memory（自动记忆）]]
- [[wiki/claude-code/claude-code|Claude Code]]
- [[wiki/claude-code/claude-code-memory|Claude Code Memory 体系]]
- [[wiki/claude-code/claude-code-六层架构|Claude Code 六层架构]]
- [[wiki/claude-code/claude-health|claude-health（六层架构审计 Skill）]]
- [[wiki/claude-code/claude-hud|Claude HUD（Statusline 仪表盘）]]
- [[wiki/claude-code/claude-rules|.claude/rules/ 规则系统]]
- [[wiki/claude-code/codex|Codex]]
- [[wiki/claude-code/codex-plugin|Codex Plugin for Claude Code]]
- [[wiki/claude-code/codex-sandbox-approval|Codex Sandbox + Approval（双维度权限）]]
- [[wiki/claude-code/everything-claude-code|Everything Claude Code]]
- [[wiki/claude-code/fail-closed-tool-defaults|Fail-Closed 工具默认]]
- [[wiki/claude-code/handoff-md|HANDOFF.md 跨会话交接]]
- [[wiki/claude-code/hooks|Hooks（钩子）]]
- [[wiki/claude-code/inline-edit|Inline Edit]]
- [[wiki/claude-code/kairos-记忆蒸馏|KAIROS 模式与记忆蒸馏]]
- [[wiki/claude-code/mcp|MCP（Model Context Protocol）]]
- [[wiki/claude-code/opencli|OpenCLI]]
- [[wiki/claude-code/permission-modes|权限模式（YOLO / Safe / Plan）]]
- [[wiki/claude-code/plan-mode|Plan Mode]]
- [[wiki/claude-code/read-before-edit|Read-Before-Edit 铁律]]
- [[wiki/claude-code/settings-scopes|Claude Code Settings Scopes]]

## Skills（生态）

- [[wiki/skills/agent-skills|Agent Skills 规范]]
- [[wiki/skills/skill-编写实践|Skill 编写实践]]
- [[wiki/skills/skills-9-分类|Skills 9 大分类]]
- [[wiki/skills/skills-marketplace|Skills 分发与市场]]
- [[wiki/skills/skills-vs-automations|Skills vs Automations（方法 vs 调度）]]
- [[wiki/skills/superpowers|Superpowers（AI 编码工作流框架）]]
- [[wiki/skills/渐进式披露|渐进式披露（Progressive Disclosure）]]

## Retrieval

### rag

- [[wiki/retrieval/rag/agentic-rag|Agentic RAG]]
- [[wiki/retrieval/rag/graph-rag|GraphRAG]]
- [[wiki/retrieval/rag/hybrid-retrieval|混合检索（Hybrid Retrieval）]]
- [[wiki/retrieval/rag/rag|RAG（检索增强生成）]]

### browser

- [[wiki/retrieval/browser/agent-browser|agent-browser]]
- [[wiki/retrieval/browser/browser-use|Browser-Use]]
- [[wiki/retrieval/browser/cdp|CDP（Chrome DevTools Protocol）]]
- [[wiki/retrieval/browser/cdp-能力边界|CDP 能力边界完整表]]

## Frontend

### web-platform

- [[wiki/frontend/web-platform/bun|Bun]]
- [[wiki/frontend/web-platform/mutation-observer|MutationObserver]]
- [[wiki/frontend/web-platform/resize-observer|ResizeObserver]]
- [[wiki/frontend/web-platform/vercel|Vercel]]
- [[wiki/frontend/web-platform/webcontainers|WebContainers]]

### network

- [[wiki/frontend/network/0-rtt-握手|0-RTT 握手]]
- [[wiki/frontend/network/connection-migration|连接迁移（Connection Migration）]]
- [[wiki/frontend/network/head-of-line-blocking|队头阻塞（Head-of-Line Blocking）]]
- [[wiki/frontend/network/http-3|HTTP/3]]
- [[wiki/frontend/network/quic|QUIC]]

### react-patterns

- [[wiki/frontend/react-patterns/key-重置组件|用 key 重置组件]]
- [[wiki/frontend/react-patterns/no-useeffect-rule|No useEffect 规则]]
- [[wiki/frontend/react-patterns/usemounteffect|useMountEffect]]
- [[wiki/frontend/react-patterns/派生状态|派生状态（Derived State）]]
- [[wiki/frontend/react-patterns/组件强制函数|组件强制函数（Forcing Function）]]

### react-native

- [[wiki/frontend/react-native/flash-list|FlashList]]
- [[wiki/frontend/react-native/pressable-vs-touchable|Pressable vs TouchableOpacity]]
- [[wiki/frontend/react-native/react-native-core-components|React Native 核心组件]]
- [[wiki/frontend/react-native/view-recycling|View 回收]]

### ui-libraries

- [[wiki/frontend/ui-libraries/css-scrollbar-styling|CSS 原生 Scrollbar 样式能力]]
- [[wiki/frontend/ui-libraries/headless-ui|Headless UI]]
- [[wiki/frontend/ui-libraries/overlay-scrollbar-pattern|Overlay Scrollbar 范式]]
- [[wiki/frontend/ui-libraries/overlayscrollbars|OverlayScrollbars]]
- [[wiki/frontend/ui-libraries/scrollbar-mock-vs-overlay|Scrollbar Mock 派 vs Overlay 派]]
- [[wiki/frontend/ui-libraries/shadcn-ui|shadcn/ui]]

## Business

- [[wiki/business/js-盈利模式分类|JS 库的 5 种盈利模式]]
- [[wiki/business/per-seat-licensing|Per-Seat Licensing（按席位授权）]]

## Obsidian

- [[wiki/obsidian/aliases|Aliases（别名）]]
- [[wiki/obsidian/block-reference|块引用（Block Reference）]]
- [[wiki/obsidian/block-reference-use-cases|块引用使用场景]]
- [[wiki/obsidian/callouts|Obsidian Callouts]]
- [[wiki/obsidian/claudian|Claudian]]
- [[wiki/obsidian/dataview|Dataview]]
- [[wiki/obsidian/defuddle|Defuddle]]
- [[wiki/obsidian/embed-files|嵌入文件（Embed）]]
- [[wiki/obsidian/inbox-工作流|Inbox 工作流]]
- [[wiki/obsidian/json-canvas|JSON Canvas]]
- [[wiki/obsidian/knowledge-graph|Obsidian 知识图谱]]
- [[wiki/obsidian/moc-索引笔记|MOC（Maps of Content）]]
- [[wiki/obsidian/obsidian-bases|Obsidian Bases]]
- [[wiki/obsidian/obsidian-cli|Obsidian CLI]]
- [[wiki/obsidian/obsidian-skills|Obsidian Skills（kepano）]]
- [[wiki/obsidian/obsidian-web-clipper|Obsidian Web Clipper]]
- [[wiki/obsidian/para-方法|PARA 方法]]
- [[wiki/obsidian/templater|Templater]]
- [[wiki/obsidian/wikilink|Wikilink]]
- [[wiki/obsidian/zettelkasten|Zettelkasten（卡片盒笔记法）]]
---

## 动态视图

最近 7 天更新的 wiki 页面：
![[index.base#recent-wiki]]

待 ingest 的 sources：
![[index.base#pending-sources]]
