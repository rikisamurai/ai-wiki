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
