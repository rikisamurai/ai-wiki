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
- [[wiki/agent-engineering/philosophy/alien-code|AI 外星代码（Alien Code）]]
- [[wiki/agent-engineering/philosophy/eval-driven-development|Eval-Driven Development]]
- [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]
- [[wiki/agent-engineering/philosophy/harness-成熟度|Harness 三层成熟度]]
- [[wiki/agent-engineering/philosophy/karpathy-四种失败模式|Karpathy 的四种 AI Coding 失败模式]]
- [[wiki/agent-engineering/philosophy/mimic-first-harness|Mimic-First Harness（找模仿对象）]]
- [[wiki/agent-engineering/philosophy/opc-一人公司|OPC（One Person Company）]]
- [[wiki/agent-engineering/philosophy/per-model-harness|Per-Model Harness（每模型定制框架）]]
- [[wiki/agent-engineering/philosophy/plausible-code|Plausible Code（似是而非的代码）]]
- [[wiki/agent-engineering/philosophy/spec-coding|Spec Coding]]
- [[wiki/agent-engineering/philosophy/vibe-coding|Vibe Coding]]
- [[wiki/agent-engineering/philosophy/vibe-coding-对-saas-的通缩|Vibe Coding 对 SaaS 的结构性通缩]]
- [[wiki/agent-engineering/philosophy/vibe-coding-的代价|Vibe Coding 的代价]]
- [[wiki/agent-engineering/philosophy/worse-is-better|Worse is Better]]
- [[wiki/agent-engineering/philosophy/yagni-与-dry-反论|YAGNI 与 DRY 反论]]
- [[wiki/agent-engineering/philosophy/ai-加速腐化|AI 不会自动收敛复杂度]]
- [[wiki/agent-engineering/philosophy/人人对齐-人机对齐|人人对齐 → 人机对齐]]
- [[wiki/agent-engineering/philosophy/架构师-操作员二分|架构师-操作员二分]]
- [[wiki/agent-engineering/philosophy/经验价值边界|经验价值边界的重定义]]
- [[wiki/agent-engineering/philosophy/跨厂商共识协议|跨厂商共识协议]]
- [[wiki/agent-engineering/philosophy/约束悖论|约束悖论（Constraint Paradox）]]
- [[wiki/agent-engineering/philosophy/行为正确性|行为正确性（Behavioral Correctness）]]
- [[wiki/agent-engineering/philosophy/高吞吐合并哲学|高吞吐合并哲学]]

### context

- [[wiki/agent-engineering/context/cache-keep-alive|Cache Keep-Alive]]
- [[wiki/agent-engineering/context/cache-命中率|Cache 命中率]]
- [[wiki/agent-engineering/context/cache-失效陷阱|Cache 失效陷阱]]
- [[wiki/agent-engineering/context/compact-vs-clear|Compact vs Clear]]
- [[wiki/agent-engineering/context/context-anxiety|Context Anxiety（上下文焦虑）]]
- [[wiki/agent-engineering/context/context-rot|Context Rot（上下文衰减）]]
- [[wiki/agent-engineering/context/context-window|Context Window]]
- [[wiki/agent-engineering/context/dynamic-context|动态上下文（Dynamic Context）]]
- [[wiki/agent-engineering/context/kv-cache|KV Cache]]
- [[wiki/agent-engineering/context/prefix-cache|Prefix Cache]]
- [[wiki/agent-engineering/context/会话管理动作|会话管理动作]]
- [[wiki/agent-engineering/context/冻结快照模式|冻结快照模式]]
- [[wiki/agent-engineering/context/稳定前缀-动态后缀|稳定前缀-动态后缀]]
- [[wiki/agent-engineering/context/隐性知识与上下文|隐性知识与上下文（Tacit Knowledge）]]

### workflow

- [[wiki/agent-engineering/workflow/agent-evals|Agent Evals（智能体评估）]]
- [[wiki/agent-engineering/workflow/agent-可读性|Agent 可读性（Legibility）]]
- [[wiki/agent-engineering/workflow/agent-等待时间|Agent 等待时间（Human Wait）]]
- [[wiki/agent-engineering/workflow/agents-md|AGENTS.md]]
- [[wiki/agent-engineering/workflow/ax-manual-accessibility|AXManualAccessibility（Electron 的 AX Tree 开关）]]
- [[wiki/agent-engineering/workflow/capability-vs-regression-eval|能力 eval vs 回归 eval]]
- [[wiki/agent-engineering/workflow/codebase-indexing|Codebase Indexing]]
- [[wiki/agent-engineering/workflow/coding-agent-eval|Coding Agent Eval]]
- [[wiki/agent-engineering/workflow/computer-use-agent-eval|Computer Use Agent Eval]]
- [[wiki/agent-engineering/workflow/continuous-checkpoint|Continuous Checkpoint Mode（WIP commit + 上下文恢复）]]
- [[wiki/agent-engineering/workflow/conversational-agent-eval|Conversational Agent Eval]]
- [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式（经理模式）]]
- [[wiki/agent-engineering/workflow/cursorbench|CursorBench]]
- [[wiki/agent-engineering/workflow/design-shotgun|Design Shotgun（mockup → HTML 流水线）]]
- [[wiki/agent-engineering/workflow/doc-gardening|Doc Gardening Agent]]
- [[wiki/agent-engineering/workflow/enforce-invariants|Enforce Invariants, Not Implementations]]
- [[wiki/agent-engineering/workflow/eval-grader-三类|Eval Grader 三类（code / model / human）]]
- [[wiki/agent-engineering/workflow/eval-方法矩阵|Eval 方法矩阵（Swiss Cheese 模型）]]
- [[wiki/agent-engineering/workflow/keep-rate|Keep Rate（保留率）]]
- [[wiki/agent-engineering/workflow/long-horizon-agent|Long Horizon Agent]]
- [[wiki/agent-engineering/workflow/mac-computer-use|Mac Computer Use 架构（视觉 + AX + 事件 + 权限）]]
- [[wiki/agent-engineering/workflow/mid-chat-model-switch|聊天中途切换模型]]
- [[wiki/agent-engineering/workflow/openspec|OpenSpec（SDD 指令工作流）]]
- [[wiki/agent-engineering/workflow/parallel-sprints|Parallel Sprints（10-15 并行 sprint）]]
- [[wiki/agent-engineering/workflow/pass-at-k-vs-pass-power-k|pass@k vs pass^k]]
- [[wiki/agent-engineering/workflow/ralph-loop|Ralph Loop]]
- [[wiki/agent-engineering/workflow/research-agent-eval|Research Agent Eval]]
- [[wiki/agent-engineering/workflow/rewind-胜过纠正|Rewind 胜过纠正]]
- [[wiki/agent-engineering/workflow/sdd-隐性功能陷阱|SDD 隐性功能陷阱]]
- [[wiki/agent-engineering/workflow/self-healing-loop|Self-Healing Loop]]
- [[wiki/agent-engineering/workflow/specialist-roles-模型|Specialist Roles 模型（多角色专家化）]]
- [[wiki/agent-engineering/workflow/sprint-七阶段范式|Sprint 七阶段范式]]
- [[wiki/agent-engineering/workflow/sub-agent-纪律|Sub-agent 纪律（每问一文件 + verdict-first）]]
- [[wiki/agent-engineering/workflow/subagent-driven-development|Subagent-Driven Development（每任务一个 subagent）]]
- [[wiki/agent-engineering/workflow/subagent-vs-team-模式|Subagent 模式 vs Team 模式]]
- [[wiki/agent-engineering/workflow/subagent-上下文隔离|Subagent 上下文隔离]]
- [[wiki/agent-engineering/workflow/writer-reviewer-模式|Writer/Reviewer 模式]]
- [[wiki/agent-engineering/workflow/三阶段联调|三阶段联调（Mock → 编译 → 联调）]]
- [[wiki/agent-engineering/workflow/两次纠正规则|两次纠正规则]]
- [[wiki/agent-engineering/workflow/任务三维划分|任务三维划分]]
- [[wiki/agent-engineering/workflow/全栈工作区|全栈工作区（多仓单 workspace）]]
- [[wiki/agent-engineering/workflow/探索-规划-编码-验证|探索-规划-编码-验证四阶段]]
- [[wiki/agent-engineering/workflow/采纳率|采纳率（Acceptance Rate）]]
- [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]
- [[wiki/agent-engineering/workflow/工具错误分类法|工具调用错误分类法]]
- [[wiki/agent-engineering/workflow/语义满意度信号|语义满意度信号]]
- [[wiki/agent-engineering/workflow/验证驱动|验证驱动（Verification-Driven）]]
- [[wiki/agent-engineering/workflow/读-transcript|读 Transcript（Read the Transcripts）]]
- [[wiki/agent-engineering/workflow/ai-辅助测试-sop|AI 辅助测试用例生成 SOP]]
- [[wiki/agent-engineering/workflow/ai-代码-attribution|AI 代码 Attribution（自报 vs 检测）]]
- [[wiki/agent-engineering/workflow/git-notes-ai-元数据|git notes 作为 AI 元数据载体]]
- [[wiki/agent-engineering/workflow/专家定向-ai-穷举|专家定向 + AI 穷举（技术债梳理）]]
- [[wiki/agent-engineering/workflow/主r打样-sop分发|主 R 打样 → SOP 分发 → 全组并行]]
- [[wiki/agent-engineering/workflow/渐进式重构|渐进式重构（顺带消化技术债）]]

### code-review

- [[wiki/agent-engineering/code-review/ai-code-review|AI Code Review]]
- [[wiki/agent-engineering/code-review/ai-写-lint|AI 写 Lint]]
- [[wiki/agent-engineering/code-review/cross-model-second-opinion|跨模型 Second Opinion]]
- [[wiki/agent-engineering/code-review/pre-pr|Pre-PR（提交前 AI 自审）机制]]
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
- [[wiki/claude-code/cursor|Cursor]]
- [[wiki/claude-code/everything-claude-code|Everything Claude Code]]
- [[wiki/claude-code/fail-closed-tool-defaults|Fail-Closed 工具默认]]
- [[wiki/claude-code/gbrain|GBrain（agent 持久知识库）]]
- [[wiki/claude-code/git-ai|Git AI（追踪 AI 生成代码的 Git 扩展）]]
- [[wiki/claude-code/gstack|gstack（Garry Tan 的 Claude Code Setup）]]
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
- [[wiki/skills/bgclick-rev-skill|bgclick-rev（深度逆向 Skill 范例）]]
- [[wiki/skills/skill-编写实践|Skill 编写实践]]
- [[wiki/skills/skills-9-分类|Skills 9 大分类]]
- [[wiki/skills/skills-marketplace|Skills 分发与市场]]
- [[wiki/skills/skills-vs-automations|Skills vs Automations（方法 vs 调度）]]
- [[wiki/skills/superpowers|Superpowers（AI 编码工作流框架）]]
- [[wiki/skills/wasc-search-skill|wasc-search-skill（低成本高精度 RAG Skill 范例）]]
- [[wiki/skills/渐进式披露|渐进式披露（Progressive Disclosure）]]

## Retrieval

### rag

- [[wiki/retrieval/rag/agentic-rag|Agentic RAG]]
- [[wiki/retrieval/rag/citation-faithfulness|引用忠实度（Citation Faithfulness）]]
- [[wiki/retrieval/rag/graph-rag|GraphRAG]]
- [[wiki/retrieval/rag/hybrid-retrieval|混合检索（Hybrid Retrieval）]]
- [[wiki/retrieval/rag/rag|RAG（检索增强生成）]]
- [[wiki/retrieval/rag/rag-降级|RAG 5 级降级（永不返回空）]]
- [[wiki/retrieval/rag/rrf|RRF（Reciprocal Rank Fusion）]]

### browser

- [[wiki/retrieval/browser/agent-browser|agent-browser]]
- [[wiki/retrieval/browser/browser-use|Browser-Use]]
- [[wiki/retrieval/browser/cdp|CDP（Chrome DevTools Protocol）]]
- [[wiki/retrieval/browser/cdp-能力边界|CDP 能力边界完整表]]
- [[wiki/retrieval/browser/domain-skills|Domain Skills（per-site 浏览器记忆）]]
- [[wiki/retrieval/browser/sidebar-agent-prompt-injection-defense|Sidebar Agent Prompt Injection 防御]]

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

- [[wiki/frontend/react-native/csf-story-format|CSF（Component Story Format）]]
- [[wiki/frontend/react-native/expo-snack|Expo Snack]]
- [[wiki/frontend/react-native/flash-list|FlashList]]
- [[wiki/frontend/react-native/ios-cjk-ime-textinput|iOS CJK 输入法被 controlled TextInput 打断]]
- [[wiki/frontend/react-native/keyboard-avoiding-view|KeyboardAvoidingView]]
- [[wiki/frontend/react-native/keyboard-should-persist-taps|keyboardShouldPersistTaps + keyboardDismissMode]]
- [[wiki/frontend/react-native/pressable-vs-touchable|Pressable vs TouchableOpacity]]
- [[wiki/frontend/react-native/react-native-component-docs-stack|React Native 组件文档站技术栈选型]]
- [[wiki/frontend/react-native/react-native-core-components|React Native 核心组件]]
- [[wiki/frontend/react-native/react-native-keyboard-controller|react-native-keyboard-controller]]
- [[wiki/frontend/react-native/rn-keyboard-pitfalls|RN 键盘相关坑点速查]]
- [[wiki/frontend/react-native/storybook-react-native|Storybook for React Native]]
- [[wiki/frontend/react-native/textinput-controlled-vs-uncontrolled|RN TextInput controlled vs uncontrolled]]
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
